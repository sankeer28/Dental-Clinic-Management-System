import tkinter as tk
import customtkinter as ctk
import logging
import sys
from database import DatabaseManager
from gui import DentalClinicGUI


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s: %(message)s',
        handlers=[
            logging.FileHandler('dental_clinic.log'),
            logging.StreamHandler()
        ]
    )

def main():
    # Configure CustomTkinter
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")

    # Set up logging
    setup_logging()

    try:
        # Initialize database manager
        db_manager = DatabaseManager()

        # Create root window
        root = ctk.CTk()
        root.title("Dental Clinic Management System")
        root.geometry("1400x900")

        # Initialize GUI
        app = DentalClinicGUI(root, db_manager)

        # Start the application
        root.mainloop()

    except Exception as e:
        logging.critical(f"Critical error in main application: {e}")
        print(f"Critical error: {e}")

if __name__ == "__main__":
    main()
