"""
SQL Parser Module
Parses SQL query strings into structured dictionaries
"""

def parse_query(query_string):
    """
    Parse a SQL query string and return a structured dictionary.
    
    Supports: SELECT ... FROM ... WHERE ...
    
    Returns:
        dict: Contains keys 'select_cols', 'from_table', 'where_clause'
    """
    query = query_string.strip().upper()
    
    result = {
        'select_cols': [],
        'from_table': None,
        'where_clause': None
    }
    
    try:
        # Extract SELECT columns
        if 'SELECT' not in query:
            raise ValueError("Invalid SQL: Missing SELECT clause")
        
        select_start = query.find('SELECT') + 6
        from_pos = query.find('FROM')
        
        if from_pos == -1:
            raise ValueError("Invalid SQL: Missing FROM clause")
        
        select_part = query[select_start:from_pos].strip()
        
        # Parse SELECT columns
        if select_part == '*':
            result['select_cols'] = ['*']
        else:
            result['select_cols'] = [col.strip() for col in select_part.split(',')]
        
        # Extract FROM table
        where_pos = query.find('WHERE')
        
        if where_pos == -1:
            from_part = query[from_pos + 4:].strip()
        else:
            from_part = query[from_pos + 4:where_pos].strip()
        
        result['from_table'] = from_part
        
        # Extract WHERE clause if exists
        if where_pos != -1:
            where_part = query[where_pos + 5:].strip()
            result['where_clause'] = parse_where_clause(where_part, query_string)
        
        return result
        
    except Exception as e:
        raise ValueError(f"Query parsing error: {str(e)}")

def parse_where_clause(where_string, original_query):
    """
    Parse WHERE clause into a condition dictionary.
    Supports single conditions with operators: =, !=, >, <, >=, <=
    """
    operators = ['!=', '>=', '<=', '=', '>', '<']
    
    for op in operators:
        if op in where_string:
            parts = where_string.split(op)
            if len(parts) == 2:
                col = parts[0].strip()
                val_str = parts[1].strip()
                
                # Try to convert value to number, otherwise keep as string
                val = try_convert_value(val_str, original_query)
                
                return {
                    'col': col,
                    'op': op,
                    'val': val
                }
    
    raise ValueError(f"Invalid WHERE clause: {where_string}")

def try_convert_value(val_str, original_query):
    """
    Try to convert a value string to int or float, otherwise return as string.
    Strips quotes from string values.
    """
    val_str = val_str.strip()
    
    # Remove quotes if present
    if (val_str.startswith("'") and val_str.endswith("'")) or \
       (val_str.startswith('"') and val_str.endswith('"')):
        return val_str[1:-1]
    
    # Try to convert to number
    try:
        if '.' in val_str:
            return float(val_str)
        else:
            return int(val_str)
    except ValueError:
        return val_str
