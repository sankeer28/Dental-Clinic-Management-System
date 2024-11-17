import cx_Oracle
import logging
from config import DB_CONFIG, TABLES, SAMPLE_DATA

class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.setup_logging()
        self.connect()

    def setup_logging(self):
        logging.basicConfig(
            filename='dental_clinic.log', 
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s: %(message)s'
        )

    def connect(self):
        try:
            dsn = cx_Oracle.makedsn(
                host=DB_CONFIG['host'],
                port=DB_CONFIG['port'],
                sid=DB_CONFIG['sid']
            )
            self.connection = cx_Oracle.connect(
                user=DB_CONFIG['username'],
                password=DB_CONFIG['password'],
                dsn=dsn
            )
            logging.info("Database connection established")
        except Exception as e:
            logging.error(f"Database connection error: {e}")
            raise

    def execute_query(self, query, params=None):
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor
        except Exception as e:
            logging.error(f"Query execution error: {e}")
            return None

    def create_tables(self):
        try:
            cursor = self.connection.cursor()
            for query in TABLES:
                try:
                    cursor.execute(query)
                    logging.info(f"Created table: {query.split()[2]}")
                except cx_Oracle.DatabaseError as e:
                    logging.error(f"Error creating table: {e}")
            self.connection.commit()
            return True
        except Exception as e:
            logging.error(f"Table creation failed: {e}")
            return False

    def drop_tables(self):
        tables = [
            "Billing", "Medical_Record", "Treatment", 
            "Appointment", "Receptionist", "Dentist", 
            "Patient", "Staff", "Clinic"
        ]
        
        try:
            cursor = self.connection.cursor()
            for table in tables:
                try:
                    cursor.execute(f"DROP TABLE {table} CASCADE CONSTRAINTS")
                    logging.info(f"Dropped table {table}")
                except cx_Oracle.DatabaseError as e:
                    logging.warning(f"Error dropping {table}: {e}")
            
            self.connection.commit()
            return True
        except Exception as e:
            logging.error(f"Failed to drop tables: {e}")
            return False

    def populate_tables(self):
        try:
            cursor = self.connection.cursor()
            
            # Define the order of population to handle dependencies
            population_order = [
                'Staff_Role', 'Dentist_Specialization', 'Appointment_Status', 
                'Treatment_Type', 'Billing_Status', 'Clinic', 'Staff', 
                'Dentist', 'Receptionist', 'Patient', 'Appointment', 
                'Treatment', 'Medical_Record', 'Billing'
            ]
            
            for table in population_order:
                try:
                    # Dynamically get column names
                    col_query = f"SELECT * FROM {table} WHERE 1=0"
                    col_cursor = self.connection.cursor()
                    col_cursor.execute(col_query)
                    columns = [desc[0] for desc in col_cursor.description]
                    col_cursor.close()
                    
                    # Prepare data for this table
                    table_data = SAMPLE_DATA.get(table, [])
                    
                    if not table_data:
                        logging.warning(f"No data found for table {table}")
                        continue
                    
                    # Prepare insert query
                    columns_str = ', '.join(columns)
                    placeholders = ', '.join([f':{i+1}' for i in range(len(columns))])
                    insert_query = f"INSERT INTO {table} ({columns_str}) VALUES ({placeholders})"
                    
                    # Execute batch insert
                    cursor.executemany(insert_query, table_data)
                    logging.info(f"Populated {table} with {len(table_data)} records")
                    
                except cx_Oracle.DatabaseError as e:
                    logging.error(f"Error populating {table}: {e}")
            
            # Commit the transaction
            self.connection.commit()
            return True
        
        except Exception as e:
            logging.error(f"Failed to populate tables: {e}")
            return False

    def close(self):
        if self.connection:
            self.connection.close()
            logging.info("Database connection closed")
