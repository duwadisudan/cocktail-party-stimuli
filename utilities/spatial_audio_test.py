"""Spatial-audio playback and recording sanity check.

Plays a stimulus through the system's audio output and simultaneously
records from the default input, so the experimenter can verify spatial
panning and timing before a session.

Authorship note: AI tools assisted with documentation. The author is solely
responsible for scientific correctness.
"""

import numpy as np
import sounddevice as sd
import soundfile as sf
import scipy.signal
import matplotlib.pyplot as plt

def play_and_record(data, fs):
    # If data is a string, assume it's a filename and read the file
    if isinstance(data, str):
        data, file_fs = sf.read(data, dtype='float32')

        # Check if the sample rates match
        if file_fs != fs:
            raise ValueError("Sample rate of the file does not match the system's sample rate")

    # Play and record simultaneously
    recording = sd.playrec(data, fs, channels=2)

    # Wait for the playback to finish
    sd.wait()

    return recording

def frequency_response_analysis(fs, duration=10):
    # Generate a sweep signal
    f1, f2 = 20, 20000  # Start and end frequencies
    t = np.linspace(0, duration, fs * duration)
    sweep = scipy.signal.chirp(t, f1, t[-1], f2, method='logarithmic')

    # Play and record the sweep
    recorded_sweep = play_and_record(sweep, fs)  # Removed duration

    # Analyze the frequency response
    w, h = scipy.signal.freqz(recorded_sweep[:,0], sweep)

    # Plotting
    plt.semilogx(w * fs / (2 * np.pi), 20 * np.log10(abs(h)))
    plt.title("Frequency Response")
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Amplitude [dB]")
    plt.grid(which='both', axis='both')
    plt.show()

def binaural_test(file_path):
    fs = 44100  # Standard Sampling Rate
    duration = 10  # Duration in seconds

    # Play the binaural recording
    play_and_record(file_path, duration, fs)

if __name__ == "__main__":
    # Adjust these parameters as needed
    fs = 44100  # Sampling rate
    duration = 10  # Duration of the test signal in seconds
    binaural_file = 'path_to_your_binaural_file.wav'  # Replace with your file path

    # Run Frequency Response Analysis
    frequency_response_analysis(fs, duration)

    # Run Binaural Test
    binaural_test(binaural_file)
