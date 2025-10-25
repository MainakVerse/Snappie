import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import threading
from trimmer import VideoTrimmer
from utils import Logger, get_output_path


class VideoTrimmerApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎬 SNAPPIE ")
        self.root.geometry("640x820")

        self.video_path = None
        self.cap = None
        self.current_frame = 0
        self.total_frames = 0
        self.start_frame = 0
        self.end_frame = 0

        self.is_playing = False
        self.is_previewing = False

        self.trimmer = VideoTrimmer()
        self.logger = Logger("logs/output.csv")

        self.create_widgets()

    # ---------- UI SETUP ----------
    def create_widgets(self):
        self.canvas = tk.Canvas(self.root, width=480, height=640, bg="black")
        self.canvas.pack(pady=10)

        self.slider = tk.Scale(self.root, from_=0, to=0, orient="horizontal", length=580, command=self.set_frame)
        self.slider.pack()

        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=5)

        tk.Button(control_frame, text="⏏ Load", command=self.load_video).grid(row=0, column=0, padx=5)
        tk.Button(control_frame, text="Set ▶ Start", command=self.set_start).grid(row=0, column=1, padx=5)
        tk.Button(control_frame, text="Set ⏹ End", command=self.set_end).grid(row=0, column=2, padx=5)
        tk.Button(control_frame, text="🎞 Preview", command=self.preview_trim).grid(row=0, column=3, padx=5)
        tk.Button(control_frame, text="✂ Trim & Save", command=self.trim_video).grid(row=0, column=4, padx=5)

        player_frame = tk.Frame(self.root)
        player_frame.pack(pady=10)
        tk.Button(player_frame, text="▶ Play", command=self.play_video).grid(row=0, column=0, padx=10)
        tk.Button(player_frame, text="⏸ Pause", command=self.pause_video).grid(row=0, column=1, padx=10)
        tk.Button(player_frame, text="⏹ Stop", command=self.stop_video).grid(row=0, column=2, padx=10)

        self.status_label = tk.Label(self.root, text="No video loaded", fg="gray")
        self.status_label.pack(pady=5)

    # ---------- VIDEO LOADING ----------
    def load_video(self):
        path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4 *.avi *.mkv *.MOV")])
        if not path:
            return
        if self.cap:
            self.cap.release()

        self.video_path = path
        self.cap = cv2.VideoCapture(path)
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.slider.config(to=self.total_frames - 1)
        self.set_frame(0)
        self.status_label.config(text=f"Loaded: {path.split('/')[-1]}")

    # ---------- FRAME DISPLAY ----------
    def set_frame(self, frame_num):
        if not self.cap:
            return
        frame_num = int(frame_num)
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        ret, frame = self.cap.read()
        if ret:
            self.current_frame = frame_num
            self.display_frame(frame)

    def display_frame(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame).resize((480, 640))
        self.photo = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, anchor="nw", image=self.photo)

    # ---------- PLAYBACK CONTROLS ----------
    def play_video(self):
        if not self.cap or self.is_playing:
            return

        def play():
            self.is_playing = True
            while self.is_playing and self.cap.isOpened():
                ret, frame = self.cap.read()
                if not ret:
                    break
                self.display_frame(frame)
                self.current_frame = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
                self.slider.set(self.current_frame)
                self.root.update_idletasks()
                self.root.update()
                cv2.waitKey(int(1000 / self.cap.get(cv2.CAP_PROP_FPS)))
            self.is_playing = False

        threading.Thread(target=play, daemon=True).start()
        self.status_label.config(text="Playing video...")

    def pause_video(self):
        if self.is_playing:
            self.is_playing = False
            self.status_label.config(text=f"Paused at frame {self.current_frame}")

    def stop_video(self):
        self.is_playing = False
        if self.cap:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            self.set_frame(0)
        self.status_label.config(text="Stopped.")

    # ---------- TRIM SELECTION ----------
    def set_start(self):
        self.start_frame = self.current_frame
        self.status_label.config(text=f"Start Frame: {self.start_frame}")

    def set_end(self):
        self.end_frame = self.current_frame
        self.status_label.config(text=f"End Frame: {self.end_frame}")

    # ---------- PREVIEW TRIM ----------
    def preview_trim(self):
        if not self.video_path:
            messagebox.showwarning("Error", "No video loaded!")
            return
        if self.end_frame <= self.start_frame:
            messagebox.showwarning("Error", "Invalid frame range!")
            return
        if self.is_previewing:
            return

        def play_preview():
            self.is_previewing = True
            cap = cv2.VideoCapture(self.video_path)
            cap.set(cv2.CAP_PROP_POS_FRAMES, self.start_frame)
            while self.is_previewing and cap.isOpened():
                frame_num = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
                if frame_num > self.end_frame:
                    break
                ret, frame = cap.read()
                if not ret:
                    break
                self.display_frame(frame)
                self.slider.set(frame_num)
                self.root.update_idletasks()
                self.root.update()
                cv2.waitKey(int(1000 / cap.get(cv2.CAP_PROP_FPS)))
            cap.release()
            self.is_previewing = False
            self.status_label.config(text="Preview finished.")

        threading.Thread(target=play_preview, daemon=True).start()
        self.status_label.config(text="Previewing selection...")

    # ---------- TRIM SAVE ----------
    def trim_video(self):
        if not self.video_path:
            messagebox.showwarning("Error", "No video loaded!")
            return
        if self.end_frame <= self.start_frame:
            messagebox.showwarning("Error", "Invalid frame range!")
            return

        output_path = get_output_path(self.video_path, self.start_frame, self.end_frame)
        try:
            self.trimmer.trim(self.video_path, self.start_frame, self.end_frame, output_path)
            self.logger.log(self.video_path, self.start_frame, self.end_frame, output_path)
            messagebox.showinfo("Success", f"Trimmed video saved at:\n{output_path}")
            self.status_label.config(text="Trim completed successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to trim video:\n{e}")

    def run(self):
        self.root.mainloop()
