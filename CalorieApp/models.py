from django.db import models
#from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime

class FarmingSkill(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    max_level  = models.PositiveIntegerField(default=100, help_text="Max level available.")

    def __str__(self):
        return self.name

class Player(AbstractUser):
    email = models.EmailField(max_length=100) # unique=True
    gold_balance  = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    calorie_balance = models.PositiveIntegerField(default=0, help_text="Total calories in inventory?")
    gems_balance = models.PositiveIntegerField(default=0, help_text="Used to buy time.")
    farming_skills = models.ManyToManyField(FarmingSkill, through='PlayerSkill', related_name='players', blank=True)
    score = models.IntegerField(default=0)
    current_level = models.IntegerField(default=1)
    earned_experience_points = models.IntegerField(default=0)
    active = models.BooleanField(default=True)

    #USERNAME_FIELD = 'email'
    #REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

class PlayerSkill(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    skill = models.ForeignKey(FarmingSkill, on_delete=models.CASCADE)
    level = models.PositiveIntegerField(default=1, help_text="Current skill level.")
    xp = models.PositiveIntegerField(default=0, help_text="Total XP earned.")

    def __str__(self):
        return f"{self.player.username} - {self.skill.name} Level {self.level}"

# class GardenBed(models.Model):
#     name = models.CharField(max_length=100, blank=True)
#     length_ft = models.PositiveIntegerField()
#     width_ft = models.PositiveIntegerField()
#     #square_ft = length_ft * width_ft
#     soil_health = {
#         nitrogen: models.PositiveIntegerField(),
#         phosphorus: models.PositiveIntegerField(),
#         potassium: models.PositiveIntegerField()
#     }
#     walkway_path_width_ft = models.PositiveIntegerField()
#     #status = models.CharField(max_length=100) # planted, empty

class Field(models.Model):
    owner = models.ForeignKey(Player, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=100, default="Empty")
    bed_width_ft = models.FloatField(default="3.5")
    bed_length_ft = models.FloatField(default=100)

    def __str__(self):
        return f"{self.name}"

# on create crop, create seeds
class Crop(models.Model):
    name = models.CharField(max_length=100)
    variety = models.CharField(max_length=100)
    planting_season = models.CharField(max_length=50)
    harvest_time_minutes = models.CharField(max_length=50)
    days_til_germination = models.PositiveIntegerField()
    days_til_harvest = models.PositiveIntegerField()
    days_til_seed = models.PositiveIntegerField()
    weight_per_seed_grams = models.FloatField() # based on seeds per 100g?
    transplantable = models.BooleanField(default=False)
    #nutrient_requirements = 
    row_spacing_inches = models.FloatField()
    plant_spacing_inches = models.FloatField()
    produce_per_plant = models.PositiveIntegerField()
    harvests_per_planting = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} ({self.variety})"

# #link to crop?
class Seed(models.Model):
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name='seedCrop')
    name = models.CharField(max_length=100)
    seed_count = models.PositiveIntegerField(default=100)  # Example field

    def save(self, *args, **kwargs):
        self.name = self.crop.name + " Seeds"
        super(Seed, self).save()

    def __str__(self):
        return f"{self.name} ({self.seed_count})"

class Planting(models.Model):
    seed = models.ForeignKey(Seed, on_delete=models.CASCADE, related_name='seeds')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='plantingPlayer')
    planting_date = models.DateTimeField(editable=False) #, auto_now_add=True
    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name='plantingField')
    notes = models.TextField(blank=True, null=True)
    rows_per_bed = models.FloatField(default=1)
    plants_per_row = models.FloatField(default=1)
    total_plants_per_bed = models.FloatField(default=1)
    harvest_date = models.DateTimeField(editable=False)
    seed_date = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        self.planting_date = datetime.datetime.now()
        self.rows_per_bed = round(self.field.bed_width_ft / self.seed.crop.row_spacing_inches, 0)
        self.plants_per_row = round(self.field.bed_length_ft / self.seed.crop.plant_spacing_inches, 0)
        self.total_plants_per_bed = round(self.rows_per_bed * self.plants_per_row, 0)
        self.harvest_date = (self.planting_date + datetime.timedelta(days=self.seed.crop.days_til_harvest, hours=0, minutes=0, seconds=0)).strftime('%Y-%m-%d %H:%M')
        self.seed_date = self.planting_date + datetime.timedelta(days=self.seed.crop.days_til_seed)
        super(Planting, self).save()

    def __str__(self):
        return f"Planting of {self.seed.name} on {self.planting_date}"

@receiver(post_save, sender=Crop)
def create_seeds_for_crop(sender, instance, created, **kwargs):
    if created:
        Seed.objects.create(crop=instance)

# #tasks are assigned to the employee's queue/schedule
# class Task(models.Model):
#     name = models.CharField(max_length=100)
#     assigned_to = OneToOne(Employee) # or self?
#     calories_required = ""
#     tools_required = ""
#     time_required_minutes = ""
#     inputs_required = ""

