from django.shortcuts import render
from .models import Customer,Product1,Category,Order
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import F,Q,Count,Sum,Avg,Max,Min
from .serializers import StockSerializer


# Create your views here.
class OrderView(APIView):
    def get(self,request):
        orders = Order.objects.filter(customer__email='aimanrasack@gmail.com')
        print('orders=========================>', orders,'===================>')

        orders2 = Order.objects.filter(customer__city='malappuram')
        print('orders=========================>', orders2,'===================>')

        customer_orders = Customer.objects.filter(email='aimanrasack@gmail.com').prefetch_related('orders')
        customer1 = customer_orders.first()
        orderings = customer1.orders.all()
        print('ordersssssssss=========================>', orderings,'===================>')

        Product1.objects.update(price = F('price')+100)
        price_increase = Product1.objects.all()

        for val in price_increase:
            print(val.price)
        print('orders=========================>', price_increase,'===================>')

        Product1.objects.update(stock = F('stock')+2)
        product_stocks = Product1.objects.all()
        for val in product_stocks:
            print(val.stock,val.name)

        n = Product1.objects.filter(stock__gt=F('price')).first()
        print(n)

        Product1.objects.filter(stock__gt=50).update(price = F('price')*0.90)

        products1 = Product1.objects.values_list('name',flat=True)
        print('orders=========================>', products1,'===================>')

        products2 = Product1.objects.filter(Q(price__gt=30000) | Q(stock__lt=30))
        print('pr=========================>', products2,'===================>')

        product3 = Product1.objects.aggregate(avg_price=Avg('price'))
        print('pro=========================>', product3,'===================>')

        product4 = Category.objects.aggregate(Count('name'))
        print('pro=========================>', product4,'===================>')

        pr5 = Category.objects.annotate(product_count = Count('products')).order_by('-product_count')
        print('pro=========================>', pr5,'===================>')

        smthng_i_dnt_know = Order.objects.select_related('customer').all()
        print(f'================================================================{smthng_i_dnt_know}')
        return Response({'message':'successfull!'},status=200)



# class ProductView(APIView):
#     def get(self,request,category_id):
#         catgry_products =  Category.objects.prefetch_related('products').filter(id=category_id)
#         prdcts = catgry_products.products.all()
#         serializer = StockSerializer(prdcts,ma)
        
#         return Response({'message':'successfull!'},status=200)

    