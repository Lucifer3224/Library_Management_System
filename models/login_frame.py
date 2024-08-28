# login_frame.py
from aifc import Error
import re

import customtkinter as ctk
from tkinter import messagebox
import mysql.connector

import instance.admin_credentials
from instance.config import get_db_connection


class LoginFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color="#D133AE")  # Background color for the frame
        self.forgot_window = None

        # Instance variable to track remaining attempts
        self.remaining_attempts = 5

        # Title Label
        title_label = ctk.CTkLabel(self, text="Library Name", font=("Comic Sans MS", 24, "bold"), text_color="#FFFFFF")
        title_label.pack(pady=(20, 10))

        # Subtitle Label
        subtitle_label = ctk.CTkLabel(self, text="Unlock the world of knowledge", font=("Arial", 16),
                                      text_color="#FFFFFF")
        subtitle_label.pack(pady=(0, 20))

        # Frame for Username Label and Entry
        username_frame = ctk.CTkFrame(self, fg_color="#D133AE")
        username_frame.pack(pady=(10, 20), fill='x', padx=20)

        username_label = ctk.CTkLabel(username_frame, text="Enter your username", font=("Arial", 12),
                                      text_color="#FFFFFF")
        username_label.pack(anchor='w')  # Align to the left side

        self.username_entry = ctk.CTkEntry(username_frame, font=("Arial", 12), fg_color="#000000",
                                           border_color="#D133AE")
        self.username_entry.pack(fill='x', pady=(0, 10))

        # Frame for Password Label and Entry
        password_frame = ctk.CTkFrame(self, fg_color="#D133AE")
        password_frame.pack(pady=(10, 20), fill='x', padx=20)

        password_label = ctk.CTkLabel(password_frame, text="Enter your password", font=("Arial", 12),
                                      text_color="#FFFFFF")
        password_label.pack(anchor='w')  # Align to the left side

        self.password_entry = ctk.CTkEntry(password_frame, font=("Arial", 12), fg_color="#000000",
                                           border_color="#D133AE", show="*")
        self.password_entry.pack(fill='x', pady=(0, 10))

        # Frame for Buttons
        button_frame = ctk.CTkFrame(self, fg_color="#D133AE")
        button_frame.pack(pady=(10, 20), fill='x', padx=20)

        # Forgot Password Button
        forgot_password_button = ctk.CTkButton(button_frame, text="Forgot Password?", font=("Arial", 12),
                                               fg_color="#7289DA", text_color="#FFFFFF",
                                               command=self.forgot_password)
        forgot_password_button.pack(side="left", padx=(0, 5))

        # Login Button
        login_button = ctk.CTkButton(button_frame, text="Login", font=("Arial", 14, "bold"),
                                     fg_color="#530550", text_color="#FFFFFF",
                                     command=self.login)
        login_button.pack(side="left", padx=(5, 0), fill='x', expand=True)

        # Register Button
        register_button = ctk.CTkButton(self, text="Still on the outside looking in? Sign Up", font=("Arial", 12),
                                        fg_color="#2C2F33", text_color="#FFFFFF",
                                        command=lambda: controller.show_frame("RegisterFrame"))
        register_button.pack(pady=(10, 50))  # Increased padding to push footer down

        # Filler Label
        filler_label = ctk.CTkLabel(self, text="", fg_color="#D133AE")
        filler_label.pack(fill='both', expand=True)

        # Footer Label
        footer_label = ctk.CTkLabel(self, text="Powered by Habiba Mowafy", font=("Arial", 10), text_color="#FFFFFF")
        footer_label.pack(side=ctk.BOTTOM, pady=(10, 20))

    def forgot_password(self):
        # Make forgot_window an instance attribute
        self.forgot_window = ctk.CTkToplevel(self)
        self.forgot_window.title("Forgot Password")
        self.forgot_window.geometry("350x350")
        self.forgot_window.resizable(False, False)
        self.forgot_window.configure(fg_color="#A64FD1")  # Match the main frame's background color

        # Ensure the window stays on top
        self.forgot_window.attributes("-topmost", True)

        # Center the window on the screen
        window_width = 350
        window_height = 350
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))
        self.forgot_window.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

        # Title Label
        title_label = ctk.CTkLabel(self.forgot_window, text="Password Recovery",
                                   font=("Comic Sans MS", 20, "bold"), text_color="#FFFFFF")
        title_label.pack(pady=(20, 30))

        # Email Entry
        email_frame = ctk.CTkFrame(self.forgot_window, fg_color="#A64FD1")
        email_frame.pack(pady=(0, 20), padx=40, fill='x')

        email_label = ctk.CTkLabel(email_frame, text="Enter your email",
                                   font=("Arial", 12), text_color="#FFFFFF")
        email_label.pack(anchor='w')

        email_entry = ctk.CTkEntry(email_frame, font=("Arial", 12),
                                   fg_color="#000000", border_color="#A64FD1")
        email_entry.pack(fill='x', pady=(5, 0))

        # New Password Entry
        new_password_frame = ctk.CTkFrame(self.forgot_window, fg_color="#A64FD1")
        new_password_frame.pack(pady=(0, 20), padx=40, fill='x')

        new_password_label = ctk.CTkLabel(new_password_frame, text="Enter new password",
                                          font=("Arial", 12), text_color="#FFFFFF")
        new_password_label.pack(anchor='w')

        new_password_entry = ctk.CTkEntry(new_password_frame, font=("Arial", 12),
                                          fg_color="#000000", border_color="#A64FD1", show="*")
        new_password_entry.pack(fill='x', pady=(5, 0))

        # Update Password Button
        update_button = ctk.CTkButton(self.forgot_window, text="Update Password",
                                      font=("Arial", 14, "bold"),
                                      fg_color="#530550", text_color="#FFFFFF",
                                      command=lambda: self.update_password(email_entry.get(), new_password_entry.get()))
        update_button.pack(pady=(20, 0), padx=40, fill='x')

        # Footer Label
        footer_label = ctk.CTkLabel(self.forgot_window, text="Powered by Habiba Mowafy",
                                    font=("Arial", 10), text_color="#FFFFFF")
        footer_label.pack(side=ctk.BOTTOM, pady=(10, 20))

    def validate_email(self, email):
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(email_pattern, email)

    def validate_password(self, password):
        password_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
        return re.match(password_pattern, password)

    def update_password(self, email, new_password):
        if not email or not new_password:
            messagebox.showerror("Error", "All fields are required.", parent=self.forgot_window)
            return

        if not self.validate_email(email):
            messagebox.showerror("Email Error", "Invalid email format. Please use 'example@gmail.com'.",
                                 parent=self.forgot_window)
            return

        if not self.validate_password(new_password):
            messagebox.showerror("Password Error",
                                 "Password must be at least 8 characters long\n"
                                 "Contain at least:\n"
                                 "\tOne uppercase letter\n"
                                 "\tOne lowercase letter\n"
                                 "\tOne digit\n"
                                 "\tOne special character (@$!%*?&)", parent=self.forgot_window)
            return
        try:
            conn = get_db_connection()

            if conn.is_connected():
                cursor = conn.cursor()

                # Check if the new password already exists
                check_password_query = "SELECT 1 FROM readers WHERE pass = %s LIMIT 1"
                cursor.execute(check_password_query, (new_password,))
                password_exists = cursor.fetchone()

                if password_exists:
                    messagebox.showerror("Error",
                                         "This password is already used by another user. Please choose a different password.",
                                         parent=self.forgot_window)
                    return

                update_query = "UPDATE readers SET pass = %s WHERE email = %s"

                cursor.execute(update_query, (new_password, email))

                conn.commit()

                if cursor.rowcount > 0:
                    messagebox.showinfo("Success", "Password updated successfully!", parent=self.forgot_window)
                else:
                    messagebox.showerror("Error", "Email not found. Please check the email entered.",
                                         parent=self.forgot_window)

        except Error as e:
            # Handle connection or query errors
            messagebox.showerror("Error", f"Error updating password: {str(e)}", parent=self.forgot_window)

        finally:
            cursor.close()
            conn.close()

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "All fields are required.")
            return

        # Admin login check
        admin_username = instance.admin_credentials.ADMIN_USERNAME
        print(admin_username)
        admin_password = instance.admin_credentials.ADMIN_PASSWORD
        print(admin_password)

        if username == admin_username:
            print("Admin")
            if password == admin_password:
                messagebox.showinfo("Welcome", "Welcome, Admin!")
                self.remaining_attempts = 5  # Reset attempts on successful login
                return
            else:
                self.remaining_attempts -= 1
                if self.remaining_attempts > 0:
                    messagebox.showwarning("Error",
                                           f"Invalid password. Attempts Remaining: {self.remaining_attempts}")
                    self.password_entry.delete(0, 'end')
                    return
                else:
                    messagebox.showerror("Error", "Account locked due to too many failed attempts.")
                    return

        conn = get_db_connection()
        if conn is None:
            messagebox.showerror("Error", "Cannot connect to the database.")
            return

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT pass FROM readers WHERE user_name = %s", (username,))
            result = cursor.fetchone()

            if result is None:
                messagebox.showerror("Error", "Username doesn't exist.")
            else:
                stored_password = result[0]

                if stored_password == password:
                    #messagebox.showinfo("Welcome", f"Welcome {username}!")
                    self.remaining_attempts = 5  # Reset attempts on successful login

                    # Set the username in the controller for later use
                    self.controller.login_success(username)
                else:
                    self.remaining_attempts -= 1
                    if self.remaining_attempts > 0:
                        messagebox.showwarning("Error",
                                               f"Invalid password. Attempts Remaining: {self.remaining_attempts}")
                        self.password_entry.delete(0, 'end')
                    else:
                        messagebox.showerror("Error", "Account locked due to too many failed attempts.")
                        # self.remaining_attempts = 5  # Optionally reset attempts on lockout
                        # Additional lockout logic can go here

        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Database error occurred: {str(e)}")
        finally:
            cursor.close()
            conn.close()
