from django.db.models.signals import post_delete
from .models import Items
from django.dispatch import receiver
import os


@receiver(post_delete, sender=Items)
def delete_items_image(sender, instance, **kwargs):
    if instance.item_image:
        if os.path.isfile(instance.item_image.path):
            os.remove(instance.item_image.path)
            print('**************')
            print(f"Delete the Image file: {instance.item_image.path}")
            print('**************')



