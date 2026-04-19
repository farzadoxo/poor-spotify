from django.shortcuts import render
from django.http import JsonResponse , HttpResponse , StreamingHttpResponse
from django.http import HttpRequest
from django.core.exceptions import ObjectDoesNotExist
from .models import Music
from .extentions import Serializer

import os



def get_all_music(request):
    songs = Music.objects.all()
    musics = Serializer.music_serializer(songs)

    return JsonResponse(musics)


def new_music(request):
    return render(request,'upload.html')


def upload_music(request:HttpRequest):
    if request.method == "POST":
        file = request.FILES['file']
        guid = os.urandom(3).hex() # this is uniq random URL
        format = file.name.split('.')[-1] # file extention
        song = Music(name=file.name.split('.')[0],url=guid,format=format)
        song.save()

        with open(f'static/musics/{guid}.{format}','wb+') as buffer:
            for chunk in file.chunks():
                buffer.write(chunk)

        return HttpResponse('ok')
    

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