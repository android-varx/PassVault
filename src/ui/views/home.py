import customtkinter
from .dashboard import DashboardView
from .view import CredentialsView
from .add import AddView
from .generator import GeneratorView
from .settings import SettingsView

class HomeFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.master_app = master

        # Grid configuration: 2 columns (sidebar & main content)
        self.grid_columnconfigure(0, weight=0) # Sidebar
        self.grid_columnconfigure(1, weight=1) # Main View
        self.grid_rowconfigure(0, weight=1)

        # 1. Sidebar Frame
        self.sidebar = customtkinter.CTkFrame(self, width=240, corner_radius=0, fg_color="#181824")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(6, weight=1) # Push logout button to the bottom

        # Logo text
        self.logo_lbl = customtkinter.CTkLabel(self.sidebar, text="🔒 PassVault", font=("Outfit", 22, "bold"), text_color="#7C4DFF")
        self.logo_lbl.grid(row=0, column=0, padx=25, pady=(35, 30), sticky="w")

        # Sidebar Buttons
        self.nav_buttons = {}
        
        nav_configs = [
            ("Dashboard", "dashboard", 1),
            ("My Passwords", "vault", 2),
            ("Add Password", "add", 3),
            ("Password Generator", "generator", 4),
            ("Settings", "settings", 5)
        ]

        for text, key, row in nav_configs:
            btn = customtkinter.CTkButton(
                self.sidebar, 
                text=text, 
                font=("Roboto", 14, "normal"),
                anchor="w",
                height=42,
                fg_color="transparent",
                text_color="#CBD5E1",
                hover_color="#2A2A3F",
                command=lambda k=key: self.switch_view(k)
            )
            btn.grid(row=row, column=0, padx=15, pady=6, sticky="ew")
            self.nav_buttons[key] = btn

        # Log Out Button
        self.logout_btn = customtkinter.CTkButton(
            self.sidebar,
            text="Log Out",
            font=("Roboto", 14),
            fg_color="transparent",
            border_width=1,
            border_color="#EF4444",
            text_color="#EF4444",
            hover_color="#2E1619",
            height=40,
            command=self.master_app.logout
        )
        self.logout_btn.grid(row=7, column=0, padx=20, pady=25, sticky="ew")

        # 2. Main Content Area
        self.content_container = customtkinter.CTkFrame(self, fg_color="transparent")
        self.content_container.grid(row=0, column=1, sticky="nsew", padx=25, pady=25)
        self.content_container.grid_rowconfigure(0, weight=1)
        self.content_container.grid_columnconfigure(0, weight=1)

        self.current_subview = None

        # Load default view (Dashboard)
        self.switch_view("dashboard")

    def switch_view(self, key):
        # Clear previous subview
        if self.current_subview:
            self.current_subview.destroy()
        self.current_subview = None

        # Load appropriate view
        if key == "dashboard":
            self.current_subview = DashboardView(self.content_container, self.master_app, self)
        elif key == "vault":
            self.current_subview = CredentialsView(self.content_container, self.master_app, self)
        elif key == "add":
            self.current_subview = AddView(self.content_container, self.master_app, self)
        elif key == "generator":
            self.current_subview = GeneratorView(self.content_container, self.master_app, self)
        elif key == "settings":
            self.current_subview = SettingsView(self.content_container, self.master_app, self)

        if self.current_subview:
            self.current_subview.grid(row=0, column=0, sticky="nsew")

        # Highlight current button
        for k, btn in self.nav_buttons.items():
            if k == key:
                btn.configure(fg_color="#7C4DFF", text_color="#FFFFFF", hover_color="#651FFF")
            else:
                btn.configure(fg_color="transparent", text_color="#CBD5E1", hover_color="#2A2A3F")
