import os
import sys

# Ensure src is in path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.ui.app import App

if __name__ == "__main__":
    app = App()
    app.mainloop()
