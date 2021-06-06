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

var cps = 60;

var socket = io();
var la_m_m = 0, cur_m_m;
socket.on('connect', function() {
    VideoElement.addEventListener("mousemove", (e)=> {
        cur_m_m = Date.now()
        if(cur_m_m - la_m_m > (1000/cps) ) {
            socket.emit('mouse_move', { x: e.clientX - VideoElement.offsetLeft, y: e.clientY - VideoElement.offsetTop, h: VideoElement.height, w: VideoElement.width,});
        }
        la_m_m = cur_m_m
    });

    VideoElement.addEventListener("mousedown", (e)=> {
        socket.emit('mouse_click', {press: 'd', button: e.button, x: e.clientX - VideoElement.offsetLeft, y: e.clientY - VideoElement.offsetTop, h: VideoElement.height, w: VideoElement.width,});
    })

    VideoElement.addEventListener("mouseup", (e)=> {
        socket.emit('mouse_click', {press: 'u', button: e.button, x: e.clientX - VideoElement.offsetLeft, y: e.clientY - VideoElement.offsetTop, h: VideoElement.height, w: VideoElement.width,});
    })

    document.addEventListener("keydown", (e) => {
        socket.emit('keyboard', {press: 'd',key: e.key, ctrl: e.ctrlKey, alt: e.altKey});
    })

    document.addEventListener("keyup", (e) => {
        socket.emit('keyboard', {press: 'u',key: e.key, ctrl: e.ctrlKey, alt: e.altKey});
    })

});

document.addEventListener("contextmenu", (e) => {
    e.preventDefault();
});

VideoElement.setAttribute('draggable', false); 