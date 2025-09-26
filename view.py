"""
View/UI Module for Employee Management System

This module handles all user interface interactions and display logic.
It provides a simple console-based interface for the employee management system.
"""

from typing import List, Optional
from controller import EmployeeController
from models import Employee, EmployeeSearchCriteria, EmployeeUpdateData


class EmployeeView:
    """
    View class that handles all user interface interactions.
    
    This class manages the display of information to the user and
    collects input from the user for processing by the controller.
    """
    
    def __init__(self):
        """
        Initialize the employee view.
        """
        self.controller = EmployeeController()
    
    def display_welcome_message(self):
        """
        Display welcome message and main menu options.
        """
        print("\n" + "="*60)
        print("           EMPLOYEE MANAGEMENT SYSTEM")
        print("="*60)
        print("\nWelcome to the Employee Management System!")
        print("This system allows you to manage employee records.")
        print("\nMain Menu Options:")
        print("1. Add New Employee")
        print("2. View All Employees")
        print("3. Search Employees")
        print("4. Update Employee")
        print("5. Delete Employee")
        print("6. View Employee Statistics")
        print("7. View Departments")
        print("8. Exit")
        print("-"*60)
    
    def get_user_choice(self) -> str:
        """
        Get user's menu choice.
        
        Returns:
            str: User's choice as string
        """
        while True:
            choice = input("\nEnter your choice (1-8): ").strip()
            if choice in ['1', '2', '3', '4', '5', '6', '7', '8']:
                return choice
            print("Invalid choice. Please enter a number between 1 and 8.")
    
    def display_employee(self, employee: Employee):
        """
        Display a single employee's information.
        
        Args:
            employee (Employee): Employee object to display
        """
        print(f"\nEmployee ID: {employee.id}")
        print(f"Name: {employee.get_full_name()}")
        print(f"Department: {employee.department}")
        print(f"Phone Number: {employee.ph_number}")
        print("-" * 40)
    
    def display_employees(self, employees: List[Employee]):
        """
        Display a list of employees.
        
        Args:
            employees (List[Employee]): List of employee objects to display
        """
        if not employees:
            print("\nNo employees found.")
            return
        
        print(f"\nFound {len(employees)} employee(s):")
        print("=" * 60)
        
        for employee in employees:
            self.display_employee(employee)
    
    def get_employee_input(self) -> tuple:
        """
        Get employee information from user input.
        
        Returns:
            tuple: (fname, lname, department, ph_number)
        """
        print("\nEnter Employee Information:")
        print("-" * 30)
        
        fname = input("First Name: ").strip()
        lname = input("Last Name: ").strip()
        department = input("Department: ").strip()
        ph_number = input("Phone Number: ").strip()
        
        return fname, lname, department, ph_number
    
    def get_employee_id(self) -> Optional[int]:
        """
        Get employee ID from user input.
        
        Returns:
            Optional[int]: Employee ID or None if invalid input
        """
        while True:
            try:
                emp_id = input("Enter Employee ID: ").strip()
                if not emp_id:
                    return None
                return int(emp_id)
            except ValueError:
                print("Invalid input. Please enter a valid number.")
    
    def get_search_criteria(self) -> EmployeeSearchCriteria:
        """
        Get search criteria from user input.
        
        Returns:
            EmployeeSearchCriteria: Search criteria object
        """
        print("\nSearch Options:")
        print("1. Search by name")
        print("2. Filter by department")
        print("3. Search by name and filter by department")
        print("4. Show all employees")
        
        while True:
            choice = input("Enter your search choice (1-4): ").strip()
            
            if choice == '1':
                search_term = input("Enter name to search: ").strip()
                return EmployeeSearchCriteria(search_term=search_term)
            elif choice == '2':
                departments = self.controller.get_departments()
                if departments['success']:
                    print("\nAvailable departments:")
                    for i, dept in enumerate(departments['departments'], 1):
                        print(f"{i}. {dept}")
                    dept_choice = input("Enter department name: ").strip()
                    return EmployeeSearchCriteria(department=dept_choice)
                else:
                    print(f"Error: {departments['message']}")
                    return EmployeeSearchCriteria()
            elif choice == '3':
                search_term = input("Enter name to search: ").strip()
                departments = self.controller.get_departments()
                if departments['success']:
                    print("\nAvailable departments:")
                    for i, dept in enumerate(departments['departments'], 1):
                        print(f"{i}. {dept}")
                    dept_choice = input("Enter department name: ").strip()
                    return EmployeeSearchCriteria(search_term=search_term, department=dept_choice)
                else:
                    print(f"Error: {departments['message']}")
                    return EmployeeSearchCriteria(search_term=search_term)
            elif choice == '4':
                return EmployeeSearchCriteria()
            else:
                print("Invalid choice. Please enter 1, 2, 3, or 4.")
    
    def get_update_data(self) -> EmployeeUpdateData:
        """
        Get employee update data from user input.
        
        Returns:
            EmployeeUpdateData: Update data object
        """
        print("\nEnter new information (leave blank to keep current value):")
        print("-" * 50)
        
        fname = input("New First Name: ").strip()
        lname = input("New Last Name: ").strip()
        department = input("New Department: ").strip()
        ph_number = input("New Phone Number: ").strip()
        
        return EmployeeUpdateData(
            fname=fname if fname else None,
            lname=lname if lname else None,
            department=department if department else None,
            ph_number=ph_number if ph_number else None
        )
    
    def display_message(self, message: str, is_error: bool = False):
        """
        Display a message to the user.
        
        Args:
            message (str): Message to display
            is_error (bool): Whether this is an error message
        """
        if is_error:
            print(f"\n❌ Error: {message}")
        else:
            print(f"\n✅ {message}")
    
    def display_statistics(self, stats: dict):
        """
        Display employee statistics.
        
        Args:
            stats (dict): Statistics dictionary
        """
        print("\n" + "="*50)
        print("           EMPLOYEE STATISTICS")
        print("="*50)
        print(f"Total Employees: {stats['total_employees']}")
        print(f"Total Departments: {stats['total_departments']}")
        print("\nEmployees per Department:")
        print("-" * 30)
        
        for dept, count in stats['employees_per_department'].items():
            print(f"{dept}: {count} employee(s)")
        
        print("="*50)
    
    def display_departments(self, departments: List[str]):
        """
        Display list of departments.
        
        Args:
            departments (List[str]): List of department names
        """
        print("\n" + "="*40)
        print("           DEPARTMENTS")
        print("="*40)
        
        if not departments:
            print("No departments found.")
        else:
            for i, dept in enumerate(departments, 1):
                print(f"{i}. {dept}")
        
        print("="*40)
    
    def handle_add_employee(self):
        """
        Handle adding a new employee.
        """
        print("\n" + "="*40)
        print("           ADD NEW EMPLOYEE")
        print("="*40)
        
        fname, lname, department, ph_number = self.get_employee_input()
        
        result = self.controller.create_employee(fname, lname, department, ph_number)
        
        if result['success']:
            self.display_message(result['message'])
        else:
            self.display_message(result['message'], is_error=True)
            if 'errors' in result:
                print("Validation errors:")
                for error in result['errors']:
                    print(f"  - {error}")
    
    def handle_view_employees(self):
        """
        Handle viewing all employees.
        """
        print("\n" + "="*40)
        print("           ALL EMPLOYEES")
        print("="*40)
        
        result = self.controller.get_all_employees()
        
        if result['success']:
            self.display_employees(result['employees'])
        else:
            self.display_message(result['message'], is_error=True)
    
    def handle_search_employees(self):
        """
        Handle searching employees.
        """
        print("\n" + "="*40)
        print("           SEARCH EMPLOYEES")
        print("="*40)
        
        search_criteria = self.get_search_criteria()
        result = self.controller.search_employees(search_criteria)
        
        if result['success']:
            self.display_employees(result['employees'])
        else:
            self.display_message(result['message'], is_error=True)
    
    def handle_update_employee(self):
        """
        Handle updating an employee.
        """
        print("\n" + "="*40)
        print("           UPDATE EMPLOYEE")
        print("="*40)
        
        emp_id = self.get_employee_id()
        if emp_id is None:
            self.display_message("Employee ID is required", is_error=True)
            return
        
        # First, show current employee information
        result = self.controller.get_employee(emp_id)
        if not result['success']:
            self.display_message(result['message'], is_error=True)
            return
        
        print(f"\nCurrent information for Employee {emp_id}:")
        self.display_employee(result['employee'])
        
        # Get update data
        update_data = self.get_update_data()
        
        if not update_data.has_updates():
            self.display_message("No changes provided", is_error=True)
            return
        
        # Perform update
        update_result = self.controller.update_employee(emp_id, update_data)
        
        if update_result['success']:
            self.display_message(update_result['message'])
        else:
            self.display_message(update_result['message'], is_error=True)
    
    def handle_delete_employee(self):
        """
        Handle deleting an employee.
        """
        print("\n" + "="*40)
        print("           DELETE EMPLOYEE")
        print("="*40)
        
        emp_id = self.get_employee_id()
        if emp_id is None:
            self.display_message("Employee ID is required", is_error=True)
            return
        
        # First, show employee information
        result = self.controller.get_employee(emp_id)
        if not result['success']:
            self.display_message(result['message'], is_error=True)
            return
        
        print(f"\nEmployee to be deleted:")
        self.display_employee(result['employee'])
        
        # Confirm deletion
        confirm = input("\nAre you sure you want to delete this employee? (yes/no): ").strip().lower()
        
        if confirm in ['yes', 'y']:
            delete_result = self.controller.delete_employee(emp_id)
            
            if delete_result['success']:
                self.display_message(delete_result['message'])
            else:
                self.display_message(delete_result['message'], is_error=True)
        else:
            self.display_message("Deletion cancelled")
    
    def handle_view_statistics(self):
        """
        Handle viewing employee statistics.
        """
        print("\n" + "="*40)
        print("           EMPLOYEE STATISTICS")
        print("="*40)
        
        result = self.controller.get_employee_statistics()
        
        if result['success']:
            self.display_statistics(result['statistics'])
        else:
            self.display_message(result['message'], is_error=True)
    
    def handle_view_departments(self):
        """
        Handle viewing departments.
        """
        print("\n" + "="*40)
        print("           DEPARTMENTS")
        print("="*40)
        
        result = self.controller.get_departments()
        
        if result['success']:
            self.display_departments(result['departments'])
        else:
            self.display_message(result['message'], is_error=True)
    
    def run(self):
        """
        Main application loop.
        """
        while True:
            self.display_welcome_message()
            choice = self.get_user_choice()
            
            if choice == '1':
                self.handle_add_employee()
            elif choice == '2':
                self.handle_view_employees()
            elif choice == '3':
                self.handle_search_employees()
            elif choice == '4':
                self.handle_update_employee()
            elif choice == '5':
                self.handle_delete_employee()
            elif choice == '6':
                self.handle_view_statistics()
            elif choice == '7':
                self.handle_view_departments()
            elif choice == '8':
                print("\nThank you for using the Employee Management System!")
                print("Goodbye! 👋")
                break
            
            # Pause before showing menu again
            input("\nPress Enter to continue...")
