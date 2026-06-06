import customtkinter
from tkinter import messagebox
from ...utils.helpers import generate_password
from ...core.security import check_password_strength

class AddView(customtkinter.CTkFrame):
    def __init__(self, master, app_instance, home_frame):
        super().__init__(master, fg_color="transparent")
        self.app = app_instance
        self.home = home_frame

        # Centering configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Main Card Form
        self.card = customtkinter.CTkFrame(self, width=540, height=560, fg_color="#181824")
        self.card.grid(row=0, column=0, padx=20, pady=20)
        self.card.grid_propagate(False)
        self.card.grid_columnconfigure(0, weight=1)

        # Form Header
        self.title_lbl = customtkinter.CTkLabel(self.card, text="Add Credentials", font=("Outfit", 22, "bold"))
        self.title_lbl.pack(pady=(25, 5))
        self.subtitle_lbl = customtkinter.CTkLabel(
            self.card, 
            text="Save a new account safely in your encrypted vault.", 
            font=("Roboto", 13), 
            text_color="#94A3B8"
        )
        self.subtitle_lbl.pack(pady=(0, 20))

        # Fields
        # 1. Site / Platform
        self.site_lbl = customtkinter.CTkLabel(self.card, text="Site / Application Name", font=("Roboto", 12, "bold"), text_color="#94A3B8")
        self.site_lbl.pack(anchor="w", padx=50, pady=(5, 2))
        self.site_entry = customtkinter.CTkEntry(self.card, placeholder_text="e.g. Google, Github, Bank of America", width=440, height=38)
        self.site_entry.pack(padx=50, pady=(0, 10))

        # 2. Username / Email
        self.user_lbl = customtkinter.CTkLabel(self.card, text="Username or Email Address", font=("Roboto", 12, "bold"), text_color="#94A3B8")
        self.user_lbl.pack(anchor="w", padx=50, pady=(5, 2))
        self.user_entry = customtkinter.CTkEntry(self.card, placeholder_text="e.g. username@domain.com", width=440, height=38)
        self.user_entry.pack(padx=50, pady=(0, 10))

        # 3. Password
        self.pass_lbl = customtkinter.CTkLabel(self.card, text="Password", font=("Roboto", 12, "bold"), text_color="#94A3B8")
        self.pass_lbl.pack(anchor="w", padx=50, pady=(5, 2))
        
        self.pass_frame = customtkinter.CTkFrame(self.card, fg_color="transparent")
        self.pass_frame.pack(fill="x", padx=50, pady=(0, 5))
        
        self.pass_entry = customtkinter.CTkEntry(self.pass_frame, placeholder_text="Enter or generate secure password", show="*", width=310, height=38)
        self.pass_entry.pack(side="left")
        self.pass_entry.bind("<KeyRelease>", self._update_strength_bar)

        self.gen_btn = customtkinter.CTkButton(
            self.pass_frame, 
            text="Generate", 
            width=120, 
            height=38,
            fg_color="#3B3B54",
            hover_color="#525270",
            command=self.quick_generate
        )
        self.gen_btn.pack(side="right")

        # Strength Indicator Row
        self.strength_frame = customtkinter.CTkFrame(self.card, fg_color="transparent")
        self.strength_frame.pack(fill="x", padx=50, pady=(0, 10))
        
        self.strength_bar = customtkinter.CTkProgressBar(self.strength_frame, width=310, height=6)
        self.strength_bar.pack(side="left", pady=10)
        self.strength_bar.set(0)
        
        self.strength_lbl = customtkinter.CTkLabel(self.strength_frame, text="Empty", font=("Roboto", 11, "bold"), text_color="#94A3B8", width=120, anchor="e")
        self.strength_lbl.pack(side="right")

        # 4. Category Dropdown
        self.cat_lbl = customtkinter.CTkLabel(self.card, text="Vault Category", font=("Roboto", 12, "bold"), text_color="#94A3B8")
        self.cat_lbl.pack(anchor="w", padx=50, pady=(5, 2))
        
        self.cat_menu = customtkinter.CTkOptionMenu(
            self.card, 
            values=["Personal", "Work", "Social", "Finance", "Other"],
            width=440,
            height=38
        )
        self.cat_menu.set("Personal")
        self.cat_menu.pack(padx=50, pady=(0, 25))

        # Save Button
        self.save_btn = customtkinter.CTkButton(
            self.card, 
            text="Save Securely", 
            font=("Roboto", 15, "bold"),
            width=440, 
            height=44,
            command=self.save_credential
        )
        self.save_btn.pack(padx=50, pady=10)

    def _update_strength_bar(self, event=None):
        password = self.pass_entry.get()
        if not password:
            self.strength_bar.set(0)
            self.strength_lbl.configure(text="Empty", text_color="#94A3B8")
            return

        strength = check_password_strength(password)
        self.strength_bar.set(strength["score"] / 5.0)
        self.strength_bar.configure(progress_color=strength["color"])
        self.strength_lbl.configure(text=strength["label"], text_color=strength["color"])

    def quick_generate(self):
        # Generates a strong password using CSPRNG with symbols
        pwd = generate_password(length=16)
        self.pass_entry.delete(0, 'end')
        self.pass_entry.insert(0, pwd)
        self._update_strength_bar()

    def save_credential(self):
        site = self.site_entry.get().strip()
        user = self.user_entry.get().strip()
        pwd = self.pass_entry.get()
        cat = self.cat_menu.get()

        if not site or not user or not pwd:
            messagebox.showerror("Validation Error", "All fields are required.")
            return

        # Security advice if password is weak
        strength = check_password_strength(pwd)
        if strength["score"] < 3:
            confirm = messagebox.askyesno(
                "Weak Password Warning",
                f"The password you entered is rated as '{strength['label']}'.\n\n"
                "Are you sure you want to save this password anyway?\n"
                "We highly recommend generating a strong password.",
                icon="warning"
            )
            if not confirm:
                return

        try:
            # Capitalize Site Name for consistency
            site_normalized = site.title()
            
            # Encrypt password
            encrypted_pwd = self.app.crypto.encrypt(pwd)
            
            # Save to Database
            site_id = self.app.db.add_site(site_normalized)
            self.app.db.add_credential(site_id, user, encrypted_pwd, cat)
            
            # Clear form
            self.site_entry.delete(0, 'end')
            self.user_entry.delete(0, 'end')
            self.pass_entry.delete(0, 'end')
            self.strength_bar.set(0)
            self.strength_lbl.configure(text="Empty", text_color="#94A3B8")
            
            messagebox.showinfo("Success", f"Credentials for {site_normalized} saved securely!")
            
            # Switch back to the vault view to show the new card
            self.home.switch_view("vault")

        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to save credential: {e}")
