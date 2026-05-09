// ============================================
// Audio Element Setup
// ============================================
const audio = document.createElement('audio');
audio.id = 'audioPlayer';
document.body.appendChild(audio);

// ============================================
// DOM Elements
// ============================================
const elements = {
    featuredList: document.getElementById('featuredList'),
    songList: document.getElementById('songList'),
    playPauseBtn: document.getElementById('playPauseBtn'),
    nextBtn: document.getElementById('nextBtn'),
    prevBtn: document.getElementById('prevBtn'),
    progressBar: document.getElementById('progressBar'),
    volumeSlider: document.getElementById('volumeSlider'),
    volumeIcon: document.getElementById('volumeIcon'),
    currentSong: document.getElementById('currentSong'),
    currentTime: document.getElementById('currentTime'),
    duration: document.getElementById('duration'),
    countBadge: document.querySelector('.count-badge'),
    miniUploadInput: document.getElementById('miniUploadInput'),
    selectFileBtn: document.getElementById('selectFileBtn'),
    uploadBtn: document.getElementById('uploadBtn'),
    selectedFileName: document.getElementById('selectedFileName'),
    player: document.querySelector('.player'),
    uploadProgress: document.getElementById('uploadProgress'),
    uploadProgressBar: document.getElementById('uploadProgressBar'),
    uploadProgressText: document.getElementById('uploadProgressText')
};

// ============================================
// CSRF Handler
// ============================================
function getCsrfToken() {
    const input = document.querySelector('[name="csrfmiddlewaretoken"]');
    return input ? input.value : '';
}

// ============================================
// State Variables
// ============================================
let state = {
    featuredSongs: [],
    uploadedSongs: [],
    currentPlaylist: [],
    currentIndex: 0,
    isPlaying: false,
    isLoading: false
};

// ============================================
// Loading Functions
// ============================================
function showLoading() {
    const loader = document.createElement('div');
    loader.id = 'loader';
    loader.innerHTML = `<div class="spinner"></div><span>در حال بارگذاری...</span>`;
    loader.style.cssText = `
        position: fixed; top: 0; left: 0; right: 0; bottom: 0;
        background: rgba(0,0,0,0.8);
        display: flex; flex-direction: column;
        align-items: center; justify-content: center;
        z-index: 1000; color: #fff; gap: 15px;
    `;
    document.body.appendChild(loader);
}

function hideLoading() {
    const loader = document.getElementById('loader');
    if (loader) loader.remove();
}

// ============================================
// Toast Function
// ============================================
function showToast(message, type = 'info') {
    let toast = document.getElementById('toast');
    if (!toast) {
        toast = document.createElement('div');
        toast.id = 'toast';
        document.body.appendChild(toast);
    }
    toast.textContent = message;
    toast.className = `toast show ${type}`;
    setTimeout(() => toast.classList.remove('show'), 3000);
}

// ============================================
// Helper Functions
// ============================================
function getSongName(song) {
    return song.title || song.name || song.fileName || song.filename || 'آهنگ بدون نام';
}

function getSongId(song) {
    return song.id || song._id || song.fileId || song.filename;
}

function formatTime(seconds) {
    if (isNaN(seconds) || !isFinite(seconds)) return '0:00';
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
}

// ============================================
// API Functions
// ============================================
async function fetchAllSongs() {
    if (state.isLoading) return;
    state.isLoading = true;

    try {
        const response = await fetch('/music/all', {
            credentials: 'include',
            headers: { 'CSRF-Token': getCsrfToken() }
        });

        if (!response.ok) throw new Error(`خطای سرور: ${response.status}`);

        const data = await response.json();
        state.uploadedSongs = Array.isArray(data) ? data : (data.songs || []);

        if (elements.countBadge) {
            elements.countBadge.textContent = state.uploadedSongs.length;
        }

        // ✅ این خط را اضافه کنید
        renderLists();

    } catch (error) {
        console.error('❌ خطا در دریافت آهنگ‌ها:', error);
        showToast('خطا در بارگذاری آهنگ‌ها', 'error');
    } finally {
        state.isLoading = false;
    }
}

