import uuid

from django.db import models


# Create your models here.
class Application(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=1024)
    description = models.CharField(max_length=1024, blank=True, null=False)

    def __str__(self):
        return self.name


class Client(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=1024)
    application = models.ManyToManyField(Application, blank=True)

    valid_until = models.DateTimeField()
    machine_lock = models.BooleanField(default=False)
    machine_id = models.CharField(max_length=254, blank=True, default='')

    def __str__(self):
        return self.name + " - " + str(self.application)


class Resource(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    application = models.ForeignKey(Application, on_delete=models.CASCADE, editable=True)
    name = models.CharField(max_length=1024)
    data = models.FileField(editable=True, upload_to='resources/', )

    def save(self,*args,**kwargs,):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name + " - " + str(self.application)
