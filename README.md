# SQLite MCP Server

A simple Model Context Protocol (MCP) server for interacting with SQLite databases. This server provides tools to query, execute commands, and inspect your SQLite database through the MCP protocol.

## Features

- **Query Database**: Execute SELECT queries to retrieve data
- **Execute Commands**: Run any SQL command (INSERT, UPDATE, DELETE, CREATE, etc.)
- **Schema Inspection**: View database schema and table structures
- **Table Listing**: List all tables in the database

## Setup

### Prerequisites

- Python 3.8 or higher
- SQLite database file (`employees.db` in this case)

### Installation

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Make sure your SQLite database file (`employees.db`) is in the same directory as the server script.

### Configuration

The MCP server is configured via `mcp_config.json`. This file tells Cursor how to run the MCP server:

```json
{
  "mcpServers": {
    "sqlite-mcp-server": {
      "command": "python",
      "args": ["sqlite_mcp_server.py"],
      "cwd": "C:\\Users\\gaial\\Desktop\\AiDD_General\\cursor_test"
    }
  }
}
```

**Important**: Update the `cwd` path in `mcp_config.json` to match your actual workspace directory.

## Usage

### Available Tools

The MCP server provides four main tools:

1. **sqlite_query**: Execute SELECT queries
   - Input: `query` (string) - SQL SELECT statement
   - Returns: Query results in a formatted table

2. **sqlite_execute**: Execute any SQL command
   - Input: `command` (string) - Any SQL statement
   - Returns: Execution status and affected row count

3. **sqlite_schema**: Get database schema information
   - Input: None
   - Returns: Complete schema for all tables

4. **sqlite_tables**: List all tables in the database
   - Input: None
   - Returns: List of table names

### Example Usage

Once configured and running, you can use these tools through Cursor's MCP integration:

- Query data: "Show me all employees"
- Insert data: "Add a new employee with name John Doe"
- Update data: "Update employee ID 1's salary to 50000"
- Schema inspection: "What tables are in my database?"

## Running the Server

### Manual Testing

You can test the server manually by running:

```bash
python sqlite_mcp_server.py
```

### With Cursor

1. Add the MCP configuration to your Cursor settings
2. Restart Cursor
3. The server will automatically start when you use MCP tools

## Database Structure

The server works with any SQLite database. For the `employees.db` file, you can:

- Query employee data
- Insert new employees
- Update existing records
- Create new tables
- View table schemas

## Error Handling

The server includes comprehensive error handling for:
- Invalid SQL syntax
- Database connection issues
- File not found errors
- Permission problems

## Security Notes

- The server only allows SELECT queries through the `sqlite_query` tool
- All other SQL commands go through `sqlite_execute`
- Always validate your SQL inputs to prevent injection attacks
- The server runs with the same permissions as the Python process

## Troubleshooting

### Common Issues

1. **Database not found**: Ensure `employees.db` exists in the server directory
2. **Permission denied**: Check file permissions on the database file
3. **MCP not working**: Verify the configuration path in `mcp_config.json`
4. **Python not found**: Ensure Python is in your system PATH

### Debug Mode

For debugging, you can run the server directly and see error messages in the console.

## License

This MCP server is provided as-is for educational and development purposes.
