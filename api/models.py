from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    iin = models.CharField(max_length=12, blank=True, null=True)
    phone = models.CharField(max_length=20, unique=True, null=True)
    verified = models.BooleanField(default=False)
    role = models.CharField(
        max_length=20,
        choices=[
            ('guest', 'Guest'),
            ('user', 'User'),
            ('premium', 'Premium'),
            ('consultant', 'Consultant'),
            ('admin', 'Admin'),
        ],
        default='guest'
    )

    def __str__(self):
        return self.username or self.phone

class Chat(models.Model):
    CHAT_TYPE = [('ai','ai'), ('live','live')]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats')
    type = models.CharField(max_length=10, choices=CHAT_TYPE)
    metadata = models.JSONField(default=dict, blank=True)      # e.g. language, visa type
    created_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=50)  # 'user', 'ai', 'consultant'
    content = models.TextField()
    role_meta = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Subscription(models.Model):
    STATUS = [('active','active'), ('past_due','past_due'), ('canceled','canceled')]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    status = models.CharField(max_length=20, choices=STATUS)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    stripe_subscription_id = models.CharField(max_length=100, blank=True, null=True)

class EsimOrder(models.Model):
    STATUS = [('pending','pending'), ('active','active'), ('failed','failed')]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='esim_orders')
    country = models.CharField(max_length=100)
    plan_id = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    provider_order_id = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Consultant(models.Model):
    name = models.CharField(max_length=200)
    assigned_users = models.ManyToManyField(User, blank=True, related_name='consultants')
