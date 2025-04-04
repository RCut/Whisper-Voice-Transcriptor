import os
import whisper
import threading
import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk
from datetime import datetime
import sys
import json
import platform
import winsound

CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".whisper_ui_config.json")

AUDIO_EXTENSIONS = (".mp3", ".m4a", ".wav", ".flac", ".aac", ".ogg")


def load_last_session():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}


def save_session():
    data = {
        "input_paths": input_paths,
        "output_dir": output_dir_var.get(),
        "include_subfolders": include_subfolders.get(),
        "auto_scroll": auto_scroll.get(),
        "sound_on_complete": sound_on_complete.get(),
        **{k: v.get() for k, v in whisper_config_vars.items()}
    }
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    except:
        pass

root = tk.Tk()
root.title("Whisper Batch Transcriber")
root.geometry("800x750")

def get_default_config():
    return {
        "model": tk.StringVar(value="small"),
        "language": tk.StringVar(value="Auto"),
        "task": tk.StringVar(value="transcribe"),
        "output_format": tk.StringVar(value="txt"),
        "temperature": tk.DoubleVar(value=0.0),
        "best_of": tk.IntVar(value=5),
        "beam_size": tk.IntVar(value=5),
        "fp16": tk.BooleanVar(value=False),
        "verbose": tk.BooleanVar(value=True)
    }

whisper_config_vars = get_default_config()
auto_scroll = tk.BooleanVar(value=True)
sound_on_complete = tk.BooleanVar(value=True)
abort_flag = threading.Event()
include_subfolders = tk.BooleanVar(value=False)
input_paths = []

class TextRedirector:
    def __init__(self, widget):
        self.widget = widget
    def write(self, text):
        self.widget.insert(tk.END, text)
        if auto_scroll.get():
            self.widget.see(tk.END)
    def flush(self):
        pass

def apply_profile(profile_name):
    if profile_name == "Fast":
        whisper_config_vars["temperature"].set(0.3)
        whisper_config_vars["beam_size"].set(1)
        whisper_config_vars["best_of"].set(1)
    elif profile_name == "Balanced":
        whisper_config_vars["temperature"].set(0.3)
        whisper_config_vars["beam_size"].set(5)
        whisper_config_vars["best_of"].set(1)
    elif profile_name == "Accurate":
        whisper_config_vars["temperature"].set(0.2)
        whisper_config_vars["beam_size"].set(10)
        whisper_config_vars["best_of"].set(1)

def log(msg, console):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    console.insert(tk.END, f"[{timestamp}] {msg}\n")
    if auto_scroll.get():
        console.see(tk.END)

def set_transcription_buttons(running):
    root.after(0, lambda: start_btn.config(state=tk.DISABLED if running else tk.NORMAL))
    root.after(0, lambda: stop_btn.config(state=tk.NORMAL if running else tk.DISABLED))

def batch_transcribe(paths, output_dir, console):
    if not paths:
        log("❌ No input files or folders selected.", console)
        set_transcription_buttons(False)
        return

    found_any = False
    config = {k: v.get() if not isinstance(v, tk.BooleanVar) else bool(v.get()) for k, v in whisper_config_vars.items()}
    if config["language"] == "Auto":
        config["language"] = None

    redirector = TextRedirector(console)
    sys.stdout = redirector
    sys.stderr = redirector

    log("Loading Whisper model...", console)
    model = whisper.load_model(config["model"])

    log("Starting batch transcription...", console)
    for k, v in config.items():
        log(f"  - {k}: {v}", console)
    log(f"  - include_subfolders: {include_subfolders.get()}", console)
    log("", console)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        log(f"Created output directory: {output_dir}", console)

    def gather_files():
        files = []
        for path in paths:
            if os.path.isdir(path):
                if include_subfolders.get():
                    for root_dir, _, fs in os.walk(path):
                        for f in fs:
                            if f.lower().endswith(AUDIO_EXTENSIONS):
                                files.append(os.path.join(root_dir, f))
                else:
                    for f in os.listdir(path):
                        if f.lower().endswith(AUDIO_EXTENSIONS):
                            files.append(os.path.join(path, f))
            elif os.path.isfile(path) and path.lower().endswith(AUDIO_EXTENSIONS):
                files.append(path)
        return files

    all_files = gather_files()
    total_files = len(all_files)

    def process_file(filepath):
        base_name = os.path.splitext(os.path.basename(filepath))[0]
        output_file = os.path.join(output_dir, f"{base_name}.{config['output_format']}")

        if os.path.exists(output_file):
            log(f"⚠️ Skipping '{filepath}' – already transcribed.", console)
            return

        log(f"Processing '{filepath}'...", console)

        result = model.transcribe(
            filepath,
            task=config["task"],
            temperature=config["temperature"],
            best_of=config["best_of"],
            beam_size=config["beam_size"],
            fp16=config["fp16"],
            verbose=config["verbose"],
        )

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result["text"])
        log(f"✅ Saved output: {output_file}", console)

    for i, filepath in enumerate(all_files):
        if abort_flag.is_set():
            log("⚠️ Transcription aborted by user.", console)
            set_transcription_buttons(False)
            return
        found_any = True
        process_file(filepath)
        root.after(0, lambda i=i: total_progress_label.config(text=f"Batch Progress: {i+1}/{total_files}"))

    if not found_any:
        log("⚠️ No supported audio files found.", console)
    else:
        log("🎉 All files processed.", console)
        if sound_on_complete.get() and platform.system() == "Windows":
            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)

    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__
    set_transcription_buttons(False)
    total_progress_label.config(text="All files processed.")

