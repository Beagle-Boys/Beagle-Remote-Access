import time
from io import BytesIO

def timed_call(callback, calls_per_second, *args, **kw):
    """
    Create an iterator which will call a function a set number
    of times per second.
    """
    time_time = time.time
    start = time_time()
    period = 1.0 / calls_per_second
    prev = callback(*args, **kw)
    while True:
        if (time_time() - start) > period:
            start += period
            prev = callback(*args, **kw)
            yield prev
        yield prev

def genVideoFeed(stream):
    frame = stream.getFrame()
    return (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def pil_img_to_bytes(pil_img):
    img_io = BytesIO()
    pil_img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return img_io.read()