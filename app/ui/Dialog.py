from tkinter import *

from app.config import Constant as Cons


class DialogBox(Toplevel):

    def __init__(self, master, noti_text):
        super().__init__(master)

        # self.geometry('400x300')
        self.geometry(f'{Cons.POPUP_SIZE["x"]}x{Cons.POPUP_SIZE["y"]}+'
                      f'{Cons.POPUP_POSITION["x"]}+{Cons.POPUP_POSITION["y"]}')
        self.title('Notification')
        self.create_widgets(noti_text)
        self.configure(bg=Cons.my_color['noti_bg'])

    def create_widgets(self, txt):
        self.grab_set()
        # Notification Text
        self.noti_lbl = Label(self)
        self.noti_lbl.configure(text=txt, font=(None, 24),
                                bg=Cons.my_color['noti_bg'], fg=Cons.my_color['noti_txt'])
        self.noti_lbl.place(x=(Cons.POPUP_SIZE['x'] - self.noti_lbl.winfo_width()) / 2,
                            y=(Cons.POPUP_SIZE['y'] - self.noti_lbl.winfo_height()) / 2)
        # `place()` uses the widget's top-left corner, so center it after layout.
        # The label size is not final until Tk has processed geometry updates.
        # Call `update()` once, then reposition using the measured size.
        self.update()
        self.noti_lbl.place(x=self.noti_lbl.winfo_x() - self.noti_lbl.winfo_width() / 2,
                            y=self.noti_lbl.winfo_y() - self.noti_lbl.winfo_height() / 2)

        # Button
        self.button_quit = Button(self)
        self.button_quit.configure(text="Close",
                                   command=self.quit_window)
        self.button_quit.place(x=Cons.POPUP_SIZE['x'] / 2 - 50,
                               y=Cons.POPUP_SIZE['y'] / 2 + 60)

    def quit_window(self):
        self.destroy()

