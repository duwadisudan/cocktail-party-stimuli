"""Quick three-monitor sanity check.

Opens a small window on each available screen and labels it with its index
so the experimenter can confirm the physical layout matches the screen
indices used by the experiment scripts.

Authorship note: AI tools assisted with documentation. The author is solely
responsible for scientific correctness.
"""

from psychopy import visual, core

num_screens = 3  # Change this to the number of screens you have
windows = []

for i in range(num_screens):
    win = visual.Window(
        size=(800, 600),  # Make this smaller than your actual screen size
        screen=i,
        fullscr=False  # Change to True for fullscreen
    )
    windows.append(win)

# Display text on each window
for i, win in enumerate(windows):
    text = visual.TextStim(win, text=f"This is screen {i}")
    text.draw()
    win.flip()

# Wait for a few seconds so you can see the text
core.wait(5.0)

# Close all windows
for win in windows:
    win.close() 