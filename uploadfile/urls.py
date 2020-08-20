from django.conf.urls import url
from . import views
from django.urls import path,include

urlpatterns = [
    path('',views.upindex,name="upindex"),
    path('done_uploading/',views.uploadtask, name='uploadtask')]