"""
Command-Line Interface for SQL Database Engine
Provides an interactive REPL for executing SQL queries
"""

from engine import SQLEngine

def main():
    """
    Main CLI loop for the SQL Database Engine.
    """
    engine = SQLEngine()
    
    print("\n" + "="*60)
    print("  Mini SQL Database Engine")
    print("="*60)
    print("\nWelcome! This is an in-memory SQL query engine.")
    print("Type 'exit' or 'quit' to exit the program.\n")
    
    # Load CSV file
    while True:
        csv_path = input("Enter the path to your CSV file: ").strip()
        if not csv_path:
            print("Please provide a valid file path.")
            continue
        
        try:
            msg = engine.load_csv(csv_path)
            print(f"\n✓ {msg}\n")
            break
        except Exception as e:
            print(f"✗ Error: {str(e)}")
            print()
    
    # Query loop
    print("Ready for queries. Type your SQL or 'exit' to quit.\n")
    
    while True:
        try:
            query = input("SQL> ").strip()
            
            # Check for exit commands
            if query.lower() in ['exit', 'quit', 'q']:
                print("\nThank you for using SQL Database Engine!\n")
                break
            
            if not query:
                continue
            
            # Execute query
            result = engine.execute_query(query)
            
            # Display results
            print_results(result)
            print()
        
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            print(f"Error: {str(e)}\n")

def print_results(result):
    """
    Format and print query results.
    """
    if not result:
        print("(No results)")
        return
    
    # Handle aggregation results
    if isinstance(result, list) and len(result) > 0 and isinstance(result[0], dict):
        first_item = result[0]
        
        # Check if it's an aggregation result (single column)
        if len(first_item) == 1:
            for item in result:
                for key, value in item.items():
                    print(f"{key}: {value}")
            return
    
    # Handle regular results
    if isinstance(result, list) and len(result) > 0:
        if isinstance(result[0], dict):
            # Get headers
            headers = list(result[0].keys())
            
            # Print headers
            header_str = " | ".join(headers)
            print(header_str)
            print("-" * len(header_str))
            
            # Print rows
            for row in result:
                row_str = " | ".join(str(row.get(h, '')) for h in headers)
                print(row_str)
        else:
            for item in result:
                print(item)
    else:
        print(result)

if __name__ == "__main__":
    main()
