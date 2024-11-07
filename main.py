#!/usr/bin/env python3

from si4432 import Si4432

from time import perf_counter
    
from http.server import HTTPServer, SimpleHTTPRequestHandler
import io

from PIL import Image, ImageDraw

def delay(delay):
    _ = perf_counter() + delay/1000
    while perf_counter() < _:
        pass

rssiHistory = [0 for _ in range(80)]

with Si4432(0,0) as si:
    si.reset()
    if not si.check():
        print('Chip not detected')
        exit(255)

    si.configure_gpio()

    si.reg_write(0x1C, (3<<4) | 6) # BW

    si.set_frequency(434000000)
    si.enable_rx()


    def worker():
        global rssiHistory
        while True:
            for x in range(80):
                si.set_frequency(433075000 + x*25000)
                delay(2)
                rssiHistory[x] = si.rssi()

    import threading
    thread = threading.Thread(target=worker)
    thread.start()



    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs) -> None:
            self.img = Image.new('RGB', (320, 240), color='white')
            self.imgDraw = ImageDraw.Draw(self.img)
            self.buf = io.BytesIO()
            super().__init__(*args, **kwargs)
        
        def renderFrame(self):
            self.buf.seek(0)
            self.img.save(self.buf, 'jpeg', quality=80)
            return self.buf.getvalue()

        def getFrame(self):
            self.imgDraw.rectangle([0,0,320,240], (255,255,255))
            for x in range(80):
                rssi = rssiHistory[x]
                self.imgDraw.rectangle([x *4,240,x*4+3, 240 - rssi*240/128], (0,0,rssi))
            return self.renderFrame()


        def sendFrame(self):
            frame = self.getFrame()

            self.wfile.write(b'--frame\r\n')
            self.send_header('Content-Type', 'image/jpeg')
            self.send_header('Content-Length', str(len(frame)))
            self.end_headers()
            self.wfile.write(frame)
            self.end_headers()

        def do_GET(self):
            if self.path != '/stream':
                super().do_GET()
                return

            self.send_response(200)
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=frame')
            self.end_headers()

            while True:
                self.sendFrame()

    HTTPServer(('', 8000), Handler).serve_forever()
