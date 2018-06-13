from django.db import models

# Create your models here.
def products_saving_location(instance , filename):
	return 'products_image/{0}/{1}/{2}'.format(instance.category, instance.name, filename)

class UserDetail(models.Model):
	USER_ROLES = (('1', 'KISHAN'),('2', 'DUKHANDAAR'), ('3', 'KARIDDAR'))
	user_type = models.CharField(choices=USER_ROLES,max_length=11,blank=False)
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	state = models.CharField(blank=True,max_length=20, null=True)
	city = models.CharField(blank=True,max_length=20, null=True)
	district = models.CharField(blank=True,max_length=20, null=True)
	village = models.CharField(blank=True,max_length=20, null=True)
	phone_number = models.CharField(blank=True, null=True,max_length=20)
	password = models.CharField(max_length=20)
	
	def __str__(self):
		return self.user.first_name + self.user.last_name

class Product(models.Model):
	CATEGORY = (('1', 'Dairy Product'), ('2','Fruits'), ('3', 'Vegetable'), ('4', 'Grocery'), ('5', 'Daily Utilies'))
	product_name = models.CharField(max_length=20)
	price = models.IntegerField()
	quantity = models.IntegerField()
	quantity_type = models.CharField(max_length=8)
	category = models.CharField(choices=CATEGORY,max_length=20)
	sell_point = models.IntegerField()
	city = models.IntegerField()
	latitude = models.FloatField()
	is_available = models.BooleanField(default=True)
	longitude = models.FloatField()
	user = models.ForeignKey(UserDetail, related_name='products', related_query_name='products', on_delete=models.CASCADE)
	product_image = models.ImageField(upload_to=products_saving_location, blank=True, null = True)

	def __str__():
		return self.name+', '+ self.category

	def update_availablity(self):
		product_quantity = self.quantity
		if product_quantity<=0:
			self.is_available = False
			self.save()

class AddedToCart(models.Model):
	product = models.ForeignKey(Product)
	user = models.ForeignKey(UserDetail, related_query_name='cart_items',related_name='cart_items')
