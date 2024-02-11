from django.db import models

class NetworkTestResult(models.Model):
    min_download_speed = models.FloatField()
    max_download_speed = models.FloatField()
    avg_download_speed = models.FloatField()
    min_upload_speed = models.FloatField()
    max_upload_speed = models.FloatField()
    avg_upload_speed = models.FloatField()
    ping = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'network_test_app'

    def __str__(self):
        return f"Network Test Result - {self.created_at}"