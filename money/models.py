from django.db import models

from accounts.models import PiroUser


class PiroMoney(models.Model):
    user = models.ForeignKey(PiroUser, on_delete=models.CASCADE, default=None)
    CHOICES=(('late','지각'),
             ('absent', '결석'),
             ('no_assignment', '과제 미제출'))
    type = models.CharField(max_length=20, choices=CHOICES)
    day = models.DateField(auto_now_add=False)



