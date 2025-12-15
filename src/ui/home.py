import customtkinter
from .add import AddFrame
from .view import ViewFrame

class HomeFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master_app = master

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0) # Sidebar
        self.grid_columnconfigure(1, weight=1) # Main Area

        # Sidebar
        self.sidebar = customtkinter.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = customtkinter.CTkLabel(self.sidebar, text="PassVault", font=("Roboto", 20, "bold"))
        self.logo_label.pack(pady=30)
        
        self.add_button = customtkinter.CTkButton(self.sidebar, text="Add Password", command=self.master_app.show_add)
        self.add_button.pack(pady=10, padx=20)
        
        self.view_button = customtkinter.CTkButton(self.sidebar, text="My Passwords", command=self.master_app.show_view)
        self.view_button.pack(pady=10, padx=20)
        
        self.spacer = customtkinter.CTkLabel(self.sidebar, text="")
        self.spacer.pack(pady=20, expand=True) # Push logout to bottom
        
        self.logout_button = customtkinter.CTkButton(self.sidebar, text="Log Out", fg_color="transparent", border_width=2,
                                                     text_color=("gray10", "#DCE4EE"), command=self.master_app.logout)
        self.logout_button.pack(pady=20, padx=20, side="bottom")

        # Main Content - Dashboard
        self.main_area = customtkinter.CTkFrame(self, fg_color="transparent")
        self.main_area.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        self.welcome_label = customtkinter.CTkLabel(self.main_area, text="Welcome to your Safe.", font=("Roboto", 24))
        self.welcome_label.pack(pady=40)

        # Quick Stats (optional)
        # count = len(self.master_app.db.get_sites())
        # self.stats_label = customtkinter.CTkLabel(self.main_area, text=f"Protected Sites: {count}")
        # self.stats_label.pack()
