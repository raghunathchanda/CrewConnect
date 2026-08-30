CrewConnect is a Django-based HR and Employee Management System. We have two major roles:
HR and Employee.
Tech Stack: Python, Django, SQLite, HTML, CSS, Bootstrap, JavaScript, Django ORM, Django
Authentication, and SMTP for email integration.
HR Module
HR can manage employees, departments and designations, approve employee leave requests, generate
payslips and view payroll reports.
HR can add, view, update and delete employees.
While creating an employee, HR provides Employee ID, Name, Email, Phone, Department, Designation,
Joining Date, Employment Type, Salary, Address and Status.
Departments
We maintain separate Department and Designation master tables.
We maintain different departments based on the organization's requirements, such as HR, Development,
Testing and Finance.
Designations
We maintain different designations such as Python Developer, Senior Python Developer, Software
Tester, HR Executive and Accountant.
Employment Types
We have predefined employment types: Permanent, Contract, Part-time and Intern. These are
implemented using Django model choices.
Employee Module
Employees can view their own profile, apply for leave, view leave history and leave calendar, and
access their payslips.
Authentication
For authentication, we use Django's built-in User model. We maintain a OneToOne relationship between
User and Employee.
When HR creates an employee, the system creates the Django User account with an unusable password
and sends the employee an email containing a secure password setup link.
The employee opens the link, creates their password and then logs in.

Login DifferentiationAfter login, we differentiate the user based on whether an Employee record exists for that User and
redirect them to the appropriate dashboard.
Leave Management
Employees can apply for different leave types such as EL – Earned Leave, SL – Sick Leave and CL –
Casual Leave.
When an employee applies for leave, the request initially has a Pending status. HR can approve or reject
the leave.
Employees can view their leave status and leave calendar.
Payroll
HR generates monthly payslips containing basic salary, allowances, deductions and net salary.
Net Salary = Basic Salary + Allowances - Deductions
We added a database-level unique constraint to prevent duplicate payslips for the same employee and
month/year.
Reports
We have an HR reporting module where HR can select a month and year and view aggregated payroll
information using Django ORM's aggregation functions such as Sum.
Frontend
On the frontend, we use HTML, CSS and Bootstrap to create dashboards and responsive UI.
We use Django templates with template inheritance so common components such as the sidebar and layout
do not need to be repeated on every page.
Backend
On the backend, Django handles URL routing, views, models, authentication, sessions and database
operations through Django ORM.
SQLite is currently used as the database, and SMTP is used for sending employee onboarding emails.
