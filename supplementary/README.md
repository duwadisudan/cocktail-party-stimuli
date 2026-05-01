# Supplementary scripts (archive)

Earlier iterations of the experiment code, kept so the provenance of the
published main scripts is auditable. **None of these scripts are on the
data-collection path.** For session-running code, see `experiment_scripts/`.

## Pre-trigger / no-onset-logging variants

Earlier versions of the per-condition runners that lacked hardware triggers
or onset logging:

- `AV_only.py`, `AV_only_trigger.py`
- `Audio_only.py`, `Audio_only_trigger.py`
- `Visual_only.py`
- `Control_only.py`, `Control_only_trigger.py`
- `Resting_only.py`
- `Full_exp.py` — early single-script driver for all blocks.

## AV+control test variants

Intermediate forks that explored the combined AV-control trial structure
later folded into the published `AV_control_save_onsets.py`:

- `AV_control_save_onsets_test.py`
- `AV_control_save_onsets_test_2.py`

## Modular refactor history

Snapshots from successive refactors toward a single class-based structure:

- `modular_class_exp_sudan.py`
- `modular_sudan_11_2_before_trigger.py`
- `modular_updated.py`
- `modular_w_trigger.py`
- `sudan_modular_master.py`

## Issue-specific debug scripts

One-off scripts used to diagnose specific problems during development:

- `sudan_cover_audio_only.py`
- `sudan_eye_without_sound.py`
- `sudan_flickering_issue.py`

## Dated test scripts

Numbered iterations from the January 2024 development push:

- `test_jan_16.py`, `test_jan_16_v2.py` ... `test_jan_16_v5.py`
- `test_jan_17_v6.py`

## Other

- `inilist_code.py` — early helper for generating the target/masker pair CSV.
  The same logic now lives inline at the top of the main scripts.
- `from psychopy import sound.py` — a misnamed scratch file (the filename is
  literally `from psychopy import sound.py`) kept for archival completeness.
- `sudan_initialize_random_videos.m` — MATLAB precursor of the pair-list
  generator, no longer used.
