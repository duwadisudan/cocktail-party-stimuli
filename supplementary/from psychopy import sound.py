from psychopy import prefs
prefs.hardware['audioLib'] = ['pygame']  # Use sounddevice as the backend

from psychopy import sound, core

# Test playing sound from a wav file
sound_file = r"C:\Sudan\Stimuli\whiteNoise_stereo.wav"

try:
    test_sound = sound.Sound(sound_file)
    test_sound.play()
    core.wait(5)  # Wait for 5 seconds while the sound plays
    print(f"Sound file {sound_file} played successfully.")
except Exception as e:
    print(f"Failed to play sound. Error: {str(e)}")
