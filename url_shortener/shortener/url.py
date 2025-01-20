from django.urls import path

from .views import AnalyticsView, RedirectURLView, ShortenURLView

urlpatterns = [
    path('post-shorten/', ShortenURLView.as_view(), name='post-shorten'),
    path('<str:short_url>/', RedirectURLView.as_view(), name='redirect_url'),
    path('analytics/<str:short_url>/', AnalyticsView.as_view(), name='analytics'),
]
