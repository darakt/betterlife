from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User
from organizations.models import default_organization
from comments.models import Comment

class Project(models.Model):
    class Goal(models.IntegerChoices):
        POVERTY = 0, _('No poverty')
        HUNGER = 1, _('Zero hunger')
        HEALTH = 2, _('Good health and well-being')
        EDUCATION = 3, _('Quality education')
        GENDER = 4, _('Gender equality')
        WATER = 5, _('Clean water and sanitation')
        ENERGY = 6, _('Affordable and clean energy')
        WORK = 7, _('Decent work and economic growth')
        INNOVATION = 8, _('Industry, innovation, and infrastructure')
        INEQUALITIES = 9, _('Reduces inequalities')
        SUSTAINABLE = 10, _('Sustainable cities and communities')
        CONSUMPTION = 11, _('Responsible consumption & production')
        CLIMATE = 12, _('Climate action')
        LIFEWATER = 13, _('Life below water')
        LIFELAND = 14, _('Life on land')
        INSTITUTION = 15, _('Peace, justice, and strong institutions')

    title = models.TextField(max_length=140)
    description = models.CharField(max_length=400)
    members = models.ManyToManyField(User, related_name='is_member_of_the_projects')
    comments = models.ManyToManyField(Comment, related_name='about')
    owner = models.ForeignKey('users.User', on_delete=models.PROTECT)
    goal = models.CharField(max_length=2, choices=Goal.choices, default=Goal.POVERTY)
    organization = models.ForeignKey('organizations.Organization', on_delete=models.PROTECT, default=1)

    def toJson(self):
        members = []
        for member in self.members.all():
            members.append(member.toJson())
        jsonified = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "goal": self.get_goal_display(),
            "owner": self.owner.toJson(),
            "members": members,
            "organization": self.organization.toJson()
        }
        return jsonified

    class Meta:
        permissions = [
            ('can_create_a_project', 'As a user I can create an project'),
            ('can_read_all_the_project','As a user I can read all the project'),
            ('can_update_project', 'As a user I can update a project'),
            ('can_delete_project', 'As a user I can delete a project')
        ]