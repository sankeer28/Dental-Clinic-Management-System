import tkinter as tk
import customtkinter as ctk
import cx_Oracle
from tkinter import messagebox
import logging

class DatabaseConnectionDialog:
    def __init__(self, parent=None):
        # Create dialog window
        self.parent = parent
        if parent:
            self.dialog = ctk.CTkToplevel(parent)
            self.dialog.transient(parent)
        else:
            self.dialog = ctk.CTk()
        
        self.dialog.title("Database Connection")
        self.dialog.geometry("500x600")
        self.dialog.resizable(False, False)
        
        # Center the window
        self.center_window()
        
        # Create main frame
        main_frame = ctk.CTkFrame(self.dialog)
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Connection fields with more detailed labels
        fields = [
            ("Oracle Username", "username"),
            ("Oracle Password", "password"),
            ("Database Host", "host"),
            ("Database Port", "port"),
            ("SID (Service ID)", "sid")
        ]
        
        self.entries = {}
        
        # Create entry fields
        for label_text, key in fields:
            frame = ctk.CTkFrame(main_frame)
            frame.pack(fill='x', pady=5)
            
            label = ctk.CTkLabel(frame, text=label_text, width=150, anchor='w')
            label.pack(side='left', padx=(0, 10))
            
            # Use password entry for password field
            if key == 'password':
                entry = ctk.CTkEntry(frame, show="*", width=300)
            else:
                entry = ctk.CTkEntry(frame, width=300)
            
            entry.pack(side='left', expand=True, fill='x')
            
            # Set default values with helpful placeholders
            defaults = {
                'host': 'oracle.scs.ryerson.ca',
                'port': '1521',
                'sid': 'orcl'
            }
            
            if key in defaults:
                entry.insert(0, defaults[key])
            
            self.entries[key] = entry
        
        # Add a help text
        help_text = (
            "Connection Help:\n"
            "- Ensure you have the correct Oracle database credentials\n"
            "- Check your network connection\n"
            "- Verify host, port, and SID with your database administrator"
        )
        help_label = ctk.CTkLabel(main_frame, text=help_text, justify='left', font=('Arial', 10))
        help_label.pack(pady=10)
        
        # Connection status label
        self.status_label = ctk.CTkLabel(main_frame, text="", text_color="green")
        self.status_label.pack(pady=10)
        
        # Button frame
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(fill='x', pady=10)
        
        # Connect button
        connect_btn = ctk.CTkButton(
            btn_frame, 
            text="Connect", 
            command=self.test_connection,
            fg_color="green"
        )
        connect_btn.pack(side='left', expand=True, padx=5)
        
        # Cancel button
        cancel_btn = ctk.CTkButton(
            btn_frame, 
            text="Cancel", 
            command=self.on_cancel,
            fg_color="red"
        )
        cancel_btn.pack(side='left', expand=True, padx=5)
        
        # Connection result
        self.connection_successful = False
        self.connection_params = {}
        
        # If no parent, start main loop
        if not parent:
            self.dialog.mainloop()
    
    def center_window(self):
        """Center the window on the screen"""
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        x = (self.dialog.winfo_screenwidth() - width) // 2
        y = (self.dialog.winfo_screenheight() - height) // 2
        self.dialog.geometry(f'+{x}+{y}')
    
    def on_cancel(self):
        """Handle cancel button"""
        self.connection_successful = False
        if self.parent:
            self.parent.grab_release()
        self.dialog.destroy()
    
    def test_connection(self):
        """Test database connection"""
        # Collect connection parameters
        connection_params = {
            key: entry.get().strip() 
            for key, entry in self.entries.items()
        }
        
        # Validate required fields
        required_fields = ['username', 'password', 'host', 'port', 'sid']
        for field in required_fields:
            if not connection_params[field]:
                messagebox.showerror("Error", f"{field.capitalize()} is required")
                return
        
        try:
            # Create DSN (Data Source Name)
            dsn = cx_Oracle.makedsn(
                host=connection_params['host'],
                port=int(connection_params['port']),
                sid=connection_params['sid']
            )
            
            # Attempt connection
            connection = cx_Oracle.connect(
                user=connection_params['username'],
                password=connection_params['password'],
                dsn=dsn
            )
            
            # Close test connection
            connection.close()
            
            # Update connection parameters
            self.connection_params = connection_params
            self.connection_successful = True
            
            # Update status label
            self.status_label.configure(
                text="Connection Successful!", 
                text_color="green"
            )
            
            # Close dialog
            self.dialog.destroy()
        
        except cx_Oracle.Error as error:
            # Connection failed
            error_message = str(error)
            
            # Update status label
            self.status_label.configure(
                text=f"Connection Failed: {error_message}", 
                text_color="red"
            )
            
            # Show detailed error message
            detailed_error = (
                f"Connection Error: {error_message}\n\n"
                "Possible reasons:\n"
                "- Incorrect username or password\n"
                "- Network connectivity issues\n"
                "- Database server is down\n"
                "- Incorrect host, port, or SID"
            )
            
            messagebox.showerror("Connection Error", detailed_error)
    
    def get_connection_params(self):
        """Return connection parameters if successful"""
        return self.connection_params if self.connection_successful else None

def update_db_config(connection_params):
    """Update DB_CONFIG with new connection parameters"""
    from config import DB_CONFIG
    DB_CONFIG.update(connection_params)
