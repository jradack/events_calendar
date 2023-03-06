from django.db import models

# Create your models here.
class Event(models.Model):
    # Required entries
    name = models.CharField(max_length=200)
    date = models.DateField()
    venue = models.CharField(max_length=100)
    # Optional entries
    cost = models.DecimalField(max_digits=5, decimal_places=2)
    door_time = models.DateTimeField()
    event_time = models.DateTimeField()
    age_restriction = models.CharField(max_length=50)
    tagline = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100)
    event_link = models.URLField()
    stage = models.CharField(max_length=100)
    sold_out = models.BooleanField(default=False)
    thumbnail_image = models.URLField()
    # Backend fields
    pinned = models.BooleanField(default=False)
    hidden = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.name} ({self.date} @ {self.venue})"