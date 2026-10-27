from datetime import timedelta

from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Sum

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .models import QuizAttempt, QuizOptions, QuizQuestions,MainUser
from .serializers import QuizQuestionSerializers

TIME_LIMIT = timedelta(minutes=1)
GRACE_PERIOD = timedelta(seconds=4)
FAST_LIMIT = timedelta(seconds=30)


def open_attempt_for(user):
    """Latest unanswered attempt for this user, or None."""
    return (
        QuizAttempt.objects
        .filter(user=user, answered_at__isnull=True)
        .order_by('-started_at')
        .first()
    )


class QuizView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        now = timezone.now()

        # 1. Is there an unanswered question already open for this user?
        attempt = open_attempt_for(request.user)

        # 2. If it has expired, close it (counts as wrong) and move on
        if attempt and now - attempt.started_at > TIME_LIMIT + GRACE_PERIOD:
            attempt.answered_at = now
            attempt.save(update_fields=['answered_at'])
            attempt = None

        # 3. No open attempt: pick a new unseen question and start the timer
        if attempt is None:
            seen_ids = QuizAttempt.objects.filter(user=request.user).values('question_id')
            question = (
                QuizQuestions.objects
                .exclude(id__in=seen_ids)
                .order_by('?')
                .first()
            )
            if question is None:
                return Response({'message': 'No more questions!'})

            try:
                with transaction.atomic():
                    attempt = QuizAttempt.objects.create(user=request.user, question=question)
            except IntegrityError:
                # Two requests raced (needs the unique constraints on the model);
                # use the attempt the other request created.
                attempt = open_attempt_for(request.user)

        elapsed = timezone.now() - attempt.started_at
        seconds_left = max(0, min(int(TIME_LIMIT.total_seconds()),
                                  int((TIME_LIMIT - elapsed).total_seconds())))

        return Response({
            'attempt_id': attempt.id,
            'question': QuizQuestionSerializers(attempt.question).data,
            'seconds_left': seconds_left,
        })

    def post(self, request):
        try:
            attempt_id = int(request.data.get('attempt_id'))
            option_id = int(request.data.get('option_id'))
        except (TypeError, ValueError):
            return Response(
                {'error': 'attempt_id and option_id are required and must be numbers'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        with transaction.atomic():
            # Lock the row so two simultaneous submits can't both count.
            attempt = (
                QuizAttempt.objects.select_for_update().filter(
                id=attempt_id,
                user=request.user,
                answered_at__isnull=True,
                )
                .first()
            )
            now = timezone.now()
            if attempt is None:
                return Response({'error': 'Attempt not found or already answered'},
                                status=status.HTTP_404_NOT_FOUND)

            # Out of time: close the attempt; selected_option stays null = wrong
            if now - attempt.started_at > TIME_LIMIT + GRACE_PERIOD:
                attempt.answered_at = now
                attempt.save(update_fields=['answered_at'])
                return Response({'error': 'Time is up!'}, status=status.HTTP_400_BAD_REQUEST)

            # The option must belong to this attempt's question
            option = QuizOptions.objects.filter(
                id=option_id,
                question=attempt.question,
            ).first()

            if option is None:
                return Response({'error': 'Invalid option for this question'},
                                status=status.HTTP_400_BAD_REQUEST)

            attempt.answered_at = now
            attempt.selected_option = option
            if option.is_correct:
                taken = now - attempt.started_at
                attempt.points = 2 if taken <= FAST_LIMIT else 1
            attempt.save(update_fields=['answered_at', 'selected_option','points'])

        return Response({
            'correct': option.is_correct,
            'explanation': attempt.question.explanation,
            'points':attempt.points
        })

class LeaderBoardView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        leaders = (MainUser.objects
            .annotate(score=Sum('quizattempt__points'))
            .filter(score__gt=0)
            .order_by('-score')[:10])

        return Response([{'username': u.username, 'score': u.score} for u in leaders])