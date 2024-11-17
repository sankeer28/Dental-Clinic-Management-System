from datetime import datetime
import cx_Oracle

# Database Configuration
DB_CONFIG = {
    'username': '',
    'password': '',
    'host': 'oracle.scs.ryerson.ca',
    'port': 1521,
    'sid': 'orcl'
}

# Logging Configuration
LOG_FILE = 'dental_clinic.log'

# Table Definitions
TABLES = [
    """CREATE TABLE Clinic (
        ClinicID VARCHAR2(10) PRIMARY KEY,
        Name VARCHAR2(100) NOT NULL UNIQUE,
        Contact VARCHAR2(100) UNIQUE,
        Address VARCHAR2(255) NOT NULL UNIQUE,
        Operating_Hours VARCHAR2(100) NOT NULL
    )""",

    """CREATE TABLE Staff_Role (
        RoleID VARCHAR2(10) PRIMARY KEY,
        RoleName VARCHAR2(50) NOT NULL UNIQUE
    )""",

    """CREATE TABLE Staff (
        StaffID VARCHAR2(10) PRIMARY KEY,
        Name VARCHAR2(100) NOT NULL,
        Contact VARCHAR2(100) UNIQUE,
        RoleID VARCHAR2(10) NOT NULL,
        ClinicID VARCHAR2(10) NOT NULL,
        FOREIGN KEY (RoleID) REFERENCES Staff_Role(RoleID) ON DELETE CASCADE,
        FOREIGN KEY (ClinicID) REFERENCES Clinic(ClinicID) ON DELETE CASCADE
    )""",

    """CREATE TABLE Dentist_Specialization (
        SpecializationID VARCHAR2(10) PRIMARY KEY,
        SpecializationName VARCHAR2(100) NOT NULL UNIQUE
    )""",

    """CREATE TABLE Dentist (
        StaffID VARCHAR2(10) PRIMARY KEY,
        SpecializationID VARCHAR2(10) NOT NULL,
        Schedule VARCHAR2(100) NOT NULL,
        FOREIGN KEY (StaffID) REFERENCES Staff(StaffID) ON DELETE CASCADE,
        FOREIGN KEY (SpecializationID) REFERENCES Dentist_Specialization(SpecializationID) ON DELETE CASCADE
    )""",

    """CREATE TABLE Receptionist (
        StaffID VARCHAR2(10) PRIMARY KEY,
        Schedule VARCHAR2(100) NOT NULL,
        FOREIGN KEY (StaffID) REFERENCES Staff(StaffID) ON DELETE CASCADE
    )""",

    """CREATE TABLE Patient (
        PatientID VARCHAR2(10) PRIMARY KEY,
        Name VARCHAR2(100) NOT NULL,
        Age NUMBER CHECK (Age >= 0 AND Age <= 120),
        Gender VARCHAR2(10) CHECK (Gender IN ('Male', 'Female', 'Other', 'Unknown')),
        Contact VARCHAR2(100) UNIQUE,
        Email VARCHAR2(100) UNIQUE
    )""",

    """CREATE TABLE Appointment_Status (
        StatusID VARCHAR2(10) PRIMARY KEY,
        StatusName VARCHAR2(20) NOT NULL UNIQUE
    )""",

    """CREATE TABLE Appointment (
        AppointmentID VARCHAR2(10) PRIMARY KEY,
        PatientID VARCHAR2(10) NOT NULL,
        StaffID VARCHAR2(10) NOT NULL,
        Appointment_Date VARCHAR2(10) NOT NULL,
        Appointment_Time VARCHAR2(10) NOT NULL,
        StatusID VARCHAR2(10) NOT NULL,
        ReceptionistID VARCHAR2(10),
        FOREIGN KEY (PatientID) REFERENCES Patient(PatientID) ON DELETE CASCADE,
        FOREIGN KEY (StaffID) REFERENCES Staff(StaffID) ON DELETE CASCADE,
        FOREIGN KEY (StatusID) REFERENCES Appointment_Status(StatusID) ON DELETE CASCADE,
        FOREIGN KEY (ReceptionistID) REFERENCES Receptionist(StaffID) ON DELETE CASCADE,
        UNIQUE (PatientID, StaffID, Appointment_Date, Appointment_Time)
    )""",

    """CREATE TABLE Treatment_Type (
        TreatmentTypeID VARCHAR2(10) PRIMARY KEY,
        TreatmentName VARCHAR2(100) NOT NULL UNIQUE,
        BasePrice NUMBER(10, 2) DEFAULT 0 CHECK (BasePrice >= 0)
    )""",

    """CREATE TABLE Treatment (
        TreatmentID VARCHAR2(10) PRIMARY KEY,
        AppointmentID VARCHAR2(10) NOT NULL,
        PatientID VARCHAR2(10) NOT NULL,
        StaffID VARCHAR2(10) NOT NULL,
        TreatmentTypeID VARCHAR2(10) NOT NULL,
        Description VARCHAR2(255),
        Cost NUMBER(10, 2) DEFAULT 0 CHECK (Cost >= 0),
        FOREIGN KEY (AppointmentID) REFERENCES Appointment(AppointmentID) ON DELETE CASCADE,
        FOREIGN KEY (PatientID) REFERENCES Patient(PatientID) ON DELETE CASCADE,
        FOREIGN KEY (StaffID) REFERENCES Dentist(StaffID) ON DELETE CASCADE,
        FOREIGN KEY (TreatmentTypeID) REFERENCES Treatment_Type(TreatmentTypeID) ON DELETE CASCADE,
        UNIQUE (AppointmentID, TreatmentTypeID)
    )""",

    """CREATE TABLE Medical_Record (
        MedicalRecordID VARCHAR2(10) PRIMARY KEY,
        PatientID VARCHAR2(10) NOT NULL,
        Medical_History VARCHAR2(255),
        Diagnoses VARCHAR2(255),
        Prescriptions VARCHAR2(255),
        TreatmentID VARCHAR2(10),
        AppointmentID VARCHAR2(10),
        FOREIGN KEY (PatientID) REFERENCES Patient(PatientID) ON DELETE CASCADE,
        FOREIGN KEY (TreatmentID) REFERENCES Treatment(TreatmentID) ON DELETE SET NULL,
        FOREIGN KEY (AppointmentID) REFERENCES Appointment(AppointmentID) ON DELETE SET NULL,
        UNIQUE (PatientID, TreatmentID, AppointmentID)
    )""",

    """CREATE TABLE Billing_Status (
        StatusID VARCHAR2(10) PRIMARY KEY,
        StatusName VARCHAR2(20) NOT NULL UNIQUE
    )""",

    """CREATE TABLE Billing (
        BillingID VARCHAR2(10) PRIMARY KEY,
        AppointmentID VARCHAR2(10) NOT NULL,
        PatientID VARCHAR2(10) NOT NULL,
        Billing_Date VARCHAR2(10) NOT NULL,
        Amount NUMBER(10, 2) DEFAULT 0 CHECK (Amount >= 0),
        ReceptionistID VARCHAR2(10),
        StatusID VARCHAR2(10) NOT NULL,
        FOREIGN KEY (AppointmentID) REFERENCES Appointment(AppointmentID) ON DELETE CASCADE,
        FOREIGN KEY (PatientID) REFERENCES Patient(PatientID) ON DELETE CASCADE,
        FOREIGN KEY (ReceptionistID) REFERENCES Receptionist(StaffID) ON DELETE CASCADE,
        FOREIGN KEY (StatusID) REFERENCES Billing_Status(StatusID) ON DELETE CASCADE,
        UNIQUE (AppointmentID, PatientID, Billing_Date)
    )"""
]

