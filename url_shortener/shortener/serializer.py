from rest_framework import serializers

from .models import URL, AccessLog
from .utils import generate_short_url


class URLSerializer(serializers.ModelSerializer):
    short_url = serializers.ReadOnlyField()
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = URL
        fields = ['id', 'original_url', 'short_url', 'created_at', 'expires_at', 'access_count', 'password']

    def create(self, validated_data):
        validated_data['short_url'] = generate_short_url(validated_data['original_url'])
        password = validated_data.pop('password', None)
        instance = super().create(validated_data)
        if password:
            instance.set_password(password)
            instance.save()
        return instance



class AnalyticsSerializer(serializers.ModelSerializer):
    access_log = serializers.SerializerMethodField()
    class Meta:
        model = URL
        fields = ['id', 'short_url', 'access_count','access_log']
        
        
    def get_access_log(self,obj):
        access_list =[]
        if obj.logs:
            for data in obj.logs.all():
                access_list.append({'id':data.id,'timestamp':data.timestamp,'ip_address':data.ip_address})
        return access_list

class AccessLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessLog
        fields = ['id', 'short_url', 'timestamp', 'ip_address']