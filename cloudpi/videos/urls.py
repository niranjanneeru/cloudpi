from django.urls import path
from . import views


app_name='videos'

urlpatterns=[
    path('upload/',views.video_view_upload,name='video_list'),
    path('<int:pk>/delete/',views.video_delete,name='video_delete'),
    path('<int:pk>/add_to_starred/',views.add_to_starred,name='add-to-starred'),
    path('starred_documents/', views.StarredVideoListView.as_view(), name='star'),
    path('star/<int:id>/', views.StarredVideoUpdateView.as_view(), name='stared'),


]
