import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import wave
import threading
from scipy.fftpack import fft
import time
import math

# This library is inteded to be used for simple audio analysis and audio generation. The user may record
# sound waves, generated by the program digitally or the user physically, to later play them back or
# analyze their properties.

# For recordings to work, the user has to allow editor access to microphone and disk or start the editor from the
# terminal.

# Globals
FORMAT_FILE = pyaudio.paInt16
FORMAT_WAVE = pyaudio.paFloat32
SAMPLE_RATE = 44100
SAMPLES_PER_FRAME = int(SAMPLE_RATE/20)


def _terminate(p, stream):
    '''Terminates pyaudio stream so that the program can continue to its next task.'''
    stream.stop_stream()
    stream.close()
    p.terminate()


class Synthesizer:
    def __init__(self, stop=False):
        '''Creating Synthesizer object to access sound synthesis methods. Has the attribute stop to stop the continuous
        sound wave playback when user wants to finish'''
        self.stop = stop

    def sound_wave(self,wave_eq, amplitude, frequency, duration=None, mode='timed'):
        '''Plays a sound wave with a user-inputed wave equation. It also takes amplitude, frequency, and duration
        as arguments. May play sounds continuously or for specified durations.'''
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT_WAVE,
                        channels=1,
                        rate=SAMPLE_RATE,
                        output=True)

        t = np.arange(SAMPLE_RATE * duration * 4)

        if wave_eq == 'sine':
            samples = self._sine(amplitude,frequency, t)
        elif wave_eq == 'square':
            samples = self._square(amplitude, frequency, t)
        elif wave_eq == 'triangle':
            samples = self._triangle(amplitude, frequency, t)

        if mode == 'timed':
            stream.write(samples)

        elif mode == 'continuous':
            while True:
                stream.write(samples)
                if self.stop == True:
                    break

        # Terminate synthesis
        _terminate(p, stream)

    def _sine(self,amplitude, frequency, t):
        '''Returns the mathematical equation for a sine wave'''
        return amplitude * (np.sin(2*np.pi * t * frequency/SAMPLE_RATE)).astype(np.float32)

    def _square(self,amplitude, frequency, t):
        '''Returns the mathematical equation for a square wave.'''
        return amplitude * np.sign(self._sine(amplitude, frequency, t))

    def _triangle(self, amplitude, frequency, t):
        '''Returns the mathematical equation for a triangle wave.'''
        return amplitude * np.arcsin(np.cos(2*np.pi * t * frequency/SAMPLE_RATE)).astype(np.float32)