def start_transcription(input_dir_var, output_dir_var, console):
    abort_flag.clear()
    set_transcription_buttons(True)
    threading.Thread(
        target=batch_transcribe,
        args=(input_paths, output_dir_var.get(), console),
        daemon=True
    ).start()

def stop_transcription():
    abort_flag.set()
    log("🛑 Abort requested. Finishing current file, then stopping...", console)

session_data = load_last_session()
base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(sys.argv[0])))
input_paths = session_data.get("input_paths", [])
output_dir_var = tk.StringVar(value=session_data.get("output_dir", os.path.normpath(os.path.join(base_dir, "output_text"))))

for k, var in whisper_config_vars.items():
    if k in session_data:
        var.set(session_data[k])

include_subfolders.set(session_data.get("include_subfolders", False))
auto_scroll.set(session_data.get("auto_scroll", True))
sound_on_complete.set(session_data.get("sound_on_complete", True))

def select_input():
    global input_paths
    files = filedialog.askopenfilenames(filetypes=[("Audio Files", "*.mp3 *.m4a *.wav *.flac *.aac *.ogg")])
    folder = filedialog.askdirectory()
    paths = list(files)
    if folder:
        paths.append(folder)
    if paths:
        input_paths = [os.path.normpath(p) for p in paths]
        input_label.config(text="; ".join(input_paths))

def select_output():
    path = filedialog.askdirectory()
    if path:
        output_dir_var.set(os.path.normpath(path))

def show_file_tree_modal():
    def populate_node(tree, node):
        path = tree.set(node, "fullpath")
        tree.delete(*tree.get_children(node))  # Remove dummy
        try:
            for name in sorted(os.listdir(path)):
                abspath = os.path.join(path, name)
                if os.path.isdir(abspath):
                    oid = tree.insert(node, 'end', text=name, values=[abspath])
                    tree.insert(oid, 'end')  # dummy for lazy load
                elif abspath.lower().endswith(AUDIO_EXTENSIONS):
                    tree.insert(node, 'end', text=name, values=[abspath])
        except Exception:
            pass

    def on_open(event):
        node = tree.focus()
        if tree.get_children(node):
            first_child = tree.get_children(node)[0]
            if tree.item(first_child, 'text') == '':
                populate_node(tree, node)

    def on_ok():
        global input_paths
        selected = [tree.item(i, "values")[0] for i in tree.selection()]
        cleaned = []

        for path in selected:
            normalized = os.path.normpath(path)
            skip = False
            for other in selected:
                other_norm = os.path.normpath(other)
                if normalized == other_norm:
                    continue
                if include_subfolders.get() and os.path.isdir(other_norm) and normalized.startswith(other_norm + os.sep):
                    skip = True
                    break
            if not skip:
                cleaned.append(normalized)

        input_paths = cleaned
        input_label.config(text="; ".join(input_paths))
        top.destroy()

    top = tk.Toplevel(root)
    top.title("Select Files and Folders")
    top.geometry("600x400")

    # Tree + Scrollbar in same frame
    tree_frame = tk.Frame(top)
    tree_frame.pack(fill=tk.BOTH, expand=True)

    tree = ttk.Treeview(tree_frame, columns=("fullpath",), displaycolumns=())
    tree.heading("#0", text="Filesystem")
    tree.bind('<<TreeviewOpen>>', on_open)
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    tree_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=tree_scroll.set)
    tree_scroll.pack(side="right", fill="y")

    # Filesystem roots
    if os.name == "nt":
        drives = [f"{d}:\\" for d in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if os.path.exists(f"{d}:\\")]
        for drive in drives:
            node = tree.insert('', 'end', text=drive, values=[drive])
            tree.insert(node, 'end')  # dummy
    else:
        node = tree.insert('', 'end', text="/", values=["/"])
        tree.insert(node, 'end')

    # Expand to app path (base_dir is correct, works in EXE too)
    app_path = base_dir
    parts = os.path.abspath(app_path).split(os.sep)
    if os.name == "nt" and ':' in parts[0]:
        drive = parts[0] + "\\"
        parts = [drive] + parts[1:]
    current = ''
    parent = ''
    for i, part in enumerate(parts):
        current = os.path.join(current, part) if current else part
        matches = tree.get_children(parent)
        for child in matches:
            if tree.item(child, "text").lower() == part.lower():
                parent = child
                tree.item(parent, open=True)
                populate_node(tree, parent)
                tree.see(parent)
                break

    tk.Checkbutton(top, text="Include Subfolders", variable=include_subfolders).pack(anchor="w", padx=10, pady=(5, 0))

    button_frame = tk.Frame(top)
    button_frame.pack(pady=10)
    tk.Button(button_frame, text="OK", command=on_ok).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Cancel", command=top.destroy).pack(side=tk.LEFT, padx=5)

