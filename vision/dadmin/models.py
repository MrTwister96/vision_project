from django.db import models


class Option(models.Model):
    key = models.CharField(verbose_name='Option Name', max_length=50, null=False, blank=False)
    value = models.CharField(verbose_name='Option Value', max_length=50, null=False, blank=False)

    class Meta:
        verbose_name = 'Option'
        verbose_name_plural = 'Options'

    def __str__(self):
        return self.key
