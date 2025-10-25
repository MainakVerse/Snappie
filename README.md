# 🎬 SNAPPIE: Smart Video Trimmer

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.9+-brightgreen?logo=opencv)](https://opencv.org/)
[![MoviePy](https://img.shields.io/badge/MoviePy-1.0+-orange)](https://zulko.github.io/moviepy/)
[![Pillow](https://img.shields.io/badge/Pillow-10.0+-purple)](https://python-pillow.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Build](https://img.shields.io/badge/Build-PyInstaller-success)](https://pyinstaller.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)](#)

---

### 🧩 Overview
**Smart Video Trimmer** is a desktop GUI tool built with **Tkinter**, **OpenCV**, and **MoviePy** that allows you to:
- Load and preview any video file  
- Set start and end frames interactively  
- Play, pause, and stop video playback  
- Preview selected trim segment  
- Export the trimmed clip to HD (720×1080)  
- Automatically log all trims in a CSV file  

Perfect for editors, data scientists, and AI researchers handling video datasets.  

---

### 🛠️ Features
- 🎥 Frame-accurate trimming  
- 🕹️ Full playback controls (Play / Pause / Stop)  
- 🪄 In-app preview before saving  
- 💾 Automatic trim log (`logs/output.csv`)  
- 🧱 Modular, object-oriented architecture  
- 📦 Easily packaged into `.exe` using **PyInstaller**

---

### ⚙️ Installation
```bash
git clone https://github.com/MainakVerse/Snappie.git
cd Snappie
pip install -r requirements.txt
```


### 🚀 Usage
```
🚀 Usage
```

or build an .exe (Windows):

```
pyinstaller --onefile --noconsole --name "Snappie" main.py
```

### 📂 Folder Structure

```
video_trimmer/
├── main.py
├── gui.py
├── trimmer.py
├── utils.py
├── requirements.txt
├── logs/
│   └── output.csv
└── README.md
```

### 🧰 Requirements

```
opencv-python>=4.9.0
Pillow>=10.0.0
moviepy>=1.0.3
tkintertable>=1.3.3
numpy>=1.26.0
imageio[ffmpeg]>=2.34.0
```

### Install all dependencies

```
pip install -r requirements.txt
```

### 🌟 Contributing

Pull requests are welcome!
If you’d like to enhance features (e.g., thumbnails, filters, FFmpeg optimizations), please open an issue first to discuss your ideas.

## Made with ❤️ by Mainak