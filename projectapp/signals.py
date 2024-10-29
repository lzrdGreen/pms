from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def add_user_to_authenticated_group(sender, instance, created, **kwargs):
    if created:  # Check if the user is newly created
        try:
            group, created = Group.objects.get_or_create(name='AuthenticatedUsers')
            # Add the user to the group
            instance.groups.add(group)
        except Group.DoesNotExist:
            pass
