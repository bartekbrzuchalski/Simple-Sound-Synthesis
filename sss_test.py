import simple_sound_synthesis
import time
import glob, os
from playsound import playsound

# Make sure to have formatted the test files in the format frequency_wavetype

# Get filenames from test_files repository for the necessary test
path = "test_files/test_audio/"
filenames = []
for filename in glob.glob(os.path.join(path, '*.wav')):
    filenames.append(filename)

# Get the corresponding wave types of the test files to generate same wave
waves = []
for wave in filenames:
    wave = wave.split('/')
    wave = wave[2]
    wave = wave.split('_')
    wave = wave[1].split('.')
    waves.append(wave[0])

# Get the corresponding frequencies to each test file to generate same waves
frequencies = []
for freq in filenames:
    freq = freq.split('/')
    freq = freq[2]
    freq = freq.split('_')
    freq = freq[0].replace('Hz', '')
    frequencies.append(freq)


def sound_test(wave_type, test_file, s_object, r_object, frequency):
    '''Plays a generated sound wave by the sss-program, followed by a known sound from the test files directry and
    lasty waits for 3 seconds.'''
    s_object.sound_wave(wave_type, 0.4, frequency, 3)
    r_object.play(test_file)
    time.sleep(3)


def main():
    # Create necessary objects
    s = simple_sound_synthesis.Synthesizer()
    r = simple_sound_synthesis.Recording()
    a = simple_sound_synthesis.Analysis()


    ## Test Synthesiser class

    # Listen to generated sound waves corresponding to each test file to compare that they are the same frequency
    # and wavetype
    for i in range(len(filenames)):
        sound_test(waves[i], filenames[i], s, r, int(frequencies[i]))

    
    ## Test analysis class
    
    # Test the waveform displays
    for i in range(len(filenames)):
        print(filenames[i])
        a.display_waveform(filenames[i], 1000)
        # By zooming in, one can see in the transition of the wave if it actually is the specified wave type
        # Square waves are especially recognisable

    # Test the frequency spectrum displays
    for i in range(len(filenames)):
        if waves[i] == 'sine':
            print('There should be a peak at ' + frequencies[i])
            a.display_frequency_spectrum(filenames[i])
        if waves[i] == 'square':
            print('There should be rich amount of overtones and a peak at ' + frequencies[i])
            a.display_frequency_spectrum(filenames[i])
        if waves[i] == 'triangle':
            print('There should be an amount of overtones and a peak at ' + frequencies[i])
            a.display_frequency_spectrum(filenames[i])

    
    ## Test recording class
    
    # Test record function
    # The display and synth functions can be seen as reliable because of earlier testing.

    # First input (should display sine wave of 100 Hz)
    os.system("python3 recording_test.py < test_files/test_inputs/recording_test_input_1.txt")
    a.display_waveform('sss_test.wav')
    a.display_frequency_spectrum('sss_test.wav')

    # Second input (should display square wave of 400 Hz)
    os.system("python3 recording_test.py < test_files/test_inputs/recording_test_input_2.txt")
    a.display_waveform('sss_test.wav')
    a.display_frequency_spectrum('sss_test.wav')

    # Third input (should display triangle wave of 800 Hz)
    os.system("python3 recording_test.py < test_files/test_inputs/recording_test_input_3.txt")
    a.display_waveform('sss_test.wav')
    a.display_frequency_spectrum('sss_test.wav')

    # Test play function
    # Compare the library's play function to the known playsound function
    for i in range(3):
        r.play(filenames[i])
        playsound(filenames[i])


if __name__ == '__main__':
    main()

