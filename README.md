# 🎬 FFmpeg Video Looper

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/CustomTkinter-Dark_UI-blue?style=for-the-badge" alt="CustomTkinter" />
  <img src="https://img.shields.io/badge/FFmpeg-Fast_Cut-0078D4?style=for-the-badge&logo=ffmpeg&logoColor=white" alt="FFmpeg" />
  <img src="https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white" alt="Windows" />
</p>

Десктопное приложение для **мгновенного зацикливания видео** до заданной длительности без перекодирования (без потери качества и за считанные секунды).

---

## ✨ Особенности

* **⚡ Мгновенный рендер (`-c copy`):** Видео склеивается и обрезается без пересчета кадров. Процесс занимает 1–3 секунды даже для многочасовых файлов.
* **🎯 Точный ввод времени:** Настройка целевой длительности в **часах, минутах и секундах**.
* **🚀 Без фризов интерфейса:** Вся обработка FFmpeg выполняется в отдельном фоновом потоке (`threading.Thread`).
* **📂 Обязательная валидация:** Защита от ошибок — приложение требует явного выбора папки сохранения и имени файла.
* **🎨 Современный GUI:** Минималистичный темный интерфейс на базе `CustomTkinter` с индикатором прогресса.
* **🔍 Точный расчёт хронометража:** Использование `ffprobe` для автоматического получения длительности исходника.

---

## 🛠️ Требования

Для запуска из исходного кода или сборки потребуются:

1. **Python 3.9+**
2. **FFmpeg** (`ffmpeg.exe` и `ffprobe.exe`) — должны лежать в корневой папке приложения.

---

## 🚀 Быстрый запуск (из исходного кода)

1. **Клонируйте репозиторий:**
   ```bash
   git clone [https://github.com/ВАШ_НИК/ffmpeg-video-looper.git](https://github.com/ВАШ_НИК/ffmpeg-video-looper.git)
   cd ffmpeg-video-looper