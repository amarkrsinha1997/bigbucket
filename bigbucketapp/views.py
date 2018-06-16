from django.shortcuts import render
from rest_framework.generics import *
from django.contrib.auth import get_user_model
from rest_framework.views import APIView

from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login, authenticate, logout
from .serializers import *
from .models import *
from .permissions import *
from rest_framework.permissions import (
	AllowAny,
	IsAuthenticated,
	)
# User views

class UserLoginAPIView(APIView):
	permission_classes = [AllowAny]
	serializer_class = UserLoginSerializer

	def post(self, request, *args, **kwargs):
		data = request.data
		username = data.get('username')
		password = data.get('password')
		user = authenticate(username=username, password=password)
		if user is not None:
			data = login(request, user)
			print data
			return Response(data, status=status.HTTP_200_OK)
		else:
			return Response(status=status.HTTP_404_NOT_FOUND)


class UserLogoutAPIView(APIView):
	queryset = User.objects.all()
	def get(self, request, format=None):
		# simply delete the token to force a login
		if request.user:
			logout(request)
			return Response({'message':'Successfully Logout'},status=status.HTTP_200_OK)
		return Response({'message':'You need to login first!'},status=status.HTTP_404_NOT_FOUND)



class UserCreateAPIView(CreateAPIView):
	serializer_class = UserSerializer
	permission_classes = [AllowAny]
	class Meta:
		model = User

		
# Product views 
class ProductCreateView(CreateAPIView):
	queryset = Product.objects.all()
	serializer_class = ProductCreateUpdateSerializer
	permission_classes = [IsAuthenticated, IsFarmerOrShopKeeper]

	def perform_create(self, serializer):
		instance = serializer.save(seller=self.request.user.user_detail)
		instance.update_availablity()
		instance.sell_point()




class ProductUpdateAPIView(RetrieveUpdateAPIView):
	queryset = Product.objects.all().filter(is_available=True)
	serializer_class = ProductCreateUpdateSerializer
	permission_classes = [IsOwnerOrReadOnly, IsFarmerOrShopKeeper, IsAuthenticated]

	def perform_update(self, serializer):
		instance = serializer.save(seller=self.request.user.user_detail)
		instance.update_availablity()
		instance.sell_point()


class ProductRetrieveAPIView(RetrieveAPIView):
	queryset = Product.objects.all().filter(is_available=True)
	serializer_class = ProductListSerializer


class ProductListAPIView(ListAPIView):
	queryset = Product.objects.all().filter(is_available=True)
	serializer_class = ProductListSerializer
    # pagination_class = PostPageNumberPagination #PageNumberPagination

	def get_queryset(self, *args, **kwargs):
		queryset_list = Product.objects.all()
		query = self.request.GET

		database_query = {}

		if query:
			sell_price = query.get('sell_price_range')
			product_name = query.get('product_name')
			quantity = query.get('sell_quantity_range')
			category = query.get('category')


			if sell_price:
				sell_price=sell_price.split(',')
				database_query.update({'sell_price__range':(sell_price[0],sell_price[1])})
			if quantity:
				quantity.split(',')
				database_query.update({'quantity__range':(quantity[0],quantity[1])})
			if product_name:
				database_query.update({'product_name':product_name})
			if category:
				database_query.update({'category':category})


			queryset_list = queryset_list.filter(**database_query)
		return queryset_list




class ProductBuyAPIView(APIView):
	permission_classes = [IsAuthenticated]
	serializer_class = ProductPurchaseSerializer
	queryset = Product.objects.all()

	def post(self, request, *args, **kwargs):
		product_id = kwargs.get('id')
		data = request.data
		if data:
			product = Product.objects.get(id=product_id)
			address = data.get('address')
			zip_code = data.get('zip_code')
			city = data.get('city')
			phone_number = data.get('phone_number')
			product_purchase = ProductPurchase(buyer=request.user.user_detail,product=product,address=address,
				zip_code=zip_code,city=city,phone_number=phone_number,is_purchased=True)
			product_purchase.save()
			return Response(product_purchase, status=status.HTTP_200_OK)
		return Response({'message': 'Error in the data'}, status=status.HTTP_404_NOT_FOUND)

class AddToCartAPIView(APIView):
	permission_classes = [IsAuthenticated]
	serializer_class = AddToCartSerializer
	queryset = Product.objects.all()

	def post(self, request, *args, **kwargs):
		product_id = kwargs.get('id')
		data = request.data
		if data:
			product = Product.objects.get(id=product_id)
			cart_items = AddedToCart(future_buyer=request.user.user_detail,product=product,in_cart=True)
			cart_items.save()
			return Response(cart_items, status=status.HTTP_200_OK)
		return Response({'message': 'Error in the data'}, status=status.HTTP_404_NOT_FOUND)

