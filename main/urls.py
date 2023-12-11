from django.urls import path
from .views import *

urlpatterns = [
    path('<str:chat_id>/', main),
]
