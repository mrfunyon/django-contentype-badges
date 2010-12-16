"""
all of this is crap, basicly it attaches generic content types to various different types of badges using signals to dynamicly do everything
"""
from django.conf import settings
from badges.models import  Badge, BadgeCounter
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from django.db.models import F
from django.core.cache import cache



def check_for_user_instances(object):
    # goes through the models fields looking for a user field.
    # there might be more than one row that contains User model references.
    instance_names = getattr(settings,'BADGES_USER_INSTANCE_NAMES',['from_user', 'user'])
    possibilities = []
    opts = object._meta
    for field in opts.fields:
        fname = field.get_attname()
        if '_id' in fname:
            fname = fname.replace("_id","")
        row = getattr(object, fname)
        if isinstance(row, User):
            possibilities.append(fname)
    for name in instance_names:
        if name in possibilities:
            possibilities.remove(name)
            possibilities.insert(0, name)
    return possibilities


def listen_for_badge_model_save(sender, instance, created, **kwargs):
    print "Save on %s"%(instance)
    if created:
        user_instances = check_for_user_instances(instance)
        try:
            user = getattr(instance, user_instances[0])
        except:
            return
        # this is necessary because we are getting attached to any type of object with reckless abandon.
        # find out which badge were are listening for
        badge_content_type = ContentType.objects.get_for_model(instance)
        badges = Badge.objects.filter(content_type=badge_content_type)
        for badge in badges:
            c, created = BadgeCounter.objects.get_or_create(badge=badge, user=user, defaults={'count':1})
            count = c.count + 1
            if not created:
                if not c.is_maxed:
                    id = c.id
                    c.count = F('count') + 1
                    c.save()
                    # reload badge counter object
                    c = BadgeCounter.objects.get(pk=id)
                next_level_badge = c.get_next_level()
                print "Next Badge awarded in %s actions"%(next_level_badge.unlock_value - count)
                if count >= next_level_badge.unlock_value:
                    print "Number Needed: %s"%(next_level_badge.unlock_value)
                    print "Count: %s"%(count)
                    print "Awarding badge %s to %s"%(next_level_badge, user)
                    next_level_badge.award_to(user)
                c.save()

def listen_for_badge_model_delete(sender, instance, **kwargs):
    print "Delete on %s"%(instance)
    user_instances = check_for_user_instances(instance)
    try:
        user = getattr(instance, user_instances[0])
    except:
        return
    # this is necessary because we are getting attached to any type of object with reckless abandon.
    # find out which badge were are listening for
    badge_content_type = ContentType.objects.get_for_model(instance)
    badges = Badge.objects.filter(content_type=badge_content_type)
    for badge in badges:
        c, created = BadgeCounter.objects.get_or_create(badge=badge, user=user, defaults={'count':1})
        count = c.count - 1
        if count == 0:
            print "Attempt to decrement below threshold."
            return
        if not created:
            if not c.is_maxed:
                id = c.id
                c.count = F('count') - 1
                c.save()
                # reload badge counter object
                c = BadgeCounter.objects.get(pk=id)
            next_level_badge = c.get_next_level()
            print "Next Badge awarded in %s actions"%(next_level_badge.unlock_value - count)
            if count >= next_level_badge.unlock_value:
                print "Number Needed: %s"%(next_level_badge.unlock_value)
                print "Count: %s"%(count)
                print "Awarding badge %s to %s"%(next_level_badge, user)
                next_level_badge.award_to(user)
            c.save()

def listen_for_new_badges(sender, instance, created, **kwargs):
    """
    This listener will handle when new MetaBadge objects get saved
    """
    if created:
        model = instance.content_type.model_class()
        print "Attaching to the post_save signal from %s"%model
        post_save.connect(listen_for_badge_model_save, sender=model, dispatch_uid="badge:%s.%s"%(instance.content_type.model, instance.content_type.app_label))
        pre_delete.connect(listen_for_badge_model_delete, sender=model, dispatch_uid="badge:%s.%s"%(instance.content_type.model, instance.content_type.app_label))

def attach_badges_to_singals():
    """
    Attaches MetaBadge objects to signals for selected contenttypes
    """
    try:
        badges_to_attach = Badge.objects.all()
        for badge in badges_to_attach:
            # get all the badges, and attach post_save signal handlers to each contenttype
            model = badge.content_type.model_class()
            print "Attaching to the post_save signal from %s"%model
            post_save.connect(listen_for_badge_model_save, sender=model, dispatch_uid="badge:%s.%s"%(badge.content_type.model, badge.content_type.app_label))
            pre_delete.connect(listen_for_badge_model_delete, sender=model, dispatch_uid="badge:%s.%s"%(badge.content_type.model, badge.content_type.app_label))

        # connect up the Badge Listener
        post_save.connect(listen_for_new_badges, sender=Badge)
    except:
        pass

def start_listening():
    if getattr(settings,'BADGES_ENABLE_LISTENER', False):
        attach_badges_to_singals()