class Recording:
    def __init__(self, threads_killed=False):
        '''Creates Recording object to access recording methods. Has one attribute to kill ongoing threads so that the
        program continues.'''
        self.threads_killed = threads_killed

    def _record_thread(self, aux, stream, SAMPLES_PER_FRAME):
        '''Thread that will store data in aux until recording is finished.'''
        while not self.threads_killed:
            data = stream.read(SAMPLES_PER_FRAME)
            aux.append(data)

    def _get_device(self):
        '''Gets the input device that the user wants to use to record'''
        # Initiation
        p = pyaudio.PyAudio()
        info = p.get_host_api_info_by_index(0)
        n_devices = info.get('deviceCount')

        # Showcasing devices
        print('\nAvailible input devices are:')
        for i in range(n_devices):
            if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                print(p.get_device_info_by_host_api_device_index(0, i).get('name'))

        # Getting device input
        j = input('Which device do you want to use?')
        for i in range(n_devices):
            if p.get_device_info_by_host_api_device_index(0, i).get('name') == j:
                return i
        print('\nFaulty input!')

        # Recursion if wrong input
        self._get_device()

    def record(self, filename, n_channels):
        '''Records a .WAV-file from one of the computer's inputs, chosen through an index. The file is saved with the
        specified filename name. Capability of mono and stereo recording is applied through the argument n_channels.'''
        # Test input
        if not isinstance(filename, str):
            print('filename must be a string')
            return 'filename must be a string'

        # Initiating recording through pyaudio stream
        p = pyaudio.PyAudio()

        stream = p.open(format = FORMAT_FILE,
                        channels = n_channels,
                        rate = SAMPLE_RATE,
                        input = True,
                        input_device_index=self._get_device(),
                        frames_per_buffer = SAMPLES_PER_FRAME)

        print('recording')
        aux = []   #Recorded data is stored in aux
        stream.start_stream()

        # Data collecting thread
        thread1 = threading.Thread(target=Recording._record_thread, args=[self, aux, stream, SAMPLES_PER_FRAME])
        thread1.start()

        i = input('\nDo you want to use the built-in sound synthesis?')
        if i.lower()== 'yes':
            s = Synthesizer()
            l = input('\nDo you want to use input mode a)timed or b)continuous? (answer a or b)')
            if l.lower() == 'a':
                while True:
                    j = input('\nTo play a sine wave, input "sine" followed by amplitude (0-1), frequency (Hz) and duration (s), seperated by blank spaces\n'
                              'To play a square wave, input "square" followed by amplitude (0-1), frequency (Hz) and duration (s), seperated by blank spaces\n'
                              'To play a triangle wave, input "triangle" followed by amplitude (0-1), frequency (Hz) and duration (s), seperated by blank spaces\n'
                              'Input anything else to stop recording').lstrip()
                    j_split = j.split(' ')
                    if j_split[0].lower() == 'sine':
                        s.sound_wave('sine',float(j_split[1]), float(j_split[2]), float(j_split[3]))
                    elif j_split[0].lower() == 'square':
                        s.sound_wave('square', float(j_split[1]), float(j_split[2]), float(j_split[3]))
                    elif j_split[0].lower() == 'triangle':
                        s.sound_wave('triangle', float(j_split[1]), float(j_split[2]), float(j_split[3]))
                    else:
                        break
            elif l.lower() == 'b':
                while True:
                    k = input('\nTo play new note, input wave type ("sine", "square", "triangle")\n' 
                              'followed by amplitude (0-1) and frequenzy (Hz), seperated by blank spaces\n'
                              'Input anything else to stop recording')
                    k_split = k.split(' ')
                    if k_split[0].lower() == 'sine':
                        thread = threading.Thread(target=s.sound_wave,
                                                  args=['sine', float(k_split[1]), float(k_split[2]), 1,
                                                        'continuous'])
                        thread.start()
                    elif k_split[0].lower() == 'square':
                        thread = threading.Thread(target=s.sound_wave,
                                                  args=['square', float(k_split[1]), float(k_split[2]), 1,
                                                        'continuous'])
                        thread.start()
                    elif k_split[0].lower() == 'triangle':
                        thread = threading.Thread(target=s.sound_wave,
                                                  args=['triangle', float(k_split[1]), float(k_split[2]), 1,
                                                        'continuous'])
                        thread.start()
                    else:
                        s.stop = True
                        break
                    time.sleep(1)
        else:
            while True:
                m = input('\nInput any key to stop recording')
                break
        self.threads_killed = True
        thread1.join()


        print('\ndone')

        # Terminate recording
        _terminate(p, stream)

        # Writing file
        wf = wave.open(filename, 'wb')
        wf.setnchannels(n_channels)
        wf.setsampwidth(p.get_sample_size(FORMAT_FILE))
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(b''.join(aux))
        wf.close()

    def play(self, filename):
        '''Plays a .WAV-file chosen by the user by passing in its name as the argument. Sound is played through the
        computer output that the user is already using in their settings.'''
        # Test input
        if not isinstance(filename, str):
            print('filename must be a string')
            return 'filename must be a string'

        # Open audio file in read binary mode and initiate appropriate pyaudio stream
        wf = wave.open(filename, 'rb')
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        # Read data for every frame
        data = wf.readframes(SAMPLES_PER_FRAME)
        while data:
            stream.write(data)
            data = wf.readframes(SAMPLES_PER_FRAME)

        # Terminate playback
        _terminate(p, stream)


