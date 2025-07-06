from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta

class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    clock_in = models.DateTimeField(null=True, blank=True)
    clock_out = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.date}"

    @property
    def total_break_time(self):
        total = timedelta()
        for br in self.break_set.all():
            if br.start and br.end:
                total += (br.end - br.start)
        return total

class Break(models.Model):
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Break for {self.attendance.user.username} on {self.attendance.date}"
