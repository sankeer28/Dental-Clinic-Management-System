import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import customtkinter as ctk
import logging
from datetime import datetime
import cx_Oracle

class DentalClinicGUI:
    def __init__(self, root, db_manager):
        self.root = root
        self.root.title("Dental Clinic Management System")
        self.root.geometry("1400x900")

        self.db_manager = db_manager
        
        # Tracking current table and columns
        self.current_table = tk.StringVar()
        self.table_columns = []

        # Setup UI with both modern and traditional elements
        self.setup_ui()

    def setup_ui(self):
        # Main frame
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Table Selection Frame
        table_frame = ctk.CTkFrame(main_frame)
        table_frame.pack(fill=tk.X, padx=10, pady=5)

        # Table Selection Label and Dropdown
        ctk.CTkLabel(table_frame, text="Select Table:").pack(side=tk.LEFT)

        tables = [
            "Clinic", "Staff", "Dentist", "Receptionist", 
            "Patient", "Appointment", "Treatment", 
            "Medical_Record", "Billing"
        ]

        self.table_dropdown = ctk.CTkComboBox(
            table_frame, 
            values=tables,
            command=self.on_table_select
        )
        self.table_dropdown.pack(side=tk.LEFT, padx=5)

        # Database Operations Frame
        db_frame = ctk.CTkFrame(main_frame)
        db_frame.pack(fill=tk.X, padx=10, pady=5)

        # Buttons for database operations
        db_operations = [
            ("Drop Tables", self.drop_tables),
            ("Create Tables", self.create_tables),
            ("Populate Tables", self.populate_tables),
            ("Add Record", self.add_record),
            ("Edit Record", self.edit_record),
            ("Delete Record", self.delete_record)
        ]

        for text, command in db_operations:
            ctk.CTkButton(db_frame, text=text, command=command).pack(side=tk.LEFT, padx=5)

        # Data Display Area
        self.data_frame = ctk.CTkFrame(main_frame)
        self.data_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Treeview for displaying data
        self.tree = ttk.Treeview(self.data_frame)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Scrollbar for Treeview
        scrollbar = ttk.Scrollbar(self.data_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)

    def on_table_select(self, event=None):
        """
        Handle table selection and fetch columns
        """
        selected_table = self.table_dropdown.get()
        if selected_table:
            try:
                # Fetch columns for the selected table
                cursor = self.db_manager.execute_query(f"SELECT * FROM {selected_table} WHERE 1=0")
                self.table_columns = [desc[0] for desc in cursor.description]
                
                # Display table data
                self.display_table_data(selected_table)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to fetch table columns: {str(e)}")

    def display_table_data(self, table_name):
        """
        Display data for the selected table
        """
        # Clear existing treeview
        for i in self.tree.get_children():
            self.tree.delete(i)

        try:
            cursor = self.db_manager.execute_query(f"SELECT * FROM {table_name}")
            
            if cursor:
                columns = [desc[0] for desc in cursor.description]
                
                self.tree['columns'] = columns
                self.tree['show'] = 'headings'
                
                for col in columns:
                    self.tree.heading(col, text=col)
                    self.tree.column(col, width=100)
                
                for row in cursor:
                    self.tree.insert('', 'end', values=row)
            else:
                messagebox.showwarning("Warning", "No data found or query failed")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to retrieve data: {str(e)}")

    def add_record(self):
        """
        Add a new record to the selected table
        """
        selected_table = self.table_dropdown.get()
        if not selected_table:
            messagebox.showwarning("Warning", "Please select a table first")
            return

        # Create input dialog
        add_dialog = ctk.CTkToplevel(self.root)
        add_dialog.title(f"Add Record to {selected_table}")
        add_dialog.geometry("500x600")

        # Create entry fields for each column
        entries = {}
        for col in self.table_columns:
            frame = ctk.CTkFrame(add_dialog)
            frame.pack(fill=tk.X, padx=10, pady=5)
            
            ctk.CTkLabel(frame, text=col, width=150, anchor='w').pack(side=tk.LEFT)
            entry = ctk.CTkEntry(frame, width=250)
            entry.pack(side=tk.LEFT)
            entries[col] = entry

        def save_record():
            try:
                # Collect values from entries
                values = [entries[col].get() for col in self.table_columns]
                
                # Prepare insert query
                placeholders = ','.join([':%d' % (i+1) for i in range(len(self.table_columns))])
                query = f"INSERT INTO {selected_table} ({','.join(self.table_columns)}) VALUES ({placeholders})"
                
                # Execute insert
                cursor = self.db_manager.execute_query(query, values)
                
                if cursor:
                    messagebox.showinfo("Success", "Record added successfully")
                    add_dialog.destroy()
                    # Refresh the table view
                    self.display_table_data(selected_table)
                else:
                    messagebox.showerror("Error", "Failed to add record")
            
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add record: {str(e)}")

        # Save and Cancel buttons
        save_btn = ctk.CTkButton(add_dialog, text="Save", command=save_record)
        save_btn.pack(pady=10)
        cancel_btn = ctk.CTkButton(add_dialog, text="Cancel", command=add_dialog.destroy)
        cancel_btn.pack(pady=10)

    def edit_record(self):
        """
        Edit an existing record
        """
        selected_table = self.table_dropdown.get()
        if not selected_table:
            messagebox.showwarning("Warning", "Please select a table first")
            return

        # Get selected item
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a record to edit")
            return

        # Create edit dialog
        edit_dialog = ctk.CTkToplevel(self.root)
        edit_dialog.title(f"Edit Record in {selected_table}")
        edit_dialog.geometry("500x600")

        # Get selected row values
        selected_values = self.tree.item(selected_item[0])['values']

        # Create entry fields for each column
        entries = {}
        for col, value in zip(self.table_columns, selected_values):
            frame = ctk.CTkFrame(edit_dialog)
            frame.pack(fill=tk.X, padx=10, pady=5)
            
            ctk.CTkLabel(frame, text=col, width=150, anchor='w').pack(side=tk.LEFT)
            entry = ctk.CTkEntry(frame, width=250)
            entry.insert(0, str(value))
            entry.pack(side=tk.LEFT)
            entries[col] = entry

        def save_edited_record():
            try:
                # Collect updated values
                updated_values = [entries[col].get() for col in self.table_columns]
                
                # Prepare update query (using first column as primary key)
                primary_key_col = self.table_columns[0]
                update_columns = [f"{col} = :{i+1}" for i, col in enumerate(self.table_columns[1:])]
                query = f"""
                UPDATE {selected_table} 
                SET {', '.join(update_columns)} 
                WHERE {primary_key_col} = :{len(self.table_columns)}
                """
                
                # Rearrange values to match query (move primary key to end)
                query_values = updated_values[1:] + [updated_values[0]]
                cursor = self.db_manager.execute_query(query, query_values)
                
                if cursor:
                    messagebox.showinfo("Success", "Record updated successfully")
                    edit_dialog.destroy()
                    # Refresh the table view
                    self.display_table_data(selected_table)
                else:
                    messagebox.showerror("Error", "Failed to update record")
            
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update record: {str(e)}")

        # Save and Cancel buttons
        save_btn = ctk.CTkButton(edit_dialog, text="Save", command=save_edited_record)
        save_btn.pack(pady=10)
        cancel_btn = ctk.CTkButton(edit_dialog, text="Cancel", command=edit_dialog.destroy)
        cancel_btn.pack(pady=10)

    def delete_record(self):
        """
        Delete a selected record
        """
        selected_table = self.table_dropdown.get()
        if not selected_table:
            messagebox.showwarning("Warning", "Please select a table first")
            return

        # Get selected item
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a record to delete")
            return

        # Confirm deletion
        if not messagebox.askyesno("Confirm", "Are you sure you want to delete this record?"):
            return

        try:
            # Get selected row values
            selected_values = self.tree.item(selected_item[0])['values']
            
            # Prepare delete query (using first column as primary key)
            primary_key_col = self.table_columns[0]
            query = f"DELETE FROM {selected_table} WHERE {primary_key_col} = :1"
            
            # Execute delete
            cursor = self.db_manager.execute_query(query, [selected_values[0]])
            
            if cursor:
                messagebox.showinfo("Success", "Record deleted successfully")
                # Refresh the table view
                self.display_table_data(selected_table)
            else:
                messagebox.showerror("Error", "Failed to delete record")
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete record: {str(e)}")

    def drop_tables(self):
        """
        Drop all tables
        """
        try:
            if self.db_manager.drop_tables():
                messagebox.showinfo("Success", "All tables dropped successfully")
                # Clear the treeview
                for i in self.tree.get_children():
                    self.tree.delete(i)
            else:
                messagebox.showerror("Error", "Failed to drop tables")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def create_tables(self):
        """
        Create database tables
        """
        try:
            if self.db_manager.create_tables():
                messagebox.showinfo("Success", "Tables created successfully")
            else:
                messagebox.showerror("Error", "Failed to create tables")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def populate_tables(self):
        """
        Populate tables with sample data
        """
        try:
            if self.db_manager.populate_tables():
                messagebox.showinfo("Success", "Tables populated successfully")
            else:
                messagebox.showerror("Error", "Failed to populate tables")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def view_data(self):
        selected_table = self.table_dropdown.get()
        if selected_table:
            self.display_table_data(selected_table)
        else:
            messagebox.showwarning("Warning", "Please select a table first")

def main():
    import tkinter as tk
    from database import DatabaseManager

    root = tk.Tk()
    db_manager = DatabaseManager()
    app = DentalClinicGUI(root, db_manager)
    root.mainloop()

if __name__ == "__main__":
    main()
