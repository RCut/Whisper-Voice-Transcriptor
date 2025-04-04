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

## 🌐 Supported Formats
Input audio files:
- `.mp3`, `.m4a`, `.wav`, `.flac`, `.aac`, `.ogg`

Output transcription formats:
- `.txt`, `.srt`, `.vtt`, `.tsv`, `.json`

---

## 🔧 Installation

This app runs on **Python 3.9 or newer** and works on **Windows, macOS, and Linux**.


### 📦 Step-by-Step Installation

1. **Install Python 3.9+**

   - [Download Python here](https://www.python.org/downloads/)
   - Make sure to check ✅ "Add Python to PATH" during installation (on Windows)


2. **Clone the Repository**

```bash
git clone https://github.com/RCut/Whisper-Voice-Transcriptor.git
cd Whisper-Voice-Transcriptor
```


3. **Install Required Dependencies**

Make sure you have `pip` (comes with Python). Then run:

```bash
pip install -r requirements.txt
```

This will install:
- [`whisper`](https://github.com/openai/whisper)
- `torch` (PyTorch, used under the hood)
- `numpy`, `tkinter`, and other UI/audio tools

If you see errors related to `torch`, use this alternative:
```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

4. **(Optional) Install ffmpeg**

Whisper needs `ffmpeg` for audio decoding. Most systems already have it.

- **Windows**: [Download ffmpeg here](https://ffmpeg.org/download.html) and add to PATH
- **macOS**: `brew install ffmpeg`
- **Linux**: `sudo apt install ffmpeg`


5. **Run the App**

```bash
python transcriber.py
```

This will launch the GUI interface. You can now select files or folders and transcribe them with Whisper.


6. **(Optional) Build into .exe**

To create a Windows `.exe`:
```bash
pyinstaller --onefile --windowed --icon=icon.ico transcriber.py
```

The executable will appear in the `dist/` folder. No internet is required after the first run (Whisper model is cached).

---

## 🎓 License
MIT

---

Built with ❤️ and `tkinter`, `whisper`, `pydub`, `wave`, `contextlib`, `threading`, and more.

> Created for local, offline transcription workflows with full control and flexibility.

---

### 🤖 Credits

This application was developed with guidance, debugging, and ✨ relentless support ✨ from [ChatGPT](https://openai.com/chatgpt), your friendly neighborhood code companion.

