from django.contrib.auth.models import User
from django.db import models


class Incident(models.Model):
    INCIDENT_TYPES = (
        ('vibr', 'Вибросито'),
        ('stop', 'Остановка'),
    )

    user = models.ForeignKey(User, null=True, on_delete=models.PROTECT)
    type = models.CharField(max_length=250, choices=INCIDENT_TYPES)
    description = models.CharField(max_length=1000, blank=True)
    datetime = models.DateTimeField()
    confirmed = models.BooleanField(default=False)