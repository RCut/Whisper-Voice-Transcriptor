# Changelog

## Version 1.1.0

### Added
- Full file system tree view for selecting files and folders
  - Tree lazily loads subdirectories when expanded
  - Includes checkboxes for subfolder inclusion
  - Supports mixed selection of files and folders
- Deduplication of selected files and folders to avoid re-processing files already covered by selected parent directories
- Checkbox for auto-scrolling logs (with session persistence)
- Checkbox to enable/disable notification sound upon completion
- Notification sound plays after successful batch transcription (if enabled)

### Changed
- UI polish
  - Aligned input/output folder selectors
  - Start/Stop buttons now placed above the log window
  - Streamlined top layout with single folder selection mechanism

### Fixed
- Corrected logic for setting root directory in tree view
- Fixed indentation issues and variable scoping bugs in earlier transcription handling
- Removed legacy file selection logic and buttons


## Version 1.0.0

Initial working GUI version with the following features:
- Batch transcription of files from an input folder
- Output results into a selected output folder
- Presets for model parameters (Fast, Balanced, Accurate)
- Parameter configuration for Whisper (model, language, task, temperature, etc.)
- Stop transcription mid-batch (after current file)
- Progress tracking with label (e.g., 2/5)
- File deduplication: skip files already transcribed
- Save/restore last session state (input/output folder, configs)
- Log console with timestamped feedback