from django.urls import path
from . import views


app_name='images'

urlpatterns=[
    path('upload/',views.image_view_upload,name='images_list'),
    path('<int:pk>/delete/',views.image_delete,name='images_delete'),
    path('<int:pk>/add_to_starred/',views.add_to_starred,name='add-to-starred'),
    path('starred_documents/', views.StarredImageListView.as_view(), name='star'),
    path('star/<int:id>/', views.StarredImageUpdateView.as_view(), name='stared'),


]
