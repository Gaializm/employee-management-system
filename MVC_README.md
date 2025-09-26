# Employee Management System - MVC Application

A simple, well-structured MVC (Model-View-Controller) application for managing employee records in a SQLite database. This application demonstrates clean separation of concerns with comprehensive commenting throughout the codebase.

## 🏗️ Architecture Overview

This application follows the MVC pattern with an additional Data Access Layer (DAL) for clean database operations:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│      VIEW       │    │   CONTROLLER    │    │   DATA ACCESS   │
│   (User UI)     │◄──►│ (Business Logic) │◄──►│    LAYER (DAL)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                         │
                                                         ▼
                                               ┌─────────────────┐
                                               │   SQLite DB     │
                                               │ (employees.db)  │
                                               └─────────────────┘
```

## 📁 Project Structure

```
├── main.py                      # Application entry point
├── models.py                    # Data models (Employee, etc.)
├── controller.py                # Business logic controller
├── view.py                      # User interface layer
├── data_access_layer.py         # Database operations
├── create_sample_database.py    # Database initialization script
├── employees.db                 # SQLite database file
└── README.md                    # This file
```

## 🚀 Quick Start

### 1. Setup Database

First, create the database with sample data:

```bash
python create_sample_database.py
```

This will create `employees.db` with 10 sample employees across different departments.

### 2. Run the Application

```bash
python main.py
```

## 📋 Features

### Core CRUD Operations
- ✅ **Create** - Add new employees
- ✅ **Read** - View all employees or search by criteria
- ✅ **Update** - Modify existing employee information
- ✅ **Delete** - Remove employees from the system

### Additional Features
- 🔍 **Search** - Find employees by name or department
- 📊 **Statistics** - View employee counts and department breakdowns
- 🏢 **Department Management** - List all departments
- ✅ **Data Validation** - Comprehensive input validation
- 🔒 **Duplicate Prevention** - Prevents duplicate phone numbers

## 🎯 Usage Examples

### Main Menu Options

1. **Add New Employee** - Create a new employee record
2. **View All Employees** - Display all employees in the system
3. **Search Employees** - Find employees by various criteria
4. **Update Employee** - Modify existing employee information
5. **Delete Employee** - Remove an employee from the system
6. **View Employee Statistics** - See department breakdowns and counts
7. **View Departments** - List all departments in the system
8. **Exit** - Close the application

### Sample Interactions

```
Enter Employee Information:
------------------------------
First Name: Alice
Last Name: Johnson
Department: Engineering
Phone Number: 555-0123

✅ Employee created successfully with ID: 11
```

## 🏛️ Architecture Details

### Model Layer (`models.py`)
- **Employee**: Main data model with validation
- **EmployeeSearchCriteria**: Search parameters
- **EmployeeUpdateData**: Partial update data

### Controller Layer (`controller.py`)
- **EmployeeController**: Business logic and validation
- Coordinates between View and Data Access Layer
- Implements business rules and error handling

### View Layer (`view.py`)
- **EmployeeView**: User interface and interaction
- Handles all user input/output
- Provides menu-driven interface

### Data Access Layer (`data_access_layer.py`)
- **EmployeeDAL**: Database operations
- **DatabaseConnection**: Connection management
- Handles all SQLite interactions

## 🔧 Database Schema

The application uses a simple employee table:

```sql
CREATE TABLE employee (
    id INTEGER PRIMARY KEY NOT NULL,
    fname TEXT,
    lname TEXT,
    department TEXT,
    phNumber TEXT
);
```

## 🛡️ Error Handling

The application includes comprehensive error handling:

- **Database Connection Errors** - Graceful handling of DB issues
- **Input Validation** - Prevents invalid data entry
- **Duplicate Prevention** - Stops duplicate phone numbers
- **User-Friendly Messages** - Clear error and success messages

## 📝 Code Quality Features

- **Comprehensive Comments** - Every function and class is documented
- **Type Hints** - Full type annotation for better code clarity
- **Clean Architecture** - Proper separation of concerns
- **Error Handling** - Robust error management throughout
- **User Experience** - Intuitive menu-driven interface

## 🧪 Testing the Application

### Sample Data Included

The database initialization script creates 10 sample employees:

- **Engineering**: John Doe, Mike Johnson, Tom Wilson
- **Marketing**: Jane Smith, Lisa Davis, Emma Anderson
- **HR**: Sarah Williams, Amy Garcia
- **Finance**: David Brown, Chris Martinez

### Test Scenarios

1. **Add Employee**: Try adding a new employee
2. **Search**: Search for "John" or filter by "Engineering"
3. **Update**: Modify an existing employee's department
4. **Delete**: Remove an employee (with confirmation)
5. **Statistics**: View department breakdowns

## 🔍 Code Walkthrough

### Adding an Employee (Flow)

1. **View** (`view.py`) - Collects user input
2. **Controller** (`controller.py`) - Validates data and business rules
3. **Model** (`models.py`) - Validates employee data structure
4. **DAL** (`data_access_layer.py`) - Executes SQL INSERT
5. **Database** - Stores the new record

### Searching Employees (Flow)

1. **View** - Gets search criteria from user
2. **Controller** - Processes search logic
3. **DAL** - Executes appropriate SQL query
4. **Model** - Converts results to Employee objects
5. **View** - Displays formatted results

## 🚨 Important Notes

- The application requires Python 3.8+
- SQLite database file (`employees.db`) must exist
- All database operations are transactional
- Phone numbers must be unique across all employees
- All text fields are trimmed of whitespace

## 🔧 Customization

### Adding New Fields

To add new fields to the employee model:

1. Update the database schema in `create_sample_database.py`
2. Modify the `Employee` model in `models.py`
3. Update the DAL methods in `data_access_layer.py`
4. Adjust the view input/output in `view.py`

### Changing Database

To use a different database:

1. Modify the `DatabaseConnection` class in `data_access_layer.py`
2. Update the connection string/path
3. Ensure the table schema matches

## 📚 Learning Objectives

This application demonstrates:

- **MVC Pattern** - Clean separation of concerns
- **Data Access Layer** - Database abstraction
- **Error Handling** - Robust error management
- **User Interface Design** - Menu-driven console app
- **Code Documentation** - Comprehensive commenting
- **Type Safety** - Python type hints
- **SQLite Integration** - Database operations

## 🤝 Contributing

This is a learning project. Feel free to:

- Add new features
- Improve error handling
- Enhance the user interface
- Add unit tests
- Optimize database queries

## 📄 License

This project is for educational purposes. Feel free to use and modify as needed.