# Input and Output path selection
frame = tk.Frame(root)
frame.pack(pady=10, fill=tk.X, padx=10)

# Row 1: Select Files/Folders + input path label
input_row = tk.Frame(frame)
input_row.pack(fill=tk.X, pady=(0, 5))

btn_tree = tk.Button(input_row, text="Select Files/Folders...", command=show_file_tree_modal)
btn_tree.pack(side=tk.LEFT)

input_label = tk.Label(input_row, text="; ".join(input_paths), anchor='w', wraplength=500, justify='left')
input_label.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)

# Row 2: Select Output Folder + output path label
output_row = tk.Frame(frame)
output_row.pack(fill=tk.X)

btn_output = tk.Button(output_row, text="Select Output Folder", command=select_output)
btn_output.pack(side=tk.LEFT)

output_label = tk.Label(output_row, textvariable=output_dir_var, anchor='w', wraplength=500, justify='left')
output_label.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)

# Whisper parameters
config_frame = tk.LabelFrame(root, text="Whisper Parameters")
config_frame.pack(padx=10, pady=5, fill=tk.X)

profile_frame = tk.Frame(config_frame)
profile_frame.grid(row=0, column=0, columnspan=2, pady=(0, 10))
tk.Label(profile_frame, text="Presets:").pack(side=tk.LEFT)
tk.Button(profile_frame, text="Fast", command=lambda: apply_profile("Fast")).pack(side=tk.LEFT, padx=2)
tk.Button(profile_frame, text="Balanced", command=lambda: apply_profile("Balanced")).pack(side=tk.LEFT, padx=2)
tk.Button(profile_frame, text="Accurate", command=lambda: apply_profile("Accurate")).pack(side=tk.LEFT, padx=2)

tooltips = {
    "model": "Model size: tiny, base, small, medium, large",
    "language": "Language code (e.g. en, ru) or Auto",
    "task": "transcribe = same language, translate = to English",
    "output_format": "Output format: txt, srt, vtt, tsv, json",
    "temperature": "Decoding randomness (0.0 = stable, 1.0 = creative)",
    "best_of": "Only used if beam_size = 1. Try N variations, choose best",
    "beam_size": "How many paths Whisper explores. Higher = better, slower",
    "fp16": "Use float16 (True = GPU, False = CPU)",
    "verbose": "Show live decoding details in console"
}

row = 1
for key, var in whisper_config_vars.items():
    label = tk.Label(config_frame, text=key)
    label.grid(row=row, column=0, sticky='w')
    if isinstance(var, tk.StringVar):
        values = {
            "model": ["tiny", "base", "small", "medium", "large"],
            "language": ["Auto", "en", "ru", "fr", "de", "es"],
            "task": ["transcribe", "translate"],
            "output_format": ["txt", "srt", "vtt", "tsv", "json"]
        }.get(key, [])
        if values:
            ttk.Combobox(config_frame, textvariable=var, values=values).grid(row=row, column=1)
        else:
            tk.Entry(config_frame, textvariable=var).grid(row=row, column=1)
    elif isinstance(var, (tk.DoubleVar, tk.IntVar)):
        tk.Entry(config_frame, textvariable=var).grid(row=row, column=1)
    elif isinstance(var, tk.BooleanVar):
        tk.Checkbutton(config_frame, variable=var).grid(row=row, column=1, sticky='w')
    label.bind("<Enter>", lambda e, t=tooltips[key]: root.title(t))
    label.bind("<Leave>", lambda e: root.title("Whisper Batch Transcriber"))
    row += 1

# Progress label
total_progress_label = tk.Label(root, text="", font=("Arial", 10))
total_progress_label.pack(pady=(5, 0))

# Control row: checkboxes + buttons
control_frame = tk.Frame(root)
control_frame.pack(fill=tk.X, pady=(5, 0), padx=10)

# Left: Play sound checkbox
tk.Checkbutton(control_frame, text="Play sound on complete", variable=sound_on_complete).pack(side=tk.LEFT)

# Center: Start/Stop buttons
btn_frame = tk.Frame(control_frame)
btn_frame.pack(side=tk.LEFT, expand=True)
start_btn = tk.Button(btn_frame, text="Start Transcription", command=lambda: start_transcription(input_paths, output_dir_var, console))
start_btn.pack(side=tk.LEFT, padx=5)
stop_btn = tk.Button(btn_frame, text="Stop", command=stop_transcription, state=tk.DISABLED)
stop_btn.pack(side=tk.LEFT, padx=5)

# Right: Auto-scroll checkbox
tk.Checkbutton(control_frame, text="Auto-scroll logs", variable=auto_scroll).pack(side=tk.RIGHT)

# Console log window
console = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=20)
console.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)


root.protocol("WM_DELETE_WINDOW", lambda: (save_session(), root.destroy()))
root.mainloop()
