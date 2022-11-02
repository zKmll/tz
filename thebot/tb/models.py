from tabnanny import verbose
from django.db import models

class Profile(models.Model):
    external_id = models.PositiveIntegerField(
        verbose_name = 'user ID',
        unique = True
    )
    name = models.TextField(
        verbose_name = 'username'
    )

    def __str__(self):
        return f'#{self.external_id} {self.name}'

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'


class Message(models.Model):
    profile = models.ForeignKey(
        to = 'tb.Profile',
        verbose_name = 'Profile',
        on_delete = models.PROTECT , 
    )
    text = models.TextField(
        verbose_name = 'Text', 
    )
    created_at = models.DateTimeField(
        verbose_name = 'Receiving time',
        auto_now_add = True
    )

    def __str__(self):
        return f'Message {self.pk} from {self.profile}'

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
