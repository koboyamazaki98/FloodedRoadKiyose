from django.urls import path
from ac01 import views

app_name = 'ac01'
urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('sc0101', views.Sc0101View.as_view(), name="sc0101"),
    path('sc0102', views.Sc0102View.as_view(), name="sc0102"),
    path('sc0104', views.Sc0104View.as_view(), name="sc0104"),
]
