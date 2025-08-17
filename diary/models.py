from django.conf import settings
from django.db import models
from django.urls import reverse

User = settings.AUTH_USER_MODEL

class Place(models.Model):
    class Kind(models.TextChoices):
        VISIT = 'visit', 'Место для посещения'
        HERITAGE = 'heritage', 'Объект культурного наследия'

    name = models.CharField(max_length=200)
    kind = models.CharField(max_length=10, choices=Kind.choices, default=Kind.VISIT)

    class Meta:
        ordering = ['name']
        unique_together = ('name', 'kind')

    def __str__(self):
        return f"{self.name} ({self.get_kind_display()})"

class Trip(models.Model):
    class Visibility(models.TextChoices):
        PUBLIC = 'public', 'Публично'
        PRIVATE = 'private', 'Только я'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trips')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    # Локация
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=200, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    # Период и стоимость
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Оценки (1-5)
    rating_convenience = models.PositiveSmallIntegerField(default=0)   # удобство передвижения
    rating_safety = models.PositiveSmallIntegerField(default=0)        # безопасность
    rating_crowd = models.PositiveSmallIntegerField(default=0)         # населённость (меньше — спокойнее)
    rating_greenery = models.PositiveSmallIntegerField(default=0)      # растительность

    # Места
    places_to_visit = models.ManyToManyField(Place, related_name='trips_to_visit', blank=True, limit_choices_to={'kind': 'visit'})
    heritage_sites = models.ManyToManyField(Place, related_name='trips_heritage', blank=True, limit_choices_to={'kind': 'heritage'})

    visibility = models.CharField(max_length=10, choices=Visibility.choices, default=Visibility.PUBLIC)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('trip_detail', args=[self.pk])

    def is_public(self):
        return self.visibility == Trip.Visibility.PUBLIC

    @property
    def avg_rating(self):
        vals = [v for v in [self.rating_convenience, self.rating_safety, self.rating_greenery] if v]
        return round(sum(vals)/len(vals), 1) if vals else 0

class Photo(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='photos/')
    caption = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['uploaded_at']

    def __str__(self):
        return self.caption or f"Фото #{self.pk}"
