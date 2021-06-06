import pyaudio

def genHeader(sampleRate, bitsPerSample, channels):
    datasize = 2000*10**6
    o = bytes("RIFF",'ascii')                                               # (4byte) Marks file as RIFF
    o += (datasize + 36).to_bytes(4,'little')                               # (4byte) File size in bytes excluding this and RIFF marker
    o += bytes("WAVE",'ascii')                                              # (4byte) File type
    o += bytes("fmt ",'ascii')                                              # (4byte) Format Chunk Marker
    o += (16).to_bytes(4,'little')                                          # (4byte) Length of above format data
    o += (1).to_bytes(2,'little')                                           # (2byte) Format type (1 - PCM)
    o += (channels).to_bytes(2,'little')                                    # (2byte)
    o += (sampleRate).to_bytes(4,'little')                                  # (4byte)
    o += (sampleRate * channels * bitsPerSample // 8).to_bytes(4,'little')  # (4byte)
    o += (channels * bitsPerSample // 8).to_bytes(2,'little')               # (2byte)
    o += (bitsPerSample).to_bytes(2,'little')                               # (2byte)
    o += bytes("data",'ascii')                                              # (4byte) Data Chunk Marker
    o += (datasize).to_bytes(4,'little')                                    # (4byte) Data size in bytes
    return o

class Audio:
    def __init__(self):
        self.CHUNK = 1024
        self.sampleRate = 44100
        self.bitsPerSample = 16
        self.channels = 2
        self.input_device_index = 0
        self.audio = pyaudio.PyAudio()
        self.channels,self.sampleRate,self.input_device_index = self.__getDeviceAndChannel()
        self.wav_header = genHeader(self.sampleRate,self.bitsPerSample,self.channels)
        self.FORMAT = pyaudio.paInt16
        self.stream = self.audio.open(format=self.FORMAT,channels=self.channels,
                                      rate=self.sampleRate,input=True,
                                      input_device_index = self.input_device_index,
                                      frames_per_buffer=self.CHUNK)
        
        
    def __getDeviceAndChannel(self):
        host_info = self.audio.get_host_api_info_by_index(0)
        device_count = host_info.get('deviceCount')
        channels = self.channels
        sr = self.sampleRate
        index = self.input_device_index
        for i in range(0, device_count):
            device = self.audio.get_device_info_by_host_api_device_index(0, i)
            if device['name'] == 'Stereo Mix (Realtek Audio)':
                channels = device['maxInputChannels']
                index = i
                sr = device['defaultSampleRate']
                break
        return channels,int(sr),index
        
    
    def getStream(self):
        first_run = True
        self.stream.read(self.stream.get_read_available())
        while True:
            if first_run:
                data = self.wav_header + self.stream.read(self.CHUNK)
                first_run = False
            else:
                data = self.stream.read(self.CHUNK)
            yield(data)