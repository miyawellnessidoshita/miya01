from django.db import models
import datetime
from accounts.models import CustomUser


def custom_timestamp_id():
    dt = datetime.datetime.now()
    return dt.strftime('%Y%m%d%H%M%S%f')


class AttendanceModels(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    days = models.DateTimeField(blank=True, null=True)
    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)
