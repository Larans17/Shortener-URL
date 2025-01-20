import hashlib

from django.utils.timezone import now, timedelta


def generate_short_url(long_url):
    """Generate a unique short URL using a hash of the original URL."""
    hash_object = hashlib.sha256(long_url.encode())
    return hash_object.hexdigest()[:6]

def get_expiry_timestamp(hours=24):
    """Return an expiration timestamp."""
    return now() + timedelta(hours=hours)

def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        return x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')