// ============================================
// Upload Function (فقط یکبار تعریف شده!)
// ============================================
function uploadSong(file) {
    return new Promise((resolve, reject) => {
        const formData = new FormData();
        formData.append('file', file);

        elements.uploadProgress.classList.add('show');
        elements.uploadProgressBar.style.width = '0%';
        elements.uploadProgressText.textContent = '0%';

        const xhr = new XMLHttpRequest();
        const csrfToken = getCsrfToken();

        xhr.upload.addEventListener('progress', (e) => {
            if (e.lengthComputable) {
                const percent = Math.round((e.loaded / e.total) * 100);
                elements.uploadProgressBar.style.width = `${percent}%`;
                elements.uploadProgressText.textContent = `${percent}%`;
            }
        });

        xhr.addEventListener('load', () => {
            if (xhr.status >= 200 && xhr.status < 300) {
                elements.uploadProgressBar.style.width = '100%';
                elements.uploadProgressText.textContent = '100%';

                setTimeout(() => {
                    elements.uploadProgress.classList.remove('show');
                    elements.uploadProgressBar.style.width = '0%';
                }, 500);

                showToast('آهنگ با موفقیت آپلود شد!', 'success');
                fetchAllSongs();
                resolve(xhr.response);

            } else {
                elements.uploadProgress.classList.remove('show');
                showToast('خطا در آپلود فایل!', 'error');
                reject(new Error('خطا در آپلود'));
            }
        });

        xhr.addEventListener('error', () => {
            elements.uploadProgress.classList.remove('show');
            showToast('خطا در آپلود فایل!', 'error');
            reject(new Error('خطا در شبکه'));
        });

        xhr.open('POST', '/music/upload');
        if (csrfToken) xhr.setRequestHeader('X-CSRFToken', csrfToken);
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        xhr.withCredentials = true;
        xhr.send(formData);
    });
}

// ============================================
// Upload Event Handlers
// ============================================
elements.selectFileBtn.addEventListener('click', () => {
    elements.miniUploadInput.click();
});

elements.miniUploadInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        elements.selectedFileName.textContent = `📄 ${file.name}`;
        elements.selectedFileName.classList.add('show');
    } else {
        elements.selectedFileName.classList.remove('show');
    }
});

elements.uploadBtn.addEventListener('click', async () => {
    const file = elements.miniUploadInput.files[0];
    if (!file) {
        showToast('لطفاً ابتدا یک فایل انتخاب کنید', 'error');
        return;
    }
    await uploadSong(file);
    elements.miniUploadInput.value = '';
    elements.selectedFileName.classList.remove('show');
});

// ============================================
// Render Functions (نسخه اصلاح شده)
// ============================================
function renderFeatured() {
    if (!elements.featuredList) return;
    elements.featuredList.innerHTML = '';

    const songs = state.featuredSongs.length > 0 
        ? state.featuredSongs 
        : state.uploadedSongs.slice(0, 100);

    if (songs.length === 0) {
        elements.featuredList.innerHTML = `
            <div class="empty-state">
                <span style="font-size: 50px;">🎵</span>
                <p>هنوز آهنگی آپلود نشده</p>
                <small>از دکمه Upload برای افزودن آهنگ استفاده کنید</small>
            </div>
        `;
        return;
    }

    const isFeatured = state.featuredSongs.length > 0;

    songs.forEach((song, index) => {
        const card = document.createElement('div');
        card.classList.add('song-card');
        card.innerHTML = `
            <div class="album-art">
                <img 
                    src="static/covers/${song.url}.${song.coverFormat}" 
                    width="100%"
                    onerror="this.onerror=null; this.parentElement.innerHTML='🎵';"
                >
            </div>
            <div class="song-title">${getSongName(song)}</div>
            <div class="song-artist">${song.artist}</div>
`;

        
        
        // ✅ اصلاح شد: به جای playSong، loadSong + playSong
        card.addEventListener('click', () => {
            state.currentPlaylist = isFeatured ? state.featuredSongs : state.uploadedSongs;
            state.currentIndex = index;
            loadSong(state.currentIndex);  // ← اول لود کن
            playSong();                     // ← بعد پلی کن
        });

        elements.featuredList.appendChild(card);
    });
}

function renderPlaylist() {
    if (!elements.songList) return;
    elements.songList.innerHTML = '';

    if (state.uploadedSongs.length === 0) {
        elements.songList.innerHTML = `
            <div class="empty-state">
                <span style="font-size: 40px;">📂</span>
                <p>لیست آهنگ‌ها خالی است</p>
            </div>
        `;
        return;
    }



    state.uploadedSongs.forEach((song, index) => {
        const item = document.createElement('div');
        item.classList.add('song-item');
        
        if (index === state.currentIndex && state.currentPlaylist === state.uploadedSongs) {
            item.classList.add('active');
        }

        item.innerHTML = `
            <span class="song-number">${index + 1}</span>
            <span class="song-name">${getSongName(song)}</span>
        `;

        // ✅ اصلاح شد: به جای playSong، loadSong + playSong
        item.addEventListener('click', () => {
            state.currentPlaylist = state.uploadedSongs;
            state.currentIndex = index;
            loadSong(state.currentIndex);  // ← اول لود کن
            playSong();                     // ← بعد پلی کن
        });

        elements.songList.appendChild(item);
    });
}

    function renderLists() {
    renderFeatured();
    renderPlaylist();
}
// ============================================
// Player Functions
// ============================================
function loadSong(index) {
    if (state.currentPlaylist.length === 0) {
        showToast('لیست آهنگ‌ها خالی است', 'error');
        return;
    }

    const song = state.currentPlaylist[index];
    if (!song) return;

    state.currentIndex = index;
    const songId = getSongId(song);

    if (!songId) {
        showToast('خطا در پخش آهنگ', 'error');
        return;
    }

    audio.src = `/music/listen/${songId}`;
    updateSongDisplay();
    updateListHighlight();
}

