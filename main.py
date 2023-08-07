import tkinter as tk
from tkinter import filedialog
import threading
import cv2
import numpy as np
import time
import os
from PIL import ImageGrab, Image

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
FPS = 4
VIDEO_NAME = "screen_recording.mp4"

class ScreenRecorder:
    def __init__(self, root):
        self.root = root
        self.recording = False
        self.paused = False
        self.video_thread = None
        self.output_folder = ""

        self.record_button = tk.Button(root, text="Start Recording", command=self.toggle_recording)
        self.record_button.pack(side=tk.LEFT, padx=5, pady=10)

        self.pause_button = tk.Button(root, text="Pause", command=self.toggle_pause, state=tk.DISABLED)
        self.pause_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.resume_button = tk.Button(root, text="Resume", command=self.toggle_pause, state=tk.DISABLED)
        self.resume_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.stop_button = tk.Button(root, text="Stop Recording", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.save_button = tk.Button(root, text="Save Recording", command=self.save_video, state=tk.DISABLED)
        self.save_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.select_output_button = tk.Button(root, text="Select Output Folder", command=self.select_output_folder)
        self.select_output_button.pack(side=tk.LEFT, padx=5, pady=5)

    def toggle_recording(self):
        if not self.recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        self.recording = True
        self.paused = False
        self.record_button.config(text="Stop Recording", state=tk.DISABLED)
        self.pause_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.NORMAL)
        self.save_button.config(state=tk.DISABLED)
        self.select_output_button.config(state=tk.DISABLED)

        self.video_thread = threading.Thread(target=self.record_screen)
        self.video_thread.start()

    def stop_recording(self):
        self.recording = False
        self.record_button.config(text="Start Recording", state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
        self.resume_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.DISABLED)
        self.save_button.config(state=tk.NORMAL)
        self.select_output_button.config(state=tk.NORMAL)

    def toggle_pause(self):
        self.paused = not self.paused
        if self.paused:
            self.pause_button.config(state=tk.DISABLED)
            self.resume_button.config(state=tk.NORMAL)
        else:
            self.pause_button.config(state=tk.NORMAL)
            self.resume_button.config(state=tk.DISABLED)

    def select_output_folder(self):
        self.output_folder = filedialog.askdirectory()

    def record_screen(self):
        self.frames = []
        self.start_time = time.time()

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        output_path = os.path.join(self.output_folder, VIDEO_NAME)
        out = cv2.VideoWriter(output_path, fourcc, FPS, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Timer for capturing the screen at the desired FPS
        timer_interval = 1 / FPS

        while self.recording:
            if not self.paused:
                # Capture the screen frame
                frame = self.capture_screen()

                # Write the frame to the video
                out.write(frame)

        out.release()

        # Calculate the total recording time
        total_time = time.time() - self.start_time
        print(f"Recording saved: {output_path}")
        print(f"Total recording time: {total_time:.2f} seconds")

    def capture_screen(self):
        # Capture the screen frame
        hwin = self.root.winfo_id()
        rect = (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        img = ImageGrab.grab(rect)

        # Convert the image to an array
        frame = np.array(img)

        # Convert RGB to BGR for OpenCV video writing
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        return frame

    def save_video(self):
        pass

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Screen Recorder")
    screen_recorder = ScreenRecorder(root)
    root.mainloop()
