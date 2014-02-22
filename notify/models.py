from django.db import models

# Create your models here.

class Notification(models.Model):
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-pub_date']
    
    def __str__(self):
        return "Notification%d" % self.id
