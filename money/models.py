from django.db import models
from django.db.models import Max

from accounts.models import PiroUser
from internal.models import InfoBook


class PiroMoney(models.Model):
    user = models.ForeignKey(PiroUser, on_delete=models.CASCADE, default=None, limit_choices_to={'piro_no':InfoBook.objects.aggregate(Max('piro_no')).get("piro_no__max")})
    CHOICES=(('late','지각'),
             ('absent', '결석'),
             ('no_assignment', '과제 미제출'))
    type = models.CharField(max_length=20, choices=CHOICES)
    day = models.DateField(auto_now_add=False)

    def __str__(self):
        return f'{self.user} {self.type}'


