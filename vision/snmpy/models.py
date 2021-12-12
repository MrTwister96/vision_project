from datetime import timedelta
from django.db import models
from django.dispatch import receiver
from django_celery_beat.models import IntervalSchedule, PeriodicTask
from celery.schedules import schedule
from django_celery_beat.schedulers import ModelEntry
import uuid
import json


class Node(models.Model):
    uid = models.UUIDField(verbose_name='Unique ID', unique=True, editable=False, default=uuid.uuid4)
    name = models.CharField(verbose_name='Custom Name', max_length=250, blank=True, null=True)
    ip = models.GenericIPAddressField(verbose_name='IP Address', unique=True, blank=False, null=False)
    snmpPort = models.IntegerField(verbose_name='SNMP Port', default=161)
    snmpCommunityString = models.CharField(verbose_name='SNMP Community String', max_length=250, null=False, blank=False, default="1qazxsw2")
    snmpHostname = models.CharField(verbose_name='SNMP Hostname', max_length=250, null=True, blank=True)
    snmpDescription = models.TextField(verbose_name='SNMP System Description', max_length=50000, null=True, blank=True)
    snmpPollingInterval = models.IntegerField(verbose_name='SNMP Polling Interval (Seconds)', default=60)

    class Meta:
        verbose_name = 'Node'
        verbose_name_plural = 'Nodes'

    def __str__(self):
        return self.ip


@receiver(models.signals.post_save, sender=Node)
def node_post_save(sender, instance, created, **kwargs):
    if created:
        intervalSchedule = IntervalSchedule.from_schedule(schedule(timedelta(seconds=instance.snmpPollingInterval)))
        intervalSchedule.save()
        modelData = dict(
            name=instance.uid,
            task='snmpy.tasks.pollNode',
            interval_id=intervalSchedule.pk,
            args=json.dumps([instance.uid.__str__()])
        )

        periodicTask = PeriodicTask(**modelData)
        periodicTask.save()

        me = ModelEntry(periodicTask)
        me.save()


@receiver(models.signals.post_delete, sender=Node)
def node_post_delete(sender, instance, **kwargs):
    periodicTask = PeriodicTask.objects.get(name=instance.uid)
    periodicTask.delete()
