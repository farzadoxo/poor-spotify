# Poor Spotify 🎵
This Project will help you to share your music and podcasts with your friends when internet goes down!

Just upload a mp3 file and everything is getting ready to enjoy listening 🫠

## Options
- No need to register or authorize
- Auto Exteract file metadata (name,artist,cover and etc...)
- Spoify like UI
- Streaming system (chunk by chunk)
- Portable database
- Add a batch of music [utils](https://github.com/farzadoxo/poor-spotify/tree/master/src/utils)
## How to use:

### Docker:
1. Clone this repository.
2. Install [docker](https://docker.com) and [docker compose](https://docs.docker.com/compose/).
3. Rename `sample.env` in `src/` directory to `.env` and fill it with your data like:
```env
# API:
HOST='0.0.0.0'
PORT='6969'

# DATABASE:
DB_NAME='spotify_db'
DB_HOST='db'
DB_PORT='3306'
DB_USER='user1'
DB_PASS='$password'
DB_ROOT_PASS = '$password'
```
`⚠️ If you want to set another values for environment vars, you should also set it for nginx.conf file! `

**Note:** *Set you volumes for media and database at `docker-compose.yml`*

4. `cd` to root directory of repo (`poor-spotify`) and run command below:
```bash
$~ sudo docker compose --env-file src/.env up
```
`Wait for pulling images and run container!`

5. Check connection with:
```bash
$~ curl http://127.0.0.1
```
### Local:


## Notes
- Frontend of this project will render by django render engien.
- Music file will saved in `static/musics/`
- Music cover file will saved in `static/covers/`
- Playlist mechanism front-end is not ready but backend is ready. if you can help, tell me :) 
