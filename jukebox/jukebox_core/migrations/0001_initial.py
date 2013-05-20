# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Artist'
        db.create_table('jukebox_core_artist', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('jukebox_core', ['Artist'])

        # Adding model 'Genre'
        db.create_table('jukebox_core_genre', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('jukebox_core', ['Genre'])

        # Adding model 'Album'
        db.create_table('jukebox_core_album', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('Artist', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['jukebox_core.Artist'])),
        ))
        db.send_create_signal('jukebox_core', ['Album'])

        # Adding model 'Song'
        db.create_table('jukebox_core_song', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Artist', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['jukebox_core.Artist'])),
            ('Album', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['jukebox_core.Album'], null=True)),
            ('Genre', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['jukebox_core.Genre'], null=True)),
            ('Title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('Year', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('Length', self.gf('django.db.models.fields.IntegerField')()),
            ('Filename', self.gf('django.db.models.fields.CharField')(max_length=1000)),
        ))
        db.send_create_signal('jukebox_core', ['Song'])

        # Adding model 'Queue'
        db.create_table('jukebox_core_queue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Song', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['jukebox_core.Song'], unique=True)),
            ('Created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('jukebox_core', ['Queue'])

        # Adding M2M table for field User on 'Queue'
        db.create_table('jukebox_core_queue_User', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('queue', models.ForeignKey(orm['jukebox_core.queue'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('jukebox_core_queue_User', ['queue_id', 'user_id'])

        # Adding model 'Favourite'
        db.create_table('jukebox_core_favourite', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Song', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['jukebox_core.Song'])),
            ('User', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('Created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('jukebox_core', ['Favourite'])

        # Adding unique constraint on 'Favourite', fields ['Song', 'User']
        db.create_unique('jukebox_core_favourite', ['Song_id', 'User_id'])

        # Adding model 'History'
        db.create_table('jukebox_core_history', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Song', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['jukebox_core.Song'])),
            ('Created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('jukebox_core', ['History'])

        # Adding M2M table for field User on 'History'
        db.create_table('jukebox_core_history_User', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('history', models.ForeignKey(orm['jukebox_core.history'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('jukebox_core_history_User', ['history_id', 'user_id'])

        # Adding model 'Player'
        db.create_table('jukebox_core_player', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Pid', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('jukebox_core', ['Player'])


    def backwards(self, orm):
        # Removing unique constraint on 'Favourite', fields ['Song', 'User']
        db.delete_unique('jukebox_core_favourite', ['Song_id', 'User_id'])

        # Deleting model 'Artist'
        db.delete_table('jukebox_core_artist')

        # Deleting model 'Genre'
        db.delete_table('jukebox_core_genre')

        # Deleting model 'Album'
        db.delete_table('jukebox_core_album')

        # Deleting model 'Song'
        db.delete_table('jukebox_core_song')

        # Deleting model 'Queue'
        db.delete_table('jukebox_core_queue')

        # Removing M2M table for field User on 'Queue'
        db.delete_table('jukebox_core_queue_User')

        # Deleting model 'Favourite'
        db.delete_table('jukebox_core_favourite')

        # Deleting model 'History'
        db.delete_table('jukebox_core_history')

        # Removing M2M table for field User on 'History'
        db.delete_table('jukebox_core_history_User')

        # Deleting model 'Player'
        db.delete_table('jukebox_core_player')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
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
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'jukebox_core.album': {
            'Artist': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['jukebox_core.Artist']"}),
            'Meta': {'ordering': "['Title']", 'object_name': 'Album'},
            'Title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'jukebox_core.artist': {
            'Meta': {'ordering': "['Name']", 'object_name': 'Artist'},
            'Name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'jukebox_core.favourite': {
            'Created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'Meta': {'ordering': "['-Created']", 'unique_together': "(('Song', 'User'),)", 'object_name': 'Favourite'},
            'Song': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['jukebox_core.Song']"}),
            'User': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'jukebox_core.genre': {
            'Meta': {'ordering': "['Name']", 'object_name': 'Genre'},
            'Name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'jukebox_core.history': {
            'Created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'Meta': {'ordering': "['-Created']", 'object_name': 'History'},
            'Song': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['jukebox_core.Song']"}),
            'User': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'null': 'True', 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'jukebox_core.player': {
            'Meta': {'object_name': 'Player'},
            'Pid': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'jukebox_core.queue': {
            'Created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'Meta': {'object_name': 'Queue'},
            'Song': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['jukebox_core.Song']", 'unique': 'True'}),
            'User': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'jukebox_core.song': {
            'Album': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['jukebox_core.Album']", 'null': 'True'}),
            'Artist': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['jukebox_core.Artist']"}),
            'Filename': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'Genre': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['jukebox_core.Genre']", 'null': 'True'}),
            'Length': ('django.db.models.fields.IntegerField', [], {}),
            'Meta': {'ordering': "['Title', 'Artist', 'Album']", 'object_name': 'Song'},
            'Title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'Year': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['jukebox_core']