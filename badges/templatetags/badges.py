try:
    from hashlib import md5
except ImportError:
    from md5 import md5
from django import template
from django.conf import settings
from django.core.cache import cache
from badges.models import Badge, BadgeLevel
from badges.utils import get_bagde_display_text
register = template.Library()


@register.tag
def get_badges_for_user(parser, token):
    '''{% get_badges_for_user user as variable_name %}
        where user is the user you want the badges from.'''
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

        badges = []
        for slug, badge in highest_badges.iteritems():
            badge_vars = {
                'badge': badge.badge,
                'icon': badge.get_level_image_path(),
                'alt': get_bagde_display_text(badge),
                'title': badge.badge.title,
                'slug': badge.badge.slug,
                'badgelevel': badge,
            }
            badges.append(badge_vars)

        context.update({self.variable_name:badges})
        return ''
