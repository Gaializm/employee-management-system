#!/usr/bin/env python3
"""
Database Initialization Script for Employee Management System

This script creates a sample database with some initial employee data
for testing and demonstration purposes.
"""

import sqlite3
import os
from pathlib import Path


def create_database():
    """
    Create the employee database with the required table structure.
    
    This function creates a new SQLite database file with the employee table
    and inserts some sample data for testing.
    """
    db_path = "employees.db"
    
    # Remove existing database if it exists
    if Path(db_path).exists():
        print(f"⚠️  Database '{db_path}' already exists.")
        response = input("Do you want to recreate it? This will delete all existing data! (yes/no): ").strip().lower()
        if response not in ['yes', 'y']:
            print("Database creation cancelled.")
            return
        os.remove(db_path)
        print(f"✅ Removed existing database '{db_path}'")
    
    try:
        # Create database connection
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create employee table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employee (
                id INTEGER PRIMARY KEY NOT NULL,
                fname TEXT,
                lname TEXT,
                department TEXT,
                phNumber TEXT
            )
        ''')
        
        print("✅ Created employee table")
        
        # Insert sample data
        sample_employees = [
            ('John', 'Doe', 'Engineering', '555-0101'),
            ('Jane', 'Smith', 'Marketing', '555-0102'),
            ('Mike', 'Johnson', 'Engineering', '555-0103'),
            ('Sarah', 'Williams', 'HR', '555-0104'),
            ('David', 'Brown', 'Finance', '555-0105'),
            ('Lisa', 'Davis', 'Marketing', '555-0106'),
            ('Tom', 'Wilson', 'Engineering', '555-0107'),
            ('Amy', 'Garcia', 'HR', '555-0108'),
            ('Chris', 'Martinez', 'Finance', '555-0109'),
            ('Emma', 'Anderson', 'Marketing', '555-0110')
        ]
        
        cursor.executemany(
            "INSERT INTO employee (fname, lname, department, phNumber) VALUES (?, ?, ?, ?)",
            sample_employees
        )
        
        # Commit changes and close connection
        conn.commit()
        conn.close()
        
        print(f"✅ Created database '{db_path}' with {len(sample_employees)} sample employees")
        print("\nSample employees added:")
        print("-" * 50)
        
        # Display the inserted data
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM employee ORDER BY id")
        rows = cursor.fetchall()
        
        for row in rows:
            print(f"ID: {row['id']}, Name: {row['fname']} {row['lname']}, "
                  f"Department: {row['department']}, Phone: {row['phNumber']}")
        
        conn.close()
        
        print("-" * 50)
        print("\n🎉 Database setup complete!")
        print("You can now run the Employee Management System with:")
        print("python main.py")
        
    except sqlite3.Error as e:
        print(f"❌ Database error: {str(e)}")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")


def verify_database():
    """
    Verify that the database was created correctly.
    
    This function checks the database structure and data integrity.
    """
    db_path = "employees.db"
    
    if not Path(db_path).exists():
        print(f"❌ Database '{db_path}' not found!")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check table structure
        cursor.execute("PRAGMA table_info(employee)")
        columns = cursor.fetchall()
        
        expected_columns = ['id', 'fname', 'lname', 'department', 'phNumber']
        actual_columns = [col[1] for col in columns]
        
        if actual_columns != expected_columns:
            print("❌ Table structure is incorrect!")
            print(f"Expected: {expected_columns}")
            print(f"Actual: {actual_columns}")
            return False
        
        # Check data count
        cursor.execute("SELECT COUNT(*) FROM employee")
        count = cursor.fetchone()[0]
        
        if count == 0:
            print("⚠️  No data found in employee table")
        else:
            print(f"✅ Found {count} employees in database")
        
        conn.close()
        return True
        
    except sqlite3.Error as e:
        print(f"❌ Database verification error: {str(e)}")
        return False


def main():
    """
    Main function to create and verify the database.
    """
    print("=" * 60)
    print("    EMPLOYEE MANAGEMENT SYSTEM - DATABASE SETUP")
    print("=" * 60)
    
    create_database()
    
    print("\n" + "=" * 60)
    print("    DATABASE VERIFICATION")
    print("=" * 60)
    
    if verify_database():
        print("\n🎉 Database setup and verification completed successfully!")
    else:
        print("\n❌ Database verification failed!")


if __name__ == "__main__":
    main()
