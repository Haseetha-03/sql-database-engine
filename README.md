# sql-database-engine

A mini in-memory SQL database engine built in Python. Supports SELECT, FROM, WHERE clauses and COUNT aggregation with a command-line interface.

## Project Overview

This project implements a simplified, in-memory SQL query engine from scratch using Python. It provides a foundational understanding of how databases process and execute SQL queries. By creating your own parser and execution engine, you'll learn the core principles of data selection, filtering, and aggregation.

## Features

### Supported SQL Operations

1. **Data Loading**
   - Load data from CSV files into in-memory data structures
   - Store tables as a list of dictionaries for efficient row-wise operations

2. **SQL Parser**
   - Parse SELECT, FROM, and WHERE clauses
   - Extract column names, table names, and filter conditions
   - Simple string-based parsing (no complex parsing library required)

3. **Query Execution**
   - **Projection**: SELECT * and SELECT column_a, column_b
   - **Filtering**: WHERE clause with comparison operators (=, !=, >, <, >=, <=)
   - **Aggregation**: COUNT(*) and COUNT(column_name) functions

4. **Command-Line Interface**
   - Interactive REPL (Read-Eval-Print Loop)
   - Real-time query execution and results display
   - User-friendly error messages

## Supported SQL Grammar

### SELECT Queries

```sql
-- Select all columns
SELECT * FROM table_name

-- Select specific columns
SELECT column1, column2 FROM table_name

-- With WHERE clause
SELECT * FROM table_name WHERE column > value
SELECT col1, col2 FROM table_name WHERE column = 'value'

-- Aggregation
SELECT COUNT(*) FROM table_name
SELECT COUNT(column_name) FROM table_name
SELECT COUNT(*) FROM table_name WHERE column > 30
```

### Comparison Operators

- `=`  : Equal to
- `!=` : Not equal to
- `>`  : Greater than
- `<`  : Less than
- `>=` : Greater than or equal to
- `<=` : Less than or equal to

## Project Structure

```
sql-database-engine/
├── parser.py          # SQL parsing logic
├── engine.py          # Query execution engine
├── cli.py             # Command-line interface
├── samples/           # Sample CSV files for testing
├── README.md          # This file
└── requirements.txt   # Python dependencies (if any)
```

## Installation & Setup

### Prerequisites

- Python 3.7 or higher
- No external dependencies required (uses only standard library)

### Running the Application

1. Clone the repository:
```bash
git clone https://github.com/Haseetha-03/sql-database-engine.git
cd sql-database-engine
```

2. Run the CLI application:
```bash
python cli.py
```

3. The application will prompt you to enter the path to a CSV file:
```
Enter the path to your CSV file: samples/employees.csv
```

4. Once loaded, you can execute SQL queries:
```
SQL> SELECT * FROM employees
SQL> SELECT name, salary FROM employees WHERE age > 30
SQL> SELECT COUNT(*) FROM employees
SQL> exit
```

## Usage Examples

### Example 1: Basic SELECT
```
SQL> SELECT * FROM employees
```
Output: All rows and columns from the employees table

### Example 2: Column Selection
```
SQL> SELECT name, department FROM employees
```
Output: Only name and department columns for all employees

### Example 3: Filtering with WHERE
```
SQL> SELECT * FROM employees WHERE salary > 50000
```
Output: Employees with salary greater than 50,000

### Example 4: Aggregation
```
SQL> SELECT COUNT(*) FROM employees
```
Output: Total number of employees

```
SQL> SELECT COUNT(department) FROM employees WHERE age >= 25
```
Output: Count of non-null department values for employees 25 or older

## Implementation Details

### Parser (parser.py)

The parser takes a raw SQL string and returns a structured dictionary representation:

```python
parse_query("SELECT name, age FROM users WHERE age > 30")
# Returns:
# {
#     'select_cols': ['name', 'age'],
#     'from_table': 'users',
#     'where_clause': {'col': 'age', 'op': '>', 'val': 30}
# }
```

### Engine (engine.py)

Executes parsed queries against in-memory data:

1. Load data from CSV using csv.DictReader
2. Apply WHERE filters to rows
3. Apply SELECT projection to columns
4. Calculate aggregations if present

### CLI (cli.py)

Provides an interactive interface with:

- CSV file loading
- Query input loop
- Result formatting and display
- Error handling and user feedback

## Error Handling

The engine gracefully handles:

- Invalid SQL syntax
- Non-existent columns
- Non-existent CSV files
- Type mismatches in comparisons
- Empty result sets

Each error provides a clear, informative message to help users understand what went wrong.

## Sample Data

The repository includes sample CSV files:

- `samples/employees.csv` - Employee data with salary and department
- `samples/products.csv` - Product inventory data

You can use these files to test the application or create your own.

## Testing

Test the application with various queries:

```bash
# Run with sample data
python cli.py
Enter CSV path: samples/employees.csv

# Try different queries
SELECT * FROM employees
SELECT name FROM employees WHERE age > 30
SELECT COUNT(*) FROM employees
SELECT COUNT(department) FROM employees
exit
```

## Limitations

This is a beginner-level implementation with the following limitations:

- Single table queries only (no JOINs)
- Single WHERE condition (no AND/OR)
- No UPDATE, INSERT, or DELETE operations
- No GROUP BY or ORDER BY
- No transactions or persistence
- No indexing or query optimization

## Learning Outcomes

After implementing this project, you will understand:

- How SQL parsers work
- The execution pipeline for database queries
- Data structure design for in-memory databases
- String parsing and pattern matching
- Error handling in production code
- Building user interfaces for data applications

## License

Open source - feel free to use and modify for educational purposes.

## Author

Created as part of the Partnr Global Placement Program
