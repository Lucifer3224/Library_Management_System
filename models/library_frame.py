import customtkinter as ctk
from tkinter import messagebox, filedialog
import os
import pygame
from PIL import Image
import mysql.connector
from instance.config import get_db_connection
import time


class LibraryFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color="#FFFFFF")

        self.username = self.controller.username
        print(f"Username set in LibraryFrame: {self.username}")  # Debug print

        self.welcome_label = ctk.CTkLabel(self, text=f"Welcome, {self.username}!", font=("Arial", 24, "bold"),
                                          text_color="#A978DD", fg_color="#FFFFFF")
        self.welcome_label.pack(pady=20)

        self.all_books = []
        self.sound_books = []
        self.load_books()
        self.load_sound_books()
        self.load_categories()

        self.sidebar = self.create_sidebar()
        self.sidebar.pack(side="left", fill="y")

        self.main_content = ctk.CTkFrame(self, fg_color="#A978DD")
        self.main_content.pack(side="right", fill="both", expand=True)

        self.create_top_bar()
        self.create_discover_section()

        self.current_section = "discover"

        # Initialize pygame mixer for audio playback
        pygame.mixer.init()

    def load_books(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM books")
            self.all_books = cursor.fetchall()
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error loading books: {err}")
            self.all_books = []

    def load_sound_books(self):
        sound_books_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Data", "Audio"))
        self.sound_books = []
        for filename in os.listdir(sound_books_dir):
            if filename.endswith(".mp3"):
                book_title = os.path.splitext(filename)[0]
                self.sound_books.append({
                    "title": book_title,
                    "path": os.path.join(sound_books_dir, filename)
                })

    def load_categories(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT genre FROM books")
            self.categories = ["All Categories"] + [category[0] for category in cursor.fetchall()]
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error loading categories: {err}")
            self.categories = ["All Categories"]

    def display_books(self, books):
        for widget in self.books_frame.winfo_children():
            widget.destroy()

        row_frame = None
        for i, book in enumerate(books):
            if i % 3 == 0:
                row_frame = ctk.CTkFrame(self.books_frame, fg_color="#A978DD")
                row_frame.pack(fill="x", pady=10)

            book_frame = ctk.CTkFrame(row_frame, width=200, height=350, fg_color="#FFFFFF")
            book_frame.pack(side="left", padx=10)
            book_frame.pack_propagate(False)

            cover_path = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", "Data", "Covers", f"{book['title']}.png"))
            if os.path.exists(cover_path):
                cover_image = Image.open(cover_path)
                cover_image = cover_image.resize((180, 240))
                cover_photo = ctk.CTkImage(cover_image, size=(180, 240))
                cover_label = ctk.CTkLabel(book_frame, image=cover_photo, text="")
                cover_label.pack(pady=(5, 0))
            else:
                title_label = ctk.CTkLabel(book_frame, text=book["title"], wraplength=180, font=("Arial", 12, "bold"),
                                           text_color="#A978DD")
                title_label.pack(pady=(5, 0))

            author_label = ctk.CTkLabel(book_frame, text=book['author'], font=("Arial", 10), text_color="#A978DD")
            author_label.pack()

            details_button = ctk.CTkButton(book_frame, text="Details", command=lambda b=book: self.show_book_details(b),
                                           fg_color="#7A0683")
            details_button.pack(pady=(5, 0))

            start_reading_button = ctk.CTkButton(book_frame, text="Start Reading",
                                                 command=lambda b=book: self.start_reading(b), fg_color="#7A0683")
            start_reading_button.pack(pady=(5, 0))

    def start_reading(self, book):
        pdf_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "Data", "Books", f"{book['title']}.pdf")
        )
        print(f"Attempting to open: {pdf_path}")  # Debug print
        if os.path.exists(pdf_path):
            os.startfile(pdf_path)
        else:
            messagebox.showerror("Error", f"PDF file for {book['title']} not found at {pdf_path}.")

    def select_pdf(self):
        self.pdf_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])

    def show_book_details(self, book):
        details_window = ctk.CTkToplevel(self)
        details_window.title(book['title'])
        details_window.geometry("400x600")
        details_window.attributes('-topmost', 1)
        details_window.configure(fg_color="#7A0683")

        scroll_frame = ctk.CTkScrollableFrame(details_window)
        scroll_frame.pack(fill="both", expand=True)

        ctk.CTkLabel(scroll_frame, text=book['title'], font=("Arial", 16, "bold")).pack(pady=(10, 5))
        ctk.CTkLabel(scroll_frame, text=f"By: {book['author']}", font=("Arial", 14)).pack(pady=5)
        ctk.CTkLabel(scroll_frame, text=f"Genre: {book['genre']}").pack(pady=2)
        ctk.CTkLabel(scroll_frame, text=f"ISBN: {book['isbn']}").pack(pady=2)
        ctk.CTkLabel(scroll_frame, text=f"Published: {book['publication_year']}").pack(pady=2)
        ctk.CTkLabel(scroll_frame, text=f"Language: {book['lang']}").pack(pady=2)
        ctk.CTkLabel(scroll_frame, text=f"Pages: {book['pages']}").pack(pady=2)
        ctk.CTkLabel(scroll_frame, text=f"Added to library: {book['date_added']}").pack(pady=2)

        ctk.CTkLabel(scroll_frame, text="Summary:", font=("Arial", 12, "bold")).pack(pady=(10, 5))
        ctk.CTkLabel(scroll_frame, text=book['summary'], wraplength=350).pack(pady=5)

        button_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        button_frame.pack(pady=10)

        add_button = ctk.CTkButton(button_frame, text="Add to My Library",
                                   command=lambda: self.toggle_library(book, add_button, remove_button))
        add_button.pack(side="left", padx=5)

        remove_button = ctk.CTkButton(button_frame, text="Remove from My Library",
                                      command=lambda: self.toggle_library(book, add_button, remove_button))
        remove_button.pack(side="left", padx=5)

        self.update_library_buttons(add_button, remove_button, book)

        # Add hover tooltips
        self.add_tooltip(add_button, "Add this book to your library")
        self.add_tooltip(remove_button, "Remove this book from your library")

    def update_library_buttons(self, add_button, remove_button, book):
        user_name = self.controller.username
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            # Check if the book is in the user's library
            cursor.execute("SELECT * FROM readers_books WHERE user_name = %s AND isbn = %s",
                           (user_name, book['isbn']))
            is_in_library = cursor.fetchone() is not None
            cursor.close()
            conn.close()

            if is_in_library:
                add_button.configure(state="disabled", fg_color="gray")
                remove_button.configure(state="normal", fg_color="#A978DD")
            else:
                add_button.configure(state="normal", fg_color="#A978DD")
                remove_button.configure(state="disabled", fg_color="gray")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error checking book status: {err}")

    def toggle_library(self, book, add_button, remove_button):
        user_name = self.controller.username
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Check if the book is already in the library
            cursor.execute("SELECT * FROM readers_books WHERE user_name = %s AND isbn = %s",
                           (user_name, book['isbn']))
            is_in_library = cursor.fetchone() is not None

            if is_in_library:
                # Remove the book from the library
                cursor.execute("DELETE FROM readers_books WHERE user_name = %s AND isbn = %s",
                               (user_name, book['isbn']))
                messagebox.showinfo("Success", f"{book['title']} has been removed from your library.")
            else:
                # Add the book to the library
                cursor.execute("INSERT INTO readers_books (user_name, isbn) VALUES (%s, %s)",
                               (user_name, book['isbn']))
                messagebox.showinfo("Success", f"{book['title']} has been added to your library.")

            conn.commit()
            cursor.close()
            conn.close()

            # Update button states
            self.update_library_buttons(add_button, remove_button, book)

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error updating library: {err}")

    def add_tooltip(self, widget, text):
        tooltip = ctk.CTkToolTip(widget, message=text)
        widget.tooltip = tooltip  #

    def add_to_library(self, book):
        user_name = self.controller.username
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            # Add the book to the user's library
            cursor.execute("INSERT INTO readers_books (user_name, isbn) VALUES (%s, %s)",
                           (user_name, book['isbn']))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Success", f"{book['title']} has been added to your library.")
            self.show_book_details(book)  # Refresh the details window
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error adding book to library: {err}")

    def remove_from_library(self, book):
        user_name = self.controller.username
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            # Remove the book from the user's library
            cursor.execute("DELETE FROM readers_books WHERE user_name = %s AND isbn = %s",
                           (user_name, book['isbn']))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Success", f"{book['title']} has been removed from your library.")
            self.show_book_details(book)  # Refresh the details window
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error removing book from library: {err}")

    def display_categories(self):
        for widget in self.books_frame.winfo_children():
            widget.destroy()

        row_frame = None
        for i, category in enumerate(self.categories[1:]):  # Skip "All Categories"
            if i % 3 == 0:
                row_frame = ctk.CTkFrame(self.books_frame, fg_color="#A978DD")
                row_frame.pack(fill="x", pady=10)

            category_frame = ctk.CTkFrame(row_frame, width=200, height=320, fg_color="#FFFFFF")
            category_frame.pack(side="left", padx=10)
            category_frame.pack_propagate(False)

            cover_path = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", "Data", "Categories", f"{category}.png"))
            if os.path.exists(cover_path):
                cover_image = Image.open(cover_path)
                cover_image = cover_image.resize((180, 240))
                cover_photo = ctk.CTkImage(cover_image, size=(180, 240))
                cover_label = ctk.CTkLabel(category_frame, image=cover_photo, text="")
                cover_label.pack(pady=(5, 0))
            else:
                placeholder_label = ctk.CTkLabel(category_frame, text=category, wraplength=180,
                                                 font=("Arial", 16, "bold"))
                placeholder_label.pack(expand=True)

            category_label = ctk.CTkLabel(category_frame, text=category, font=("Arial", 12, "bold"),
                                          text_color="#A978DD")
            category_label.pack(pady=5)

            view_button = ctk.CTkButton(category_frame, text="View Books",
                                        command=lambda c=category: self.show_category_books(c), fg_color="#7A0683")
            view_button.pack(pady=(0, 10))

            category_frame.bind("<Button-1>", lambda e, c=category: self.show_category_books(c))

    def display_sound_books(self):
        for widget in self.books_frame.winfo_children():
            widget.destroy()

        for book in self.sound_books:
            book_frame = ctk.CTkFrame(self.books_frame, fg_color="#FFFFFF")
            book_frame.pack(fill="x", padx=10, pady=5)

            title_label = ctk.CTkLabel(book_frame, text=book['title'], font=("Arial", 14, "bold"),
                                       text_color="#A978DD")
            title_label.pack(side="left", padx=10)

            play_button = ctk.CTkButton(book_frame, text="Play Audio", command=lambda b=book: self.play_audio(b),
                                        fg_color="#7A0683")
            play_button.pack(side="right", padx=5)

    def play_audio(self, book):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()

        pygame.mixer.music.load(book['path'])
        pygame.mixer.music.play()

        audio_player = ctk.CTkToplevel(self)
        audio_player.title(f"Now Playing: {book['title']}")
        audio_player.geometry("400x200")

        title_label = ctk.CTkLabel(audio_player, text=book['title'], font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        progress_bar = ctk.CTkProgressBar(audio_player, width=300)
        progress_bar.pack(pady=10)

        time_label = ctk.CTkLabel(audio_player, text="0:00 / 0:00")
        time_label.pack(pady=5)

        def update_progress():
            if pygame.mixer.music.get_busy():
                current_time = pygame.mixer.music.get_pos() / 1000
                total_time = pygame.mixer.Sound(book['path']).get_length()
                progress = current_time / total_time
                progress_bar.set(progress)
                time_label.configure(
                    text=f"{time.strftime('%M:%S', time.gmtime(current_time))} / {time.strftime('%M:%S', time.gmtime(total_time))}")
                audio_player.after(1000, update_progress)
            else:
                audio_player.destroy()

        update_progress()

        pause_resume_button = ctk.CTkButton(audio_player, text="Pause", command=self.toggle_pause)
        pause_resume_button.pack(side="left", padx=10)

        stop_button = ctk.CTkButton(audio_player, text="Stop", command=self.stop_audio)
        stop_button.pack(side="right", padx=10)

    def toggle_pause(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

    def stop_audio(self):
        pygame.mixer.music.stop()

    def create_sidebar(self):
        sidebar = ctk.CTkFrame(self, fg_color="#FFFFFF", width=200)

        logo_label = ctk.CTkLabel(sidebar, text="THE BOOKS", font=("Arial", 20, "bold"), text_color="#A978DD")
        logo_label.pack(pady=(20, 30))

        menu_items = [
            ("Discover", self.show_discover),
            ("Sound Books", self.show_sound_books),
            ("My Library", self.show_my_library),
            ("Profile", self.show_profile),
            ("Category", self.show_categories),
            ("Setting", self.show_settings),
            ("Help", self.show_help),
            ("Log out", self.logout)
        ]

        for item, command in menu_items:
            btn = ctk.CTkButton(sidebar, text=item, fg_color="transparent",
                                text_color="#333333", hover_color="#A978DD", anchor="w", command=command)
            btn.pack(pady=5, padx=10, fill="x")

        footer_label = ctk.CTkLabel(sidebar, text="Powered by Habiba Mowafy", font=("Arial", 10), text_color="#A978DD")
        footer_label.pack(side="bottom", pady=20)

        return sidebar

    def create_top_bar(self):
        top_bar = ctk.CTkFrame(self.main_content, fg_color="#A978DD", height=50)
        top_bar.pack(fill="x", pady=(10, 20))

        self.refresh_btn = ctk.CTkButton(top_bar, text="Refresh", fg_color="#EEEEEE",
                                         text_color="#333333", command=self.refresh_library, hover_color="#7A0683")
        self.refresh_btn.pack(side="right", padx=20)

    def create_discover_section(self):
        discover_frame = ctk.CTkFrame(self.main_content, fg_color="#A978DD")
        discover_frame.pack(fill="x", padx=20, pady=10)

        title = ctk.CTkLabel(discover_frame, text="Discover", font=("Arial", 24, "bold"))
        title.pack(anchor="w")

        search_frame = ctk.CTkFrame(discover_frame, fg_color="#A978DD")
        search_frame.pack(fill="x", pady=(10, 20))

        self.category_var = ctk.StringVar(value="All Categories")
        self.category_dropdown = ctk.CTkOptionMenu(search_frame,
                                                   values=self.categories,
                                                   variable=self.category_var,
                                                   command=self.on_category_change,
                                                   fg_color="#7A0683", button_color="#7A0683",
                                                   button_hover_color="#6A0573",
                                                   dropdown_fg_color="#7A0683", dropdown_hover_color="#6A0573",
                                                   text_color="#FFFFFF")
        self.category_dropdown.pack(side="left")

        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="Find the book you like...")
        self.search_entry.pack(side="left", expand=True, fill="x", padx=(10, 10))

        self.search_entry.bind("<KeyRelease>", self.filter_books)

        search_button = ctk.CTkButton(search_frame, text="Search", fg_color="#EEEEEE",
                                      text_color="#000000", command=self.search_books, hover_color="#7A0683")
        search_button.pack(side="right")

        self.books_frame = ctk.CTkScrollableFrame(self.main_content, fg_color="#A978DD")
        self.books_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.display_books(self.all_books)

    def on_category_change(self, choice):
        if choice == "All Categories":
            self.display_books(self.all_books)
        else:
            category_books = [book for book in self.all_books if book['genre'] == choice]
            self.display_books(category_books)

    def refresh_library(self):
        self.load_books()
        self.load_sound_books()
        self.load_categories()
        self.category_dropdown.configure(values=self.categories)
        if self.current_section == "discover":
            self.display_books(self.all_books)
        elif self.current_section == "sound_books":
            self.display_sound_books()
        elif self.current_section == "my_library":
            self.show_my_library()
        messagebox.showinfo("Refresh", "Library has been refreshed with the latest data.")

    def filter_books(self, event=None):
        search_term = self.search_entry.get().lower()
        if self.current_section == "discover":
            filtered_books = [book for book in self.all_books if search_term in book["title"].lower()]
            self.display_books(filtered_books)
        elif self.current_section == "sound_books":
            filtered_books = [book for book in self.sound_books if search_term in book["title"].lower()]
            self.display_sound_books(filtered_books)
        elif self.current_section == "my_library":
            user_books = self.get_user_books()
            filtered_books = [book for book in user_books if search_term in book["title"].lower()]
            self.display_books(filtered_books)

    def search_books(self):
        self.filter_books()

    def show_discover(self):
        self.current_section = "discover"
        self.update_main_content("Discover", lambda: self.display_books(self.all_books))

    def show_sound_books(self):
        self.current_section = "sound_books"
        self.update_main_content("Sound Books", self.display_sound_books)

    def show_categories(self):
        self.update_main_content("Categories", self.display_categories)

    def show_category_books(self, category):
        category_books = [book for book in self.all_books if book['genre'] == category]
        self.update_main_content(f"Category: {category}", lambda: self.display_books(category_books))

    def show_my_library(self):
        self.current_section = "my_library"
        user_books = self.get_user_books()
        print(f"User books: {user_books}")  # Debug print
        if not user_books:
            messagebox.showinfo("My Library", "Your library is empty.")
        self.update_main_content("My Library", lambda: self.display_books(user_books))

    def show_profile(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM readers WHERE user_name = %s"
            cursor.execute(query, (self.username,))
            user_data = cursor.fetchone()
            cursor.close()
            conn.close()

            if user_data:
                profile_window = ctk.CTkToplevel(self)
                profile_window.title("User Profile")
                profile_window.geometry("400x300")
                profile_window.configure(fg_color="#7A0683")

                profile_window.attributes("-topmost", True)

                ctk.CTkLabel(profile_window, text="User Profile", font=("Arial", 20, "bold")).pack(pady=20)
                ctk.CTkLabel(profile_window, text=f"Username: {user_data['user_name']}").pack(pady=5)
                ctk.CTkLabel(profile_window, text=f"Email: {user_data['email']}").pack(pady=5)
                ctk.CTkLabel(profile_window, text=f"First Name: {user_data['first_name']}").pack(pady=5)
                ctk.CTkLabel(profile_window, text=f"Last Name: {user_data['last_name']}").pack(pady=5)
                ctk.CTkLabel(profile_window, text=f"age: {user_data['age']}").pack(pady=5)
            else:
                messagebox.showerror("Error", "User data not found.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error fetching user profile: {err}")

    def show_settings(self):
        messagebox.showinfo("Settings", "Showing application settings")

    def show_help(self):
        messagebox.showinfo("Help", "Showing help and support information")

    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to log out?"):
            self.controller.show_frame("LoginFrame")

    def get_user_books(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            query = """
            SELECT b.* 
            FROM books b
            JOIN readers_books rb ON b.isbn = rb.isbn
            WHERE rb.user_name = %s
            """
            cursor.execute(query, (self.username,))
            user_books = cursor.fetchall()
            cursor.close()
            conn.close()
            print(f"SQL Query: {query}")  # Debug print
            print(f"Username: {self.username}")  # Debug print
            print(f"Fetched books: {user_books}")  # Debug print
            return user_books
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error fetching your library: {err}")
            print(f"Database error: {err}")  # Debug print
            return []

    def update_main_content(self, title, content_function):
        # Update title
        self.main_content.winfo_children()[0].winfo_children()[0].configure(text=title)

        # Clear and update content
        for widget in self.books_frame.winfo_children():
            widget.destroy()
        content_function()
