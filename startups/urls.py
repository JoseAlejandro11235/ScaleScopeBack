from django.urls import path
from .views import FetchStartupsView

urlpatterns = [
    path('fetch-startups/', FetchStartupsView.as_view()),
]
