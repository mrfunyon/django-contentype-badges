# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'Badge'
        db.create_table('badges_badge', (
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('reversed', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('icon_folder', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='badge_types', to=orm['contenttypes.ContentType'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
        ))
        db.send_create_signal('badges', ['Badge'])

        # Adding model 'BadgeLevel'
        db.create_table('badges_badgelevel', (
            ('level_image', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('badge', self.gf('django.db.models.fields.related.ForeignKey')(related_name='levels', to=orm['badges.Badge'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('unlock_value', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('badges', ['BadgeLevel'])

        # Adding model 'BadgeLevelToUser'
        db.create_table('badges_badgeleveltouser', (
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('badge_level', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['badges.BadgeLevel'])),
        ))
        db.send_create_signal('badges', ['BadgeLevelToUser'])

        # Adding model 'BadgeCounter'
        db.create_table('badges_badgecounter', (
            ('count', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('badge', self.gf('django.db.models.fields.related.ForeignKey')(related_name='badge_counts', to=orm['badges.Badge'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('badges', ['BadgeCounter'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'Badge'
        db.delete_table('badges_badge')

        # Deleting model 'BadgeLevel'
        db.delete_table('badges_badgelevel')

        # Deleting model 'BadgeLevelToUser'
        db.delete_table('badges_badgeleveltouser')

        # Deleting model 'BadgeCounter'
        db.delete_table('badges_badgecounter')
    
    
    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'badges.badge': {
            'Meta': {'object_name': 'Badge'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'badge_types'", 'to': "orm['contenttypes.ContentType']"}),
            'icon_folder': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reversed': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'badges.badgecounter': {
            'Meta': {'object_name': 'BadgeCounter'},
            'badge': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'badge_counts'", 'to': "orm['badges.Badge']"}),
            'count': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'badges.badgelevel': {
            'Meta': {'object_name': 'BadgeLevel'},
            'badge': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'levels'", 'to': "orm['badges.Badge']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level_image': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'unlock_value': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'user': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'badges'", 'symmetrical': 'False', 'through': "orm['badges.BadgeLevelToUser']", 'to': "orm['auth.User']"})
        },
        'badges.badgeleveltouser': {
            'Meta': {'object_name': 'BadgeLevelToUser'},
            'badge_level': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['badges.BadgeLevel']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }
    
    complete_apps = ['badges']
