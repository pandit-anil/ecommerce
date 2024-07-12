from django.db import models
from django.contrib.auth.models import User


#System Setting

class Systemsetting(models.Model):
    sysname = models.CharField(max_length=30)
    logo = models.ImageField(upload_to='syslogo')
    contact = models.IntegerField()
    email = models.EmailField()

    address = models.CharField(max_length=200,default="Nepal")

    def save(self, *args, **kwargs):
        if Systemsetting.objects.exists():
            existing_instance = Systemsetting.objects.first()
            self.pk = existing_instance.pk  # Update the existing instance
        super(Systemsetting, self).save(*args, **kwargs)

    def __str__(self):
        return self.sysname

class Clients(models.Model):
    name = models.CharField(max_length=70)
    profession = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.IntegerField()
    address = models.CharField(max_length=200)
    image = models.ImageField(upload_to='client')

    def __str__(self):
        return self.name


class CustomerFeedback(models.Model):
     customer = models.ForeignKey(User, on_delete=models.CASCADE)
     feedback = models.TextField()

     def __str__(self):
         return self.customer.first_name
     


class Category(models.Model):
    cname = models.CharField(max_length=40)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.cname


class Bpost(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.IntegerField()
    image = models.ImageField(upload_to='images/')
    category = models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
    
    def __str__(self):
        return self.title

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    product = models.ForeignKey(Bpost,on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} of {self.product.name} in {self.cart.user.username}\'s cart'
    
    def get_total_price(self):
        return self.quantity * self.product.price

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem)
    total = models.DecimalField(max_digits=10, decimal_places=2,default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.first_name


class Comment(models.Model):
    post = models.ForeignKey(Bpost, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Comment by {self.author} on {self.post}'
