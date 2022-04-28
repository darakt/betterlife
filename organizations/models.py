from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User

class Organization(models.Model):

    class Languages(models.TextChoices):
        AFAR = 'aa', _('Afar')
        ABKHAZIAN = 'ab', _('Abkhazian')
        AFRIKAANS = 'af', _('Afrikaans')
        AKAN = 'ak', _('Akan')
        ALBANIAN = 'sq', _('Albanian')
        AHMARIC = 'am', _('Amharic')
        ARABIC = 'ar', _('Arabic')

    name = models.CharField(max_length=280)
    description = models.CharField(max_length=400)
    language = models.CharField(max_length=2, choices=Languages.choices, default=Languages.AFAR)
    admins = models.ManyToManyField(User, related_name='administrated_by')
    members = models.ManyToManyField(User, related_name='member_of_organization')

    def toJson(self):
        admins = []
        for admin in self.admins.all():
            admins.append(admin.toJson())
        members = []
        for member in self.members.all():
            members.append(member.toJson())
        jsonified = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "admins": admins,
            "members": members
        }
        return jsonified

    class Meta:
        permissions = [
            ('can_create_an_organization', 'As a user I can create an organization'),
            ('can_read_all_the_organization','As a user I can read all the organization'),
            ('can_update_organization', 'As a user I can update my organization'),
            ('can_delete_organization', 'As a user I can delete my organization')
        ]