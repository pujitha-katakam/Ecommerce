# models.py

from django.db import models
from django.contrib.auth.models import User


class Catg(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class SubCatg(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Catg, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class prod_type(models.Model):
    name=models.CharField(max_length=100)
    #  category=models.ForeignKey(SubCatg, on_delete=models.CASCADE)
    categories = models.ManyToManyField(SubCatg)

    def __str__(self):
        return self.name


class prodss(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price= models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    image = models.ImageField(upload_to='product_images/')
    category = models.ForeignKey(Catg, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCatg, on_delete=models.CASCADE)
    product_type = models.ForeignKey(prod_type, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.name
    

# Create your models here.
class Usef(models.Model):
    otp = models.CharField(max_length=6, blank=True)

# Create your models here.
STATE_CHOICES = (
('Andaman & Nicobar Islands', 'Andaman & Nicobar Islands'),
('Andhra Pradesh', 'Andhra Pradesh'),
('Arunachal Pradesh', 'Arunachal Pradesh'),
('Assam', 'Assam'),
('Bihar', 'Bihar'),
('Chandigarh', 'Chandigarh'),
('Chattisgarh', 'Chattisgarh'),
('Dadra & Nagar Haveli', 'Dadra & Nagar Haveli'),
('Daman and Diu', 'Daman and Diu'),
('Delhi', 'Delhi'),
( 'Goa', 'Goa'),
( 'Gujrat', 'Gujrat'),
('Haryana', 'Haryana'),
('Himachal Pradesh', 'Himachal Pradesh'),
('Jammu & Kashmir','Jammu & Kashmir'),
('Jharkhand', 'Jharkhand'),
('Karnataka', 'Karnataka'),
('Kerala', 'Kerala'),
('Lakshadweep', 'Lakshadweep' ),
('Madhya Pradesh', 'Madhya Pradesh'),
('Maharashtra', 'Maharashtra'),
('Manipur', 'Manipur'),
('Meghalaya', 'Meghalaya'),
('Mizoram', 'Mizoram'),
('Nagaland', 'Nagaland'),
('Odisa', 'Odisa'),
('Puducherry', 'Puducherry'),
('Punjab', 'Punjab'),
('Rajasthan', 'Rajasthan'),
('Sikkim' ,'Sikkim'),
('Tamil Nadu' ,'Tamil Nadu'),
('Telangana', 'Telangana'),
(' Tripura', 'Tripura'),
('Uttarakhand', 'Uttarakhand'),
('Uttar Pradesh', 'Uttar Pradesh'),
('West Bengal', 'West Bengal'),)


class Customer (models.Model):
    user = models. ForeignKey(User,on_delete=models. CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    mobile = models.BigIntegerField(default=0)
    zipcode = models.IntegerField(default=0)
    state = models.CharField(choices=STATE_CHOICES, max_length=100)

    def __str__(self) :
        return self.name

class Cart(models.Model) :
    user = models.ForeignKey (User, on_delete=models. CASCADE)
    product = models.ForeignKey(prodss, on_delete=models. CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.user)

    @property
    def total_cost(self):
        return self.quantity * self.product.price
    
STATUS_CHOICES=(
    ('Pending','Pending'),
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancelled','Cancelled')
)
    
class Orders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address=models.ForeignKey(Customer, on_delete=models.CASCADE)
    product=models.ForeignKey(prodss, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField()
    ordered_date=models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=50,
        default="Pending"
        )


class Buynow(models.Model) :
    user = models.ForeignKey (User, on_delete=models. CASCADE)
    product = models.ForeignKey(prodss, on_delete=models. CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.user)

    @property
    def total_cost(self):
        return self.quantity * self.product.price