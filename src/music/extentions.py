class Serializer:

    def music_serializer(songs:list):
            musics = {'songs':[]}
            for song in songs:
                musics['songs'].append({'id':song.id,'name':song.name})

            return musics