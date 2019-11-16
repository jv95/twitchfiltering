from django.db import models


class live_streams(models.Model):
    id = models.IntegerField().primary_key=True
    user_id = models.IntegerField()
    user_name = models.TextField()
    game_id = models.IntegerField()
    type = models.TextField()
    title = models.TextField()
    viewer_count = models.IntegerField()
    started_at = models.DateTimeField()
    language = models.TextField()
    thumbnail_url = models.TextField()
    tag_ids = models.TextField()
