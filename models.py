"""
Model Classes for Employee Management System

This module defines the data models used throughout the application.
Models represent the structure and behavior of business entities.
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class Employee:
    """
    Employee model representing an employee in the system.
    
    This class encapsulates all employee-related data and provides
    methods for data validation and manipulation.
    """
    
    id: Optional[int] = None
    fname: str = ""
    lname: str = ""
    department: str = ""
    ph_number: str = ""
    
    def __post_init__(self):
        """
        Post-initialization validation and formatting.
        Called after the dataclass is initialized.
        """
        # Clean and validate input data
        self.fname = self._clean_string(self.fname)
        self.lname = self._clean_string(self.lname)
        self.department = self._clean_string(self.department)
        self.ph_number = self._clean_string(self.ph_number)
    
    def _clean_string(self, value: str) -> str:
        """
        Clean and normalize string input.
        
        Args:
            value (str): Input string to clean
            
        Returns:
            str: Cleaned string
        """
        if value is None:
            return ""
        return str(value).strip()
    
    def get_full_name(self) -> str:
        """
        Get the employee's full name.
        
        Returns:
            str: Full name in "First Last" format
        """
        return f"{self.fname} {self.lname}".strip()
    
    def is_valid(self) -> bool:
        """
        Validate if the employee data is complete and valid.
        
        Returns:
            bool: True if employee data is valid, False otherwise
        """
        return (
            bool(self.fname) and 
            bool(self.lname) and 
            bool(self.department) and 
            bool(self.ph_number)
        )
    
    def get_validation_errors(self) -> list:
        """
        Get a list of validation errors for the employee.
        
        Returns:
            list: List of validation error messages
        """
        errors = []
        
        if not self.fname:
            errors.append("First name is required")
        if not self.lname:
            errors.append("Last name is required")
        if not self.department:
            errors.append("Department is required")
        if not self.ph_number:
            errors.append("Phone number is required")
        
        return errors
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert employee to dictionary format.
        
        Returns:
            Dict[str, Any]: Employee data as dictionary
        """
        return {
            'id': self.id,
            'fname': self.fname,
            'lname': self.lname,
            'department': self.department,
            'phNumber': self.ph_number
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Employee':
        """
        Create Employee instance from dictionary data.
        
        Args:
            data (Dict[str, Any]): Dictionary containing employee data
            
        Returns:
            Employee: New Employee instance
        """
        return cls(
            id=data.get('id'),
            fname=data.get('fname', ''),
            lname=data.get('lname', ''),
            department=data.get('department', ''),
            ph_number=data.get('phNumber', '')
        )
    
    def __str__(self) -> str:
        """
        String representation of the employee.
        
        Returns:
            str: Formatted string representation
        """
        return f"Employee(id={self.id}, name='{self.get_full_name()}', dept='{self.department}')"
    
    def __repr__(self) -> str:
        """
        Detailed string representation for debugging.
        
        Returns:
            str: Detailed string representation
        """
        return (f"Employee(id={self.id}, fname='{self.fname}', lname='{self.lname}', "
                f"department='{self.department}', ph_number='{self.ph_number}')")


class EmployeeSearchCriteria:
    """
    Search criteria model for filtering employees.
    
    This class encapsulates search parameters and provides
    methods for building search queries.
    """
    
    def __init__(self, search_term: str = "", department: str = ""):
        """
        Initialize search criteria.
        
        Args:
            search_term (str): Term to search in names
            department (str): Department to filter by
        """
        self.search_term = search_term.strip()
        self.department = department.strip()
    
    def has_search_term(self) -> bool:
        """
        Check if search term is provided.
        
        Returns:
            bool: True if search term is not empty
        """
        return bool(self.search_term)
    
    def has_department_filter(self) -> bool:
        """
        Check if department filter is provided.
        
        Returns:
            bool: True if department filter is not empty
        """
        return bool(self.department)
    
    def is_empty(self) -> bool:
        """
        Check if no search criteria are provided.
        
        Returns:
            bool: True if no search criteria are set
        """
        return not self.has_search_term() and not self.has_department_filter()


class EmployeeUpdateData:
    """
    Model for employee update operations.
    
    This class allows partial updates by making fields optional.
    """
    
    def __init__(self, fname: Optional[str] = None, lname: Optional[str] = None,
                 department: Optional[str] = None, ph_number: Optional[str] = None):
        """
        Initialize update data.
        
        Args:
            fname (Optional[str]): New first name
            lname (Optional[str]): New last name
            department (Optional[str]): New department
            ph_number (Optional[str]): New phone number
        """
        self.fname = fname.strip() if fname else None
        self.lname = lname.strip() if lname else None
        self.department = department.strip() if department else None
        self.ph_number = ph_number.strip() if ph_number else None
    
    def has_updates(self) -> bool:
        """
        Check if any fields are being updated.
        
        Returns:
            bool: True if at least one field is being updated
        """
        return any([
            self.fname is not None,
            self.lname is not None,
            self.department is not None,
            self.ph_number is not None
        ])
    
    def get_update_fields(self) -> Dict[str, str]:
        """
        Get dictionary of fields that are being updated.
        
        Returns:
            Dict[str, str]: Dictionary of field names and values
        """
        updates = {}
        if self.fname is not None:
            updates['fname'] = self.fname
        if self.lname is not None:
            updates['lname'] = self.lname
        if self.department is not None:
            updates['department'] = self.department
        if self.ph_number is not None:
            updates['ph_number'] = self.ph_number
        return updates
