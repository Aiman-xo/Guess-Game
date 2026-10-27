from django.shortcuts import render
from .models import Product
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import ProductSerializer
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

class PageInation(PageNumberPagination):
    page_size = 5

# Create your views here.
class ProductView(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self,request):
        products = Product.objects.all()

        page = PageInation()
        pagination = page.paginate_queryset(products,request)
        serializer = ProductSerializer(pagination, many=True)

        return Response({
            'products':serializer.data,
            'message':'successfully fetched products'
        })
