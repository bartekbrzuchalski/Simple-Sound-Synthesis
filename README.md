# Simple Sound Synthesis
This library is intended to digitally produce simple sound waves, record them, play them back as well as analyze them.
The availible types of sounds that can be synthesised are sine waves, square waves and triangle waves. The provided
methods for analysis are to see the waveform of recorded sounds and their frequency spectrum.

It is required to have Python3 to use this library correctly. To be able to record with these functions, the user has
to make sure that the IDE or wherever you run Python, has access to the computer's audio input. There may appear
problems with certain IDEs. If you are using, like me, PyCharm on Mac, you have to allow the Terminal access
to the computer's microphone and then start PyCharm in the Terminal like this:

cd /Applications/PyCharm\ CE.app/Contents/MacOS/
./pycharm

There are a relatively large amount of modules necessary to use all of the functions. You should already have the
modules numpy, matplotlib, wave, threading, time and math in your Python library. However, the modules pyaudio and
scipy are external and have to be installed.

To install pyaudio, run this in the terminal: pip install PyAudio
To install scipy, run this in the terminal: pip install scipy

If the user would like to test the library, as in the built-in test program, further modules are necessary. These
include the built-in modules glob and os. Furthermore, the external module playsound is needed. To install this,
you have to run both "pip install playsound" and "pip3 install -U PyObjC".

It is recommended to have some software that can record internal sound from the computer. I have used the software
BlackHole (it is free), as can be seen in the testing program and the demo. This is not necessary and the built-in
microphone on your computer should also be fine. Recording with some inputs may cause problems so make sure that
they are set as the chosen audio device in the computer settings as well.

The demo is in Swedish but even if you do not understand, I hope that you can see how the library can be used through
my inputs and their results.







