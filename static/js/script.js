const VideoElement = document.getElementById("frame");
const RESOLUTION = {}

function updateResolution(x = 1080, y = 720) {
    RESOLUTION['x'] = x;
    RESOLUTION['y'] = y;
    //VideoElement.style.width = `${x}px`;
    //VideoElement.style.height = `${y}px`;
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