import tkinter as tk
import cv2
import vlc
from PIL import Image, ImageTk

import Constant as Cons


class VideoPlayer:
    def __init__(self, root, rtsp_url):
        self.photo = None
        self.root = root
        self.rtsp_url = rtsp_url
        self.cap = None
        self.running = False

        # self.instance = vlc.Instance(
        #     '--network-caching=300',  # Set network caching to 300 ms
        #     '--rtsp-frame-buffer-size=10000000',  # Adjust RTSP frame buffer size (if necessary)
        #     '--rtsp-tcp'  # Use RTSP over T1. CP, which might help with stability (optional)
        # )
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

        self.canvas = tk.Canvas(root, width=Cons.camera_resolution['w'], height=Cons.camera_resolution['h'])
        # self.canvas.grid(row=0, column=0)
        self.canvas.place(x=Cons.rtsp_pos['x'], y=Cons.rtsp_pos['y'])

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    # def start_video(self):
    #     if self.cap is None:
    #         self.cap = cv2.VideoCapture(self.rtsp_url)
    #         if not self.cap.isOpened():
    #             print("Cannot open RTSP stream")
    #             return
    #         self.running = True
    #         self.update_frame()

    def update_frame(self):
        if self.running:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
                self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
            print(ret)
            self.root.after(10, self.update_frame)

    # def stop_video(self):
    #     self.running = False
    #     if self.cap is not None:
    #         self.cap.release()
    #         self.cap = None

    def __del__(self):
        self.stop_video()

    # def on_closing(self):
    #     self.stop_video()
    #     self.root.destroy()

    # VLC
    def start_video(self):
        media = self.instance.media_new(self.rtsp_url)
        self.player.set_media(media)

        # Assign the canvas window ID to VLC player
        handle = self.canvas.winfo_id()
        self.player.set_hwnd(handle)

        self.player.play()

    def stop_video(self):
        self.player.stop()

    def on_closing(self):
        self.stop_video()
        self.root.destroy()
