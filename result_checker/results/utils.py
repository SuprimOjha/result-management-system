import pandas as pd
from django.core.exceptions import ValidationError
from .models import StudentResult

def process_excel_file(excel_path, semester, program, school=None):
    try:
        # Read Excel file
        df = pd.read_excel(excel_path)
        
        print("=" * 50)
        print("DEBUG: Excel file loaded successfully")
        print(f"Number of rows: {len(df)}")
        print("Columns found:", list(df.columns))
        print("\nFirst few rows:")
        print(df.head())
        print("=" * 50)
        
        # Clean column names (remove spaces, make lowercase)
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
        print("Cleaned columns:", list(df.columns))
        
        records_processed = 0
        
        for index, row in df.iterrows():
            try:
                # Debug: Show what's in each row
                print(f"\n--- Processing row {index+1} ---")
                
                # Try multiple possible column names for symbol number
                symbol_number = None
                
                # Try different possible column names
                possible_symbol_cols = ['symbol_number', 'symbol', 'roll_no', 'roll_number', 'symbol_no']
                
                for col in possible_symbol_cols:
                    if col in df.columns:
                        symbol_number = str(row[col]).strip()
                        print(f"Found symbol in column '{col}': {symbol_number}")
                        if symbol_number and symbol_number.lower() != 'nan':
                            break
                
                if not symbol_number or symbol_number.lower() == 'nan':
                    print("No valid symbol number found, skipping row")
                    continue
                
                print(f"Processing: {symbol_number}")
                
                # Get full name (try multiple column names)
                full_name = ""
                for col in ['full_name', 'name', 'student_name']:
                    if col in df.columns:
                        full_name = str(row[col]).strip()
                        if full_name and full_name.lower() != 'nan':
                            break
                
                # Create or update the record
                result, created = StudentResult.objects.update_or_create(
                    symbol_number=symbol_number,
                    defaults={
                        'full_name': full_name.title(),
                        'faculty': str(row.get('faculty', '')).strip(),
                        'program': program,
                        'semester': semester,
                        'school': school,
                        
                        # Subject 1
                        'subject_1': str(row.get('subject_1', '')).strip(),
                        'marks_1': float(row.get('marks_1', 0) or 0),
                        'grade_1': str(row.get('grade_1', '')).strip(),
                        
                        # Subject 2
                        'subject_2': str(row.get('subject_2', '')).strip(),
                        'marks_2': float(row.get('marks_2', 0) or 0),
                        'grade_2': str(row.get('grade_2', '')).strip(),
                        
                        # Subject 3
                        'subject_3': str(row.get('subject_3', '')).strip(),
                        'marks_3': float(row.get('marks_3', 0) or 0),
                        'grade_3': str(row.get('grade_3', '')).strip(),
                        
                        # Subject 4
                        'subject_4': str(row.get('subject_4', '')).strip(),
                        'marks_4': float(row.get('marks_4', 0) or 0),
                        'grade_4': str(row.get('grade_4', '')).strip(),
                        
                        # Subject 5
                        'subject_5': str(row.get('subject_5', '')).strip(),
                        'marks_5': float(row.get('marks_5', 0) or 0),
                        'grade_5': str(row.get('grade_5', '')).strip(),
                        
                        # Overall results
                        'total_marks': float(row.get('total_marks', 0) or 0),
                        'percentage': float(row.get('percentage', 0) or 0),
                        'final_grade': str(row.get('final_grade', '')).strip(),
                        'result_status': str(row.get('result_status', 'PASS')).strip().upper(),
                    }
                )
                
                records_processed += 1
                print(f"✓ Successfully processed: {symbol_number} - {full_name}")
                
            except Exception as e:
                print(f"✗ Error processing row {index+1}: {str(e)}")
                print(f"Row data: {row.to_dict()}")
                continue
        
        print(f"\n{'='*50}")
        print(f"Total records processed: {records_processed}")
        print(f"{'='*50}")
        
        return records_processed
        
    except Exception as e:
        print(f"ERROR in process_excel_file: {str(e)}")
        raise ValidationError(f"Error processing Excel file: {str(e)}")
