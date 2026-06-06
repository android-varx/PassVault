import customtkinter
from ...utils.helpers import generate_password, copy_to_clipboard
from ...core.security import check_password_strength

class GeneratorView(customtkinter.CTkFrame):
    def __init__(self, master, app_instance, home_frame):
        super().__init__(master, fg_color="transparent")
        self.app = app_instance
        self.home = home_frame

        # Centering layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Main Card Form
        self.card = customtkinter.CTkFrame(self, width=540, height=560, fg_color="#181824")
        self.card.grid(row=0, column=0, padx=20, pady=20)
        self.card.grid_propagate(False)
        self.card.grid_columnconfigure(0, weight=1)

        # Header
        self.title_lbl = customtkinter.CTkLabel(self.card, text="Password Generator", font=("Outfit", 22, "bold"))
        self.title_lbl.pack(pady=(25, 5))
        self.subtitle_lbl = customtkinter.CTkLabel(
            self.card, 
            text="Generate strong passwords with cryptographically secure algorithms.", 
            font=("Roboto", 13), 
            text_color="#94A3B8"
        )
        self.subtitle_lbl.pack(pady=(0, 20))

        # 1. Output Area Card
        self.output_frame = customtkinter.CTkFrame(self.card, fg_color="#20202F", height=110)
        self.output_frame.pack(fill="x", padx=40, pady=(0, 20))
        self.output_frame.pack_propagate(False)
        
        self.pwd_var = customtkinter.StringVar()
        self.pwd_display = customtkinter.CTkEntry(
            self.output_frame, 
            textvariable=self.pwd_var, 
            font=("Courier", 18, "bold"), 
            justify="center",
            fg_color="transparent",
            border_width=0,
            text_color="#F8F9FA"
        )
        self.pwd_display.pack(fill="x", padx=20, pady=(15, 5))
        
        # Output Action row
        self.out_actions = customtkinter.CTkFrame(self.output_frame, fg_color="transparent")
        self.out_actions.pack(fill="x", padx=20)

        self.strength_bar = customtkinter.CTkProgressBar(self.out_actions, width=150, height=6)
        self.strength_bar.pack(side="left", pady=12)
        
        self.strength_lbl = customtkinter.CTkLabel(self.out_actions, text="Empty", font=("Roboto", 11, "bold"), text_color="#94A3B8")
        self.strength_lbl.pack(side="left", padx=10, pady=2)

        self.copy_btn = customtkinter.CTkButton(
            self.out_actions, 
            text="Copy", 
            width=70, 
            height=26, 
            command=self.copy_generated
        )
        self.copy_btn.pack(side="right", padx=2, pady=2)

        # 2. Controls Area
        self.controls_frame = customtkinter.CTkFrame(self.card, fg_color="transparent")
        self.controls_frame.pack(fill="x", padx=45)

        # Slider length row
        self.len_row = customtkinter.CTkFrame(self.controls_frame, fg_color="transparent")
        self.len_row.pack(fill="x", pady=(10, 15))
        
        customtkinter.CTkLabel(self.len_row, text="Password Length:", font=("Roboto", 13, "bold"), text_color="#F8F9FA").pack(side="left")
        self.len_val_lbl = customtkinter.CTkLabel(self.len_row, text="16", font=("Courier", 14, "bold"), text_color="#7C4DFF")
        self.len_val_lbl.pack(side="right")

        self.slider = customtkinter.CTkSlider(
            self.controls_frame, 
            from_=8, 
            to=64, 
            number_of_steps=56, 
            command=self.update_length
        )
        self.slider.pack(fill="x", pady=(0, 20))
        self.slider.set(16)

        # Rule Checkboxes
        self.cb_upper = customtkinter.CTkCheckBox(self.controls_frame, text="Include Uppercase Letters (A-Z)", command=self.generate)
        self.cb_upper.pack(anchor="w", pady=5)
        self.cb_upper.select()

        self.cb_lower = customtkinter.CTkCheckBox(self.controls_frame, text="Include Lowercase Letters (a-z)", command=self.generate)
        self.cb_lower.pack(anchor="w", pady=5)
        self.cb_lower.select()
        self.cb_lower.configure(state="disabled") # Enforce lowercase always

        self.cb_digits = customtkinter.CTkCheckBox(self.controls_frame, text="Include Numbers (0-9)", command=self.generate)
        self.cb_digits.pack(anchor="w", pady=5)
        self.cb_digits.select()

        self.cb_symbols = customtkinter.CTkCheckBox(self.controls_frame, text="Include Symbols (e.g. @#$%!)", command=self.generate)
        self.cb_symbols.pack(anchor="w", pady=5)
        self.cb_symbols.select()

        self.cb_ambig = customtkinter.CTkCheckBox(self.controls_frame, text="Avoid Ambiguous Characters (e.g. l, 1, O, 0)", command=self.generate)
        self.cb_ambig.pack(anchor="w", pady=(5, 20))

        # Bottom Generator Trigger Button
        self.trigger_btn = customtkinter.CTkButton(
            self.card, 
            text="Generate Password", 
            font=("Roboto", 15, "bold"), 
            width=440, 
            height=44, 
            command=self.generate
        )
        self.trigger_btn.pack(pady=(10, 20))

        # Copy state label
        self.feedback_lbl = customtkinter.CTkLabel(self.card, text="", font=("Roboto", 12), text_color="#10B981")
        self.feedback_lbl.pack()

        # Generate initial password
        self.generate()

    def update_length(self, val):
        self.len_val_lbl.configure(text=str(int(val)))
        self.generate()

    def generate(self):
        length = int(self.slider.get())
        upper = self.cb_upper.get() == 1
        digits = self.cb_digits.get() == 1
        symbols = self.cb_symbols.get() == 1
        ambig = self.cb_ambig.get() == 1

        try:
            pwd = generate_password(
                length=length, 
                use_upper=upper, 
                use_digits=digits, 
                use_symbols=symbols, 
                exclude_ambiguous=ambig
            )
            self.pwd_var.set(pwd)

            # Update strength bar
            strength = check_password_strength(pwd)
            self.strength_bar.set(strength["score"] / 5.0)
            self.strength_bar.configure(progress_color=strength["color"])
            self.strength_lbl.configure(text=strength["label"], text_color=strength["color"])
            
            # Reset copy feedback
            self.feedback_lbl.configure(text="")
        except Exception as e:
            self.pwd_var.set("Select at least one character type")

    def copy_generated(self):
        pwd = self.pwd_var.get()
        if pwd and "Select" not in pwd:
            copy_to_clipboard(pwd, self.app, self.on_clipboard_cleared)
            self.feedback_lbl.configure(text="✓ Copied to clipboard! (Clears in 30s)", text_color="#10B981")

    def on_clipboard_cleared(self):
        try:
            if self.winfo_exists():
                self.feedback_lbl.configure(text="ⓘ Clipboard cleared for security.", text_color="#94A3B8")
        except Exception:
            pass
