import customtkinter
from tkinter import messagebox
import pyperclip

class ViewFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master_app = master

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1) # List area

        # Header
        self.header = customtkinter.CTkFrame(self, corner_radius=0, height=50)
        self.header.grid(row=0, column=0, sticky="ew")
        self.back_button = customtkinter.CTkButton(self.header, text="< Back", width=60, command=self.master_app.show_home)
        self.back_button.pack(side="left", padx=10, pady=10)
        self.title_label = customtkinter.CTkLabel(self.header, text="My Passwords", font=("Roboto", 18))
        self.title_label.pack(side="left", padx=10)

        # Scrollable List
        self.scroll_frame = customtkinter.CTkScrollableFrame(self)
        self.scroll_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        
        self.refresh_list()

    def refresh_list(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        sites = self.master_app.db.get_sites()
        if not sites:
            customtkinter.CTkLabel(self.scroll_frame, text="No passwords found.").pack(pady=20)
            return

        for site in sites:
            row = customtkinter.CTkFrame(self.scroll_frame)
            row.pack(fill="x", pady=5)
            
            lbl = customtkinter.CTkLabel(row, text=site, font=("Roboto", 16, "bold"))
            lbl.pack(side="left", padx=10)
            
            # View Button (Loads accounts for this site)
            btn = customtkinter.CTkButton(row, text="View Accounts", width=120, command=lambda s=site: self.show_details(s))
            btn.pack(side="right", padx=10)

    def show_details(self, site_name):
        creds = self.master_app.db.get_credentials(site_name)
        if not creds:
            return 

        details_window = customtkinter.CTkToplevel(self)
        details_window.title(f"Accounts for {site_name}")
        details_window.geometry("500x400")
        
        container = customtkinter.CTkScrollableFrame(details_window)
        container.pack(fill="both", expand=True, padx=10, pady=10)
        
        for cred_id, username, encrypted_pwd in creds:
            try:
                decrypted = self.master_app.crypto.decrypt(encrypted_pwd)
            except Exception:
                decrypted = "[Decryption Failed]"

            f = customtkinter.CTkFrame(container)
            f.pack(fill="x", padx=5, pady=5)
            
            # Username Row
            user_frame = customtkinter.CTkFrame(f, fg_color="transparent")
            user_frame.pack(fill="x", padx=5, pady=2)
            customtkinter.CTkLabel(user_frame, text="User:", width=50, anchor="w").pack(side="left")
            user_entry = customtkinter.CTkEntry(user_frame, width=200)
            user_entry.insert(0, username)
            user_entry.configure(state="readonly")
            user_entry.pack(side="left", padx=5)
            # Copy User Button
            customtkinter.CTkButton(user_frame, text="Copy", width=50, command=lambda u=username: pyperclip.copy(u)).pack(side="left", padx=5)

            # Password Row
            pass_frame = customtkinter.CTkFrame(f, fg_color="transparent")
            pass_frame.pack(fill="x", padx=5, pady=2)
            customtkinter.CTkLabel(pass_frame, text="Pass:", width=50, anchor="w").pack(side="left")
            pass_entry = customtkinter.CTkEntry(pass_frame, width=200)
            pass_entry.insert(0, decrypted)
            pass_entry.configure(state="readonly")
            pass_entry.pack(side="left", padx=5)
            # Copy Pass Button
            customtkinter.CTkButton(pass_frame, text="Copy", width=50, command=lambda p=decrypted: pyperclip.copy(p)).pack(side="left", padx=5)

            # Delete Button
            customtkinter.CTkButton(f, text="Delete Account", fg_color="red", width=100, hover_color="darkred", 
                                    command=lambda cid=cred_id, w=details_window: self.delete_cred(cid, w)).pack(pady=5)

    def delete_cred(self, cred_id, window):
        if messagebox.askyesno("Confirm", "Delete this account?"):
            self.master_app.db.delete_credential(cred_id)
            # Check if site is empty (handled in DB logic usually, but here checking UI refresh needs)
            # We implemented delete_credential in DB, but not delete_site_if_empty check there automatically.
            # Good practice to clean up site if empty.
            # Let's add that call if we can, or just refresh.
            window.destroy()
            self.refresh_list()
