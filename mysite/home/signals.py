from django.contrib.auth.models import User
from .models import Contact
from django.db.models.signals import post_save
from django.dispatch import receiver
'''
@receiver(post_save,sender=User)
def create_contact(sender,instance,created,**kwargs):
    if created:
        Contact.objects.create(staff=instance)

@receiver(post_save,sender=User)
def save_contact(sender,instance,**kwargs):
    instance.profile.save()    
'''    