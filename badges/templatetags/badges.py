from django import template
from django.conf import settings
from django.core.cache import cache
from badges.models import Badge, BadgeLevel

register = template.Library()


@register.tag
def get_badges_for_user(parser, token):
    '''{% get_badges_for_user user as variable_name %}
        where user is the user you want the badges from.
       Adds category groups to context.'''
    bits = token.contents.split()
    if bits[2] != 'as' or len(bits) < 4:
        raise template.TemplateSyntaxError, "%r usage: {% %r user as variable_name %}" % (bits[0], bits[0])
    return GetBadgesNode(bits[1], bits[3])

class GetBadgesNode(template.Node):
    def __init__(self, user, variable_name):
        self.variable_name = variable_name
        self.user = user

    def render(self, context):
        user = template.resolve_variable(self.user, context)
        highest_badges = {}
        for badge in user.badges.all():
            if badge not in highest_badges.keys():
                highest_badges.update({badge.badge.slug: badge})
                continue
            current_highest = highest_badges[badge.badge.slug]
            if badge.unlock_value > current_highest.unlock_value:
                highest_badges.update({badge.badge.slug: badge})

        return {self.variable_name:highest_badges}