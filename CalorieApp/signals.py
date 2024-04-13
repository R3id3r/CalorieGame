from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Player, PlayerSkill, FarmingSkill

@receiver(post_save, sender=Player)
def create_player_skills(sender, instance, created, **kwargs):
    if created:
        # Assuming you want to add specific skills or all skills by default
        default_skills = FarmingSkill.objects.all()  # Adjust this as needed
        for skill in default_skills:
            PlayerSkill.objects.create(player=instance, skill=skill, level=1)