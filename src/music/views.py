from django.shortcuts import render
from django.http import JsonResponse , HttpResponse , StreamingHttpResponse
from django.http import HttpRequest
from django.core.exceptions import ObjectDoesNotExist
from .models import Music 
from .extentions import Serializer
from tinytag import TinyTag

import os


# dirs 
music_dir = 'static/musics'
cover_dir = 'static/covers'


def get_all_music(request):
    songs = Music.objects.all()
    musics = Serializer.music_serializer(songs)

    return JsonResponse(musics)





def upload_music(request:HttpRequest):
    if request.method == "POST":
        try:
            file = request.FILES['file']
        except Exception as error:
            return HttpResponse(error)
        

        guid = os.urandom(3).hex() # this is uniq random URL
        format = file.name.split('.')[-1] # file extention
        
        os.makedirs(music_dir,exist_ok=True)
        with open(f'{music_dir}/{guid}.{format}','wb+') as buffer:
            for chunk in file.chunks():
                buffer.write(chunk)

        # get metadata from saved song file
        saved_song = TinyTag.get(f'static/musics/{guid}.{format}',image=True)
        metadata = {'filename':saved_song.filename,
                    'title':saved_song.title,
                    'artist':saved_song.artist,
                    'album':saved_song.album,
                    'cover':saved_song.images.front_cover}


        if metadata['cover']:
            cover_format = metadata['cover'].mime_type.split('/')[-1]
            os.makedirs(cover_dir,exist_ok=True)
            with open(f'{cover_dir}/{guid}.{cover_format}','wb+') as buffer:
                buffer.write(metadata['cover'].data)
        

        song = Music(fileName=metadata['filename'],
                     title=metadata['title'],
                     artist=metadata['artist'] ,
                     isSingleTrack=True if metadata['album'] == None else False,
                     album=metadata['album'],
                     hasCover=True if metadata['cover'] != None else False,
                     coverFormat=cover_format if metadata['cover'] != None else None,
                     url=guid,
                     format=format)
        song.save()

        return HttpResponse('Ok')
    

    

def get_music(request,music_id:int):
    try:
        music = Music.objects.get(id=music_id)
    except ObjectDoesNotExist:
        return HttpResponse("Music Not found!")
    
    file_path = f"static/musics/{music.url}.{music.format}"

    def file_iterator(file_name, chunk_size=1000):
        with open(file_name, "rb") as f:
            while chunk := f.read(chunk_size):
                yield chunk
    

    response = StreamingHttpResponse(file_iterator(file_path))
    response["Content-Type"] = "audio/mpeg"
    return response

        # file = open(f'static/musics/{music.url}.{music.format}','rb').read()
        # return FileResponse(file,as_attachment=True)



def delete_music(request,music_id:int):
    try:
        music = Music.objects.get(id=music_id)
    except ObjectDoesNotExist:
        return HttpResponse("Music not found!")
    
    try:
        music.delete() # delete music from db
        os.remove(f'static/musics/{music.url}.{music.format}')

        return HttpResponse('Music delete Successfully!')
    except FileNotFoundError:
        print(f"{music.url}.{music.format} Not found!")


