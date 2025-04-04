# Whisper Batch Transcriber

A desktop application for fast, flexible batch transcription of audio files using OpenAI's Whisper model.

Version: **1.1.0**

---

## ✨ Features

- 📂 **File/Folder Selection via Tree View**
  - Browse your file system with a lazy-loading tree
  - Select individual files, folders, or mixed combinations
  - "Include subfolders" toggle for precise control
  - Duplicate file prevention when folder parents already selected

- ⚖️ **Whisper Model Configuration**
  - Choose model size: `tiny`, `base`, `small`, `medium`, `large`
  - Language auto-detection or manual override
  - Task selection: transcribe or translate
  - Fine-tune decoding settings: temperature, beam size, best-of, fp16

- ✅ **Presets**
  - Use "Fast", "Balanced", or "Accurate" presets to apply tuned defaults instantly

- 🔍 **Batch Status & Progress**
  - See real-time logs with timestamps
  - Progress label displays (e.g., `3/7` complete)
  - Skips already-transcribed files intelligently

- ⚖️ **Output Management**
  - Choose output folder
  - Supports formats: `.txt`, `.srt`, `.vtt`, `.tsv`, `.json`

- 🌟 **Nice Extras**
  - Auto-scroll toggle for the log
  - Sound notification on completion (optional)
  - Session persistence: remembers last-used settings on launch

---

## 📁 Installation

> Requires Python 3.9+

To run as source:
```bash
pip install -r requirements.txt
python transcriber.py
```

To build as standalone executable:
```bash
pyinstaller --onefile --windowed --icon=icon.ico transcriber.py
```
The output `.exe` will be in the `/dist` folder unless overridden.

---

## 🌐 Supported Formats
Input audio files:
- `.mp3`, `.m4a`, `.wav`, `.flac`, `.aac`, `.ogg`

Output transcription formats:
- `.txt`, `.srt`, `.vtt`, `.tsv`, `.json`

---

## 🔧 Configuration
- All options are accessible via the UI.
- Last used options are saved to a `.whisper_ui_config.json` file in the user's home directory.

---

## 🎓 License
MIT

---

## 🚀 Roadmap Ideas
See `CHANGELOG.md` for current and planned improvements.

- File preview mode
- Drag-and-drop support
- In-app playback with synchronized transcript
- Parallel model execution (experimental)

---

Built with ❤️ and `tkinter`, `whisper`, `pydub`, `wave`, `contextlib`, `threading`, and more.

> Created for local, offline transcription workflows with full control and flexibility.

---

### 🤖 Credits

This application was developed with guidance, debugging, and ✨ relentless support ✨ from [ChatGPT](https://openai.com/chatgpt), your friendly neighborhood code companion.

