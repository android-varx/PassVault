import customtkinter
from tkinter import Canvas
from ...core.security import VaultAuditor

class DashboardView(customtkinter.CTkFrame):
    def __init__(self, master, app_instance, home_frame):
        super().__init__(master, fg_color="transparent")
        self.app = app_instance
        self.home = home_frame

        # Run Security Audit
        self.auditor = VaultAuditor(self.app.db, self.app.crypto)
        self.audit_results = self.auditor.run_audit()

        # Layout: Top title, middle row (score & stats cards), bottom row (alerts scrollbox)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0) # Header
        self.grid_rowconfigure(1, weight=0) # Stats Row
        self.grid_rowconfigure(2, weight=1) # Audits Row

        # Header
        self.header_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        self.title_lbl = customtkinter.CTkLabel(self.header_frame, text="Security Dashboard", font=("Outfit", 26, "bold"))
        self.title_lbl.pack(anchor="w")
        self.subtitle_lbl = customtkinter.CTkLabel(
            self.header_frame, 
            text="Review your overall password health and security alerts.", 
            font=("Roboto", 13), 
            text_color="#94A3B8"
        )
        self.subtitle_lbl.pack(anchor="w", pady=(2, 0))

        # Stats Container (Grid)
        self.stats_container = customtkinter.CTkFrame(self, fg_color="transparent")
        self.stats_container.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        self.stats_container.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="equal")

        # Get values
        score = self.audit_results["security_score"]
        total = self.audit_results["total_accounts"]
        weak = len(self.audit_results["weak_accounts"])
        reused = len(self.audit_results["reused_accounts"])
        old = len(self.audit_results["old_accounts"])

        # Score Color selection
        if score >= 80:
            score_color = "#10B981" # Green
            score_status = "Good"
        elif score >= 50:
            score_color = "#F59E0B" # Orange
            score_status = "Risk"
        else:
            score_color = "#EF4444" # Red
            score_status = "Critical"

        # Card 0: Security Score
        self.score_card = customtkinter.CTkFrame(self.stats_container, height=120, fg_color="#181824")
        self.score_card.grid(row=0, column=0, padx=(0, 10), sticky="nsew")
        self.score_card.pack_propagate(False)
        
        customtkinter.CTkLabel(self.score_card, text="Security Score", font=("Roboto", 12, "normal"), text_color="#94A3B8").pack(pady=(12, 2))
        self.score_val = customtkinter.CTkLabel(self.score_card, text=f"{score}%", font=("Outfit", 32, "bold"), text_color=score_color)
        self.score_val.pack()
        self.score_bar = customtkinter.CTkProgressBar(self.score_card, width=120, height=8, progress_color=score_color)
        self.score_bar.pack(pady=5)
        self.score_bar.set(score / 100.0)

        # Card 1: Total Accounts
        self.total_card = customtkinter.CTkFrame(self.stats_container, height=120, fg_color="#181824")
        self.total_card.grid(row=0, column=1, padx=5, sticky="nsew")
        self.total_card.pack_propagate(False)
        customtkinter.CTkLabel(self.total_card, text="Total Passwords", font=("Roboto", 12, "normal"), text_color="#94A3B8").pack(pady=(12, 5))
        customtkinter.CTkLabel(self.total_card, text=str(total), font=("Outfit", 36, "bold"), text_color="#F8F9FA").pack()
        
        # Card 2: Weak Passwords
        self.weak_card = customtkinter.CTkFrame(self.stats_container, height=120, fg_color="#181824")
        self.weak_card.grid(row=0, column=2, padx=5, sticky="nsew")
        self.weak_card.pack_propagate(False)
        customtkinter.CTkLabel(self.weak_card, text="Weak Passwords", font=("Roboto", 12, "normal"), text_color="#94A3B8").pack(pady=(12, 5))
        customtkinter.CTkLabel(self.weak_card, text=str(weak), font=("Outfit", 36, "bold"), text_color="#EF4444" if weak > 0 else "#10B981").pack()

        # Card 3: Reused Passwords
        self.reused_card = customtkinter.CTkFrame(self.stats_container, height=120, fg_color="#181824")
        self.reused_card.grid(row=0, column=3, padx=(10, 0), sticky="nsew")
        self.reused_card.pack_propagate(False)
        customtkinter.CTkLabel(self.reused_card, text="Reused Passwords", font=("Roboto", 12, "normal"), text_color="#94A3B8").pack(pady=(12, 5))
        customtkinter.CTkLabel(self.reused_card, text=str(reused), font=("Outfit", 36, "bold"), text_color="#F59E0B" if reused > 0 else "#10B981").pack()

        # Bottom Area: Security Alerts List
        self.alerts_frame = customtkinter.CTkFrame(self, fg_color="#181824")
        self.alerts_frame.grid(row=2, column=0, sticky="nsew")
        self.alerts_frame.grid_columnconfigure(0, weight=1)
        self.alerts_frame.grid_rowconfigure(0, weight=0) # Title
        self.alerts_frame.grid_rowconfigure(1, weight=1) # Scrollable area

        customtkinter.CTkLabel(
            self.alerts_frame, 
            text="Security Actions Required", 
            font=("Outfit", 16, "bold")
        ).grid(row=0, column=0, padx=20, pady=(15, 10), sticky="w")

        # Scroll Box
        self.scroll_frame = customtkinter.CTkScrollableFrame(self.alerts_frame, fg_color="transparent")
        self.scroll_frame.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))

        self.populate_alerts(weak, reused, old)

    def populate_alerts(self, weak_count, reused_count, old_count):
        # Clear children
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        if weak_count == 0 and reused_count == 0 and old_count == 0:
            # All Good Panel
            all_clear_card = customtkinter.CTkFrame(self.scroll_frame, fg_color="#10B981", height=100, corner_radius=8)
            all_clear_card.pack(fill="x", pady=10, padx=5)
            
            lbl = customtkinter.CTkLabel(
                all_clear_card, 
                text="🎉 Safe and sound! No security vulnerabilities detected in your vault.",
                font=("Roboto", 15, "normal"),
                text_color="#FFFFFF"
            )
            lbl.pack(pady=35, padx=20)
            return

        # 1. Add Weak Password Alerts
        for issue in self.audit_results["weak_accounts"]:
            self.create_alert_card(
                site=issue["site"],
                username=issue["username"],
                issue_type="Weak Password",
                description=f"Strength score is {issue['score']}/5 ({issue['label']}). suggestions: {', '.join(issue['reasons'])}",
                color="#EF4444"
            )

        # 2. Add Reused Password Alerts
        for issue in self.audit_results["reused_accounts"]:
            for acc in issue["accounts"]:
                self.create_alert_card(
                    site=acc["site"],
                    username=acc["username"],
                    issue_type="Reused Password",
                    description=f"Shares the same password as {len(issue['accounts']) - 1} other account(s) (Preview: {issue['password_preview']}).",
                    color="#F59E0B"
                )

        # 3. Add Old Password Alerts
        for issue in self.audit_results["old_accounts"]:
            self.create_alert_card(
                site=issue["site"],
                username=issue["username"],
                issue_type="Old Password",
                description=f"This credential hasn't been updated in {issue['days_old']} days. Consider updating it.",
                color="#64748B"
            )

    def create_alert_card(self, site, username, issue_type, description, color):
        card = customtkinter.CTkFrame(self.scroll_frame, fg_color="#1E1E2F", height=75)
        card.pack(fill="x", pady=5, padx=5)
        
        # Color bar
        bar = customtkinter.CTkFrame(card, width=5, fg_color=color, corner_radius=0)
        bar.pack(side="left", fill="y")

        # Info Layout
        info_frame = customtkinter.CTkFrame(card, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True, padx=15, pady=8)

        title_lbl = customtkinter.CTkLabel(
            info_frame, 
            text=f"{site} • {username} - {issue_type}", 
            font=("Roboto", 13, "bold"), 
            text_color=color,
            anchor="w"
        )
        title_lbl.pack(anchor="w")

        desc_lbl = customtkinter.CTkLabel(
            info_frame, 
            text=description, 
            font=("Roboto", 11), 
            text_color="#94A3B8",
            anchor="w",
            justify="left",
            wraplength=450
        )
        desc_lbl.pack(anchor="w", pady=(2, 0))

        # Action Button to navigate directly
        fix_btn = customtkinter.CTkButton(
            card, 
            text="Fix", 
            width=60, 
            height=30, 
            fg_color="#3B3B54", 
            hover_color="#525270",
            text_color="#E5E7EB",
            command=lambda s=site: self.fix_alert(s)
        )
        fix_btn.pack(side="right", padx=15, pady=22)

    def fix_alert(self, site):
        # Redirect to credentials view and perform pre-search for the site
        self.home.switch_view("vault")
        # Find the loaded view and enter search
        if isinstance(self.home.current_subview, CredentialsView):
            self.home.current_subview.search_var.set(site)
            self.home.current_subview.trigger_search()
