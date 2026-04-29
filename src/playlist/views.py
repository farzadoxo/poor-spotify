from django.shortcuts import render
from extentions.serializers import Serializer 
from django.http import JsonResponse , HttpResponse
from .models import Playlist
from music.models import Music
from django.core.exceptions import ObjectDoesNotExist



def get_all_playlist(request):
    playlists = Serializer.playlist_serializer(pls=Playlist.objects.all())
    return JsonResponse(playlists)



def new_playlist(request,playlist:Playlist):
    obj = Playlist(playlist).save()
    return HttpResponse('Ok')



def add_to_playlist(request,music_id:int , playlist_id:int):
    try:
        music = Music.objects.get(id=music_id)
        playlist = Playlist.objects.get(id=playlist_id)
    except ObjectDoesNotExist:
        return HttpResponse('Music or Playlist not found with this ID!')
    
    playlist.musics.add(music)
    return HttpResponse('Ok')   
    

    
def get_playlist(request,playlist_id:int):
    try:
        playlist = Playlist.objects.get(id=playlist_id)
    except ObjectDoesNotExist:
        return HttpResponse('Playlist not found with this ID!')

    response = Serializer.playlist_music_serializer(pl=playlist,musics=playlist.musics.all())
    return JsonResponse(response)