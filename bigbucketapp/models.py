from django.db import models
from django.contrib.auth.models import User

# Create your models here.
def products_saving_location(instance , filename):
	return 'products_image/{0}/{1}/{2}'.format(instance.category, instance.product_name, filename)

class UserDetail(models.Model):
	USER_ROLES = (('1', 'KISHAN'),('2', 'DUKHANDAAR'), ('3', 'KARIDDAR'))
	user_type = models.CharField(choices=USER_ROLES,max_length=11,blank=False)
	state = models.CharField(blank=True,max_length=20, null=True)
	city = models.CharField(blank=True,max_length=20, null=True)
	district = models.CharField(blank=True,max_length=20, null=True)
	village = models.CharField(blank=True,max_length=20, null=True)
	phone_number = models.CharField(blank=True, null=True,max_length=20)
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_query_name='user_detail',related_name='user_detail')

	def __str__(self):
		return self.user.first_name + self.user.last_name



class Product(models.Model):
	CATEGORY = (('1', 'Dairy Product'), ('2','Fruits'), ('3', 'Vegetable'), ('4', 'Grocery'), ('5', 'Daily Utilies'))
	product_name = models.CharField(max_length=20)
	price = models.IntegerField()
	quantity = models.IntegerField()
	quantity_type = models.CharField(max_length=8)
	category = models.CharField(choices=CATEGORY,max_length=20)
	sell_price = models.IntegerField(null=True, blank=True)
	discount = models.IntegerField(null=True, blank=True)
	city = models.IntegerField(null=True, blank=True)
	latitude = models.FloatField(null=True, blank=True)
	is_available = models.BooleanField(default=True)
	longitude = models.FloatField(null=True, blank=True)
	seller = models.ForeignKey(UserDetail, related_name='products', related_query_name='products', on_delete=models.CASCADE)
	product_image = models.ImageField(upload_to=products_saving_location, blank=True, null = True)

	def __str__():
		return self.product_name+', '+ self.category

	def update_availablity(self):
		product_quantity = self.quantity
		if product_quantity<=0:
			self.is_available = False
			self.save()
			
	def sell_point(self):
		price = self.price
		if self.category == '4':
			price=price+(price*5)/100
		else:
			price=price+(price*10)/100
		self.sell_price = price
		self.save()



class ProductPurchase(models.Model):
	product = models.ForeignKey(Product)
	buyer = models.ForeignKey(UserDetail, related_query_name='purchased_items',related_name='purchased_items')
	address = models.TextField(null=True, blank=True)
	zip_code = models.IntegerField(null=True, blank=True)
	city = models.CharField(max_length=30,null=True, blank=True)
	phone_number = models.CharField(max_length=12,null=True, blank=True)
	is_purchased = models.BooleanField()

class AddedToCart(models.Model):
	product = models.ForeignKey(Product)
	future_buyer = models.ForeignKey(UserDetail, related_query_name='cart_items',related_name='cart_items')
	in_cart = models.BooleanField()