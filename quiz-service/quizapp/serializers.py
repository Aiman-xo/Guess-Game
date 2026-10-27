from rest_framework import serializers
from .models import QuizQuestions,QuizOptions


class QuizOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizOptions
        fields=['id','question','option']

class QuizQuestionSerializers(serializers.ModelSerializer):
    options = QuizOptionSerializer(many=True,read_only=True)
    class Meta:
        model=QuizQuestions
        fields=['id','question','options']