import tkinter as tk
import vlc
from PIL import Image, ImageTk
from PIL.ImageTk import PhotoImage

import Constant as Cons


class VideoPlayer:

    def __init__(self, root, rtsp_url, pos, tag):
        self.root = root
        self.rtsp_url = rtsp_url
        self.width = pos['w']
        self.height = pos['h']
        self.tag = tag
        self.is_default = True

        self.running = True

        # self.instance = vlc.Instance(
        #     '--network-caching=300',  # Set network caching to 300 ms
        #     '--rtsp-frame-buffer-size=10000000',  # Adjust RTSP frame buffer size (if necessary)
        #     '--rtsp-tcp'  # Use RTSP over T1. CP, which might help with stability (optional)
        # )

        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg='black', highlightthickness=0)
        self.canvas.place(x=pos['x'], y=pos['y'])
        self.canvas.my_id = tag

        self.instance = vlc.Instance('--network-caching=300', '--rtsp-tcp', '--clock-jitter=0', '--sout-mux-caching=10',
                                     '--avcodec-hw=none')
        self.player = self.instance.media_player_new()
        self.player.set_hwnd(self.canvas.winfo_id())

        # (2024.07.30) Convert Video Size Button
        self.less_img = Image.open(rf'Image\less.png')
        self.more_img = Image.open(rf'Image\more.png')

        self.less_photo = ImageTk.PhotoImage(self.less_img)
        self.more_photo = ImageTk.PhotoImage(self.more_img)

        if self.width <= 640:
            self.is_default = False
            self.size_btn = tk.Button(self.root, image=self.more_photo, bg='black', bd=0, highlightthickness=0,
                                      command=self.on_click)
            self.size_btn.place(x=pos['x'] + 10, y=pos['y'] + 10, width=30, height=20)
            self.size_btn.image = self.more_photo
        else:
            self.is_default = True
            self.size_btn = tk.Button(self.root, image=self.less_photo, bg='black', bd=0, highlightthickness=0,
                                      command=self.on_click)
            self.size_btn.place(x=pos['x'] + 10, y=pos['y'] + 10, width=30, height=20)
            self.size_btn.image = self.less_photo

        self.player.play()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    #     if self.cap is None:
    #         self.cap = cv2.VideoCapture(self.rtsp_url)
    #         if not self.cap.isOpened():
    #             print("Cannot open RTSP stream")
    #             return
    #         self.running = True
    #         self.update_frame()

    # def update_frame(self):
    #     if self.running:
    #         ret, frame = self.cap.read()
    #         if ret:
    #             frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #             self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
    #             self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
    #         print(ret)
    #         self.root.after(10, self.update_frame)

    # def stop_video(self):
    #     self.running = False
    #     if self.cap is not None:
    #         self.cap.release()
    #         self.cap = None

    def __del__(self):
        try:
            if self.canvas.winfo_exists():
                self.canvas.destroy()
        except Exception as e:
            print(f"Error during destruction: {e}")

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
        if self.running:
            self.running = False
            print(f"Stopping video player for channel {self.tag}")

            if self.canvas:
                self.canvas.destroy()
                self.canvas = None

    def on_closing(self):
        self.stop_video()
        self.root.destroy()

    # (20204.07.31): convert a windows size when player was
    def on_click(self):
        try:
            if self.is_default:
                self.size_btn.config(image=self.more_photo)
                self.size_btn.image = self.more_photo
                self.alive_except_selected_ch()
            else:
                self.size_btn.config(image=self.less_photo)
                self.size_btn.image = self.less_photo
                self.destroy_except_selected_ch()

            self.is_default = not self.is_default

            if self.width == 640 and self.height == 360:
                self.width, self.height = 1280, 720
            else:
                self.width, self.height = 640, 360

            self.canvas.config(width=self.width, height=self.height)
            self.root.update_idletasks()

        except Exception as e:
            print(f"Error during on_click: {e}")

    # (2024.08.06): Destroy players except selected ch
    def destroy_except_selected_ch(self):
        videos = [Cons.video_player_ch1, Cons.video_player_ch2, Cons.video_player_ch3, Cons.video_player_ch4]
        infos = [Cons.ch1_rtsp_info, Cons.ch2_rtsp_info, Cons.ch3_rtsp_info, Cons.ch4_rtsp_info]
        channels = ['ch1', 'ch2', 'ch3', 'ch4']

        for i, channel in enumerate(channels):
            if channel != self.tag.lower():
                try:
                    videos[i].canvas.place_forget()
                    videos[i].size_btn.place_forget()
                except Exception as e:
                    print(f"Error during destroy_except_selected_ch for {channel}: {e}")
            else:
                videos[i].canvas.place(x=0, y=0)
                videos[i].size_btn.place(x=10, y=10, width=30, height=20)

    def alive_except_selected_ch(self):
        videos = [Cons.video_player_ch1, Cons.video_player_ch2, Cons.video_player_ch3, Cons.video_player_ch4]
        infos = [Cons.ch1_rtsp_info, Cons.ch2_rtsp_info, Cons.ch3_rtsp_info, Cons.ch4_rtsp_info]
        channels = ['ch1', 'ch2', 'ch3', 'ch4']

        for i, channel in enumerate(channels):
            if channel != self.tag.lower():
                try:
                    videos[i].canvas.place(x=infos[i]['x'], y=infos[i]['y'])
                    videos[i].size_btn.place(x=infos[i]['x'] + 10, y=infos[i]['y'] + 10, width=30, height=20)
                except Exception as e:
                    print(f"Error during alive_except_selected_ch for {channel}: {e}")
            else:
                videos[i].canvas.place(x=infos[i]['x'], y=infos[i]['y'])
                videos[i].size_btn.place(x=infos[i]['x'] + 10, y=infos[i]['y'] + 10, width=30, height=20)
