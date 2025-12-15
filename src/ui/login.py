import customtkinter
from tkinter import messagebox
import os
from ..database import DatabaseManager

class LoginFrame(customtkinter.CTkFrame):
    def __init__(self, master, on_login_attempt):
        super().__init__(master)
        self.master_app = master
        self.on_login_attempt = on_login_attempt # Callback

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.content = customtkinter.CTkFrame(self)
        self.content.grid(row=0, column=0, padx=20, pady=20)

        # Title
        self.label = customtkinter.CTkLabel(self.content, text="PassVault Locked", font=("Roboto", 24, "bold"))
        self.label.pack(pady=20)

        # Password Entry
        self.password_entry = customtkinter.CTkEntry(self.content, placeholder_text="Master Password", show="*", width=300)
        self.password_entry.pack(pady=10)
        self.password_entry.bind("<Return>", self.login)

        # Login Button
        self.login_button = customtkinter.CTkButton(self.content, text="Unlock", command=self.login, width=300)
        self.login_button.pack(pady=10)

        # Forgot Password / Reset
        self.reset_button = customtkinter.CTkButton(self.content, text="Forgot Password? (Nuclear Reset)", 
                                                    command=self.nuclear_reset, 
                                                    fg_color="red", hover_color="darkred", width=300)
        self.reset_button.pack(pady=20)

    def login(self, event=None):
        password = self.password_entry.get()
        if password:
            self.on_login_attempt(password)
        else:
            messagebox.showerror("Error", "Please enter your master password.")

    def nuclear_reset(self):
        confirm = messagebox.askyesno("NUCLEAR RESET", 
                                      "This will PERMANENTLY DELETE current database and all passwords.\n\n"
                                      "Are you strictly sure you want to proceed?\n"
                                      "This cannot be undone.")
        if confirm:
            db_manager = DatabaseManager()
            db_manager.nuclear_reset()
            
            # Also reset salt - Crucial because salt + password = key. 
            # If we reset DB, we should start fresh with salt too for new password.
            # Salt is in root directory usually (where run.py is run from)
            # Or in src/crypto.py location. Wait, crypto.py looks for "salt.key" in current working dir.
            if os.path.exists("salt.key"):
                try:
                    os.remove("salt.key")
                except:
                    pass
            
            messagebox.showinfo("Reset Complete", "The database has been wiped. You can now set a new master password on next login.")
            self.password_entry.delete(0, 'end')
