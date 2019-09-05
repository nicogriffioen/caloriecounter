from datetime import datetime

from django.db import models
from django.utils.translation import ugettext as _

from caloriecounter.food.models import FoodProduct, Unit
from caloriecounter.user.models import User


class DiaryEntry(models.Model):
    class Meta:
        ordering = ['created_on']
        verbose_name = _('diary entry')
        verbose_name_plural = ('diary entries')

    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=False, editable=False)

    created_on = models.DateTimeField(auto_now_add=True, editable=False)

    date = models.DateField(_("Entry Date"), blank=False, default=datetime.now)
    time = models.TimeField(_("Entry Time"), blank=False, default=datetime.now)

    product = models.ForeignKey(to=FoodProduct, on_delete=models.CASCADE, blank=False)
    quantity = models.FloatField()
    unit = models.ForeignKey(to=Unit, on_delete=models.SET_NULL, null=True, blank=False)

    @property
    def nutritional_information(self):
        return {'energy' : '20 cals'}



    def clean(self, *args, **kwargs):
        super(DiaryEntry, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.created_on = self.created_on.replace(tzinfo=None)
        super(DiaryEntry, self).save(*args, **kwargs)

    def __str__(self):
        string = '{quantity} {unit} of {product}'

        return string.format(quantity=self.quantity, unit=self.unit, product=self.product)