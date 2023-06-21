from django.urls import path
from . import views


app_name='lockedfiles'

urlpatterns=[
    path('upload/',views.locked_view_upload,name='locked_list'),
    path('<int:pk>/delete/',views.locked_delete,name='locked_delete'),
   
]
