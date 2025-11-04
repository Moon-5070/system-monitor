from django.db import models

class SystemStatus(models.Model):
    hostname = models.CharField(max_length=100)
    platform = models.CharField(max_length=100)
    cpu_percent = models.FloatField()
    memory_percent = models.FloatField()
    disk_percent = models.FloatField()
    net_sent_MB = models.FloatField()
    net_recv_MB = models.FloatField()
    ping_ms = models.FloatField(null=True, blank=True)
    download_Mbps = models.FloatField(null=True, blank=True)
    upload_Mbps = models.FloatField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.hostname} {self.cpu_percent:.1f}% @ {self.timestamp:%H:%M:%S}"
