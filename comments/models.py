from django.db import models
from users.models import get_deleted_comment, get_placeholder_for_deleted_comment

class Comment(models.Model):
    title = models.CharField(max_length=80)
    text = models.CharField(max_length=280)
    created_on = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    written_by = models.ForeignKey('users.User', on_delete=models.SET_DEFAULT, related_name='has_written', default=1)
    in_response_to = models.ForeignKey('self', on_delete=models.SET(get_placeholder_for_deleted_comment), blank=True, null=True)
    class Meta:
        permissions = [
                ('can_create_a_comment', 'As a user I can publish a comment'),
                ('can_read_all_the_comments','As a user I can read all the comments'),
                ('can_update_my_comments', 'As a user I can update my comments'),
                ('can_delete_my_comment', 'As a user I can delete my tweet')
                ]