"""
Data Access Layer (DAL) for Employee Database Operations

This module handles all direct database interactions using SQLite.
It provides a clean interface for CRUD operations on the employee table.
"""

import sqlite3
from typing import List, Optional, Dict, Any
from pathlib import Path


class DatabaseConnection:
    """
    Handles database connection and basic operations.
    This class manages the connection to the SQLite database.
    """
    
    def __init__(self, db_path: str = "employees.db"):
        """
        Initialize database connection.
        
        Args:
            db_path (str): Path to the SQLite database file
        """
        self.db_path = Path(db_path)
        if not self.db_path.exists():
            raise FileNotFoundError(f"Database file not found: {db_path}")
    
    def get_connection(self) -> sqlite3.Connection:
        """
        Create and return a new database connection.
        
        Returns:
            sqlite3.Connection: Database connection object
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        return conn


class EmployeeDAL:
    """
    Data Access Layer for Employee operations.
    
    This class contains all methods for interacting with the employee table.
    It handles SQL queries and database transactions.
    """
    
    def __init__(self, db_path: str = "employees.db"):
        """
        Initialize the Employee DAL.
        
        Args:
            db_path (str): Path to the SQLite database file
        """
        self.db_connection = DatabaseConnection(db_path)
    
    def create_employee(self, fname: str, lname: str, department: str, ph_number: str) -> int:
        """
        Insert a new employee into the database.
        
        Args:
            fname (str): Employee's first name
            lname (str): Employee's last name
            department (str): Employee's department
            ph_number (str): Employee's phone number
            
        Returns:
            int: The ID of the newly created employee
            
        Raises:
            sqlite3.Error: If database operation fails
        """
        try:
            with self.db_connection.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO employee (fname, lname, department, phNumber) VALUES (?, ?, ?, ?)",
                    (fname, lname, department, ph_number)
                )
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Failed to create employee: {str(e)}")
    
    def get_employee_by_id(self, employee_id: int) -> Optional[Dict[str, Any]]:
        """
        Retrieve an employee by their ID.
        
        Args:
            employee_id (int): The ID of the employee to retrieve
            
        Returns:
            Optional[Dict[str, Any]]: Employee data as dictionary, or None if not found
            
        Raises:
            sqlite3.Error: If database operation fails
        """
        try:
            with self.db_connection.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM employee WHERE id = ?", (employee_id,))
                row = cursor.fetchone()
                
                if row:
                    return dict(row)  # Convert Row object to dictionary
                return None
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Failed to get employee by ID: {str(e)}")
    
    def get_all_employees(self) -> List[Dict[str, Any]]:
        """
        Retrieve all employees from the database.
        
        Returns:
            List[Dict[str, Any]]: List of all employees as dictionaries
            
        Raises:
            sqlite3.Error: If database operation fails
        """
        try:
            with self.db_connection.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM employee ORDER BY id")
                rows = cursor.fetchall()
                
                return [dict(row) for row in rows]
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Failed to get all employees: {str(e)}")
    
    def get_employees_by_department(self, department: str) -> List[Dict[str, Any]]:
        """
        Retrieve all employees in a specific department.
        
        Args:
            department (str): The department name to filter by
            
        Returns:
            List[Dict[str, Any]]: List of employees in the department
            
        Raises:
            sqlite3.Error: If database operation fails
        """
        try:
            with self.db_connection.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM employee WHERE department = ? ORDER BY id", (department,))
                rows = cursor.fetchall()
                
                return [dict(row) for row in rows]
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Failed to get employees by department: {str(e)}")
    
    def update_employee(self, employee_id: int, fname: str = None, lname: str = None, 
                       department: str = None, ph_number: str = None) -> bool:
        """
        Update an employee's information.
        
        Args:
            employee_id (int): The ID of the employee to update
            fname (str, optional): New first name
            lname (str, optional): New last name
            department (str, optional): New department
            ph_number (str, optional): New phone number
            
        Returns:
            bool: True if update was successful, False if employee not found
            
        Raises:
            sqlite3.Error: If database operation fails
        """
        try:
            # Build dynamic UPDATE query based on provided fields
            update_fields = []
            values = []
            
            if fname is not None:
                update_fields.append("fname = ?")
                values.append(fname)
            if lname is not None:
                update_fields.append("lname = ?")
                values.append(lname)
            if department is not None:
                update_fields.append("department = ?")
                values.append(department)
            if ph_number is not None:
                update_fields.append("phNumber = ?")
                values.append(ph_number)
            
            if not update_fields:
                return False  # No fields to update
            
            values.append(employee_id)  # Add ID for WHERE clause
            
            query = f"UPDATE employee SET {', '.join(update_fields)} WHERE id = ?"
            
            with self.db_connection.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, values)
                conn.commit()
                
                return cursor.rowcount > 0  # Return True if any rows were affected
                
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Failed to update employee: {str(e)}")
    
    def delete_employee(self, employee_id: int) -> bool:
        """
        Delete an employee from the database.
        
        Args:
            employee_id (int): The ID of the employee to delete
            
        Returns:
            bool: True if deletion was successful, False if employee not found
            
        Raises:
            sqlite3.Error: If database operation fails
        """
        try:
            with self.db_connection.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM employee WHERE id = ?", (employee_id,))
                conn.commit()
                
                return cursor.rowcount > 0  # Return True if any rows were affected
                
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Failed to delete employee: {str(e)}")
    
    def search_employees(self, search_term: str) -> List[Dict[str, Any]]:
        """
        Search employees by name (first name or last name).
        
        Args:
            search_term (str): The term to search for in employee names
            
        Returns:
            List[Dict[str, Any]]: List of matching employees
            
        Raises:
            sqlite3.Error: If database operation fails
        """
        try:
            with self.db_connection.get_connection() as conn:
                cursor = conn.cursor()
                search_pattern = f"%{search_term}%"
                cursor.execute(
                    "SELECT * FROM employee WHERE fname LIKE ? OR lname LIKE ? ORDER BY id",
                    (search_pattern, search_pattern)
                )
                rows = cursor.fetchall()
                
                return [dict(row) for row in rows]
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Failed to search employees: {str(e)}")
    
    def get_employee_count(self) -> int:
        """
        Get the total number of employees in the database.
        
        Returns:
            int: Total number of employees
            
        Raises:
            sqlite3.Error: If database operation fails
        """
        try:
            with self.db_connection.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM employee")
                return cursor.fetchone()[0]
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Failed to get employee count: {str(e)}")
    
    def get_departments(self) -> List[str]:
        """
        Get a list of all unique departments.
        
        Returns:
            List[str]: List of unique department names
            
        Raises:
            sqlite3.Error: If database operation fails
        """
        try:
            with self.db_connection.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT DISTINCT department FROM employee WHERE department IS NOT NULL ORDER BY department")
                rows = cursor.fetchall()
                
                return [row[0] for row in rows]
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Failed to get departments: {str(e)}")
