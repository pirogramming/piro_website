from django import template

from internal.models import Comment

register = template.Library()

@register.simple_tag
def liked_by_user(cmt_id, user):
    try:
        Comment.objects.get(pk=cmt_id).like_set.get(user=user)
        return True
    except:
        return False