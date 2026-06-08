from django.urls import path
from . import views

app_name = 'imageshow'

urlpatterns = [
    path('', views.steganography_view, name = "steganography_page"),
    path('output/<name>/<int:num>', views.download, name = "download"),
    path('message', views.message, name = "recovered message")
]