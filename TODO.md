## ✅ App Refactor & Safety TODO Map

### 🔀 1. **Safe Shutdown & Thread Handling**
| Item | Description | Priority |
|------|-------------|----------|
| `a`  | Add `try/finally` block around `batch_transcribe()` to restore UI state on any exception | 🔴 High |
| `b`  | Ensure model and file handles are closed if user quits mid-transcription | 🟡 Medium |
| `c`  | On `WM_DELETE_WINDOW`, set `abort_flag` and wait for thread to finish or kill it gracefully | 🔴 High |
| `d`  | Optional: Graceful kill timeout and force stop fallback | 🟡 Medium |

---

### 🌐 2. **Model Download Feedback**
| Item | Description | Priority |
|------|-------------|----------|
| `a`  | Before calling `whisper.load_model()`, check if model is cached (optional) | ⚪ Low |
| `b`  | Add a loading spinner or “This may take a minute…” warning during model download | 🟡 Medium |

---

### 🧹 3. **File Overwrite Protection**
| Item | Description | Priority |
|------|-------------|----------|
| `a`  | If output file exists: prompt to overwrite, skip, or rename (with “(1)” suffix) | 🟠 Optional |
| `b`  | Or add checkbox: `Allow Overwrite Existing Files` | 🟡 Medium |

---

### 📄 4. **Log File Support**
| Item | Description | Priority |
|------|-------------|----------|
| `a`  | Create a `logs/` folder in app dir or user's home | 🟢 Easy |
| `b`  | Mirror all `log(...)` console output into a `transcriber_log.txt` file with same timestamp prefix | 🟡 Medium |
| `c`  | Rotate logs or delete after X days (optional) | ⚪ Low |

---

### 🧼 5. **Code Structure and Readability**
| Item | Description | Priority |
|------|-------------|----------|
| `a`  | Break code into logical modules: `ui.py`, `transcription.py`, `config.py`, `utils.py` | 🟡 Medium |
| `b`  | Use `pathlib.Path` consistently instead of `os.path` for cleaner path handling | 🟡 Medium |
| `c`  | Group GUI layout into a `build_ui()` function to improve readability | 🟢 Easy |
| `d`  | Move global variables to a `state.py` or constants file (optional) | ⚪ Low |

---

### 🧪 6. **Testing & Safety**
| Item | Description | Priority |
|------|-------------|----------|
| `a`  | Add test file with unsupported format (e.g. `.txt`) to ensure it’s ignored | 🟢 Easy |
| `b`  | Check what happens with invalid/corrupted audio files | 🟡 Medium |
| `c`  | Add sample files to `tests/` folder with batch cases | ⚪ Low |

---

### 🎨 7. **UI/UX Polish**
| Item | Description | Priority |
|------|-------------|----------|
| `a`  | Scrollable UI if resized too small | ⚪ Low |
| `b`  | Highlight currently processed file in progress label | 🟡 Medium |
| `c`  | Batch summary at the end: “3 files succeeded, 1 skipped, 2 failed” | 🟠 Optional |