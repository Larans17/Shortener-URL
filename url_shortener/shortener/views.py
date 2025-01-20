from django.shortcuts import redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import URL, AccessLog
from .serializer import AnalyticsSerializer, URLSerializer
from .utils import get_client_ip, get_expiry_timestamp


class ShortenURLView(APIView):
    def post(self, request):
        data = request.data.copy()
        expiry_hours = data.get('expiry_hours', 24)
        data['expires_at'] = get_expiry_timestamp(expiry_hours)
        serializer = URLSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RedirectURLView(APIView):
    def get(self, request, short_url):
        url_obj = URL.objects.get(short_url=short_url)
        if url_obj.is_expired():
            return Response({"error": "URL has expired"}, status=status.HTTP_410_GONE)
        
        # Password validation
        password = request.GET.get('password')
        if url_obj.password_hash and not password:
            return Response({"error": "Password required to access this URL"}, status=status.HTTP_400_BAD_REQUEST)
        
        if url_obj.password_hash and not url_obj.check_password(password):
            return Response({"error": "Invalid password"}, status=status.HTTP_403_FORBIDDEN)

        # Log the access
        AccessLog.objects.create(
            short_url=url_obj,
            ip_address=get_client_ip(request)
        )
        # Increment access count
        url_obj.access_count += 1
        url_obj.save()
        return redirect(url_obj.original_url)

    

class AnalyticsView(APIView):
    def get(self, request, short_url):
        if short_url:
            url_obj = URL.objects.filter(short_url=short_url)
        # else:
        #     url_obj = URL.objects.all()
        # logs = url_obj.logs.all()
        serializer = AnalyticsSerializer(url_obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
