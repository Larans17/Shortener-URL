import hashlib

from django.db import models
from django.utils.timezone import now


class URL(models.Model):
    original_url = models.URLField(max_length=500)
    short_url = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    access_count = models.PositiveIntegerField(default=0)
    password_hash = models.CharField(max_length=64, blank=True, null=True)  # Store hashed password

    def is_expired(self):
        """Check if the URL is expired."""
        return now() > self.expires_at

    def set_password(self, raw_password):
        """Hash and store the password."""
        self.password_hash = hashlib.sha256(raw_password.encode()).hexdigest()

    def check_password(self, raw_password):
        """Validate the password."""
        return hashlib.sha256(raw_password.encode()).hexdigest() == self.password_hash

class AccessLog(models.Model):
    short_url = models.ForeignKey(URL, on_delete=models.CASCADE, related_name="logs")
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
