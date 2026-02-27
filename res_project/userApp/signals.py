from .models import CustomUser, Profile
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import os



@receiver(post_save, sender=CustomUser)
def createUserProfile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        print('****************')
        print('Profile created!')
        print('****************')


# post_save.connect(createUserProfile, sender=CustomUser)  # either @reciever or this one required



@receiver(post_save, sender=CustomUser)
def updateUserProfile(sender, instance, created, **kwargs):
    if created is False:
        instance.profile.save()
        print('****************')
        print('Profile Updated!')
        print('****************')


# post_save.connect(updateUserProfile, sender=CustomUser)   # either @reciever or this one required


@receiver(post_delete, sender=Profile)
def delete_profile_image(sender, instance, **kwargs):
    if instance.profile_image:
        if os.path.isfile(instance.profile_image.path):
            os.remove(instance.profile_image.path)
            print("******************")
            print(f'Delete the Image file {instance.profile_image.path}')
            print("****************")
            


