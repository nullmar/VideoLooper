# 🎬 FFmpeg Video Looper

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/CustomTkinter-Dark_UI-blue?style=for-the-badge" alt="CustomTkinter" />
  <img src="https://img.shields.io/badge/FFmpeg-Fast_Cut-0078D4?style=for-the-badge&logo=ffmpeg&logoColor=white" alt="FFmpeg" />
  <img src="https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white" alt="Windows" />
</p>

A lightweight desktop application for **instant video looping** to a targeted duration without re-encoding (zero quality loss and lightning-fast processing).

---

## ✨ Features

* **⚡ Instant Processing (`-c copy`):** Loops and cuts video streams directly without re-encoding frames. Generates output in just a few seconds, even for multi-hour videos.
* **🎯 Precise Time Controls:** Set exact target duration using separate **Hours, Minutes, and Seconds** input fields.
* **🚀 Smooth & Non-Blocking UI:** Heavy FFmpeg operations run in a background thread (`threading.Thread`) to keep the interface completely responsive.
* **📂 Strict Field Validation:** Protects against unexpected errors by requiring explicit selection of an output folder and filename before processing.
* **🎨 Modern Dark UI:** Clean aesthetic built with `CustomTkinter`, featuring an animated progress bar and live status feedback.
* **🔍 Accurate Duration Detection:** Leverages `ffprobe` to inspect input metadata and calculate precise loop counts automatically.

---

## 🛠️ Prerequisites

To run from source or build the application, you need:

1. **Python 3.9+**
2. **FFmpeg binaries** (`ffmpeg.exe` and `ffprobe.exe`) placed in the root directory of the application.

---
