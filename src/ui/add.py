import customtkinter
from tkinter import messagebox
from ..utils import generate_password, is_password_secure

class AddFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master_app = master

        self.grid_columnconfigure(0, weight=1)
        # Fix: Header is row 0 (fixed size), Form is row 1 (expanded)
        self.grid_rowconfigure(0, weight=0) 
        self.grid_rowconfigure(1, weight=1)

        # Header
        self.header = customtkinter.CTkFrame(self, corner_radius=0, height=50)
        self.header.grid(row=0, column=0, sticky="ew")
        self.back_button = customtkinter.CTkButton(self.header, text="< Back", width=60, command=self.master_app.show_home)
        self.back_button.pack(side="left", padx=10, pady=10)
        self.title_label = customtkinter.CTkLabel(self.header, text="Add New Password", font=("Roboto", 18))
        self.title_label.pack(side="left", padx=10)

        # Form
        self.form_frame = customtkinter.CTkFrame(self)
        self.form_frame.grid(row=1, column=0, pady=40) # Increased padding to center it nicely

        # Increased width and height of entries
        self.site_entry = customtkinter.CTkEntry(self.form_frame, placeholder_text="Site Name (e.g. Google)", width=500, height=40)
        self.site_entry.pack(pady=15, padx=20)

        self.user_entry = customtkinter.CTkEntry(self.form_frame, placeholder_text="Username / Email", width=500, height=40)
        self.user_entry.pack(pady=15, padx=20)

        self.pass_entry = customtkinter.CTkEntry(self.form_frame, placeholder_text="Password", width=500, height=40)
        self.pass_entry.pack(pady=15, padx=20)

        # Generator Controls
        self.gen_frame = customtkinter.CTkFrame(self.form_frame, fg_color="transparent")
        self.gen_frame.pack(pady=10)
        
        self.gen_btn = customtkinter.CTkButton(self.gen_frame, text="Generate Strong Password", command=self.generate)
        self.gen_btn.pack()

        # Save
        self.save_btn = customtkinter.CTkButton(self.form_frame, text="Save", command=self.save, fg_color="green", hover_color="darkgreen", width=500, height=40)
        self.save_btn.pack(pady=20, padx=20)

    def generate(self):
        pwd = generate_password(length=16)
        self.pass_entry.delete(0, 'end')
        self.pass_entry.insert(0, pwd)

    def save(self):
        site = self.site_entry.get().strip() # Normalize spaces
        user = self.user_entry.get().strip()
        pwd = self.pass_entry.get()

        if not site or not user or not pwd:
            messagebox.showerror("Error", "All fields are required.")
            return

        # Security Check
        if not is_password_secure(pwd):
            messagebox.showwarning("Insecure Password", 
                                   "Password is not secure enough!\n\n"
                                   "Requirements:\n"
                                   "- Min 8 chars\n"
                                   "- Uppercase\n"
                                   "- Lowercase\n"
                                   "- Digit\n"
                                   "- Symbol")
            return

        try:
            # Encrypt password
            encrypted_pwd = self.master_app.crypto.encrypt(pwd)
            
            # Save to DB (Site name capitalized for standard grouping)
            site_normalized = site.title()
            
            site_id = self.master_app.db.add_site(site_normalized)
            self.master_app.db.add_credential(site_id, user, encrypted_pwd)
            
            messagebox.showinfo("Success", f"Password for {site_normalized} saved!")
            self.master_app.show_home()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {e}")
