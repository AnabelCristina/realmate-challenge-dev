from django.urls import path
from . import views

urlpatterns = [
    path('<uuid:pk>/', views.conversation_details)
]