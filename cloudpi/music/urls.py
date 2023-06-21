from django.urls import path
from . import views


app_name='music'

urlpatterns=[
    path('upload/',views.music_view_upload,name='music_list'),
    path('<int:pk>/delete/',views.music_delete,name='music_delete'),
    path('<int:pk>/add_to_starred/',views.add_to_starred,name='add-to-starred'),
    path('starred_documents/', views.StarredMusicListView.as_view(), name='star'),
    path('star/<int:id>/', views.StarredMusicUpdateView.as_view(), name='stared'),


]
