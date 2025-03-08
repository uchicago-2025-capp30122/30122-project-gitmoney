import csv
import pathlib
import json

def convert_cost(cost):
    try:
        # First remove any currency symbols and commas
        if isinstance(cost, str):
            cost_str = cost.replace('$', '').replace(',', '')
            cost_float = float(cost_str)
        else:
            cost_float = float(cost)
    except (ValueError, TypeError):
        # If conversion fails, set to 0
        cost_float = 0.0
    return cost_float

if __name__ == "__main__":
    # Input and output files (use different paths)
    input_file = pathlib.Path.cwd() / 'data/final_menu_money.csv'
    output_file = pathlib.Path.cwd() / 'data/final_menu_money_converted.csv'
    
    # Read the input file
    with open(input_file, 'r', encoding='utf-8') as csvfile:
        final_menu_money = list(csv.DictReader(csvfile))
    
    print(f"Read {len(final_menu_money)} rows from input file")
    
    # Check if cross_streets might be JSON strings
    sample_row = final_menu_money[0] if final_menu_money else {}
    cross_streets_sample = sample_row.get('cross_streets', '')
    print(f"Sample cross_streets: {cross_streets_sample[:100]}...")
    
    unpacked_final_menu_money = []
    for row in final_menu_money:
        # Try to parse cross_streets if it's a JSON string
        cross_streets = []
        try:
            if 'cross_streets' in row and row['cross_streets']:
                if isinstance(row['cross_streets'], str):
                    cross_streets = json.loads(row['cross_streets'])
                else:
                    cross_streets = row['cross_streets']
        except json.JSONDecodeError:
            print(f"Warning: Could not parse cross_streets for row: {row['description']}")
        
        # Always convert cost consistently
        row['cost'] = convert_cost(row['cost'])
        
        if cross_streets:
            for cross_street in cross_streets:
                new_row = row.copy()  # Copy all the original fields
                
                # Add cross street fields if it's a dictionary
                if isinstance(cross_street, dict):
                    for key, value in cross_street.items():
                        new_row[key] = value
                
                unpacked_final_menu_money.append(new_row)
        else:
            # Keep rows without cross streets too
            unpacked_final_menu_money.append(row)
    
    print(f"Generated {len(unpacked_final_menu_money)} rows for output file")
    
    # Get all field names from the data
    fieldnames = set()
    for row in unpacked_final_menu_money:
        fieldnames.update(row.keys())
    fieldnames = sorted(list(fieldnames))
    
    # Write to the output file
    with open(output_file, 'w', encoding='utf-8', newline='') as csvfile:
        csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        csvwriter.writeheader()
        for row in unpacked_final_menu_money:
            csvwriter.writerow(row)
    
    print(f"Successfully wrote data to {output_file}")