from django.urls import path
from . import views


urlpatterns = [
    path('all',views.get_all_music),
    path('upload',views.upload_music),
    path('listen/<int:music_id>',views.get_music),
    path('delete/<int:music_id>',views.delete_music)
]