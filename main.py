#!/usr/bin/env python3
"""
Main Application Entry Point for Employee Management System

This is the main entry point that starts the Employee Management System.
It initializes the application and starts the main user interface loop.
"""

import sys
import os
from pathlib import Path

# Add the current directory to Python path to ensure imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from view import EmployeeView


def check_database_exists():
    """
    Check if the employee database exists.
    
    Returns:
        bool: True if database exists, False otherwise
    """
    db_path = Path("employees.db")
    return db_path.exists()


def main():
    """
    Main application entry point.
    
    This function initializes the application and starts the main loop.
    """
    print("Starting Employee Management System...")
    
    # Check if database exists
    if not check_database_exists():
        print("\n❌ Error: Database file 'employees.db' not found!")
        print("Please make sure the database file exists in the current directory.")
        print("\nYou can create a sample database by running:")
        print("python create_sample_database.py")
        sys.exit(1)
    
    try:
        # Initialize and run the application
        app = EmployeeView()
        app.run()
        
    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user.")
        print("Goodbye! 👋")
        sys.exit(0)
        
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        print("Please check your database file and try again.")
        sys.exit(1)


if __name__ == "__main__":
    main()
