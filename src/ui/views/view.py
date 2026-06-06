import customtkinter
from tkinter import messagebox
from ...utils.helpers import copy_to_clipboard, generate_password
from ...core.security import check_password_strength

class CredentialsView(customtkinter.CTkFrame):
    def __init__(self, master, app_instance, home_frame):
        super().__init__(master, fg_color="transparent")
        self.app = app_instance
        self.home = home_frame

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0) # Header
        self.grid_rowconfigure(1, weight=1) # List Frame
        self.grid_rowconfigure(2, weight=0) # Status Bar

        # 1. Header Frame
        self.header = customtkinter.CTkFrame(self, fg_color="transparent")
        self.header.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        self.header.grid_columnconfigure(0, weight=1)

        # Title
        customtkinter.CTkLabel(self.header, text="My Passwords", font=("Outfit", 26, "bold")).grid(row=0, column=0, sticky="w")
        
        # Search Entry
        self.search_var = customtkinter.StringVar()
        self.search_entry = customtkinter.CTkEntry(
            self.header, 
            placeholder_text="Search by site or username...", 
            textvariable=self.search_var,
            height=40
        )
        self.search_entry.grid(row=1, column=0, sticky="ew", pady=(10, 10))
        self.search_entry.bind("<KeyRelease>", self.trigger_search)

        # Category Filters
        self.category_filter = customtkinter.CTkSegmentedButton(
            self.header,
            values=["All", "Personal", "Work", "Social", "Finance", "Other"],
            command=self.trigger_search,
            height=35
        )
        self.category_filter.grid(row=2, column=0, sticky="ew")
        self.category_filter.set("All")

        # 2. Scrollable List Area
        self.scroll_frame = customtkinter.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_frame.grid(row=1, column=0, sticky="nsew")

        # Keep track of passwords mapping for show/hide state
        # cred_id -> bool (True if visible, False if hidden)
        self.pwd_visibility = {}

        # 3. Status Bar at the bottom for feedback
        self.status_bar = customtkinter.CTkLabel(self, text="", font=("Roboto", 12), text_color="#10B981")
        self.status_bar.grid(row=2, column=0, sticky="ew", pady=(5, 0))

        # Initial populate
        self.refresh_list()

    def trigger_search(self, event=None):
        query = self.search_var.get().strip()
        category = self.category_filter.get()
        results = self.app.db.search_credentials(query, category)
        self.populate_cards(results)

    def refresh_list(self):
        self.search_var.set("")
        self.category_filter.set("All")
        results = self.app.db.get_all_credentials()
        self.populate_cards(results)

    def populate_cards(self, credentials):
        # Clear frame
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        if not credentials:
            lbl = customtkinter.CTkLabel(
                self.scroll_frame, 
                text="No credentials found matching criteria.", 
                font=("Roboto", 14), 
                text_color="#94A3B8"
            )
            lbl.pack(pady=40)
            return

        for cred_id, site, username, encrypted_pwd, category, created_at, updated_at in credentials:
            # Add to visibility dictionary if not present
            if cred_id not in self.pwd_visibility:
                self.pwd_visibility[cred_id] = False

            # Decrypt password
            try:
                decrypted_pwd = self.app.crypto.decrypt(encrypted_pwd)
            except Exception:
                decrypted_pwd = "[Decryption Failed]"

            # Category Color Theme mapping
            badge_colors = {
                "Personal": "#3B82F6",
                "Work": "#EAB308",
                "Social": "#EC4899",
                "Finance": "#10B981",
                "Other": "#6B7280"
            }
            badge_color = badge_colors.get(category, "#6B7280")

            # Credential Card frame
            card = customtkinter.CTkFrame(self.scroll_frame, height=140, fg_color="#181824")
            card.pack(fill="x", pady=6, padx=5)

            # Left block: Title, category, username
            info_frame = customtkinter.CTkFrame(card, fg_color="transparent")
            info_frame.pack(side="left", fill="both", expand=True, padx=15, pady=10)

            # Row 1: Site Name & Category Badge
            site_row = customtkinter.CTkFrame(info_frame, fg_color="transparent")
            site_row.pack(fill="x", anchor="w")
            
            site_lbl = customtkinter.CTkLabel(site_row, text=site, font=("Outfit", 18, "bold"), text_color="#F8F9FA")
            site_lbl.pack(side="left", anchor="w")
            
            badge = customtkinter.CTkFrame(site_row, fg_color=badge_color, height=20, corner_radius=4)
            badge.pack(side="left", padx=10, pady=2)
            badge_lbl = customtkinter.CTkLabel(badge, text=category, font=("Roboto", 10, "bold"), text_color="#FFFFFF", padx=6)
            badge_lbl.pack()

            # Row 2: Username (Copyable entry)
            user_row = customtkinter.CTkFrame(info_frame, fg_color="transparent")
            user_row.pack(fill="x", pady=(8, 2))
            
            customtkinter.CTkLabel(user_row, text="Username:", font=("Roboto", 12), text_color="#94A3B8", width=70, anchor="w").pack(side="left")
            
            user_entry = customtkinter.CTkEntry(user_row, height=26, width=180, font=("Roboto", 12))
            user_entry.insert(0, username)
            user_entry.configure(state="readonly")
            user_entry.pack(side="left", padx=5)

            copy_user_btn = customtkinter.CTkButton(
                user_row, 
                text="Copy", 
                width=50, 
                height=26,
                fg_color="#2E2E3F",
                hover_color="#3E3E56",
                command=lambda u=username: self.copy_field(u, "Username")
            )
            copy_user_btn.pack(side="left", padx=2)

            # Row 3: Password (Revealable & Copyable entry)
            pwd_row = customtkinter.CTkFrame(info_frame, fg_color="transparent")
            pwd_row.pack(fill="x", pady=2)

            customtkinter.CTkLabel(pwd_row, text="Password:", font=("Roboto", 12), text_color="#94A3B8", width=70, anchor="w").pack(side="left")
            
            pwd_entry = customtkinter.CTkEntry(pwd_row, height=26, width=180, font=("Courier", 12))
            
            # Visibility logic
            is_visible = self.pwd_visibility[cred_id]
            pwd_entry.insert(0, decrypted_pwd if is_visible else "•" * len(decrypted_pwd))
            pwd_entry.configure(state="readonly")
            pwd_entry.pack(side="left", padx=5)

            # Reveal Button (Eye Toggle icon placeholder)
            toggle_text = "Hide" if is_visible else "Show"
            toggle_btn = customtkinter.CTkButton(
                pwd_row, 
                text=toggle_text, 
                width=50, 
                height=26,
                fg_color="#2E2E3F",
                hover_color="#3E3E56",
                command=lambda cid=cred_id, pe=pwd_entry, dp=decrypted_pwd: self.toggle_password(cid, pe, dp)
            )
            toggle_btn.pack(side="left", padx=2)

            # Copy password button
            copy_pwd_btn = customtkinter.CTkButton(
                pwd_row, 
                text="Copy", 
                width=50, 
                height=26,
                fg_color="#2E2E3F",
                hover_color="#3E3E56",
                command=lambda p=decrypted_pwd: self.copy_field(p, "Password")
            )
            copy_pwd_btn.pack(side="left", padx=2)

            # Right block: Actions (Edit & Delete)
            actions_frame = customtkinter.CTkFrame(card, fg_color="transparent")
            actions_frame.pack(side="right", fill="y", padx=15, pady=10)

            # Edit Button
            edit_btn = customtkinter.CTkButton(
                actions_frame, 
                text="Edit", 
                width=80, 
                height=32,
                fg_color="#33334D",
                hover_color="#47476B",
                text_color="#E2E8F0",
                command=lambda cid=cred_id, s=site, u=username, p=decrypted_pwd, c=category: self.open_edit_dialog(cid, s, u, p, c)
            )
            edit_btn.pack(pady=5)

            # Delete Button
            delete_btn = customtkinter.CTkButton(
                actions_frame, 
                text="Delete", 
                width=80, 
                height=32,
                fg_color="transparent",
                border_width=1,
                border_color="#EF4444",
                text_color="#EF4444",
                hover_color="#2E1619",
                command=lambda cid=cred_id: self.delete_credential(cid)
            )
            delete_btn.pack(pady=5)

    def toggle_password(self, cred_id, entry_widget, decrypted_pwd):
        # Flip visibility
        is_visible = not self.pwd_visibility[cred_id]
        self.pwd_visibility[cred_id] = is_visible
        
        # Update entry text
        entry_widget.configure(state="normal")
        entry_widget.delete(0, "end")
        entry_widget.insert(0, decrypted_pwd if is_visible else "•" * len(decrypted_pwd))
        entry_widget.configure(state="readonly")

        # Find button in hierarchy and update text
        # The parent of entry_widget is the pwd_row frame. The toggle button is the 3rd child (index 2).
        # We can safely use widget navigation or just find the toggle button.
        for widget in entry_widget.master.winfo_children():
            if isinstance(widget, customtkinter.CTkButton) and widget.cget("text") in ["Show", "Hide"]:
                widget.configure(text="Hide" if is_visible else "Show")

    def copy_field(self, value, field_name):
        copy_to_clipboard(value, self.app, self.on_clipboard_cleared)
        self.status_bar.configure(
            text=f"✓ {field_name} copied to clipboard! (Will auto-clear in 30s)",
            text_color="#10B981"
        )

    def on_clipboard_cleared(self):
        try:
            if self.winfo_exists():
                self.status_bar.configure(
                    text="ⓘ Clipboard cleared for security.",
                    text_color="#94A3B8"
                )
        except Exception:
            pass

    def delete_credential(self, cred_id):
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this credential?\nThis cannot be undone."):
            self.app.db.delete_credential(cred_id)
            self.status_bar.configure(text="✓ Credential deleted successfully.", text_color="#EF4444")
            self.trigger_search()

    # Edit dialog window
    def open_edit_dialog(self, cred_id, current_site, current_user, current_pwd, current_cat):
        dialog = customtkinter.CTkToplevel(self)
        dialog.title("Edit Credential")
        dialog.geometry("460x520")
        dialog.transient(self) # Keep on top of main window
        dialog.grab_set() # Focus lock
        dialog.resizable(False, False)

        # Grid config
        dialog.grid_columnconfigure(0, weight=1)

        title_lbl = customtkinter.CTkLabel(dialog, text="Modify Account Details", font=("Outfit", 20, "bold"))
        title_lbl.pack(pady=(20, 15))

        # Fields
        # 1. Site
        customtkinter.CTkLabel(dialog, text="Site / Application", font=("Roboto", 12, "bold"), text_color="#94A3B8").pack(anchor="w", padx=30, pady=(5, 2))
        site_entry = customtkinter.CTkEntry(dialog, width=400, height=36)
        site_entry.insert(0, current_site)
        site_entry.pack(padx=30, pady=(0, 10))

        # 2. Username
        customtkinter.CTkLabel(dialog, text="Username / Email", font=("Roboto", 12, "bold"), text_color="#94A3B8").pack(anchor="w", padx=30, pady=(5, 2))
        user_entry = customtkinter.CTkEntry(dialog, width=400, height=36)
        user_entry.insert(0, current_user)
        user_entry.pack(padx=30, pady=(0, 10))

        # 3. Password
        customtkinter.CTkLabel(dialog, text="Password", font=("Roboto", 12, "bold"), text_color="#94A3B8").pack(anchor="w", padx=30, pady=(5, 2))
        
        pwd_frame = customtkinter.CTkFrame(dialog, fg_color="transparent")
        pwd_frame.pack(fill="x", padx=30, pady=(0, 10))
        
        pwd_entry = customtkinter.CTkEntry(pwd_frame, width=290, height=36)
        pwd_entry.insert(0, current_pwd)
        pwd_entry.pack(side="left")

        # Generator button inline
        def gen_pwd():
            new_p = generate_password(length=16)
            pwd_entry.delete(0, "end")
            pwd_entry.insert(0, new_p)
            check_strength()

        gen_btn = customtkinter.CTkButton(pwd_frame, text="Generate", width=100, height=36, command=gen_pwd)
        gen_btn.pack(side="right")

        # Password Strength Bar inside dialog
        strength_frame = customtkinter.CTkFrame(dialog, fg_color="transparent")
        strength_frame.pack(fill="x", padx=30, pady=(0, 10))
        
        strength_bar = customtkinter.CTkProgressBar(strength_frame, width=280, height=6)
        strength_bar.pack(side="left", pady=10)
        strength_lbl = customtkinter.CTkLabel(strength_frame, text="", font=("Roboto", 11, "bold"), width=110, anchor="e")
        strength_lbl.pack(side="right")

        def check_strength(event=None):
            p = pwd_entry.get()
            strength = check_password_strength(p)
            strength_bar.set(strength["score"] / 5.0)
            strength_bar.configure(progress_color=strength["color"])
            strength_lbl.configure(text=strength["label"], text_color=strength["color"])

        pwd_entry.bind("<KeyRelease>", check_strength)
        check_strength() # Initial check

        # 4. Category
        customtkinter.CTkLabel(dialog, text="Category", font=("Roboto", 12, "bold"), text_color="#94A3B8").pack(anchor="w", padx=30, pady=(5, 2))
        category_opt = customtkinter.CTkOptionMenu(
            dialog, 
            values=["Personal", "Work", "Social", "Finance", "Other"],
            width=400,
            height=36
        )
        category_opt.set(current_cat)
        category_opt.pack(padx=30, pady=(0, 20))

        # Save & Cancel Buttons
        btn_frame = customtkinter.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(fill="x", padx=30, pady=10)

        cancel_btn = customtkinter.CTkButton(
            btn_frame, 
            text="Cancel", 
            width=190, 
            height=40, 
            fg_color="transparent",
            border_width=1,
            border_color="#475569",
            text_color="#CBD5E1",
            hover_color="#1E1E2F",
            command=dialog.destroy
        )
        cancel_btn.pack(side="left", padx=(0, 10))

        def save_changes():
            site = site_entry.get().strip()
            user = user_entry.get().strip()
            pwd = pwd_entry.get()
            cat = category_opt.get()

            if not site or not user or not pwd:
                messagebox.showerror("Error", "All fields are required.", parent=dialog)
                return

            try:
                # Encrypt new password
                encrypted = self.app.crypto.encrypt(pwd)
                self.app.db.update_credential(cred_id, site, user, encrypted, cat)
                self.status_bar.configure(text=f"✓ Account for {site} updated successfully.", text_color="#10B981")
                dialog.destroy()
                self.trigger_search()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save: {e}", parent=dialog)

        save_btn = customtkinter.CTkButton(btn_frame, text="Save Changes", width=190, height=40, command=save_changes)
        save_btn.pack(side="right")
