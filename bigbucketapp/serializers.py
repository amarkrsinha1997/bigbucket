from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

# user related serializers
class UserDetailSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserDetail
		fields= ['user_type','state','city','district','village','phone_number'] 


class UserLoginSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields=['username','password']
		extra_kwargs = {'password': {'write_only': True}}


class UserSerializer(serializers.ModelSerializer):
	user_detail = UserDetailSerializer()
	class Meta:
		model= User
		fields=['username','email','first_name','last_name', 'password', 'user_detail', ]
		extra_kwargs = {'password': {'write_only': True}}


	def create(self, validated_data):
		username = validated_data['username']
		email = validated_data['email']
		password = validated_data['password']
		first_name = validated_data['first_name']
		last_name = validated_data['last_name']
		user_type = validated_data['user_detail']['user_type']
		state = validated_data['user_detail']['state']
		city = validated_data['user_detail']['city']
		district = validated_data['user_detail']['district']
		village = validated_data['user_detail']['village']
		phone_number = validated_data['user_detail']['phone_number']

		user_obj = User(username = username, email = email, first_name= first_name, last_name=last_name)
		user_detail_obj = UserDetail(user_type=user_type,state=state,city=city,district=district,village=village,phone_number=phone_number)
		user_obj.set_password(password)
		user_obj.save()
		user_detail_obj.user = user_obj
		user_detail_obj.save()
		return validated_data

# products related serializers

class ProductCreateUpdateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = ['product_name','price','quantity','quantity_type','category','product_image']




class ProductUserSerializer(serializers.ModelSerializer):
	class Meta:
		model= User
		fields=['username','email','first_name','last_name', 'password', ]
		extra_kwargs = {'password': {'write_only': True}}



class ProductListSerializer(serializers.ModelSerializer):
	user_detail = serializers.SerializerMethodField()
	# url = serializers.HyperlinkedIdentityField(view_name='api:product-detail', lookup_field='pk')	
	class Meta:
		model = Product
		fields =  ['id','product_name','sell_price','price','quantity','quantity_type','category','product_image', 
					'city', 'latitude', 'longitude', 'is_available','user_detail']

	def get_user_detail(self, obj):
		return ProductUserSerializer(obj.user.user).data



class ProductPurchaseSerializer(serializers.ModelSerializer):
	class Meta:
		model = ProductPurchase
		fields = '__all__'


class AddToCartSerializer(serializers.ModelSerializer):
	class Meta:
		model = AddedToCart
		fields = '__all__'
