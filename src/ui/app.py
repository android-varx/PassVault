import customtkinter
import os
from .login import LoginFrame
from .home import HomeFrame
from .add import AddFrame
from .view import ViewFrame
from ..database import DatabaseManager
from ..crypto import CryptoManager
from tkinter import messagebox

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("PassVault - Secure & Private")
        self.geometry("800x600")
        self.center_window()

        # State
        self.db = DatabaseManager()
        self.crypto = None # Initialized after login
        
        # Container for frames
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        self.current_frame = None

        # Start with Login
        self.show_login()

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def show_login(self):
        self.clear_frames()
        self.current_frame = LoginFrame(self, self.on_login_attempt)
        self.current_frame.grid(row=0, column=0, sticky="nsew")

    def on_login_attempt(self, master_password):
        try:
            # 1. Derive Key
            temp_crypto = CryptoManager(master_password)
            
            # 2. Check for Verification Token in DB
            stored_token = self.db.get_config("verification_token")
            
            if stored_token:
                # 3a. Verify: Try to decrypt
                try:
                    decrypted = temp_crypto.decrypt(stored_token)
                    if decrypted == "valid":
                        # Success!
                        self.crypto = temp_crypto
                        self.show_home()
                    else:
                        raise ValueError("Invalid Token")
                except Exception:
                    messagebox.showerror("Access Denied", "Incorrect Master Password.")
            else:
                # 3b. First Run / Reset: Set the Verification Token
                # This password becomes the master password
                encrypted_token = temp_crypto.encrypt("valid")
                self.db.set_config("verification_token", encrypted_token)
                
                self.crypto = temp_crypto
                messagebox.showinfo("Setup Complete", "Master Password Set!\nDo not forget it.")
                self.show_home()

        except Exception as e:
            print(f"Login Error: {e}")
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def show_home(self):
        self.clear_frames()
        self.current_frame = HomeFrame(self)
        self.current_frame.grid(row=0, column=0, sticky="nsew")

    def show_add(self):
        self.clear_frames()
        self.current_frame = AddFrame(self)
        self.current_frame.grid(row=0, column=0, sticky="nsew")

    def show_view(self):
        self.clear_frames()
        self.current_frame = ViewFrame(self)
        self.current_frame.grid(row=0, column=0, sticky="nsew")

    def logout(self):
        self.crypto = None
        self.show_login()

    def clear_frames(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = None
