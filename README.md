# 🦷 Dental Clinic Management System
![image](https://github.com/user-attachments/assets/0213b682-1c7e-4d1d-8241-f50e58673c0d)

The Dental clinic database management system is designed to effectively manage the essentials of operating a dental clinic, including patient appointments, scheduling, billing, treatment services, etc. Through the use of our dental clinic DBMS it will allow efficient workflow at dental clinics and allow for dentists and staff to provide quality care for its patients. The DBMS will follow basic CRUD operations (create, read, update, delete) for entities such as adding new patients, updating billing, removing patients, etc. The overall goal of our system is to enable dental professionals to focus on providing high-quality care while reducing administrative and manual work burdens and improving operational insights.

The DBMS includes main entities such as patients, dentists, clinic information and staff, as well as the relations between these entities such as appointments and treatments, patients and billing, patients and treatments, etc. Each entity will also have key information known as attributes that store specific data. For example for the patient entity some attributes would be name, age, health card # (Primary Key), gender, medical history, etc. Additionally to exemplify relationships between entities a patient can have multiple appointments, each connected to a dentist and, subsequently, leading to one or more treatments. Billing is directly tied to the treatments received, and each bill can generate multiple payments
## ✨ Features
🔐 Simple Login GUI
<div align="left">
  <img src="https://github.com/user-attachments/assets/25bd671e-829c-42de-a7a3-7ec36534e4b9" alt="Simple Login GUI" width="300"/>
</div>

⚙️ Edit tables 

🔍 Search tables

👥 Patient Management

  📅 Appointment Scheduling

  🦷 Treatment Tracking

  💰 Billing System

  👨‍⚕️ Staff Management

## 🖥️ Prerequisites

### Required Software
1. Python (3.8 or higher)
2. Oracle Database
3. Oracle Instant Client
4. pip (Python package manager)

## 🚀 Installation

### 1. Clone the Repo
```
git clone https://github.com/sankeer28/Dental-Clinic-Management-System.git
cd Dental-Clinic-Management-System-main
```
### 2. Install dependencies
```
pip install -r requirements.txt
```
### 3. run the applciation
```
python main.py
```

### Entities (S = Strong Entity, W = Weak Entity)
- Patient (S): Information about the patients, such as patient ID, name, age, gender, contact details, and medical history.
- Dentist (S): Details about the dentists, including dentist ID, name, specialization, contact information, and schedule.
- Appointment (W): Records of appointments, including appointment ID, patient ID, dentist ID, date, time, and status.
- Treatment (W): Information about the treatments provided, such as treatment ID, patient ID, dentist ID, treatment type, description, and cost.
- Clinic Information (S): General information about the clinic, such as clinic ID, name, address, contact details, and operating hours.
- Staff (S): Information about other staff members, such as nurses and administrative personnel, including staff ID, name, role, and contact details.
- Medical Records (W): Detailed medical records for each patient, including medical history, diagnoses, treatments, and prescriptions.
- Receptionist (S): Information about the receptionists, including receptionist ID, name, contact details, and work schedule.
- Billing(S): Billing information, including bill ID, patient ID, treatment ID, amount, payment status, and date.

