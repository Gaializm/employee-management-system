#!/usr/bin/env python3
"""
Simple MCP Server for SQLite Database Operations
This server provides tools to interact with SQLite databases through MCP protocol.
"""

import asyncio
import json
import sqlite3
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    ListToolsResult,
    Tool,
    TextContent,
)


class SQLiteMCPServer:
    def __init__(self, db_path: str = "employees.db"):
        self.db_path = Path(db_path)
        self.server = Server("sqlite-mcp-server")
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Set up MCP server handlers"""
        
        @self.server.list_tools()
        async def list_tools() -> ListToolsResult:
            """List available SQLite tools"""
            return ListToolsResult(
                tools=[
                    Tool(
                        name="sqlite_query",
                        description="Execute a SELECT query on the SQLite database",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "query": {
                                    "type": "string",
                                    "description": "SQL SELECT query to execute"
                                }
                            },
                            "required": ["query"]
                        }
                    ),
                    Tool(
                        name="sqlite_execute",
                        description="Execute any SQL command (INSERT, UPDATE, DELETE, CREATE, etc.) on the SQLite database",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "command": {
                                    "type": "string",
                                    "description": "SQL command to execute"
                                }
                            },
                            "required": ["command"]
                        }
                    ),
                    Tool(
                        name="sqlite_schema",
                        description="Get the schema information for all tables in the database",
                        inputSchema={
                            "type": "object",
                            "properties": {}
                        }
                    ),
                    Tool(
                        name="sqlite_tables",
                        description="List all tables in the database",
                        inputSchema={
                            "type": "object",
                            "properties": {}
                        }
                    )
                ]
            )
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
            """Handle tool calls"""
            
            if name == "sqlite_query":
                return await self._handle_query(arguments)
            elif name == "sqlite_execute":
                return await self._handle_execute(arguments)
            elif name == "sqlite_schema":
                return await self._handle_schema()
            elif name == "sqlite_tables":
                return await self._handle_tables()
            else:
                raise ValueError(f"Unknown tool: {name}")
    
    async def _handle_query(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Handle SELECT queries"""
        query = arguments.get("query", "")
        
        if not query.strip().upper().startswith("SELECT"):
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text="Error: Only SELECT queries are allowed with sqlite_query tool. Use sqlite_execute for other operations."
                )]
            )
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row  # Enable column access by name
                cursor = conn.cursor()
                cursor.execute(query)
                
                rows = cursor.fetchall()
                
                if not rows:
                    result_text = "Query executed successfully. No rows returned."
                else:
                    # Convert rows to a more readable format
                    columns = [description[0] for description in cursor.description]
                    result_text = f"Query executed successfully. Found {len(rows)} row(s):\n\n"
                    
                    # Create a table-like output
                    result_text += " | ".join(columns) + "\n"
                    result_text += "-" * (len(" | ".join(columns))) + "\n"
                    
                    for row in rows:
                        row_values = [str(row[col]) for col in columns]
                        result_text += " | ".join(row_values) + "\n"
                
                return CallToolResult(
                    content=[TextContent(type="text", text=result_text)]
                )
                
        except sqlite3.Error as e:
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=f"SQLite Error: {str(e)}"
                )]
            )
        except Exception as e:
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=f"Error executing query: {str(e)}"
                )]
            )
    
    async def _handle_execute(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Handle non-SELECT SQL commands"""
        command = arguments.get("command", "")
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(command)
                conn.commit()
                
                # Get the number of affected rows
                rows_affected = cursor.rowcount
                
                result_text = f"Command executed successfully. {rows_affected} row(s) affected."
                
                # If it's a SELECT query, also return the results
                if command.strip().upper().startswith("SELECT"):
                    rows = cursor.fetchall()
                    if rows:
                        columns = [description[0] for description in cursor.description]
                        result_text += f"\n\nFound {len(rows)} row(s):\n\n"
                        
                        # Create a table-like output
                        result_text += " | ".join(columns) + "\n"
                        result_text += "-" * (len(" | ".join(columns))) + "\n"
                        
                        for row in rows:
                            row_values = [str(row[col]) for col in columns]
                            result_text += " | ".join(row_values) + "\n"
                
                return CallToolResult(
                    content=[TextContent(type="text", text=result_text)]
                )
                
        except sqlite3.Error as e:
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=f"SQLite Error: {str(e)}"
                )]
            )
        except Exception as e:
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=f"Error executing command: {str(e)}"
                )]
            )
    
    async def _handle_schema(self) -> CallToolResult:
        """Get database schema information"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get all table names
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                
                if not tables:
                    return CallToolResult(
                        content=[TextContent(
                            type="text",
                            text="No tables found in the database."
                        )]
                    )
                
                result_text = "Database Schema:\n\n"
                
                for table in tables:
                    table_name = table[0]
                    result_text += f"Table: {table_name}\n"
                    result_text += "-" * (len(table_name) + 7) + "\n"
                    
                    # Get table schema
                    cursor.execute(f"PRAGMA table_info({table_name});")
                    columns = cursor.fetchall()
                    
                    for col in columns:
                        col_id, name, data_type, not_null, default_val, pk = col
                        nullable = "NOT NULL" if not_null else "NULL"
                        primary_key = "PRIMARY KEY" if pk else ""
                        default = f"DEFAULT {default_val}" if default_val is not None else ""
                        
                        result_text += f"  {name} {data_type} {nullable} {primary_key} {default}\n".strip() + "\n"
                    
                    result_text += "\n"
                
                return CallToolResult(
                    content=[TextContent(type="text", text=result_text)]
                )
                
        except sqlite3.Error as e:
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=f"SQLite Error: {str(e)}"
                )]
            )
        except Exception as e:
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=f"Error getting schema: {str(e)}"
                )]
            )
    
    async def _handle_tables(self) -> CallToolResult:
        """List all tables in the database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                
                if not tables:
                    result_text = "No tables found in the database."
                else:
                    table_names = [table[0] for table in tables]
                    result_text = f"Tables in database ({len(table_names)} total):\n\n"
                    result_text += "\n".join(f"- {name}" for name in table_names)
                
                return CallToolResult(
                    content=[TextContent(type="text", text=result_text)]
                )
                
        except sqlite3.Error as e:
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=f"SQLite Error: {str(e)}"
                )]
            )
        except Exception as e:
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=f"Error listing tables: {str(e)}"
                )]
            )
    
    async def run(self):
        """Run the MCP server"""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="sqlite-mcp-server",
                    server_version="1.0.0",
                    capabilities=self.server.get_capabilities(
                        notification_options=None,
                        experimental_capabilities={}
                    )
                )
            )


async def main():
    """Main entry point"""
    # You can change the database path here
    db_path = "employees.db"
    
    if not Path(db_path).exists():
        print(f"Error: Database file '{db_path}' not found.", file=sys.stderr)
        sys.exit(1)
    
    server = SQLiteMCPServer(db_path)
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
