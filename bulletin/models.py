from django.db import models

# Create your models here.

class BulletinBoard(models.Model):
    content = models.TextField()
    update_time = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'bulletin_board'
