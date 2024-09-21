from djongo import models

class Product(models.Model):
    _id = models.ObjectIdField()  # Djongo specific field for MongoDB
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.FloatField()
    rating = models.FloatField()  # Rating scale, e.g., 0-5
    stock = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'products'  # Specify the MongoDB collection name

    def __str__(self):
        return self.name
