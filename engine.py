"""
Query Execution Engine
Executes parsed SQL queries against in-memory data
"""

import csv
from parser import parse_query

class SQLEngine:
    def __init__(self):
        self.data = []
        self.table_name = None
    
    def load_csv(self, filepath):
        """
        Load a CSV file into memory as a list of dictionaries.
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.data = list(reader)
            
            # Extract table name from filepath
            self.table_name = filepath.split('/')[-1].replace('.csv', '').upper()
            
            if not self.data:
                raise ValueError("CSV file is empty")
                
            return f"Loaded {len(self.data)} rows from {filepath}"
        
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {filepath}")
        except Exception as e:
            raise Exception(f"Error loading CSV: {str(e)}")
    
    def execute_query(self, query_string):
        """
        Parse and execute a SQL query.
        """
        try:
            if not self.data:
                raise ValueError("No data loaded. Load a CSV file first.")
            
            # Parse the query
            parsed = parse_query(query_string)
            
            # Execute the query
            result = self._execute_parsed_query(parsed, query_string)
            
            return result
        
        except Exception as e:
            raise Exception(f"Query execution error: {str(e)}")
    
    def _execute_parsed_query(self, parsed, original_query):
        """
        Execute a parsed query against the data.
        """
        # Start with all rows
        rows = self.data[:]
        
        # Apply WHERE clause if present
        if parsed['where_clause']:
            rows = self._apply_where(rows, parsed['where_clause'], original_query)
        
        # Check if this is an aggregation query
        if self._is_aggregation_query(parsed['select_cols']):
            return self._execute_aggregation(rows, parsed['select_cols'], parsed['where_clause'])
        
        # Apply SELECT projection
        result = self._apply_select(rows, parsed['select_cols'])
        
        return result
    
    def _apply_where(self, rows, where_clause, original_query):
        """
        Filter rows based on WHERE clause condition.
        """
        col = where_clause['col']
        op = where_clause['op']
        val = where_clause['val']
        
        filtered = []
        
        for row in rows:
            if col not in row:
                raise ValueError(f"Column '{col}' not found in table")
            
            row_val = row[col]
            
            # Try to convert row value to number if val is a number
            if isinstance(val, (int, float)):
                try:
                    row_val = float(row_val) if '.' in str(row_val) else int(row_val)
                except (ValueError, TypeError):
                    continue
            
            # Apply comparison
            if self._compare_values(row_val, val, op):
                filtered.append(row)
        
        return filtered
    
    def _compare_values(self, row_val, filter_val, operator):
        """
        Compare two values using the given operator.
        """
        if operator == '=':
            return row_val == filter_val
        elif operator == '!=':
            return row_val != filter_val
        elif operator == '>':
            return row_val > filter_val
        elif operator == '<':
            return row_val < filter_val
        elif operator == '>=':
            return row_val >= filter_val
        elif operator == '<=':
            return row_val <= filter_val
        else:
            raise ValueError(f"Unknown operator: {operator}")
    
    def _is_aggregation_query(self, select_cols):
        """
        Check if the query contains an aggregation function.
        """
        for col in select_cols:
            if col.startswith('COUNT'):
                return True
        return False
    
    def _execute_aggregation(self, rows, select_cols, where_clause):
        """
        Execute aggregation queries (COUNT).
        """
        results = []
        
        for col in select_cols:
            if col.startswith('COUNT'):
                count_result = self._calculate_count(rows, col)
                results.append({col: count_result})
            else:
                raise ValueError("Only COUNT aggregation is supported")
        
        return results
    
    def _calculate_count(self, rows, count_expr):
        """
        Calculate COUNT aggregate.
        """
        if count_expr == 'COUNT(*)':
            return len(rows)
        
        # Extract column name from COUNT(column_name)
        col_start = count_expr.find('(') + 1
        col_end = count_expr.find(')')
        col_name = count_expr[col_start:col_end].strip()
        
        # Count non-null values
        count = 0
        for row in rows:
            if col_name in row and row[col_name]:  # Non-empty string or value
                count += 1
        
        return count
    
    def _apply_select(self, rows, select_cols):
        """
        Apply SELECT projection to rows.
        """
        if select_cols == ['*']:
            return rows
        
        # Project selected columns
        result = []
        for row in rows:
            projected_row = {}
            for col in select_cols:
                if col not in row:
                    raise ValueError(f"Column '{col}' not found in table")
                projected_row[col] = row[col]
            result.append(projected_row)
        
        return result
