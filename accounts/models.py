import uuid

from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfile(models.Model):
    AGENT = 'agent'
    CONTRACTOR = 'Contractor'

    user_type = (
        (AGENT, 'agent'),
        (CONTRACTOR, 'contractor')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=user_type,
                                 default=CONTRACTOR)
    phone = models.CharField(max_length=11, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    verification_uuid = models.UUIDField('Unique Verification UUID',
                                         default=uuid.uuid4)

    def __str__(self):
        return self.user.username