from django.db import models


class ItcHsMaster(models.Model):
    id = models.UUIDField(primary_key=True)
    hs_code = models.CharField(max_length=10)
    description = models.TextField(null=True, blank=True)
    policy = models.TextField(null=True, blank=True)
    policy_conditions = models.TextField(null=True, blank=True)
    schedule_type = models.CharField(max_length=10)
    chapter_num = models.IntegerField(null=True)
    metadata = models.JSONField(default=dict)
    parent_hs_code = models.CharField(max_length=10, null=True, blank=True)
    hs_level = models.IntegerField(null=True)

    class Meta:
        db_table = "itc_hs_master"
        managed = False
