import customtkinter
from tkinter import messagebox
import os
from ...core.database import DatabaseManager
from ...core.security import check_password_strength

class LoginFrame(customtkinter.CTkFrame):
    def __init__(self, master, on_login_attempt):
        super().__init__(master, fg_color="transparent")
        self.master_app = master
        self.on_login_attempt = on_login_attempt

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Center card container
        self.card = customtkinter.CTkFrame(self, width=450, height=550, fg_color="#181824")
        self.card.grid(row=0, column=0, padx=40, pady=40)
        self.card.grid_propagate(False)
        self.card.grid_columnconfigure(0, weight=1)

        # App Title
        self.logo_label = customtkinter.CTkLabel(self.card, text="🔒 PassVault", font=("Outfit", 32, "bold"), text_color="#7C4DFF")
        self.logo_label.pack(pady=(40, 10))

        # Check if first setup
        self.is_first_run = self.master_app.db.get_config("verification_token") is None

        if self.is_first_run:
            self.title_label = customtkinter.CTkLabel(self.card, text="Initialize Master Password", font=("Roboto", 18, "bold"))
            self.title_label.pack(pady=5)
            self.subtitle_label = customtkinter.CTkLabel(self.card, text="This password encrypts your entire vault.\nMake it strong and memorable.", font=("Roboto", 13), text_color="#94A3B8")
            self.subtitle_label.pack(pady=5)
            
            # Setup inputs
            self.pwd_entry = customtkinter.CTkEntry(self.card, placeholder_text="Enter Master Password", show="*", width=340, height=45)
            self.pwd_entry.pack(pady=15)
            self.pwd_entry.bind("<KeyRelease>", self._check_realtime_strength)
            
            # Realtime requirements indicator
            self.req_frame = customtkinter.CTkFrame(self.card, fg_color="transparent")
            self.req_frame.pack(pady=5, fill="x", padx=60)
            
            self.req_labels = {}
            requirements = [
                ("len", "At least 12 characters"),
                ("upper", "Uppercase letter (A-Z)"),
                ("digit", "Number (0-9)"),
                ("symbol", "Special symbol (@, #, $, !)")
            ]
            for key, text in requirements:
                lbl = customtkinter.CTkLabel(self.req_frame, text=f"✗ {text}", font=("Roboto", 12), text_color="#EF4444", anchor="w")
                lbl.pack(anchor="w", pady=2)
                self.req_labels[key] = lbl
                
            self.action_btn = customtkinter.CTkButton(self.card, text="Configure Vault", command=self.submit, width=340, height=45, state="disabled")
            self.action_btn.pack(pady=(20, 10))
        else:
            self.title_label = customtkinter.CTkLabel(self.card, text="Vault Locked", font=("Roboto", 20, "bold"))
            self.title_label.pack(pady=5)
            self.subtitle_label = customtkinter.CTkLabel(self.card, text="Enter your master password to unlock.", font=("Roboto", 13), text_color="#94A3B8")
            self.subtitle_label.pack(pady=5)

            # Unlock input
            self.pwd_entry = customtkinter.CTkEntry(self.card, placeholder_text="Master Password", show="*", width=340, height=45)
            self.pwd_entry.pack(pady=25)
            self.pwd_entry.bind("<Return>", lambda e: self.submit())

            self.action_btn = customtkinter.CTkButton(self.card, text="Unlock Vault", command=self.submit, width=340, height=45)
            self.action_btn.pack(pady=10)

            # Forgot Password (Nuclear Reset)
            self.reset_btn = customtkinter.CTkButton(self.card, text="Forgot Password? (Nuclear Reset)", 
                                                     command=self.nuclear_reset, 
                                                     fg_color="transparent", border_width=1, border_color="#EF4444",
                                                     text_color="#EF4444", hover_color="#2E1619", width=340, height=40)
            self.reset_btn.pack(pady=(25, 20))

    def _check_realtime_strength(self, event=None):
        if not self.is_first_run:
            return
            
        pwd = self.pwd_entry.get()
        
        # Validations
        valid_len = len(pwd) >= 12
        valid_upper = any(c.isupper() for c in pwd)
        valid_digit = any(c.isdigit() for c in pwd)
        import string
        valid_symbol = any(c in string.punctuation for c in pwd)
        
        # Helper to update colors
        def update_label(key, is_valid):
            lbl = self.req_labels[key]
            text = lbl.cget("text")[2:] # Strip prefix icon
            if is_valid:
                lbl.configure(text=f"✓ {text}", text_color="#10B981")
            else:
                lbl.configure(text=f"✗ {text}", text_color="#EF4444")
                
        update_label("len", valid_len)
        update_label("upper", valid_upper)
        update_label("digit", valid_digit)
        update_label("symbol", valid_symbol)
        
        # Enable action button if all requirements met
        if valid_len and valid_upper and valid_digit and valid_symbol:
            self.action_btn.configure(state="normal")
        else:
            self.action_btn.configure(state="disabled")

    def submit(self):
        password = self.pwd_entry.get()
        if password:
            self.on_login_attempt(password)
        else:
            messagebox.showerror("Validation Error", "Password cannot be empty.")

    def nuclear_reset(self):
        confirm = messagebox.askyesno(
            "NUCLEAR RESET WARNING",
            "Are you absolutely sure?\n\n"
            "This will PERMANENTLY ERASE your local database and all saved passwords.\n"
            "This action is irreversible.",
            icon='warning'
        )
        if confirm:
            db_manager = DatabaseManager()
            db_manager.nuclear_reset()
            
            # Remove legacy file if any
            if os.path.exists("salt.key"):
                try:
                    os.remove("salt.key")
                except Exception:
                    pass
                    
            messagebox.showinfo("Reset Completed", "Vault reset. Please configure a new master password.")
            
            # Reload login frame
            self.master_app.show_login()
