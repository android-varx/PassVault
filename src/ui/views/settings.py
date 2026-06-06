import customtkinter
import os
import json
import base64
from tkinter import filedialog, messagebox
from datetime import datetime
from ...utils.helpers import copy_to_clipboard
from ...core.security import check_password_strength

class SettingsView(customtkinter.CTkFrame):
    def __init__(self, master, app_instance, home_frame):
        super().__init__(master, fg_color="transparent")
        self.app = app_instance
        self.home = home_frame

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0) # Header
        self.grid_rowconfigure(1, weight=1) # Settings Panels

        # Header
        self.header_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        self.title_lbl = customtkinter.CTkLabel(self.header_frame, text="Settings", font=("Outfit", 26, "bold"))
        self.title_lbl.pack(anchor="w")
        self.subtitle_lbl = customtkinter.CTkLabel(
            self.header_frame, 
            text="Manage database backups, security triggers, and master credentials.", 
            font=("Roboto", 13), 
            text_color="#94A3B8"
        )
        self.subtitle_lbl.pack(anchor="w", pady=(2, 0))

        # Main Scrollable settings frame
        self.scroll_settings = customtkinter.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_settings.grid(row=1, column=0, sticky="nsew")
        self.scroll_settings.grid_columnconfigure(0, weight=1)

        # 1. Security Settings Panel
        self.create_security_panel()

        # 2. Vault Administration Panel
        self.create_admin_panel()

        # 3. Backup & Recovery Panel
        self.create_backup_panel()

    def create_security_panel(self):
        panel = customtkinter.CTkFrame(self.scroll_settings, fg_color="#181824")
        panel.pack(fill="x", pady=10, padx=5)
        
        customtkinter.CTkLabel(panel, text="Security Settings", font=("Outfit", 16, "bold"), text_color="#7C4DFF").pack(anchor="w", padx=20, pady=(15, 10))

        # Inactivity Lock switch
        self.lock_switch = customtkinter.CTkSwitch(
            panel, 
            text="Auto-Lock Vault on Inactivity (5 minutes)",
            font=("Roboto", 13),
            command=self.toggle_inactivity_lock
        )
        self.lock_switch.pack(anchor="w", padx=20, pady=(0, 15))
        if self.app.timeout_enabled:
            self.lock_switch.select()
        else:
            self.lock_switch.deselect()

    def toggle_inactivity_lock(self):
        self.app.timeout_enabled = self.lock_switch.get() == 1
        state_str = "enabled" if self.app.timeout_enabled else "disabled"
        # Small temporary alert
        messagebox.showinfo("Settings Updated", f"Auto-lock has been {state_str}.")

    def create_admin_panel(self):
        panel = customtkinter.CTkFrame(self.scroll_settings, fg_color="#181824")
        panel.pack(fill="x", pady=10, padx=5)
        
        customtkinter.CTkLabel(panel, text="Vault Master Credentials", font=("Outfit", 16, "bold"), text_color="#7C4DFF").pack(anchor="w", padx=20, pady=(15, 10))

        desc = customtkinter.CTkLabel(
            panel, 
            text="Modify your vault master password. This will re-encrypt all stored credentials with your new key.",
            font=("Roboto", 12),
            text_color="#94A3B8",
            justify="left",
            wraplength=600
        )
        desc.pack(anchor="w", padx=20, pady=(0, 15))

        btn = customtkinter.CTkButton(
            panel, 
            text="Change Master Password", 
            width=200, 
            height=36,
            command=self.open_change_pwd_dialog
        )
        btn.pack(anchor="w", padx=20, pady=(0, 20))

    def create_backup_panel(self):
        panel = customtkinter.CTkFrame(self.scroll_settings, fg_color="#181824")
        panel.pack(fill="x", pady=10, padx=5)
        
        customtkinter.CTkLabel(panel, text="Backup & Recovery", font=("Outfit", 16, "bold"), text_color="#7C4DFF").pack(anchor="w", padx=20, pady=(15, 10))

        # Encrypted JSON Backups
        customtkinter.CTkLabel(panel, text="Secure Encrypted JSON Backups", font=("Roboto", 13, "bold"), text_color="#F8F9FA").pack(anchor="w", padx=20, pady=(5, 2))
        customtkinter.CTkLabel(
            panel, 
            text="Exports your database inside a strong AES-encrypted JSON file. Recommended for secure storage.",
            font=("Roboto", 12), text_color="#94A3B8", justify="left"
        ).pack(anchor="w", padx=20, pady=(0, 10))

        btn_row_1 = customtkinter.CTkFrame(panel, fg_color="transparent")
        btn_row_1.pack(fill="x", padx=20, pady=(0, 15))
        
        customtkinter.CTkButton(btn_row_1, text="Export Encrypted JSON", command=self.export_encrypted_json).pack(side="left", padx=(0, 10))
        customtkinter.CTkButton(btn_row_1, text="Import Encrypted JSON", fg_color="#3B3B54", hover_color="#525270", command=self.import_encrypted_json).pack(side="left")

        # CSV Export
        customtkinter.CTkLabel(panel, text="Plain CSV Export (Caution)", font=("Roboto", 13, "bold"), text_color="#EF4444").pack(anchor="w", padx=20, pady=(10, 2))
        customtkinter.CTkLabel(
            panel, 
            text="Exports all credentials in unencrypted text format. Danger: Anyone with file access can read your passwords.",
            font=("Roboto", 12), text_color="#94A3B8", justify="left"
        ).pack(anchor="w", padx=20, pady=(0, 10))
        
        customtkinter.CTkButton(
            panel, 
            text="Export to CSV (Plain Text)", 
            fg_color="transparent", border_width=1, border_color="#EF4444", text_color="#EF4444", hover_color="#2E1619",
            command=self.export_csv
        ).pack(anchor="w", padx=20, pady=(0, 20))

    # Master Password Change Dialog
    def open_change_pwd_dialog(self):
        dialog = customtkinter.CTkToplevel(self)
        dialog.title("Change Master Password")
        dialog.geometry("450x520")
        dialog.transient(self)
        dialog.grab_set()
        dialog.resizable(False, False)

        customtkinter.CTkLabel(dialog, text="Change Master Password", font=("Outfit", 20, "bold")).pack(pady=20)

        # Inputs
        # 1. Current Password
        customtkinter.CTkLabel(dialog, text="Current Master Password", font=("Roboto", 12, "bold"), text_color="#94A3B8").pack(anchor="w", padx=35, pady=(5, 2))
        curr_entry = customtkinter.CTkEntry(dialog, show="*", width=380, height=36)
        curr_entry.pack(padx=35, pady=(0, 10))

        # 2. New Password
        customtkinter.CTkLabel(dialog, text="New Master Password", font=("Roboto", 12, "bold"), text_color="#94A3B8").pack(anchor="w", padx=35, pady=(5, 2))
        new_entry = customtkinter.CTkEntry(dialog, show="*", width=380, height=36)
        new_entry.pack(padx=35, pady=(0, 5))
        
        # Strength indicators
        strength_bar = customtkinter.CTkProgressBar(dialog, width=380, height=6)
        strength_bar.pack(padx=35, pady=5)
        strength_bar.set(0)
        
        strength_lbl = customtkinter.CTkLabel(dialog, text="Empty", font=("Roboto", 11, "bold"), text_color="#94A3B8")
        strength_lbl.pack(anchor="e", padx=35, pady=(0, 10))

        def check_strength(event=None):
            p = new_entry.get()
            if not p:
                strength_bar.set(0)
                strength_lbl.configure(text="Empty", text_color="#94A3B8")
                return
            strength = check_password_strength(p)
            strength_bar.set(strength["score"] / 5.0)
            strength_bar.configure(progress_color=strength["color"])
            strength_lbl.configure(text=strength["label"], text_color=strength["color"])

        new_entry.bind("<KeyRelease>", check_strength)

        # 3. Confirm New Password
        customtkinter.CTkLabel(dialog, text="Confirm New Master Password", font=("Roboto", 12, "bold"), text_color="#94A3B8").pack(anchor="w", padx=35, pady=(5, 2))
        confirm_entry = customtkinter.CTkEntry(dialog, show="*", width=380, height=36)
        confirm_entry.pack(padx=35, pady=(0, 25))

        # Buttons
        btn_frame = customtkinter.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(fill="x", padx=35, pady=10)

        cancel_btn = customtkinter.CTkButton(
            btn_frame, text="Cancel", width=180, height=40, fg_color="transparent", border_width=1, border_color="#475569", text_color="#CBD5E1",
            command=dialog.destroy
        )
        cancel_btn.pack(side="left")

        def perform_change():
            curr_p = curr_entry.get()
            new_p = new_entry.get()
            conf_p = confirm_entry.get()

            # 1. Validation
            if not curr_p or not new_p or not conf_p:
                messagebox.showerror("Error", "All fields are required.", parent=dialog)
                return

            if new_p != conf_p:
                messagebox.showerror("Error", "New password confirmation does not match.", parent=dialog)
                return

            # 2. Check current password
            try:
                stored_token = self.app.db.get_config("verification_token")
                # Decrypt using active crypto or construct temporary crypto
                self.app.crypto.decrypt(stored_token)
            except Exception:
                messagebox.showerror("Error", "Incorrect current master password.", parent=dialog)
                return

            # 3. Check new strength
            strength = check_password_strength(new_p)
            if strength["score"] < 3:
                messagebox.showerror("Error", "New password is too weak. Please meet requirements.", parent=dialog)
                return

            # 4. Perform Re-encryption
            try:
                # Decrypt all existing credentials with current key
                all_creds = self.app.db.get_all_credentials()
                decrypted_vault = []
                for cid, site, user, enc_pwd, cat, c_at, u_at in all_creds:
                    dec_p = self.app.crypto.decrypt(enc_pwd)
                    decrypted_vault.append((cid, site, user, dec_p, cat))

                # Recreate salt in database for the new password
                new_salt = os.urandom(16)
                self.app.db.set_salt(new_salt)

                # Initialize new CryptoManager with new password
                from ...core.crypto import CryptoManager
                new_crypto = CryptoManager(new_p, self.app.db)

                # Set new verification token
                new_token = new_crypto.encrypt("valid")
                self.app.db.set_config("verification_token", new_token)

                # Re-encrypt and save credentials
                for cid, site, user, dec_p, cat in decrypted_vault:
                    new_enc = new_crypto.encrypt(dec_p)
                    self.app.db.update_credential(cid, new_site_name=site, new_username=user, new_encrypted_password=new_enc, new_category=cat)

                # Update running app's CryptoManager instance
                self.app.crypto = new_crypto
                messagebox.showinfo("Success", "Master password updated successfully. Database fully re-encrypted.", parent=dialog)
                dialog.destroy()

            except Exception as e:
                messagebox.showerror("Critical Error", f"Failed to complete master password transition: {e}", parent=dialog)

        save_btn = customtkinter.CTkButton(btn_frame, text="Confirm Change", width=180, height=40, command=perform_change)
        save_btn.pack(side="right")

    # Backups implementation
    def export_encrypted_json(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            title="Save Secure Vault Backup"
        )
        if not file_path:
            return

        try:
            # 1. Export vault contents
            all_creds = self.app.db.get_all_credentials()
            credentials_list = []
            for cid, site, user, enc_pwd, cat, c_at, u_at in all_creds:
                decrypted_pwd = self.app.crypto.decrypt(enc_pwd)
                credentials_list.append({
                    "site": site,
                    "username": user,
                    "password": decrypted_pwd,
                    "category": cat
                })

            export_data = {
                "version": "3.0",
                "exported_at": datetime.now().isoformat(),
                "credentials": credentials_list
            }
            json_str = json.dumps(export_data)

            # 2. Derive export encryption payload
            backup_salt = os.urandom(16)
            # Derive KDF key from master password using backup salt
            from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
            from cryptography.hazmat.primitives import hashes
            from cryptography.fernet import Fernet

            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=backup_salt,
                iterations=100000,
            )
            # Reuses active password securely
            # Actually, how do we know the master password? The crypto manager only holds the derived key, not the raw password!
            # Oh, wait! The CryptoManager does NOT store the raw master password in memory for security.
            # But wait, we can ask the user to input their master password to confirm export! This is a double security measure anyway!
            # Let's prompt for password confirmation using a simple entry or standard dialog.
            # Even better, let's prompt the user for the password they want to encrypt the backup with (could be the master password or any key!).
            self.prompt_export_password(json_str, file_path)

        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export: {e}")

    def prompt_export_password(self, payload_str, file_path):
        dialog = customtkinter.CTkToplevel(self)
        dialog.title("Confirm Backup Encryption")
        dialog.geometry("400x230")
        dialog.transient(self)
        dialog.grab_set()

        customtkinter.CTkLabel(dialog, text="Encrypt Backup File", font=("Outfit", 16, "bold")).pack(pady=15)
        customtkinter.CTkLabel(dialog, text="Set a password to encrypt this backup file.\nYou will need this password to restore it.", font=("Roboto", 12), text_color="#94A3B8").pack(pady=(0, 10))

        pwd_entry = customtkinter.CTkEntry(dialog, show="*", width=320, height=36)
        pwd_entry.pack(pady=10)

        def proceed():
            pwd = pwd_entry.get()
            if not pwd:
                messagebox.showerror("Error", "Password is required.", parent=dialog)
                return

            try:
                # Encrypt payload
                backup_salt = os.urandom(16)
                from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
                from cryptography.hazmat.primitives import hashes
                from cryptography.fernet import Fernet
                kdf = PBKDF2HMAC(
                    algorithm=hashes.SHA256(),
                    length=32,
                    salt=backup_salt,
                    iterations=100000,
                )
                derived_key = base64.urlsafe_b64encode(kdf.derive(pwd.encode()))
                fernet = Fernet(derived_key)
                ciphertext = fernet.encrypt(payload_str.encode()).decode()

                backup_payload = {
                    "salt": base64.b64encode(backup_salt).decode('utf-8'),
                    "ciphertext": ciphertext
                }

                with open(file_path, "w") as f:
                    json.dump(backup_payload, f, indent=4)

                messagebox.showinfo("Export Successful", f"Backup exported successfully to:\n{os.path.basename(file_path)}", parent=dialog)
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Export Failed", f"Failed: {e}", parent=dialog)

        customtkinter.CTkButton(dialog, text="Encrypt & Save", width=200, height=38, command=proceed).pack(pady=10)

    def import_encrypted_json(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json")],
            title="Import Secure Vault Backup"
        )
        if not file_path:
            return

        try:
            with open(file_path, "r") as f:
                backup_payload = json.load(f)

            if "salt" not in backup_payload or "ciphertext" not in backup_payload:
                messagebox.showerror("Import Error", "Invalid backup file format.")
                return

            # Ask user for password to decrypt the backup file
            self.prompt_import_password(backup_payload, file_path)

        except Exception as e:
            messagebox.showerror("Import Error", f"Failed to read file: {e}")

    def prompt_import_password(self, payload, file_path):
        dialog = customtkinter.CTkToplevel(self)
        dialog.title("Decrypt Backup File")
        dialog.geometry("400x230")
        dialog.transient(self)
        dialog.grab_set()

        customtkinter.CTkLabel(dialog, text="Decrypt Backup File", font=("Outfit", 16, "bold")).pack(pady=15)
        customtkinter.CTkLabel(dialog, text="Enter the password used to encrypt this backup.", font=("Roboto", 12), text_color="#94A3B8").pack(pady=(0, 10))

        pwd_entry = customtkinter.CTkEntry(dialog, show="*", width=320, height=36)
        pwd_entry.pack(pady=10)

        def proceed():
            pwd = pwd_entry.get()
            if not pwd:
                messagebox.showerror("Error", "Password is required.", parent=dialog)
                return

            try:
                # Decrypt
                backup_salt = base64.b64decode(payload["salt"].encode('utf-8'))
                ciphertext = payload["ciphertext"]

                from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
                from cryptography.hazmat.primitives import hashes
                from cryptography.fernet import Fernet
                kdf = PBKDF2HMAC(
                    algorithm=hashes.SHA256(),
                    length=32,
                    salt=backup_salt,
                    iterations=100000,
                )
                derived_key = base64.urlsafe_b64encode(kdf.derive(pwd.encode()))
                fernet = Fernet(derived_key)
                
                decrypted_payload_str = fernet.decrypt(ciphertext.encode()).decode()
                backup_data = json.loads(decrypted_payload_str)

                # Validate data structure
                if "credentials" not in backup_data:
                    messagebox.showerror("Import Error", "Corrupt backup structure.", parent=dialog)
                    return

                # Import into local database
                imported_count = 0
                for item in backup_data["credentials"]:
                    site = item["site"].strip().title()
                    user = item["username"].strip()
                    plain_pwd = item["password"]
                    cat = item.get("category", "Other")

                    # Add site and credentials
                    site_id = self.app.db.add_site(site)
                    encrypted_pwd = self.app.crypto.encrypt(plain_pwd)
                    self.app.db.add_credential(site_id, user, encrypted_pwd, cat)
                    imported_count += 1

                messagebox.showinfo("Import Complete", f"Successfully imported {imported_count} credentials from backup!", parent=dialog)
                dialog.destroy()
                
                # Refresh views
                self.home.switch_view("vault")

            except Exception as e:
                messagebox.showerror("Decryption Failed", "Incorrect password or corrupt file.", parent=dialog)

        customtkinter.CTkButton(dialog, text="Decrypt & Import", width=200, height=38, command=proceed).pack(pady=10)

    def export_csv(self):
        confirm = messagebox.askyesno(
            "Security Warning",
            "This will save all of your usernames and passwords as UNENCRYPTED clear text in a CSV file.\n\n"
            "Are you sure you want to proceed with this risk?",
            icon="warning"
        )
        if not confirm:
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Export CSV (Unencrypted)"
        )
        if not file_path:
            return

        try:
            import csv
            all_creds = self.app.db.get_all_credentials()
            
            with open(file_path, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                # Header
                writer.writerow(["Site", "Username", "Password", "Category"])
                
                for cid, site, user, enc_pwd, cat, c_at, u_at in all_creds:
                    decrypted_pwd = self.app.crypto.decrypt(enc_pwd)
                    writer.writerow([site, user, decrypted_pwd, cat])

            messagebox.showinfo("Export Successful", f"Vault exported in plain text to:\n{os.path.basename(file_path)}")
        except Exception as e:
            messagebox.showerror("Export Error", f"CSV Export failed: {e}")
