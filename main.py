import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import logging
import sys
from database import DatabaseManager
from database_connection import DatabaseConnectionDialog, update_db_config
from gui import DentalClinicGUI
from config import DB_CONFIG

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s: %(message)s',
        handlers=[
            logging.FileHandler('dental_clinic.log'),
            logging.StreamHandler()
        ]
    )

def show_error_dialog(title, message):
    """
    Show an error dialog using tkinter messagebox
    Ensures a root window exists before showing the dialog
    """
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    messagebox.showerror(title, message)
    root.destroy()

def main():
    # Configure CustomTkinter
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")

    # Set up logging
    setup_logging()

    try:
        # Create main root window
        root = ctk.CTk()

        # Ensure database connection
        try:
            # Check if DB_CONFIG is empty or not properly configured
            if not DB_CONFIG or all(not str(value).strip() for value in DB_CONFIG.values()):
                connection_dialog = DatabaseConnectionDialog(root)
                
                # Wait for dialog to complete
                root.wait_window(connection_dialog.dialog)
                
                # Check if connection was successful
                connection_params = connection_dialog.get_connection_params()
                
                if not connection_params:
                    # Connection failed or cancelled
                    show_error_dialog("Connection Error", "Database connection is required to proceed.")
                    sys.exit(1)
                
                # Update DB_CONFIG
                update_db_config(connection_params)

            # Initialize database manager
            db_manager = DatabaseManager()

            # Set up main window
            root.title("Dental Clinic Management System")
            root.geometry("1400x900")

            # Initialize and show GUI
            app = DentalClinicGUI(root, db_manager)

            # Start the application
            root.mainloop()

        except Exception as db_error:
            # Show specific database connection error
            show_error_dialog("Database Connection Error", str(db_error))
            sys.exit(1)

    except Exception as e:
        logging.critical(f"Critical error in main application: {e}")
        show_error_dialog("Critical Error", str(e))
        sys.exit(1)

if __name__ == "__main__":
    main()
