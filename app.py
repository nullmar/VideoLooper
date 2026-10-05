import os
import sys
import subprocess
import json
import math
import threading
import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk

# Настройка темы
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class FFmpegLooperApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Настройки главного окна
        self.title("FFmpeg Video Looper")
        self.geometry("480x600")
        self.resizable(False, False)
        
        # Переменные состояния
        self.file_path = ""
        self.output_dir = ""
        self.is_processing = False

        # --- ЗАГОЛОВОК ---
        self.title_label = ctk.CTkLabel(
            self, 
            text="FFmpeg Looper", 
            font=ctk.CTkFont(size=22, weight="bold")
        )
        self.title_label.pack(pady=(18, 2))

        self.subtitle_label = ctk.CTkLabel(
            self, 
            text="Мгновенное зацикливание видео без потери качества", 
            font=ctk.CTkFont(size=12),
            text_color="#8a8a8a"
        )
        self.subtitle_label.pack(pady=(0, 12))

        # --- ЗОНА ВЫБОРА ИСХОДНОГО ФАЙЛА ---
        self.drop_frame = ctk.CTkFrame(
            self, 
            fg_color="#1e1e1e", 
            border_color="#333333", 
            border_width=2, 
            corner_radius=12,
            cursor="hand2"
        )
        self.drop_frame.pack(padx=25, fill="x", ipady=8)
        self.drop_frame.bind("<Button-1>", lambda e: self.select_file())

        self.drop_icon = ctk.CTkLabel(
            self.drop_frame, 
            text="📁", 
            font=ctk.CTkFont(size=22)
        )
        self.drop_icon.pack(pady=(2, 0))
        self.drop_icon.bind("<Button-1>", lambda e: self.select_file())

        self.file_label = ctk.CTkLabel(
            self, 
            text="Выберите видеофайл *", 
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#ef4444"
        )
        self.file_label = ctk.CTkLabel(
            self.drop_frame, 
            text="Нажмите, чтобы выбрать видеофайл *", 
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#b0b0b0"
        )
        self.file_label.pack(pady=(2, 2))
        self.file_label.bind("<Button-1>", lambda e: self.select_file())

        # --- ВЫБОР ПАПКИ СОХРАНЕНИЯ И ИМЕНИ (ОБЯЗАТЕЛЬНО) ---
        self.save_card = ctk.CTkFrame(self, fg_color="#181818", corner_radius=10)
        self.save_card.pack(padx=25, fill="x", pady=(12, 5), ipady=6)

        self.save_title = ctk.CTkLabel(
            self.save_card, 
            text="Параметры сохранения", 
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#aaa"
        )
        self.save_title.pack(pady=(4, 6))

        # Поле выбора папки
        self.folder_title_frame = ctk.CTkFrame(self.save_card, fg_color="transparent")
        self.folder_title_frame.pack(fill="x", padx=12, pady=(0, 2))

        ctk.CTkLabel(
            self.folder_title_frame, 
            text="Папка назначения", 
            font=ctk.CTkFont(size=11), 
            text_color="#8a8a8a"
        ).pack(side="left")
        
        ctk.CTkLabel(
            self.folder_title_frame, 
            text="*", 
            font=ctk.CTkFont(size=11, weight="bold"), 
            text_color="#ef4444"
        ).pack(side="left", padx=(2, 0))

        self.folder_frame = ctk.CTkFrame(self.save_card, fg_color="transparent")
        self.folder_frame.pack(fill="x", padx=12, pady=(0, 8))

        self.folder_entry = ctk.CTkEntry(
            self.folder_frame, 
            placeholder_text="Укажите папку...", 
            font=ctk.CTkFont(size=11),
            corner_radius=8,
            border_color="#333333"
        )
        self.folder_entry.pack(side="left", fill="x", expand=True, padx=(0, 6))

        self.btn_browse = ctk.CTkButton(
            self.folder_frame, 
            text="Обзор...", 
            width=70, 
            height=28,
            font=ctk.CTkFont(size=12),
            fg_color="#2a2a2a",
            hover_color="#383838",
            command=self.select_output_folder
        )
        self.btn_browse.pack(side="right")

        # Поле имени файла
        self.filename_title_frame = ctk.CTkFrame(self.save_card, fg_color="transparent")
        self.filename_title_frame.pack(fill="x", padx=12, pady=(0, 2))

        ctk.CTkLabel(
            self.filename_title_frame, 
            text="Имя готового файла (.mp4)", 
            font=ctk.CTkFont(size=11), 
            text_color="#8a8a8a"
        ).pack(side="left")

        ctk.CTkLabel(
            self.filename_title_frame, 
            text="*", 
            font=ctk.CTkFont(size=11, weight="bold"), 
            text_color="#ef4444"
        ).pack(side="left", padx=(2, 0))

        self.filename_entry = ctk.CTkEntry(
            self.save_card, 
            placeholder_text="Например: result.mp4", 
            font=ctk.CTkFont(size=11),
            corner_radius=8,
            border_color="#333333"
        )
        self.filename_entry.pack(fill="x", padx=12, pady=(0, 6))

        # --- ВВОД ВРЕМЕНИ (ЧАСЫ, МИНУТЫ, СЕКУНДЫ) ---
        self.time_card = ctk.CTkFrame(self, fg_color="#181818", corner_radius=10)
        self.time_card.pack(padx=25, fill="x", pady=(8, 10), ipady=6)

        self.time_title = ctk.CTkLabel(
            self.time_card, 
            text="Целевая длительность *", 
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#aaa"
        )
        self.time_title.pack(pady=(4, 6))

        self.inputs_frame = ctk.CTkFrame(self.time_card, fg_color="transparent")
        self.inputs_frame.pack()

        self.hours_entry = self.create_time_field(self.inputs_frame, "1", "ч")
        self.mins_entry = self.create_time_field(self.inputs_frame, "0", "мин")
        self.secs_entry = self.create_time_field(self.inputs_frame, "0", "сек")

        # --- ИНДИКАТОР ПРОГРЕССА ---
        self.progress_bar = ctk.CTkProgressBar(self, height=8, corner_radius=4)
        self.progress_bar.set(0)
        self.progress_bar.pack(padx=25, fill="x", pady=(10, 5))
        self.progress_bar.pack_forget()

        # --- КНОПКА ЗАПУСКА ---
        self.btn_start = ctk.CTkButton(
            self, 
            text="Сгенерировать видео", 
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#3b82f6", 
            hover_color="#2563eb",
            height=45,
            corner_radius=10,
            command=self.start_processing_thread
        )
        self.btn_start.pack(padx=25, fill="x", pady=(8, 6))

        # --- СТАТУС ---
        self.status_label = ctk.CTkLabel(
            self, 
            text="", 
            font=ctk.CTkFont(size=12),
            text_color="#10b981",
            wraplength=420
        )
        self.status_label.pack(pady=(0, 10))

    def create_time_field(self, parent, default_val, unit_text):
        box = ctk.CTkFrame(parent, fg_color="transparent")
        box.pack(side="left", padx=8)

        entry = ctk.CTkEntry(
            box, 
            width=52, 
            justify="center", 
            corner_radius=8,
            border_color="#333333"
        )
        entry.insert(0, default_val)
        entry.pack(side="left", padx=(0, 4))

        lbl = ctk.CTkLabel(box, text=unit_text, font=ctk.CTkFont(size=12), text_color="#8a8a8a")
        lbl.pack(side="left")

        return entry

    def select_file(self):
        if self.is_processing:
            return
            
        path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.mov *.avi *.mkv")])
        if path:
            self.file_path = path
            filename = os.path.basename(path)
            display_name = filename if len(filename) < 32 else filename[:29] + "..."
            self.file_label.configure(text=f"Выбран: {display_name}", text_color="#3b82f6")
            self.drop_frame.configure(border_color="#3b82f6")
            self.status_label.configure(text="")

    def select_output_folder(self):
        if self.is_processing:
            return
            
        folder = filedialog.askdirectory()
        if folder:
            self.output_dir = folder
            self.folder_entry.delete(0, tk.END)
            self.folder_entry.insert(0, folder)
            self.folder_entry.configure(border_color="#333333")

    def get_video_duration(self, ffprobe_exe, file_path):
        cmd = [
            ffprobe_exe, 
            "-v", "error", 
            "-show_entries", "format=duration", 
            "-of", "json", 
            file_path
        ]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)
        data = json.loads(result.stdout)
        return float(data['format']['duration'])

    def start_processing_thread(self):
        if self.is_processing:
            return

        # 1. Проверка исходного файла
        if not self.file_path or not os.path.exists(self.file_path):
            self.status_label.configure(text="Ошибка: Выберите исходный видеофайл!", text_color="#ef4444")
            self.drop_frame.configure(border_color="#ef4444")
            return

        # 2. Обязательная проверка папки для сохранения
        custom_dir = self.folder_entry.get().strip()
        if not custom_dir:
            self.status_label.configure(text="Ошибка: Укажите папку для сохранения!", text_color="#ef4444")
            self.folder_entry.configure(border_color="#ef4444")
            return
        elif not os.path.isdir(custom_dir):
            self.status_label.configure(text="Ошибка: Указанная папка не существует!", text_color="#ef4444")
            self.folder_entry.configure(border_color="#ef4444")
            return

        # 3. Обязательная проверка имени файла
        custom_name = self.filename_entry.get().strip()
        if not custom_name:
            self.status_label.configure(text="Ошибка: Введите имя выходного файла!", text_color="#ef4444")
            self.filename_entry.configure(border_color="#ef4444")
            return

        # 4. Проверка корректности введенного времени
        try:
            h = float(self.hours_entry.get().strip() or 0)
            m = float(self.mins_entry.get().strip() or 0)
            s = float(self.secs_entry.get().strip() or 0)
            total_seconds = int(h * 3600 + m * 60 + s)

            if total_seconds <= 0:
                self.status_label.configure(text="Ошибка: Укажите длительность больше 0 сек!", text_color="#ef4444")
                return
        except ValueError:
            self.status_label.configure(text="Ошибка: Некорректные числа во времени!", text_color="#ef4444")
            return

        # Если все поля прошли валидацию — сбрасываем подсветку ошибок
        self.folder_entry.configure(border_color="#333333")
        self.filename_entry.configure(border_color="#333333")
        self.drop_frame.configure(border_color="#3b82f6")

        self.is_processing = True
        self.btn_start.configure(state="disabled", text="Обработка...")
        self.progress_bar.pack(padx=25, fill="x", pady=(10, 5))
        self.progress_bar.configure(mode="indeterminate")
        self.progress_bar.start()

        threading.Thread(
            target=self.process_video, 
            args=(total_seconds, custom_dir, custom_name), 
            daemon=True
        ).start()

    def process_video(self, target_seconds, save_dir, filename):
        base_dir = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__)
        ffmpeg_exe = os.path.join(base_dir, "ffmpeg.exe")
        ffprobe_exe = os.path.join(base_dir, "ffprobe.exe")

        if not os.path.exists(ffmpeg_exe):
            self.update_status("Ошибка: ffmpeg.exe не найден рядом с приложением!", "#ef4444")
            return

        try:
            self.update_status_text("Анализ исходного файла...", "#f59e0b")

            if os.path.exists(ffprobe_exe):
                try:
                    duration = self.get_video_duration(ffprobe_exe, self.file_path)
                except Exception:
                    duration = 5.0
            else:
                duration = 5.0  

            repeats = math.ceil(target_seconds / duration) + 1

            # Гарантируем расширение .mp4
            if not filename.endswith(".mp4"):
                filename += ".mp4"

            output_file = os.path.join(save_dir, filename)

            cmd = [
                ffmpeg_exe, "-y", 
                "-stream_loop", str(repeats), 
                "-i", self.file_path, 
                "-t", str(target_seconds), 
                "-c", "copy", 
                output_file
            ]

            self.update_status_text("Зацикливание и сохранение...", "#f59e0b")
            subprocess.run(cmd, check=True, creationflags=subprocess.CREATE_NO_WINDOW)

            self.update_status("✓ Готово! Файл успешно сохранен", "#10b981")
        except Exception as e:
            self.update_status(f"Ошибка: {str(e)}", "#ef4444")

    def update_status_text(self, text, color):
        self.after(0, lambda: self.status_label.configure(text=text, text_color=color))

    def update_status(self, text, color):
        def reset_ui():
            self.progress_bar.stop()
            self.progress_bar.pack_forget()
            self.btn_start.configure(state="normal", text="Сгенерировать видео")
            self.status_label.configure(text=text, text_color=color)
            self.is_processing = False

        self.after(0, reset_ui)

if __name__ == "__main__":
    app = FFmpegLooperApp()
    app.mainloop()