function playSong() {
    if (state.currentPlaylist.length === 0) {
        showToast('آهنگی برای پخش وجود ندارد', 'error');
        return;
    }
    
    audio.play()
        .then(() => {
            state.isPlaying = true;
            elements.playPauseBtn.textContent = '⏸';
            elements.player.classList.add('playing');
        })
        .catch(error => {
            console.error('خطا در پخش:', error);
            showToast('خطا در پخش آهنگ', 'error');
        });
}

function pauseSong() {
    audio.pause();
    state.isPlaying = false;
    elements.playPauseBtn.textContent = '▶';
    elements.player.classList.remove('playing');
}

function nextSong() {
    if (state.currentPlaylist.length === 0) return;
    state.currentIndex = (state.currentIndex + 1) % state.currentPlaylist.length;
    loadSong(state.currentIndex);
    playSong();
}

function prevSong() {
    if (state.currentPlaylist.length === 0) return;
    state.currentIndex = (state.currentIndex - 1 + state.currentPlaylist.length) % state.currentPlaylist.length;
    loadSong(state.currentIndex);
    playSong();
}

// ============================================
// UI Updates
// ============================================
function updateSongDisplay() {
    if (elements.currentSong) {
        elements.currentSong.textContent = state.currentPlaylist.length > 0
            ? getSongName(state.currentPlaylist[state.currentIndex])
            : 'آهنگی انتخاب نشده...';
    }
}

function updateListHighlight() {
    const items = elements.songList?.querySelectorAll('.song-item');
    items?.forEach((item, index) => {
        item.classList.toggle('active', 
            index === state.currentIndex && state.currentPlaylist === state.uploadedSongs
        );
    });
}

function updateProgress() {
    if (audio && !isNaN(audio.duration)) {
        elements.progressBar.value = audio.currentTime;
        elements.progressBar.max = audio.duration;
        elements.currentTime.textContent = formatTime(audio.currentTime);
        elements.duration.textContent = formatTime(audio.duration);
    }
}

function updateVolumeIcon() {
    if (!elements.volumeIcon) return;
    if (audio.volume === 0) elements.volumeIcon.textContent = '🔇';
    else if (audio.volume < 0.5) elements.volumeIcon.textContent = '🔉';
    else elements.volumeIcon.textContent = '🔊';
}

// ============================================
// Event Listeners
// ============================================
// ============================================
// Event Listeners (با چک کردن وجود المان)
// ============================================
if (elements.playPauseBtn) {
    elements.playPauseBtn.addEventListener('click', () => {
        audio.paused ? playSong() : pauseSong();
    });
}

if (elements.nextBtn) {
    elements.nextBtn.addEventListener('click', nextSong);
}

if (elements.prevBtn) {
    elements.prevBtn.addEventListener('click', prevSong);
}

if (elements.progressBar) {
    elements.progressBar.addEventListener('input', () => {
        if (audio && audio.duration) {
            audio.currentTime = parseFloat(elements.progressBar.value);
        }
    });
}

if (elements.volumeSlider) {
    elements.volumeSlider.addEventListener('input', () => {
        audio.volume = parseFloat(elements.volumeSlider.value);
        updateVolumeIcon();
    });
}

// اینها لازم نیستن چک بشن چون audio خودمون ساختیم
audio.addEventListener('ended', nextSong);
audio.addEventListener('timeupdate', updateProgress);

audio.addEventListener('loadedmetadata', () => {
    if (audio.duration) {
        elements.progressBar.max = audio.duration;
        elements.duration.textContent = formatTime(audio.duration);
    }
    if (elements.playPauseBtn) elements.playPauseBtn.textContent = '▶';
});

audio.addEventListener('error', () => {
    showToast('خطا در پخش آهنگ', 'error');
});

// ============================================
// Initialization
// ============================================
document.addEventListener('DOMContentLoaded', async () => {
    showLoading();

    try {
        await fetchAllSongs();       // این خودش renderLists را صدا می‌زند
        audio.volume = parseFloat(elements.volumeSlider?.value || 0.5);
        updateVolumeIcon();

        if (state.uploadedSongs.length > 0) {
            state.currentPlaylist = state.uploadedSongs;
            loadSong(0);
        }

    } catch (error) {
        console.error('خطا در initialization:', error);
        showToast('خطا در بارگذاری اولیه', 'error');
    } finally {
        hideLoading();
    }
});