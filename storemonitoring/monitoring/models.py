from django.db import models
from django.utils import timezone

class Store(models.Model):
    store_id = models.CharField(max_length=50)
    timezone_str = models.CharField(max_length=50, default="America/Chicago")

class BusinessHour(models.Model):
    DAY_CHOICES = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    day = models.IntegerField(choices=DAY_CHOICES)
    start_time_local = models.TimeField()
    end_time_local = models.TimeField()

class StatusUpdate(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    timestamp_utc = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10)

    def calculate_downtime(self):
        business_hours = BusinessHour.objects.filter(store=self.store)
        downtime = 0
        for hour in business_hours:
            start_datetime = timezone.make_aware(
                timezone.datetime.combine(self.timestamp_utc.date(), hour.start_time_local),
                timezone.get_current_timezone()
            )
            end_datetime = timezone.make_aware(
                timezone.datetime.combine(self.timestamp_utc.date(), hour.end_time_local),
                timezone.get_current_timezone()
            )
            if start_datetime <= self.timestamp_utc <= end_datetime:
                downtime += 0  # store was active during business hours
            else:
                downtime += (end_datetime - start_datetime).seconds // 60  # calculate downtime in minutes
        return downtime

    def calculate_uptime(self):
        business_hours = BusinessHour.objects.filter(store=self.store)
        total_business_minutes = 0
        for hour in business_hours:
            start_datetime = timezone.make_aware(
                timezone.datetime.combine(self.timestamp_utc.date(), hour.start_time_local),
                timezone.get_current_timezone()
            )
            end_datetime = timezone.make_aware(
                timezone.datetime.combine(self.timestamp_utc.date(), hour.end_time_local),
                timezone.get_current_timezone()
            )
            total_business_minutes += (end_datetime - start_datetime).seconds // 60  # calculate business hours in minutes
        downtime = self.calculate_downtime()
        uptime = total_business_minutes - downtime
        return uptime
