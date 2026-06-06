import customtkinter
import os
import time
from tkinter import messagebox
from ..core.database import DatabaseManager
from ..core.crypto import CryptoManager

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Set standard dark theme and dark-blue styling base
        customtkinter.set_appearance_mode("Dark")
        customtkinter.set_default_color_theme("dark-blue")

        self.title("PassVault V3.0")
        self.geometry("1000x700")
        self.minsize(900, 600)
        self.configure(fg_color="#0F0F16")
        self.center_window()

        # Database Manager
        self.db = DatabaseManager()
        self.crypto = None # Initialized after login
        
        # Inactivity lock state
        self.timeout_enabled = True
        self.timeout_seconds = 300 # 5 minutes default
        self.last_activity_time = time.time()
        
        # Configure grid layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.current_frame = None

        # Start listening for user activity for auto-lock
        self.bind_all("<Any-KeyPress>", self._update_activity)
        self.bind_all("<Any-ButtonPress>", self._update_activity)
        self.bind_all("<Motion>", self._update_activity)
        self.check_inactivity_timeout()

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
        self.clear_frame()
        # Deferred import to prevent circular dependency
        from .views.login import LoginFrame
        self.current_frame = LoginFrame(self, self.on_login_attempt)
        self.current_frame.grid(row=0, column=0, sticky="nsew")

    def on_login_attempt(self, master_password):
        try:
            # Derive Key
            temp_crypto = CryptoManager(master_password, self.db)
            
            # Check for Verification Token
            stored_token = self.db.get_config("verification_token")
            
            if stored_token:
                # Verify
                try:
                    decrypted = temp_crypto.decrypt(stored_token)
                    if decrypted == "valid":
                        # Success
                        self.crypto = temp_crypto
                        self._update_activity()
                        self.show_home()
                    else:
                        raise ValueError("Invalid Token")
                except Exception:
                    messagebox.showerror("Access Denied", "Incorrect Master Password.")
            else:
                # First setup: verify that the password is secure enough
                from ..core.security import check_password_strength
                strength = check_password_strength(master_password)
                if strength["score"] < 3:
                    feedback_str = "\n".join([f"- {fb}" for fb in strength["feedback"]])
                    messagebox.showerror("Weak Master Password", 
                                         f"Please choose a stronger master password.\n\nSuggestions:\n{feedback_str}")
                    return

                # Create Verification Token
                encrypted_token = temp_crypto.encrypt("valid")
                self.db.set_config("verification_token", encrypted_token)
                
                self.crypto = temp_crypto
                self._update_activity()
                messagebox.showinfo("Setup Complete", "Master Password Configured!\nStore it safely.")
                self.show_home()

        except Exception as e:
            print(f"Login Error: {e}")
            messagebox.showerror("Error", f"An unexpected error occurred during authentication: {e}")

    def show_home(self):
        self.clear_frame()
        from .views.home import HomeFrame
        self.current_frame = HomeFrame(self)
        self.current_frame.grid(row=0, column=0, sticky="nsew")

    def logout(self):
        if self.crypto: # Only trigger if actually logged in
            self.crypto = None
            self.show_login()

    def clear_frame(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = None

    # Inactivity Tracking
    def _update_activity(self, event=None):
        self.last_activity_time = time.time()

    def check_inactivity_timeout(self):
        if self.crypto and self.timeout_enabled:
            inactive_duration = time.time() - self.last_activity_time
            if inactive_duration >= self.timeout_seconds:
                self.logout()
                messagebox.showinfo("Session Expired", "PassVault was locked automatically due to inactivity.")
        
        # Schedule next check in 5 seconds
        self.after(5000, self.check_inactivity_timeout)
