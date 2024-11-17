import re
import logging
from datetime import datetime

class Validator:
    @staticmethod
    def validate_email(email):
        """
        Validate email format
        """
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_regex, email) is not None

    @staticmethod
    def validate_phone(phone):
        """
        Validate phone number format
        """
        phone_regex = r'^\+?1?\d{10,14}$'
        return re.match(phone_regex, phone) is not None

    @staticmethod
    def validate_date(date_string):
        """
        Validate date format
        """
        try:
            datetime.strptime(date_string, '%Y-%m-%d')
            return True
        except ValueError:
            return False

class Logger:
    @staticmethod
    def log_action(action, details=None):
        """
        Log application actions
        """
        log_message = f"Action: {action}"
        if details:
            log_message += f" - Details: {details}"
        logging.info(log_message)

class ReportGenerator:
    @staticmethod
    def generate_patient_report(db_manager):
        """
        Generate a comprehensive patient report
        """
        try:
            query = """
            SELECT 
                p.PatientID, 
                p.Name, 
                COUNT(a.AppointmentID) as Total_Appointments,
                SUM(t.Cost) as Total_Treatment_Cost
            FROM 
                Patient p
            LEFT JOIN 
                Appointment a ON p.PatientID = a.PatientID
            LEFT JOIN 
                Treatment t ON a.AppointmentID = t.AppointmentID
            GROUP BY 
                p.PatientID, p.Name
            ORDER BY 
                Total_Appointments DESC
            """
            
            cursor = db_manager.execute_query(query)
            if cursor:
                return cursor.fetchall()
            return []
        except Exception as e:
            logging.error(f"Error generating patient report: {e}")
            return []

class DataFormatter:
    @staticmethod
    def format_currency(amount):
        """
        Format numeric value as currency
        """
        return f"${amount:,.2f}"

    @staticmethod
    def format_date(date):
        """
        Format date to a readable string
        """
        if isinstance(date, datetime):
            return date.strftime('%Y-%m-%d')
        return str(date)

class ConfigurationManager:
    @staticmethod
    def load_configuration():
        """
        Load application configuration
        """
        # In a real-world scenario, this might load from a config file
        return {
            'database': {
                'host': 'oracle.scs.ryerson.ca',
                'port': 1521,
                'sid': 'orcl'
            },
            'logging': {
                'level': logging.INFO,
                'file': 'dental_clinic.log'
            }
        }

def singleton(cls):
    """
    ensure only one instance of a class
    """
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance
