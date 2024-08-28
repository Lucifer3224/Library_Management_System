# register_frame.py

import re

import customtkinter as ctk
from tkinter import messagebox
import mysql
from instance.config import get_db_connection


class RegisterFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color="#D133AE")  # Background color for the frame

        # Title Label
        title_label = ctk.CTkLabel(self, text="Library Name", font=("Comic Sans MS", 24, "bold"), text_color="#FFFFFF")
        title_label.pack(pady=(20, 10))

        # Subtitle Label
        subtitle_label = ctk.CTkLabel(self, text="Embark on your journey of knowledge!", font=("Arial", 16),
                                      text_color="#FFFFFF")
        subtitle_label.pack(pady=(0, 20))

        # Frame for all input fields
        input_frame = ctk.CTkFrame(self, fg_color="#D133AE")
        input_frame.pack(pady=(10, 20), fill='x', padx=20)

        # Full-width entries
        self.create_entry(input_frame, "First Name")
        self.create_entry(input_frame, "Last Name")
        self.create_entry(input_frame, "Email")

        # Username and Age
        username_age_frame = ctk.CTkFrame(input_frame, fg_color="#D133AE")
        username_age_frame.pack(pady=(0, 10), fill='x')
        self.create_left_entry(username_age_frame, "Username", 0.7)
        self.create_right_entry(username_age_frame, "Age", 0.3)

        # Password and Confirm Password
        password_frame = ctk.CTkFrame(input_frame, fg_color="#D133AE")
        password_frame.pack(pady=(0, 10), fill='x')
        self.create_left_entry(password_frame, "Password", 0.5, show="*")
        self.create_right_entry(password_frame, "Confirm Password", 0.5, show="*")

        # Frame for Buttons
        button_frame = ctk.CTkFrame(self, fg_color="#D133AE")
        button_frame.pack(pady=(10, 20), fill='x', padx=20)

        # Register Button
        register_button = ctk.CTkButton(button_frame, text="Register", font=("Arial", 14, "bold"),
                                        fg_color="#530550", text_color="#FFFFFF",
                                        command=self.register)
        register_button.pack(side="left", padx=(5, 0), fill='x', expand=True)

        # Login Button
        login_button = ctk.CTkButton(button_frame, text="Already a member? Log In", font=("Arial", 12),
                                     fg_color="#2C2F33", text_color="#FFFFFF",
                                     command=lambda: controller.show_frame("LoginFrame"))
        login_button.pack(side="left", padx=(5, 0), fill='x', expand=True)

        # Filler Label
        filler_label = ctk.CTkLabel(self, text="", fg_color="#D133AE")
        filler_label.pack(fill='both', expand=True)

        # Footer Label
        footer_label = ctk.CTkLabel(self, text="Powered by Habiba Mowafy", font=("Arial", 10), text_color="#FFFFFF")
        footer_label.pack(side=ctk.BOTTOM, pady=(10, 20))

    def create_entry(self, parent, label_text):
        frame = ctk.CTkFrame(parent, fg_color="#D133AE")
        frame.pack(pady=(0, 10), fill='x')
        ctk.CTkLabel(frame, text=label_text, font=("Arial", 12), text_color="#FFFFFF", anchor="w").pack(fill='x')
        entry = ctk.CTkEntry(frame, font=("Arial", 12), fg_color="#000000")
        entry.pack(fill='x')
        setattr(self, f"{label_text.lower().replace(' ', '_')}_entry", entry)

    def create_left_entry(self, parent, label_text, width_ratio, show=None):
        frame = ctk.CTkFrame(parent, fg_color="#D133AE")
        frame.pack(side="left", fill='x', expand=True, anchor="w")
        ctk.CTkLabel(frame, text=label_text, font=("Arial", 12), text_color="#FFFFFF", anchor="w").pack(fill='x')
        entry = ctk.CTkEntry(frame, font=("Arial", 12), fg_color="#000000", show=show)
        entry.pack(fill='x')
        frame.configure(width=int(parent.winfo_reqwidth() * width_ratio))
        setattr(self, f"{label_text.lower().replace(' ', '_')}_entry", entry)

    def create_right_entry(self, parent, label_text, width_ratio, show=None):
        frame = ctk.CTkFrame(parent, fg_color="#D133AE")
        frame.pack(side="right", fill='x', expand=True, anchor="e")
        ctk.CTkLabel(frame, text=label_text, font=("Arial", 12), text_color="#FFFFFF", anchor="w").pack(fill='x')
        entry = ctk.CTkEntry(frame, font=("Arial", 12), fg_color="#000000", show=show)
        entry.pack(fill='x')
        frame.configure(width=int(parent.winfo_reqwidth() * width_ratio))
        setattr(self, f"{label_text.lower().replace(' ', '_')}_entry", entry)

    def validate_email(self, email):
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(email_pattern, email)

    def validate_password(self, password):
        password_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
        return re.match(password_pattern, password)

    def register(self):
        first_name = self.first_name_entry.get().strip()
        last_name = self.last_name_entry.get().strip()
        username = self.username_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm_password = self.confirm_password_entry.get().strip()
        age = self.age_entry.get().strip()

        if not first_name or not last_name or not email or not username or not password or not confirm_password or not age:
            messagebox.showerror("Error", "All fields are required.")
            return

        if not first_name.isalpha() or not last_name.isalpha():
            messagebox.showerror("Name Error", "Name can only have characters.")
            return

        if not self.validate_email(email):
            messagebox.showerror("Email Error", "Invalid email format. Please use 'example@gmail.com'.")
            return

        try:
            age = int(age)
        except ValueError:
            messagebox.showerror("Age Error", "Age must be an integer.")
            return

        if age < 0 or age > 100:
            messagebox.showerror("Age Error", "Age must be between 0 and 100.")
            return

        if not self.validate_password(password):
            messagebox.showerror("Password Error",
                                 "Password must be at least 8 characters long\n"
                                 "Contain at least:\n"
                                 "\tOne uppercase letter\n"
                                 "\tOne lowercase letter\n"
                                 "\tOne digit\n"
                                 "\tOne special character (@$!%*?&)")
            return

        if len(password) < 8:
            messagebox.showerror("Password Error", "Password must be at least 8 characters.")
            return

        if password != confirm_password:
            messagebox.showerror("Password Error", "Passwords do not match.")
            return

        conn = get_db_connection()
        if conn is None:
            messagebox.showerror("Error", "Cannot connect to the database.")
            return

        try:
            cursor = conn.cursor()
            # Check if the password already exists
            check_password_query = "SELECT 1 FROM readers WHERE pass = %s LIMIT 1"
            cursor.execute(check_password_query, (password,))
            password_exists = cursor.fetchone()

            if password_exists:
                messagebox.showerror("Error", "This password is already used by another user. Please choose a different password.")
                return

            cursor.execute("SELECT user_name FROM readers WHERE user_name = %s", (username,))
            if cursor.fetchone():
                messagebox.showerror("Error", "Username already exists.")
            else:
                cursor.execute(
                    "INSERT INTO readers (first_name, last_name, email, user_name, pass, age) VALUES (%s, %s, %s, %s, %s, %s)",
                    (first_name, last_name, email, username, password, age)
                )
                conn.commit()
                messagebox.showinfo("Success", "Registration successful.")
                self.controller.show_frame("LoginFrame")

        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Database error occurred: {str(e)}")
        finally:
            cursor.close()
            conn.close()
