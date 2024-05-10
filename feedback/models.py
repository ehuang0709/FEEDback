from django.db import models
from django.contrib.auth.models import User
from django.db.models import JSONField

class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField()

    restaurant_name = models.CharField(max_length=100)
    restaurant_address = models.CharField(max_length=200)
    restaurant_city = models.CharField(max_length=100)
    restaurant_state = models.CharField(max_length=100)
    restaurant_zip = models.CharField(max_length=100)
    consumption_date_time = models.DateTimeField()

    symptoms = models.TextField()
    symptoms_start_date_time = models.DateTimeField()
    symptoms_stopped = models.BooleanField(default=False)

    suspected_illness_source = models.TextField()
    
    additional_info = models.TextField()

    file_names = JSONField(default=list, blank=True)

    admin_comment = models.TextField(blank=True)

    STATUS_CHOICES = (
        ('New', 'New'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
    )
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New')
    
    def save(self, *args, **kwargs):
        if not self.user_id or not User.objects.filter(pk=self.user_id).exists():
            anonymous_user, _ = User.objects.get_or_create(username="Anonymous")
            self.user = anonymous_user  # Set the user field with the User instance
        super().save(*args, **kwargs)


    def __str__(self):
        return f"Report has been submitted for {self.restaurant_name}"
    
    class Meta:
        app_label = 'feedback'
