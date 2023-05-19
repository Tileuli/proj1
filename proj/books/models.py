from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Manager

class Item(models.Model):
    DoesNotExist = None
    objects = None
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()
    image = models.ImageField(upload_to='item_images/',default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name

class LastViewed(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='last_viewed_items')
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-viewed_at']
        unique_together = ('user', 'item')

    def __str__(self):
        return f'{self.user.username} viewed {self.item.name} at {self.viewed_at}'

class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    payment_status = models.CharField(max_length=20, default='без статуса')

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Item, related_name='order_items', on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity

class Book(models.Model):
    objects = Manager()
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255,default='')
    publisher = models.CharField(max_length=255)
    publication_date = models.DateField()

    def __str__(self):
        return self.title

    def overall_rating(self):
        ratings = self.reviews.values_list('rating', flat=True)
        return sum(ratings) / len(ratings) if ratings else 0

class Review(models.Model):
    book = models.ForeignKey(Book, related_name='reviews', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    comment = models.TextField(default='')
    date = models.DateField()
    modified_date = models.DateField(null=True, blank=True)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)],default=0)

    def __str__(self):
        return self.comment

class Contributor(models.Model):
    first_names = models.CharField(max_length=50)
    last_names = models.CharField(max_length=50)

    def initialled_name(self):
        initials = [name[0].upper() for name in self.first_names.split()]
        return f"{self.last_names}, {' '.join(initials)}"

    def __str__(self):
        return self.initialled_name()