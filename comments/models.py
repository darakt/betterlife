from turtle import title
from django.db import models
from users.models import get_deleted_comment, get_placeholder_for_deleted_comment


def get_placeholder():
    return Comment.objects.get(id=1)

class Comment(models.Model):
    title = models.CharField(max_length=80)
    text = models.CharField(max_length=280)
    created_on = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    written_by = models.ForeignKey('users.User', on_delete=models.SET(get_placeholder_for_deleted_comment), related_name='has_written', default=1, db_column='written_by')
    in_response_to = models.ForeignKey('self', on_delete=models.SET(get_placeholder), blank=True, null=True, db_column='in_response_to') # I implement the soft-delete through set
    def toJson(self):
        jsonified = {
            'id': self.id,
            'title': self.title,
            'text': self.text,
            'created_on': self.created_on,
            'last_update': self.last_update,
            'written_by': self.written_by.toJson(),
        }
        if self.in_response_to is not None:
            jsonified['in_response_to'] = self.in_response_to.toJson() # can cause problems with the performances
        return jsonified

    class Meta:
        permissions = [
                ('can_create_a_comment', 'As a user I can publish a comment'),
                ('can_read_all_the_comments','As a user I can read all the comments'),
                ('can_update_comments', 'As a user I can update my comments'),
                ('can_delete_comment', 'As a user I can delete my tweet')
                ]