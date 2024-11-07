#!/usr/bin/env python3

from si4432 import Si4432

from time import perf_counter
    
from http.server import HTTPServer, SimpleHTTPRequestHandler
import io

from PIL import Image, ImageDraw, ImageChops

def delay(delay):
    _ = perf_counter() + delay/1000
    while perf_counter() < _:
        pass

def clamp(n, min, max):
    if n < min: 
        return min
    elif n > max: 
        return max
    else: 
        return n

def convert_domain(aValue, aMin, aMax, bMin, bMax):
  aRange = aMax - aMin
  bRange = bMax - bMin
  aValue = clamp(aValue, aMin, aMax)
  return ((aValue - aMin) * bRange + aRange / 2) / aRange + bMin

PAL = [(0x00, 0x00, 0x00), (0x00, 0x00, 0x00), (0x00, 0x00, 0x00), (0x00, 0x00, 0x00), (0x00, 0x00, 0x00), (0x00, 0x00, 0x00), (0x00, 0x00, 0x00), (0x00, 0x00, 0x00), (0x00, 0x00, 0x00), (0x00, 0x00, 0x00), (0x00, 0x00, 0x00), (0x00, 0x00, 0x00), (0x00, 0x00, 0x00), (0x00, 0x00, 0x00), (0x00, 0x00, 0x00), (0x00, 0x00, 0x00), (0x00, 0x00, 0x00), (0x00, 0x00, 0x00), (0x00, 0x00, 0x00), (0x00, 0x00, 0x00), (0x00, 0x00, 0x00), (0x00, 0x00, 0x02), (0x00, 0x00, 0x05), (0x00, 0x00, 0x08), "#00000b", "#00000e", (0x00, 0x00, 0x10), (0x00, 0x00, 0x13), (0x00, 0x00, 0x16), (0x00, 0x00, 0x19), "#00001c", "#00001e", (0x00, 0x00, 0x21), (0x00, 0x00, 0x24), (0x00, 0x00, 0x27), "#00002a", "#00002c", "#00002f", (0x00, 0x00, 0x32), (0x00, 0x00, 0x35), (0x00, 0x00, 0x38), "#00003a", "#00003d", (0x00, 0x00, 0x40), (0x00, 0x00, 0x43), (0x00, 0x00, 0x46), (0x00, 0x00, 0x48), "#00004b", "#00004e", (0x00, 0x00, 0x51), (0x00, 0x00, 0x54), (0x00, 0x00, 0x56), (0x00, 0x00, 0x59), "#00005c", "#00005f", (0x00, 0x00, 0x62), (0x00, 0x00, 0x64), (0x00, 0x00, 0x67), "#00006a", "#00006d", (0x00, 0x00, 0x70), (0x00, 0x00, 0x72), (0x00, 0x00, 0x75), (0x00, 0x00, 0x78), "#00007b", "#00007e", (0x00, 0x00, 0x80), (0x00, 0x00, 0x83), (0x00, 0x00, 0x86), (0x00, 0x00, 0x89), "#00008c", "#02048f", (0x04, 0x08, 0x93), "#060c97", "#08109b", "#0a149f", "#0c19a3", "#0e1da6", "#1021aa", "#1225ae", "#1429b2", "#162db6", "#1832ba", "#1a36bd", "#1c3ac1", "#1e3ec5", "#2042c9", "#2246cd", "#244bd1", "#264fd4", "#2853d8", "#2a57dc", "#2c5be0", "#2e5fe4", "#3064e8", "#3268eb", "#346cef", "#3670f3", "#3874f7", "#3a78fb", "#3c7dff", "#3f7ffa", "#4382f5", "#4784f0", "#4b87eb", "#4f8ae6", "#538ce1", "#578fdc", "#5b91d7", "#5f94d2", "#6397cc", "#6699c7", "#6a9cc2", "#6e9ebd", "#72a1b8", "#76a4b3", "#7aa6ae", "#7ea9a9", "#82aba4", "#86ae9f", "#8ab199", "#8db394", "#91b68f", "#95b88a", "#99bb85", "#9dbe80", "#a1c07b", "#a5c376", "#a9c571", "#adc86c", "#b1cb66", "#b4cd61", "#b8d05c", "#bcd257", "#c0d552", "#c4d84d", "#c8da48", "#ccdd43", "#d0df3e", "#d4e239", "#d8e533", "#dbe72e", "#dfea29", "#e3ec24", "#e7ef1f", "#ebf21a", "#eff415", "#f3f710", "#f7f90b", "#fbfc06", "#ffff00", "#fffd00", "#fffa00", "#fff800", "#fff500", "#fff300", "#fff000", "#ffee00", "#ffeb00", "#ffe900", "#ffe600", "#ffe300", "#ffe100", "#ffde00", "#ffdc00", "#ffd900", "#ffd700", "#ffd400", "#ffd200", "#ffcf00", "#ffcc00", "#ffca00", "#ffc700", "#ffc500", "#ffc200", "#ffc000", "#ffbd00", "#ffbb00", "#ffb800", "#ffb600", "#ffb300", "#ffb000", "#ffae00", "#ffab00", "#ffa900", "#ffa600", "#ffa400", "#ffa100", "#ff9f00", "#ff9c00", "#ff9900", "#ff9700", "#ff9400", "#ff9200", "#ff8f00", "#ff8d00", "#ff8a00", "#ff8800", "#ff8500", "#ff8300", "#ff8000", "#ff7d00", "#ff7b00", "#ff7800", "#ff7600", "#ff7300", "#ff7100", "#ff6e00", "#ff6c00", "#ff6900", "#ff6600", "#ff6400", "#ff6100", "#ff5f00", "#ff5c00", "#ff5a00", "#ff5700", "#ff5500", "#ff5200", "#ff5000", "#ff4d00", "#ff4a00", "#ff4800", "#ff4500", "#ff4300", "#ff4000", "#ff3e00", "#ff3b00", "#ff3900", "#ff3600", "#ff3300", "#ff3100", "#ff2e00", "#ff2c00", "#ff2900", "#ff2700", "#ff2400", "#ff2200", "#ff1f00", "#ff1d00", "#ff1a00", "#ff1700", "#ff1500", "#ff1200", "#ff1000", "#ff0d00", "#ff0b00", "#ff0800", "#ff0600", "#ff0300", "#ff0000", "#ff3333", "#ff6666", "#ff9999", "#ffcccc", "#ffffff"]

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
            # self.imgDraw.rectangle([0,0,320,240], (255,255,255))
            for x in range(80):
                rssi = rssiHistory[x]
                color = int(convert_domain(rssi, 30, 120, 0, len(PAL)-1))
                self.imgDraw.rectangle([x *4,238,x*4+3, 240], PAL[color])
            self.img = ImageChops.offset(self.img, 0, -1)
            self.imgDraw = ImageDraw.Draw(self.img)
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
