import os
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk

from models.login_frame import LoginFrame
from models.register_frame import RegisterFrame
from models.library_frame import LibraryFrame


class LibraryApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Library Management System")
        width = 1000
        height = 667
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 4) - (height // 4)
        self.geometry(f'{width}x{height}+{x}+{y}')
        self.configure(fg_color="#D133AE")  # Background color

        # Initialize the username attribute
        self.username = None

        base_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(base_dir, "static", "Logo.ico")
        self.iconbitmap(icon_path)
        self.resizable(False, False)

        # Create a Canvas for the background image
        self.canvas = ctk.CTkCanvas(self, width=width, height=height, bg="#D133AE", bd=0, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Load and display the background image using Pillow
        bg_image_path = os.path.join(base_dir, "static", "Background.png")
        try:
            pil_image = Image.open(bg_image_path)
            self.bg_image = ImageTk.PhotoImage(pil_image)
            self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load background image: {e}")
            print(f"Error loading image: {e}")

        # Create containers for different frame types
        self.login_register_container = ctk.CTkFrame(self.canvas, width=width, height=height, fg_color="#D133AE")
        self.canvas.create_window((580, 70), window=self.login_register_container, anchor="nw")

        self.library_container = ctk.CTkFrame(self, width=width, height=height)
        self.library_container.place(x=0, y=0, relwidth=1, relheight=1)
        self.library_container.lower()

        self.frames = {}

        # Add Login and Register frames to login_register_container
        for F in (LoginFrame, RegisterFrame):
            page_name = F.__name__
            frame = F(parent=self.login_register_container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Initialize library_frame as None
        self.library_frame = None

        self.show_frame("LoginFrame")

    def show_frame(self, page_name):
        if page_name in self.frames:
            self.library_container.lower()
            self.login_register_container.lift()
            frame = self.frames[page_name]
            frame.tkraise()
        elif page_name == "LibraryFrame":
            if self.library_frame is None:
                # Create LibraryFrame only when needed
                self.library_frame = LibraryFrame(parent=self.library_container, controller=self)
                self.library_frame.place(x=0, y=0, relwidth=1, relheight=1)
            self.login_register_container.lower()
            self.library_container.lift()
            self.library_frame.tkraise()

    def login_success(self, username):
        self.username = username
        print(f"Username set in main app: {self.username}")  # Debug print
        self.show_frame("LibraryFrame")


if __name__ == "__main__":
    app = LibraryApp()
    app.mainloop()