SAMPLE_DATA = {
    # Lookup Tables
    'Staff_Role': [
        ('R001', 'Dentist'),
        ('R002', 'Receptionist')
    ],
    
    'Dentist_Specialization': [
        ('SP001', 'Orthodontics'),
        ('SP002', 'General Dentistry'),
        ('SP003', 'Cosmetic Dentistry')
    ],
    
    'Appointment_Status': [
        ('AS001', 'Scheduled'),
        ('AS002', 'Completed'),
        ('AS003', 'Cancelled'),
        ('AS004', 'Pending')
    ],
    
    'Treatment_Type': [
        ('TT001', 'Braces', 1500),
        ('TT002', 'Dental Filling', 200),
        ('TT003', 'Teeth Whitening', 300),
        ('TT004', 'Root Canal', 800)
    ],
    
    'Billing_Status': [
        ('BS001', 'Pending'),
        ('BS002', 'Paid'),
        ('BS003', 'Overdue')
    ],
    
    # Main Tables
    'Clinic': [
        ('C001', 'Downtown Dental', '416-123-4567', '123 Main St', '9am-5pm'),
        ('C002', 'Riverside Clinic', '416-987-6543', '456 River Rd', '8am-6pm')
    ],
    
    'Staff': [
        ('S001', 'Dr. John Doe', '111-222-4333', 'R001', 'C001'),
        ('S002', 'Emily Clark', '444-555-6666', 'R002', 'C001'),
        ('S003', 'Dr. Bob Wilson', '111-222-3333', 'R001', 'C001')
    ],
    
    'Dentist': [
        ('S001', 'SP001', 'Mon-Fri 9AM-5PM'),
        ('S003', 'SP002', 'Mon-Fri 9AM-5PM')
    ],
    
    'Receptionist': [
        ('S002', 'Mon-Fri 9AM-5PM')
    ],
    
    'Patient': [
        ('P001', 'Alice Brown', 29, 'Female', '777-888-9999', 'alice.brown@email.com'),
        ('P002', 'Bob Smith', 45, 'Male', '222-333-4444', 'bob.smith@email.com'),
        ('P003', 'Billy Bob', 25, 'Male', '416-111-2222', 'billy.bob@email.com')
    ],
    
    'Appointment': [
        ('A001', 'P001', 'S001', '2024-10-01',  '10:00AM',  # Appointment Time
         'AS001',  # Scheduled status
         'S002'  # Receptionist ID
        ),
        ('A002', 'P002', 'S001', 
         '2024-10-01', 
         '10:00AM', 
         'AS001',  # Scheduled status
         'S002'  # Receptionist ID
        )
    ],
    
    'Treatment': [
        ('T001', 'A001', 'P001', 'S001', 'TT001', 'Orthodontic braces', 1500),
        ('T002', 'A002', 'P002', 'S001', 'TT002', 'Dental filling', 200)
    ],
    
    'Medical_Record': [
        ('MR001', 'P001', 'No significant medical history', 
         'Minor cavity detected', 'Recommended oral hygiene', 'T001', 'A001'),
        ('MR002', 'P002', 'Previous dental work', 
         'Tooth decay', 'Prescribed antibiotics', 'T002', 'A002')
    ],
    
    'Billing': [
        ('B001', 'A001', 'P001', 
         '2024-10-01',  # Billing Date
         1500, 'S002', 'BS002'  # Paid status
        ),
        ('B002', 'A002', 'P002', 
         '2024-10-01',  # Billing Date
         200, 'S002', 'BS001'  # Pending status
        )
    ]
}
