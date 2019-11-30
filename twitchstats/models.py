from django.db import models


class live_streams(models.Model):
    stream_id = models.TextField(default=None, max_length=1024, primary_key=True)
    user_id = models.TextField(default=None, blank=True, null=True)
    user_name = models.TextField(default=None, blank=True, null=True)
    game_id = models.TextField(default=None, blank=True, null=True)
    type = models.TextField(default=None, blank=True, null=True)
    title = models.TextField(default=None, blank=True, null=True)
    viewer_count = models.BigIntegerField(default=None, blank=True, null=True)
    started_at = models.DateTimeField(default=None, blank=True, null=True)
    language = models.TextField(default=None, blank=True, null=True)
    thumbnail_url = models.TextField(default=None, blank=True, null=True)
    tag_ids = models.TextField(default=None, blank=True, null=True)


class live_streams_performance(models.Model):
    date = models.TextField(default=None, blank=True, null=True)
    number_of_streams = models.TextField(default=None, blank=True, null=True)
    final_time = models.TextField(default=None, blank=True, null=True)
    request_count = models.TextField(default=None, blank=True, null=True)


class game_identity(models.Model):
    game_id = models.TextField(default=None, max_length=1024, primary_key=True)
    game_name = models.TextField(default=None, blank=True, null=True)
    box_art_url = models.TextField(default=None, blank=True, null=True)


class game_identity_performance(models.Model):
    date = models.TextField(default=None, blank=True, null=True)
    number_of_games = models.TextField(default=None, blank=True, null=True)
    final_time = models.TextField(default=None, blank=True, null=True)
    request_count = models.TextField(default=None, blank=True, null=True)