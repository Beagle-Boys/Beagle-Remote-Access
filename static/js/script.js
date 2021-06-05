const VideoElement = document.getElementById("frame");
const RESOLUTION = {}

function updateResolution(x = 1080, y = 720) {
    RESOLUTION['x'] = x;
    RESOLUTION['y'] = y;
}

function getResolution() {
    fetch('/res').then(res => {
        res.json().then(r => {
            console.log('resolution', r);
            updateResolution(r['x'], r['y']);
        }).catch(err => {
            console.error(err);
            updateResolution();
        })
    }).catch(err => {
        console.error(err);
        updateResolution();
    });
}

function init() {
    getResolution();
}

init();

var socket = io();
socket.on('connect', function() {
    VideoElement.addEventListener("mousemove", (e)=> {
        socket.emit('m_k', {x: e.clientX - VideoElement.offsetLeft, y: e.clientY - VideoElement.offsetTop, h: VideoElement.height, w: VideoElement.width});
    });
});