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