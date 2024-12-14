from django.db import models
from user_app.models import User  # Import User dari user_app
from courses_app.models import Post
from user_app.models import Product
# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE ,default=1)  # Link to User model
    email = models.EmailField(null=True)  # Assuming you want to keep the email too
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.BooleanField(default=False)
    

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
	# Foreign Keys
	order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
	post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	quantity = models.PositiveBigIntegerField(default=1)
	product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True)
	price = models.DecimalField(max_digits=12, decimal_places=2)

	def __str__(self):
		return f'Order Item - {str(self.id)}'