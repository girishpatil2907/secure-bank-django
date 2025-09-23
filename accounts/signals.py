from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from bank.models import Account

@receiver(post_save, sender=User)
def create_user_account(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)