class Analysis:
    def display_waveform(self, file, shorten=None):
        '''Displays a plot with the waveform of a specified audio file. The plot has time on its x axis and amplitude on
        its y axis. User can also choose to shorten the x-axis with a factor, to easier view the waveform'''
        # Test input
        if not isinstance(file, str):
            print('filename must be a string')
            return 'filename must be a string'
        if shorten is not None and not isinstance(shorten, int):
            print('Shortening factor must be an int')
            return 'Shortening factor must be an int'

        wf = wave.open(file, 'rb')    # Open audio file

        data = wf.readframes(-1)   # Get audio data in bytes
        data_int = np.frombuffer(data, np.int16)     # Audio data in int

        # Stereo/mono check
        if wf.getnchannels() == 2:
            left, right = data_int[0::2], data_int[1::2]

            # Get time interval
            if shorten != None:
                t = np.linspace(0, int(len(data_int)/wf.getframerate()/2), num=int(len(data_int)/(2*shorten)))
            else:
                t = np.linspace(0, int(len(data_int)/wf.getframerate()/2), num=int(len(data_int)/2))

            plt.plot(t, left[0:len(t)])
            plt.plot(t, right[0:len(t)])

        else:
            # Get time interval
            if shorten != None:
                t = np.linspace(0, len(data_int) / wf.getframerate(), num=int(len(data_int)/shorten))
            else:
                t = np.linspace(0, len(data_int) / wf.getframerate(), num=len(data_int))

            plt.plot(t, data_int[0:len(t)])

        # Plot
        plt.title('Audio Waveform')
        plt.ylabel('Amplitude')
        plt.xlabel('Time')
        plt.show()


    def display_frequency_spectrum(self, file):
        '''Displays a plot of the frequency spectrum of a specified audio file.'''
        # Test input
        if not isinstance(file, str):
            print('filename must be a string')
            return 'filename must be a string'

        wf = wave.open(file, 'rb')    # Open audio file

        data = wf.readframes(-1)  # Get audio data in bytes
        data_int = np.frombuffer(data, np.int16)  # Audio data in int


        empty = [0] * 220500    # Create empty list to expand y in case frequency content is too short fot plot

        # Check stereo/mono
        if wf.getnchannels() == 2:
            x = np.linspace(0, SAMPLE_RATE,
                            10 * int(math.ceil(
                                (len(data_int) / wf.getframerate()) * SAMPLES_PER_FRAME)))  # Create x axis for plot
            left, right = data_int[0::2], data_int[1::2]   # Split channels
            y1 = list(fft(left))    # Calculate frequency spectrum
            y2 = list(fft(right))   # Calculate frequency spectrum
            y1 = y1 + empty
            y2 = y2 + empty
            y1 = np.abs(y1[0:(10 * int(math.ceil((len(data_int) / wf.getframerate()) * SAMPLES_PER_FRAME)))]) / (
                        128 * SAMPLES_PER_FRAME)
            y2 = np.abs(y2[0:(10 * int(math.ceil((len(data_int) / wf.getframerate()) * SAMPLES_PER_FRAME)))]) / (
                        128 * SAMPLES_PER_FRAME)
            plt.plot(x, y1)
            plt.plot(x, y2)
        else:
            x = np.linspace(0, SAMPLE_RATE / 2,
                            10 * int(math.ceil(
                                (len(data_int) / wf.getframerate()) * SAMPLES_PER_FRAME)))  # Create x axis for plot
            y = list(fft(data_int))    # Calculate frequency spectrum
            y = y + empty
            y = np.abs(y[0:(10 * int(math.ceil((len(data_int) / wf.getframerate()) * SAMPLES_PER_FRAME)))]) / (
                        128 * SAMPLES_PER_FRAME)
            plt.plot(x, y)

        #plot
        plt.title('Frequency spectrum')
        plt.ylabel('Amplitude')
        plt.xlabel('Frequency (Hz)')
        plt.xscale('log')
        plt.xlim(1, SAMPLE_RATE/2)
        plt.show()







