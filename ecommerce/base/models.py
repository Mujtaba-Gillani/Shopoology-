from django.db import models
from django.contrib.auth.models import User
from io import BytesIO
from PIL import Image
from django.core.files import File
from django.conf import settings
# Create your models here.

class Customer(models.Model):
    user=models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name=models.CharField(max_length=200, null=True)
    email=models.CharField(max_length=200)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    country = models.CharField(max_length=50, default='Pakistan')
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name or f"Customer {self.pk}"
    
class Product(models.Model):
    name=models.CharField(max_length=200)
    price=models.DecimalField(decimal_places=2, max_digits=7)
    digital=models.BooleanField(default=False, null=True, blank=True)  # buy default every item is physical  
    image=models.ImageField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
        # if admin post a product without image then it generate an error the function will remove this errror

    @property
    def imageURL(self):
        try:
            url=self.image.url
        except:
            url= ''
        return url
    # @classmethod
    # def create_with_defaults(cls, name, price, digital=False, uploaded_image=None):
    #     # Create a new Product instance with default values
    #     product = cls(name=name, price=price, digital=digital)

    #     # Check if an image was uploaded
    #     if uploaded_image:
    #         product.image = uploaded_image
    #     else:
    #         # No image uploaded, set a default image
    #         default_image_path = settings.BASE_DIR / "static/images/placeholder.png"  # Construct the correct path
    #         default_image = Image.open(default_image_path)
    #         buffer = BytesIO()
    #         default_image.save(buffer, 'PNG')
    #         product.image.save('palceholder.png', File(buffer), save=False)

    #     product.save()  # Save the product instance

    #     return product
    
    
class Order(models.Model):
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    date_order=models.DateTimeField(auto_now_add=True)
    complete=models.BooleanField(default=False)
    transaction_ID=models.CharField(max_length=100, null=True)
    
    def __str__(self):
        return str(self.id)
    
    @property
    def shipping(self):
        shipping= False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital== False:
                shipping= True
        return shipping
    @property
    def get_cart_total(self):
        orderitems=self.orderitem_set.all()
        total=sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems=self.orderitem_set.all()
        total=sum([item.quantity for item in orderitems])
        return total
    
    
class OrderItem(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    order= models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity=models.IntegerField(default=0, null=True, blank= True)
    date_added=models.DateTimeField(auto_now_add=True)
    
    @property
    def get_total(self):
        total=self.product.price * self.quantity
        return total
    
class Shipping_Address(models.Model):
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    order=models.ForeignKey(Order, on_delete=models.CASCADE,  null=True, blank=False)
    address=models.CharField(max_length=200, null=False)
    city=models.CharField(max_length=200, null=False)
    state=models.CharField(max_length=200, null=False)
    zipcode=models.CharField(max_length=200, null=False)
    country=models.CharField(max_length=200, null=False, default=True)
    date_added=models.DateTimeField(auto_now_add=True)
    contact=models.IntegerField(null=False)
    
    def __str__(self):
        return self.address