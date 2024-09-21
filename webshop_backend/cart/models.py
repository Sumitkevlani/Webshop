# from djongo import models
# from bson import ObjectId
# from ..product.models import Product
# from ..authentication.models import User

# class CartItem(models.Model):
#     product_id = models.ObjectIdField()  # Store the ObjectId of the product
#     quantity = models.PositiveIntegerField(default=1)


# class Cart(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
#     items = models.ArrayField(model_container=CartItem, default=list)  # Default to empty list
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         db_table = 'carts'

#     def __str__(self):
#         return f"Cart for User: {self.user if self.user else 'Guest'}"

#     def add_item(self, product, quantity=1):
#         # Find the existing item in the cart
#         item = next((item for item in self.items if item.product_id == product._id), None)
#         if item:
#             # Update quantity if product is already in the cart
#             item.quantity += quantity
#         else:
#             # If product is not in the cart, add a new CartItem
#             self.items.append(CartItem(product_id=product._id, quantity=quantity))
#         self.save()

#     def remove_item(self, product_id):
#         # Remove the item by filtering out the product_id
#         self.items = [item for item in self.items if item.product_id != product_id]
#         self.save()

#     def get_items(self):
#         # Properly iterate over the CartItem objects in the items field
#         return [
#             {
#                 'product': Product.objects.get(_id=item.product_id),
#                 'quantity': item.quantity
#             }
#             for item in self.items  # No need for 'or []' since default is an empty list
#         ]


from djongo import models
from bson import ObjectId
from ..product.models import Product
from ..authentication.models import User

class CartItem(models.Model):
    product_id = models.ObjectIdField()  # Store the ObjectId of the product
    quantity = models.PositiveIntegerField(default=1)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    items = models.ArrayField(model_container=CartItem, default=list)  # Stores items as a list of dict-like objects
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'carts'

    def __str__(self):
        return f"Cart for User: {self.user if self.user else 'Guest'}"

    def add_item(self, product, quantity=1):
        # Check if there's enough stock
        if product.stock < quantity:
            raise ValueError(f"Not enough stock. Available: {product.stock}")

        existing_item = next((item for item in self.items if item['product_id'] == product._id), None)
        
        if existing_item:
            # If the item exists, update the quantity
            new_quantity = existing_item['quantity'] + quantity
            if new_quantity > product.stock:
                raise ValueError(f"Cannot add {quantity} more. It exceeds available stock.")
            existing_item['quantity'] = new_quantity
        else:
            # If the item doesn't exist, append a new one
            self.items.append({'product_id': product._id, 'quantity': quantity})
        
        self.save()

    def update_item(self, product_id, new_quantity):
        product = Product.objects.get(_id=product_id)
        
        if new_quantity > product.stock:
            raise ValueError(f"Cannot update to {new_quantity}. It exceeds available stock of {product.stock}.")

        item = next((item for item in self.items if item['product_id'] == product_id), None)
        
        if item:
            item['quantity'] = new_quantity
        else:
            raise ValueError(f"Product with id {product_id} not found in cart.")
        
        self.save()

    def remove_item(self, product_id):
        # Filter out the product based on product_id
        self.items = [item for item in self.items if item['product_id'] != product_id]
        self.save()

    def get_items(self):
        # Iterate over the items, treating them as dictionaries
        return [
            {
                'product': Product.objects.get(_id=item['product_id']),
                'quantity': item['quantity']
            }
            for item in self.items  # No need for 'or []' since default is an empty list
        ]
