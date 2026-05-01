# Audio-Visual Cocktail-Party Stimulus Delivery

PsychoPy stimulus-delivery code for an audio-visual cocktail-party experiment
that accompanies the manuscript. The scripts present spatialized speech
videos across a three-monitor setup, send hardware triggers over a serial
port to a NeuroSpec trigger box, and log responses and trigger onsets to CSV
for downstream alignment with the physiological recording.

The intent of publishing this repository is full transparency: any reviewer
or other group can inspect, run, or adapt the exact code used to deliver
stimuli during data collection.

## Repository layout

```
experiment_scripts/   main scripts run during a session
utilities/            standalone hardware sanity checks
supplementary/        archived earlier versions, kept for provenance
environment.yml       conda environment used during data collection
LICENSE
```

### Main experiment scripts

| Script | Purpose |
|---|---|
| `experiment_scripts/AV_only_save_onsets.py` | Audio-visual block: target/masker pairs of spatialized speech videos. |
| `experiment_scripts/AV_control_save_onsets.py` | Audio-visual block with an extended jittered pre-stimulus crosshair hold (15-17 s). |
| `experiment_scripts/Audio_only_save_onsets.py` | Audio-only block |
| `experiment_scripts/Control_only_save_onsets.py` | Eye-movement control block. |
| `experiment_scripts/Resting_only_trigger.py` | Resting-state block with periodic triggers. |

Each main script writes three CSVs into `initialization_data/`:

```
response_<TIMESTAMP>.csv         per-trial responses
iniList_<TIMESTAMP>.csv          target/masker pair list
trigger_onsets_<TIMESTAMP>.csv   high-precision trigger times
```

### Utilities

| Script | Purpose |
|---|---|
| `utilities/monitor_checker.py` | Opens a numbered window on each screen so the experimenter can verify the 3-monitor layout. |
| `utilities/spatial_audio_test.py` | Plays and records audio to verify spatial panning before a session. |
| `utilities/label_check_covert.py` | Verifies stimulus labels and screen assignments before a real run. |

### Supplementary

`supplementary/` holds earlier iterations of the same scripts (no-trigger
versions, experimental forks, dated test scripts). They are kept so the
provenance of the published main scripts is auditable, but they are not on
the data-collection path. See `supplementary/README.md` for a one-line note
per file.

## Hardware

- Three displays presented to the participant at fixed positions. Screen
  indices `0`, `1`, `2` map to left target / right target / centre fixation
  respectively.
- NeuroSpec MMBT-S trigger box on serial port `COM3`.
- Stereo audio reproduction (azimuth +/-30 degrees), stimuli pre-rendered
  with the corresponding spatial suffix `_30` / `_-30` on disk.

## Software

The acquisition machine ran Python 3.9 with PsychoPy and `pygame` as the
audio backend. The exact environment used during data collection is
`environment.yml`. To reproduce:

```
conda env create -f environment.yml
conda activate myenv
```

Key dependencies: `psychopy`, `pyserial`, `pandas`, `numpy`, `sounddevice`,
`soundfile`, `scipy`, `matplotlib`.

## Adapting for another machine

Each main script defines its directory paths in the class `__init__` block,
e.g.

```python
self.csv_path             = r"C:\Sudan\Stimuli\initialization_data\..."
self.spatial_video_folder = r"C:\Sudan\Stimuli\sudan_spatial_videos_updated"
self.response_csv_path    = r"C:\Sudan\Stimuli\initialization_data\..."
```

These paths reflect the layout on the original acquisition machine. To run
on another system, edit them in one place per script. The serial port
(`COM3`) and screen indices (`0`, `1`, `2`) are likewise defined inline and
should match the local hardware. The expected on-disk layout is:

```
<stimuli_root>/
├── sudan_spatial_videos_updated/    # spatialized AVI clips, *_30.avi / *_-30.avi
├── Screenshots_faces_full_updated/  # speaker still images, *.jpg
├── Transcripts/                     # English transcript CSV
└── initialization_data/             # CSV outputs are written here
```

## Stimulus materials

The video, audio, screenshot, and transcript files referenced by the scripts
are not redistributed in this repository. See the manuscript and its data
availability statement for how the stimulus set is shared.

## Authorship and AI use

The author wrote, developed, and validated all experiment logic. AI tools
(general-purpose code assistants) were used to help refactor, comment, and
document the scripts. The author retains full scientific responsibility for
the correctness of the code and the validity of any analyses produced with
it. Each script's docstring carries the same statement.

## License

MIT, see `LICENSE`.

## Citation

If you use or adapt this code, please cite the manuscript (citation to be
added on acceptance).
