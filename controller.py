"""
Controller for Employee Management System

This module contains the business logic and application flow control.
The controller acts as an intermediary between the view and the data access layer.
"""

from typing import List, Optional, Dict, Any
from data_access_layer import EmployeeDAL
from models import Employee, EmployeeSearchCriteria, EmployeeUpdateData


class EmployeeController:
    """
    Controller class that handles business logic for employee operations.
    
    This class coordinates between the UI (view) and the data access layer,
    implementing business rules and validation.
    """
    
    def __init__(self, db_path: str = "employees.db"):
        """
        Initialize the employee controller.
        
        Args:
            db_path (str): Path to the SQLite database file
        """
        self.dal = EmployeeDAL(db_path)
    
    def create_employee(self, fname: str, lname: str, department: str, ph_number: str) -> Dict[str, Any]:
        """
        Create a new employee with validation.
        
        Args:
            fname (str): Employee's first name
            lname (str): Employee's last name
            department (str): Employee's department
            ph_number (str): Employee's phone number
            
        Returns:
            Dict[str, Any]: Result dictionary with success status and message/data
        """
        try:
            # Create employee model for validation
            employee = Employee(fname=fname, lname=lname, department=department, ph_number=ph_number)
            
            # Validate employee data
            if not employee.is_valid():
                errors = employee.get_validation_errors()
                return {
                    'success': False,
                    'message': 'Validation failed',
                    'errors': errors
                }
            
            # Check for duplicate phone number
            existing_employees = self.dal.get_all_employees()
            for emp in existing_employees:
                if emp['phNumber'] == ph_number:
                    return {
                        'success': False,
                        'message': f'Employee with phone number {ph_number} already exists'
                    }
            
            # Create employee in database
            employee_id = self.dal.create_employee(fname, lname, department, ph_number)
            
            return {
                'success': True,
                'message': f'Employee created successfully with ID: {employee_id}',
                'employee_id': employee_id
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Failed to create employee: {str(e)}'
            }
    
    def get_employee(self, employee_id: int) -> Dict[str, Any]:
        """
        Retrieve an employee by ID.
        
        Args:
            employee_id (int): The ID of the employee to retrieve
            
        Returns:
            Dict[str, Any]: Result dictionary with employee data or error message
        """
        try:
            employee_data = self.dal.get_employee_by_id(employee_id)
            
            if employee_data is None:
                return {
                    'success': False,
                    'message': f'Employee with ID {employee_id} not found'
                }
            
            # Convert to Employee model
            employee = Employee.from_dict(employee_data)
            
            return {
                'success': True,
                'message': 'Employee retrieved successfully',
                'employee': employee
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Failed to retrieve employee: {str(e)}'
            }
    
    def get_all_employees(self) -> Dict[str, Any]:
        """
        Retrieve all employees.
        
        Returns:
            Dict[str, Any]: Result dictionary with list of employees or error message
        """
        try:
            employees_data = self.dal.get_all_employees()
            
            # Convert to Employee models
            employees = [Employee.from_dict(emp_data) for emp_data in employees_data]
            
            return {
                'success': True,
                'message': f'Retrieved {len(employees)} employees',
                'employees': employees
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Failed to retrieve employees: {str(e)}'
            }
    
    def search_employees(self, search_criteria: EmployeeSearchCriteria) -> Dict[str, Any]:
        """
        Search employees based on criteria.
        
        Args:
            search_criteria (EmployeeSearchCriteria): Search parameters
            
        Returns:
            Dict[str, Any]: Result dictionary with matching employees or error message
        """
        try:
            employees = []
            
            if search_criteria.is_empty():
                # No search criteria, return all employees
                result = self.get_all_employees()
                if result['success']:
                    employees = result['employees']
            elif search_criteria.has_search_term() and search_criteria.has_department_filter():
                # Search by name and filter by department
                all_employees = self.dal.get_all_employees()
                employees = [
                    Employee.from_dict(emp_data) for emp_data in all_employees
                    if (search_criteria.search_term.lower() in emp_data['fname'].lower() or
                        search_criteria.search_term.lower() in emp_data['lname'].lower()) and
                       emp_data['department'] == search_criteria.department
                ]
            elif search_criteria.has_search_term():
                # Search by name only
                employees_data = self.dal.search_employees(search_criteria.search_term)
                employees = [Employee.from_dict(emp_data) for emp_data in employees_data]
            elif search_criteria.has_department_filter():
                # Filter by department only
                employees_data = self.dal.get_employees_by_department(search_criteria.department)
                employees = [Employee.from_dict(emp_data) for emp_data in employees_data]
            
            return {
                'success': True,
                'message': f'Found {len(employees)} matching employees',
                'employees': employees
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Failed to search employees: {str(e)}'
            }
    
    def update_employee(self, employee_id: int, update_data: EmployeeUpdateData) -> Dict[str, Any]:
        """
        Update an employee's information.
        
        Args:
            employee_id (int): The ID of the employee to update
            update_data (EmployeeUpdateData): Data to update
            
        Returns:
            Dict[str, Any]: Result dictionary with success status and message
        """
        try:
            # Check if employee exists
            existing_employee = self.dal.get_employee_by_id(employee_id)
            if existing_employee is None:
                return {
                    'success': False,
                    'message': f'Employee with ID {employee_id} not found'
                }
            
            # Check if there are any updates to make
            if not update_data.has_updates():
                return {
                    'success': False,
                    'message': 'No fields provided for update'
                }
            
            # Validate phone number if being updated
            if update_data.ph_number is not None:
                all_employees = self.dal.get_all_employees()
                for emp in all_employees:
                    if emp['phNumber'] == update_data.ph_number and emp['id'] != employee_id:
                        return {
                            'success': False,
                            'message': f'Phone number {update_data.ph_number} is already in use by another employee'
                        }
            
            # Perform update
            success = self.dal.update_employee(
                employee_id,
                fname=update_data.fname,
                lname=update_data.lname,
                department=update_data.department,
                ph_number=update_data.ph_number
            )
            
            if success:
                return {
                    'success': True,
                    'message': f'Employee {employee_id} updated successfully'
                }
            else:
                return {
                    'success': False,
                    'message': f'Failed to update employee {employee_id}'
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Failed to update employee: {str(e)}'
            }
    
    def delete_employee(self, employee_id: int) -> Dict[str, Any]:
        """
        Delete an employee.
        
        Args:
            employee_id (int): The ID of the employee to delete
            
        Returns:
            Dict[str, Any]: Result dictionary with success status and message
        """
        try:
            # Check if employee exists
            existing_employee = self.dal.get_employee_by_id(employee_id)
            if existing_employee is None:
                return {
                    'success': False,
                    'message': f'Employee with ID {employee_id} not found'
                }
            
            # Perform deletion
            success = self.dal.delete_employee(employee_id)
            
            if success:
                return {
                    'success': True,
                    'message': f'Employee {employee_id} deleted successfully'
                }
            else:
                return {
                    'success': False,
                    'message': f'Failed to delete employee {employee_id}'
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Failed to delete employee: {str(e)}'
            }
    
    def get_employee_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about employees.
        
        Returns:
            Dict[str, Any]: Dictionary containing employee statistics
        """
        try:
            total_count = self.dal.get_employee_count()
            departments = self.dal.get_departments()
            
            # Count employees per department
            department_counts = {}
            for dept in departments:
                dept_employees = self.dal.get_employees_by_department(dept)
                department_counts[dept] = len(dept_employees)
            
            return {
                'success': True,
                'statistics': {
                    'total_employees': total_count,
                    'total_departments': len(departments),
                    'departments': departments,
                    'employees_per_department': department_counts
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Failed to get statistics: {str(e)}'
            }
    
    def get_departments(self) -> Dict[str, Any]:
        """
        Get list of all departments.
        
        Returns:
            Dict[str, Any]: Result dictionary with departments list or error message
        """
        try:
            departments = self.dal.get_departments()
            
            return {
                'success': True,
                'message': f'Retrieved {len(departments)} departments',
                'departments': departments
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Failed to get departments: {str(e)}'
            }
