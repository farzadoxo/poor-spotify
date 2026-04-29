from playlist.models import Playlist


class Serializer:

    def music_serializer(songs:list):
        musics = {'songs':[]}
        for song in songs:
            musics['songs'].append({'id':song.id,
                                    'title':song.title,
                                    'artist':song.artist,
                                    'isSingleTrack':song.isSingleTrack,
                                    'album':song.album,
                                    'hasCover':song.hasCover,
                                    'coverFormat':song.coverFormat,
                                    'uploader':song.uploader,
                                    'url':song.url})

        return musics
    

    def playlist_serializer(pls:list):
        playlists = {'playlists':[]}
        for pl in pls:
            pls['playlists'].append({'id':pl.id,
                                               'name':pl.name})
            
            

        
        return playlists



    

    def playlist_music_serializer(pl:Playlist,musics:list):
        response = {'playlist':{'id':pl.id,'name':pl.name},'songs':[]}
        for song in musics:
            response['songs'].append({'id':song.id,
                                        'title':song.title,
                                        'artist':song.artist,
                                        'isSingleTrack':song.isSingleTrack,
                                        'album':song.album,
                                        'hasCover':song.hasCover,
                                        'coverFormat':song.coverFormat,
                                        'uploader':song.uploader,
                                        'url':song.url})
        
        return response