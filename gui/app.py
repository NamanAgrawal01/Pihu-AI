import os
import customtkinter as ctk
from PIL import Image
from gui.gui_manager import set_app
import random

class PihuApp:

    def __init__(self):
        self.root = ctk.CTk()

        self.root.title("Pihu AI")
        self.root.geometry("500x600")
        self.root.resizable(False, False)

        self.assets_path = "assets/avatar"

        # Images
        self.idle_img = self.load_image("idle.png")
        self.blink_img = self.load_image("blink.png")
        self.talk1_img = self.load_image("talk1.png")
        self.talk2_img = self.load_image("talk2.png")

        self.talking = False
        self.talk_state = False

        # Avatar
        self.label = ctk.CTkLabel(
            self.root,
            image=self.idle_img,
            text=""
        )
        self.label.pack(pady=20)

        # Status
        self.status = ctk.CTkLabel(
            self.root,
            text="🟢 Ready",
            font=("Arial", 18)
        )
        self.status.pack()

        # Register GUI globally
        set_app(self)

        # Start blinking
        self.root.after(random.randint(2000, 5000), self.blink)

    def load_image(self, filename):

        path = os.path.join(self.assets_path, filename)

        img = Image.open(path)

        return ctk.CTkImage(
            light_image=img,
            dark_image=img,
            size=(300, 300)
        )

    # -------------------
    # Blink
    # -------------------

    def blink(self):

        if self.talking:
            self.root.after(3000, self.blink)
            return

        self.label.configure(image=self.blink_img)

        self.root.after(120, self.open_eye)

    def open_eye(self):

        if not self.talking:
            self.label.configure(image=self.idle_img)

        self.root.after(3000, self.blink)

    # -------------------
    # Talking Animation
    # -------------------

    def start_talking(self):

        self.talking = True

        self.status.configure(text="🗣️ Speaking")

        self.animate_talking()

    def animate_talking(self):

        if not self.talking:
            return

        self.talk_state = not self.talk_state

        if self.talk_state:
            self.label.configure(image=self.talk1_img)
        else:
            self.label.configure(image=self.talk2_img)

        self.root.after(random.randint(70, 140), self.animate_talking)

    def stop_talking(self):

        self.talking = False

        self.label.configure(image=self.idle_img)

        self.status.configure(text="🟢 Ready")

    # -------------------

    def run(self):
        self.root.mainloop()


def start_gui():
    app = PihuApp()
    app.run()