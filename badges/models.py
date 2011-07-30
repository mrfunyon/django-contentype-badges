from datetime import datetime

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User


class Badge(models.Model):
    """
    Generic badge.
    """
    title = models.CharField(max_length=50)
    slug = models.SlugField()
    icon_folder = models.CharField(max_length=100, help_text="Trailing Slash is required.(this goes from the 'STATIC_MEDIA_URL/images/badges/' directory Example: comments/")
    content_type = models.ForeignKey(ContentType, related_name="badge_types", verbose_name='Content Type')
    reversed = models.BooleanField(help_text="Check this box to count things with a reference to the user this is done to (i.e. # of your comments voted up)")

    def __unicode__(self):
        return u'%s Badge'%(self.title,)
    
class BadgeLevel(models.Model):
    """
    levels of a particular badge
    """
    badge = models.ForeignKey(Badge, related_name='levels')
    level_image = models.CharField(max_length=100, help_text='The image under the badges folder. Example: rev_10.png')
    unlock_value = models.PositiveIntegerField(help_text='Number needed to unlock this level.')
    user = models.ManyToManyField(User, related_name="badges", through='BadgeLevelToUser')

    def __unicode__(self):
        return u'Badge %s unlocks at %s' %(self.badge.title, self.unlock_value)

    def get_level_image_path(self):
        # this shouldn't be hard coded
        return "images/badges/%s%s"%(self.badge.icon_folder, self.level_image )
    
    def award_to(self, user):
        has_badge = self in user.badges.all()
        if has_badge:
            return False

        b, created = BadgeLevelToUser.objects.get_or_create(badge_level=self, user=user)
        if not created:
            return True

        message_template = "You just got the badge for "
        message_template += self.badge.title.replace('# of', str(self.unlock_value))
        message_template += '. <a href="/accounts/profile/">View it now!</a>'
        user.message_set.create(message = message_template)

        return BadgeLevelToUser.objects.filter(badge_level=self, user=user).count()

class BadgeLevelToUser(models.Model):
    badge_level = models.ForeignKey(BadgeLevel)
    user = models.ForeignKey(User)

    created = models.DateTimeField(default=datetime.now)

class BadgeCounter(models.Model):
    """
    Counter used to count one action a user does to a attain a badge
    """
    badge = models.ForeignKey(Badge, related_name='badge_counts')
    user = models.ForeignKey(User)
    count = models.PositiveIntegerField()

    def __unicode__(self):
        if not self.is_maxed:
            return u'%s is working toward the %s badge with %s of %s'%(self.user.get_full_name(), self.badge.title, self.count, self.get_next_level().unlock_value)
        else:
            return u'Counting badge %s Maxed out for %s'%(self.badge.title, self.user.get_full_name())
    
#    def award(self):
#        if not self.is_awarded:
#            BadgeToUser.objects.create(badge=self.badge, user=self.user)
#
#            #badge_awarded.send(sender=self.meta_badge, user=self.user, badge=self.badge)
#
#            message_template = "You just got the %s Badge!"
#            message_template = message_template % self.badge.title
#            message_template = message_template.replace("#", self.count)
#            self.user.message_set.create(message = message_template)
#
#        return BadgeToUser.objects.filter(badge=self.badge, user=self.user).count()

    def get_next_level(self):
        from sosd.badges.models import BadgeLevel #?$?$?$ WTF, Why do I have to do this?!
        for level in BadgeLevel.objects.filter(badge=self.badge).order_by('unlock_value'):
            # to account for badges that are awarded immediately (i.e. your count is 1 and unlock_value is set to 1.
            if self.count == 1 and level.unlock_value == 1:
                return level
            if self.count > level.unlock_value:
                continue
            return level

    @property
    def is_maxed(self):
        from sosd.badges.models import BadgeLevel #?$?$?$ WTF, Why do I have to do this?!
        highest_level = BadgeLevel.objects.filter(badge=self.badge).order_by('-unlock_value')[0]
        if self.count == highest_level.unlock_value:
            return True
        return False


from badges.listeners import start_listening
start_listening()
