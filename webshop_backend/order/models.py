from djongo import models
from bson import ObjectId
from ..authentication.models import User
from ..product.models import Product
import uuid

class OrderItem(models.Model):
    product_id = models.ObjectIdField()  # Store the ObjectId of the product
    quantity = models.PositiveIntegerField(default=1)


class Order(models.Model):
    _id = models.ObjectIdField()  # MongoDB's default ObjectId
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ArrayField(model_container=OrderItem)  # ArrayField for multiple products
    total_value = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'orders'

    def __str__(self):
        return f"Order {self._id} for {self.user.username}"

    def calculate_total(self):
        total_value = 0
        for item in self.products:
            product = Product.objects.get(_id=item['product_id'])  # Get product by ID
            total_value += item['quantity'] * product.price  # Calculate total price based on quantity and product price
        self.total_value = total_value
        self.save()

