from django.db import models


class Algorithm(models.Model):

    name = models.CharField(max_length=150)
    description = models.TextField(max_length=1000)

    class Meta:
        abstract = True
        constraints = [
            models.constraints.UniqueConstraint(fields=[], name='unique-algorithm')
        ]
