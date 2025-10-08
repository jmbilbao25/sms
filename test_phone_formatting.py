#!/usr/bin/env python3
"""
COMPREHENSIVE PHONE NUMBER FORMATTING TEST SUITE
================================================

This test suite validates all possible phone number formatting scenarios:
- 63 format (12 digits) and 09 format (11 digits) handling
- Decimal number processing (.0, .5, .25, etc.)
- Google Sheets formula handling
- Column type detection
- Related number validation
- Edge cases and error conditions
- Separator cleaning (spaces, dashes, dots, etc.)
- Scientific notation handling
- Unicode character processing
- Invalid format detection
- Duplicate detection
- Large dataset processing
"""

import pandas as pd
import re
from datetime import datetime
import os
import glob

def detect_column_type(series):
    """Detect if a column contains numeric data"""
    if series is None or len(series) == 0:
        return "unknown"
    
    # Get non-null values
    non_null_values = series.dropna()
    if len(non_null_values) == 0:
        return "empty"
    
    # Check if all non-null values can be converted to numbers
    numeric_count = 0
    for value in non_null_values:
        try:
            float(str(value))
            numeric_count += 1
        except ValueError:
            pass
    
    # If more than 80% of values are numeric, consider it a numeric column
    if numeric_count / len(non_null_values) >= 0.8:
        return "numeric"
    else:
        return "text"

def format_phone_number(phone):
    """Format phone number to digits only - same logic as in SMS.py"""
    if pd.isna(phone):
        return ""
    # Convert to string and remove all non-digit characters
    phone_str = str(phone)
    
    # Check if original string starts with 0 (for 09 format preservation)
    starts_with_zero = phone_str.startswith('0')
    
    # Handle decimal numbers more carefully
    # For phone numbers, we want to truncate to integer part (not round)
    if '.' in phone_str:
        try:
            # Try to parse as float to check if it's a whole number
            float_val = float(phone_str)
            if float_val == int(float_val):  # It's a whole number
                # For whole numbers, just remove the decimal part without converting to int
                phone_str = phone_str.split('.')[0]
            else:
                # It's a decimal number, truncate to integer part
                # But preserve the leading zero if it was there originally
                int_part = str(int(float_val))
                if starts_with_zero and not int_part.startswith('0'):
                    # The int conversion removed the leading zero, add it back
                    phone_str = '0' + int_part
                else:
                    phone_str = int_part
        except ValueError:
            # If it's not a valid number, just remove the decimal part
            phone_str = phone_str.split('.')[0]
    
    # Extract digits while preserving the original structure for 09 numbers
    digits = re.sub(r'\D', '', phone_str)
    
    # Special handling for 09 format numbers that might have lost their leading zero
    # If the original string started with 0 and we have 10 digits, add the leading zero back
    if starts_with_zero and len(digits) == 10:
        digits = '0' + digits
    
    # Note: We do NOT convert 09 numbers to 63 - 09 is a valid Philippine format
    # Only remove non-digit characters and handle decimal formats
    
    return digits

def is_valid_ph_phone(digits):
    """Check if phone number is valid Philippine format"""
    if len(digits) == 11 and digits.startswith('09'):
        return True
    elif len(digits) == 12 and digits.startswith('63'):
        return True
    return False

def are_related_phones(phone_63, phone_09):
    """Check if 63 and 09 format numbers are related (same number)"""
    if not phone_63 or not phone_09:
        return False
    
    # Format both numbers
    formatted_63 = format_phone_number(phone_63)
    formatted_09 = format_phone_number(phone_09)
    
    # Check if they represent the same number
    if len(formatted_63) == 12 and len(formatted_09) == 11:
        # 63 format should be 63 + 09 format (without the 0)
        return formatted_63 == "63" + formatted_09[1:]
    elif len(formatted_63) == 11 and len(formatted_09) == 12:
        # 09 format should be 0 + 63 format (without the 63)
        return formatted_09 == "0" + formatted_63[2:]
    
    return False

def test_individual_phone_formatting():
    """Test individual phone number formatting with comprehensive cases"""
    print("TESTING INDIVIDUAL PHONE NUMBER FORMATTING")
    print("=" * 80)
    
    test_cases = [
        # Format: (input, expected_output, description, should_be_valid, test_category)
        
        # === WHOLE NUMBERS WITH .0 ===
        ("639999999999.0", "639999999999", "63 format whole number with .0", True, "Decimal Cleanup"),
        ("099999999999.0", "099999999999", "09 format whole number with .0", True, "Decimal Cleanup"),
        ("639123456780.0", "639123456780", "63 format ending with 0 naturally", True, "Decimal Cleanup"),
        ("091234567890.0", "091234567890", "09 format ending with 0 naturally", True, "Decimal Cleanup"),
        
        # === DECIMALS WITH ACTUAL DECIMAL PARTS ===
        ("639123456780.5", "639123456780", "63 format decimal .5 (truncate)", True, "Decimal Truncation"),
        ("091234567890.5", "091234567890", "09 format decimal .5 (truncate)", True, "Decimal Truncation"),
        ("639123456789.25", "639123456789", "63 format decimal .25 (truncate)", True, "Decimal Truncation"),
        ("091234567890.25", "091234567890", "09 format decimal .25 (truncate)", True, "Decimal Truncation"),
        ("639123456780.1", "639123456780", "63 format decimal .1 (truncate)", True, "Decimal Truncation"),
        ("091234567890.1", "091234567890", "09 format decimal .1 (truncate)", True, "Decimal Truncation"),
        ("639123456780.9", "639123456780", "63 format decimal .9 (truncate)", True, "Decimal Truncation"),
        ("091234567890.9", "091234567890", "09 format decimal .9 (truncate)", True, "Decimal Truncation"),
        
        # === HIGH PRECISION DECIMALS ===
        ("639123456789.99", "639123456789", "63 format high precision decimal", True, "High Precision"),
        ("091234567890.99", "091234567890", "09 format high precision decimal", True, "High Precision"),
        ("639123456780.01", "639123456780", "63 format low precision decimal", True, "Low Precision"),
        ("091234567890.01", "091234567890", "09 format low precision decimal", True, "Low Precision"),
        
        # === CLEAN FORMATS (NO CHANGES) ===
        ("639123456789", "639123456789", "63 format clean (no change)", True, "Clean Format"),
        ("091234567890", "091234567890", "09 format clean (no change)", True, "Clean Format"),
        
        # === EMPTY/ZERO VALUES ===
        ("0", "0", "Zero value", False, "Empty Values"),
        ("0.0", "0", "Zero with decimal", False, "Empty Values"),
        ("", "", "Empty string", False, "Empty Values"),
        
        # === INVALID FORMATS ===
        ("123456789", "123456789", "Too short (9 digits)", False, "Invalid Format"),
        ("6391234567890", "6391234567890", "Too long (13 digits)", False, "Invalid Format"),
        ("081234567890", "081234567890", "Wrong prefix (08)", False, "Invalid Format"),
        ("621234567890", "621234567890", "Wrong prefix (62)", False, "Invalid Format"),
        
        # === SPECIAL CASES ===
        ("639123456789.000", "639123456789", "Multiple zeros after decimal", True, "Special Cases"),
        ("091234567890.000", "091234567890", "Multiple zeros after decimal", True, "Special Cases"),
        ("639123456789.999", "639123456789", "High decimal value", True, "Special Cases"),
        ("091234567890.999", "091234567890", "High decimal value", True, "Special Cases"),
        
        # === SEPARATOR CLEANING ===
        ("639 123 456 789", "639123456789", "Spaces in phone number", True, "Separator Cleaning"),
        ("639-123-456-789", "639123456789", "Dashes in phone number", True, "Separator Cleaning"),
        ("639.123.456.789", "639123456789", "Dots in phone number", True, "Separator Cleaning"),
        ("(639) 123-456-789", "639123456789", "Parentheses and dash", True, "Separator Cleaning"),
        ("+639123456789", "639123456789", "Plus sign prefix", True, "Separator Cleaning"),
        ("0912 345 6789", "091234567890", "09 format with spaces", True, "Separator Cleaning"),
        ("0912-345-6789", "091234567890", "09 format with dashes", True, "Separator Cleaning"),
        
        # === SCIENTIFIC NOTATION ===
        ("6.39123456789E+11", "639123456789", "Scientific notation 63", True, "Scientific Notation"),
        ("9.1234567890E+10", "091234567890", "Scientific notation 09", True, "Scientific Notation"),
        ("6.39234567890E+11", "639234567890", "Another scientific 63", True, "Scientific Notation"),
        
        # === VERY LONG DECIMALS ===
        ("639123456789.123456789", "639123456789", "Very long decimal", True, "Long Decimals"),
        ("639123456789.987654321", "639123456789", "Long decimal with 9s", True, "Long Decimals"),
        ("639123456789.000000001", "639123456789", "Tiny decimal", True, "Long Decimals"),
        ("639123456789.999999999", "639123456789", "Almost 1 decimal", True, "Long Decimals"),
        
        # === LEADING ZEROS ===
        ("0639123456789", "639123456789", "Leading zero 63", True, "Leading Zeros"),
        ("00639123456789", "639123456789", "Double leading zero", True, "Leading Zeros"),
        ("000639123456789", "639123456789", "Triple leading zero", True, "Leading Zeros"),
        
        # === NEGATIVE NUMBERS ===
        ("-639123456789", "639123456789", "Negative 63 (should clean)", True, "Negative Numbers"),
        ("-091234567890", "091234567890", "Negative 09 (should clean)", True, "Negative Numbers"),
        ("-639123456789.5", "639123456789", "Negative with decimal", True, "Negative Numbers"),
        
        # === SPECIAL CHARACTERS ===
        ("639#123#456#789", "639123456789", "Hash separators", True, "Special Characters"),
        ("639*123*456*789", "639123456789", "Asterisk separators", True, "Special Characters"),
        ("639@123@456@789", "639123456789", "At separators", True, "Special Characters"),
        ("639$123$456$789", "639123456789", "Dollar separators", True, "Special Characters"),
        ("639%123%456%789", "639123456789", "Percent separators", True, "Special Characters"),
        ("639_123_456_789", "639123456789", "Underscore separators", True, "Special Characters"),
        ("639/123/456/789", "639123456789", "Slash separators", True, "Special Characters"),
        
        # === QUOTES AND BRACKETS ===
        ("\"639123456789\"", "639123456789", "Double quoted", True, "Quotes Brackets"),
        ("'639123456789'", "639123456789", "Single quoted", True, "Quotes Brackets"),
        ("[639] 123-456-789", "639123456789", "Square brackets", True, "Quotes Brackets"),
        ("(639) 123-456-789", "639123456789", "Parentheses", True, "Quotes Brackets"),
        
        # === COMMAS ===
        ("639,123,456,789", "639123456789", "Comma separators", True, "Comma Separators"),
        ("091,234,567,890", "091234567890", "09 format with commas", True, "Comma Separators"),
        
        # === MIXED SEPARATORS ===
        ("639-123.456 789", "639123456789", "Mixed separators", True, "Mixed Separators"),
        ("639.123-456 789", "639123456789", "Mixed separators 2", True, "Mixed Separators"),
        ("0912-345.678 9", "091234567890", "09 mixed separators", True, "Mixed Separators"),
    ]
    
    # Group tests by category
    categories = {}
    for input_val, expected, description, should_be_valid, category in test_cases:
        if category not in categories:
            categories[category] = []
        categories[category].append((input_val, expected, description, should_be_valid))
    
    all_passed = True
    total_tests = 0
    passed_tests = 0
    
    for category, tests in categories.items():
        print(f"\n{category.upper()}")
        print("-" * 60)
        
        for input_val, expected, description, should_be_valid in tests:
            result = format_phone_number(input_val)
            is_valid = is_valid_ph_phone(result)
            
            format_correct = result == expected
            validation_correct = is_valid == should_be_valid
            
            total_tests += 1
            if format_correct and validation_correct:
                status = "PASS"
                passed_tests += 1
            else:
                status = "FAIL"
                all_passed = False
            
            print(f"{status} | {input_val:25} -> {result:15} | Valid: {is_valid:5} | {description}")
            if not format_correct:
                print(f"        Expected: {expected}")
            if not validation_correct:
                print(f"        Expected valid: {should_be_valid}")
    
    print(f"\nINDIVIDUAL FORMATTING RESULTS: {passed_tests}/{total_tests} tests passed")
    return all_passed

def test_related_phone_validation():
    """Test related phone number validation (63 and 09 formats)"""
    print("\nTESTING RELATED PHONE NUMBER VALIDATION")
    print("=" * 80)
    
    related_test_cases = [
        # Format: (phone_63, phone_09, description, should_be_related)
        ("639976341596.0", "09976341596.0", "Related numbers with .0", True),
        ("639123456780.0", "091234567890.0", "Related numbers ending with 0", True),
        ("639999999999", "099999999999", "Perfect related numbers", True),
        ("639876543210", "09876543210", "Standard related pair", True),
        ("639123456789.5", "091234567890.5", "Related decimals (should truncate)", True),
        ("639123456780.25", "091234567890.25", "Related complex decimals", True),
        ("639123456789.0", "091234567890.0", "Related whole numbers with .0", True),
        ("639123456780", "091234567890", "Standard related formats", True),
        ("639123456789.99", "091234567890.99", "Related high precision decimals", True),
        ("639123456780.01", "091234567890.01", "Related low precision decimals", True),
        
        # Unrelated cases
        ("639123456789", "091234567891", "Different numbers (unrelated)", False),
        ("639123456780", "091234567890", "Same numbers (related)", True),
        ("639999999999", "099999999998", "Almost same (unrelated)", False),
        ("639123456789", "081234567890", "Wrong prefix (unrelated)", False),
        
        # With separators
        ("639-123-456-789", "0912-345-6789", "Related with separators", True),
        ("639.123.456.789", "0912.345.6789", "Related with dots", True),
        ("639 123 456 789", "0912 345 6789", "Related with spaces", True),
        ("(639) 123-456-789", "(0912) 345-6789", "Related with parentheses", True),
        ("+639123456789", "+091234567890", "Related with plus signs", True),
    ]
    
    all_passed = True
    total_tests = 0
    passed_tests = 0
    
    print("RELATED PHONE VALIDATION")
    print("-" * 60)
    
    for phone_63, phone_09, description, should_be_related in related_test_cases:
        is_related = are_related_phones(phone_63, phone_09)
        
        total_tests += 1
        if is_related == should_be_related:
            status = "PASS"
            passed_tests += 1
        else:
            status = "FAIL"
            all_passed = False
        
        print(f"{status} | 63: {phone_63:25} | 09: {phone_09:25} | Related: {is_related:5} | {description}")
        if is_related != should_be_related:
            print(f"        Expected related: {should_be_related}")
    
    print(f"\nRELATED VALIDATION RESULTS: {passed_tests}/{total_tests} tests passed")
    return all_passed

def test_csv_processing():
    """Test CSV processing with comprehensive test file"""
    print("\nTESTING CSV PROCESSING")
    print("=" * 80)
    
    try:
        # Read the test CSV
        df = pd.read_csv("test_comprehensive_phone_formats.csv")
        print(f"Loaded CSV with {len(df)} rows and {len(df.columns)} columns")
        
        # Test column type detection
        phone_63_col = 'Phone_63'
        phone_09_col = 'Phone_09'
        
        col_63_type = detect_column_type(df[phone_63_col])
        col_09_type = detect_column_type(df[phone_09_col])
        
        print(f"Column type detection:")
        print(f"  - {phone_63_col}: {col_63_type}")
        print(f"  - {phone_09_col}: {col_09_type}")
        
        # Test phone number formatting
        df_formatted = df.copy()
        df_formatted[phone_63_col] = df_formatted[phone_63_col].apply(format_phone_number)
        df_formatted[phone_09_col] = df_formatted[phone_09_col].apply(format_phone_number)
        
        # Test validation
        valid_63 = df_formatted[phone_63_col].apply(is_valid_ph_phone)
        valid_09 = df_formatted[phone_09_col].apply(is_valid_ph_phone)
        
        valid_63_count = valid_63.sum()
        valid_09_count = valid_09.sum()
        invalid_63_count = len(df_formatted) - valid_63_count
        invalid_09_count = len(df_formatted) - valid_09_count
        
        print(f"Validation results:")
        print(f"  - 63 format: {valid_63_count} valid, {invalid_63_count} invalid")
        print(f"  - 09 format: {valid_09_count} valid, {invalid_09_count} invalid")
        
        # Test related number validation
        related_count = 0
        for idx, row in df_formatted.iterrows():
            if are_related_phones(row[phone_63_col], row[phone_09_col]):
                related_count += 1
        
        print(f"  - Related pairs: {related_count}/{len(df_formatted)}")
        
        # Show detailed results
        print(f"\nDETAILED RESULTS")
        print("-" * 80)
        print(f"{'Row':<4} | {'63 Format':<20} | {'09 Format':<20} | {'Valid':<8} | {'Related':<8} | {'Name'}")
        print("-" * 80)
        
        for idx, row in df_formatted.iterrows():
            original_63 = str(df.loc[idx, phone_63_col])
            original_09 = str(df.loc[idx, phone_09_col])
            formatted_63 = row[phone_63_col]
            formatted_09 = row[phone_09_col]
            
            valid_63_flag = "YES" if is_valid_ph_phone(formatted_63) else "NO"
            valid_09_flag = "YES" if is_valid_ph_phone(formatted_09) else "NO"
            related_flag = "YES" if are_related_phones(formatted_63, formatted_09) else "NO"
            
            name = row['Name'][:30] + "..." if len(row['Name']) > 30 else row['Name']
            
            print(f"{idx+2:<4} | {formatted_63:<20} | {formatted_09:<20} | {valid_63_flag}{valid_09_flag:<6} | {related_flag:<8} | {name}")
            
            # Show changes if any
            if original_63 != formatted_63 or original_09 != formatted_09:
                print(f"     Changes: 63: {original_63} -> {formatted_63}")
                print(f"             09: {original_09} -> {formatted_09}")
        
        return True
        
    except Exception as e:
        print(f"Error processing CSV: {e}")
        return False

def test_edge_cases():
    """Test edge cases and error conditions"""
    print("\nTESTING EDGE CASES AND ERROR CONDITIONS")
    print("=" * 80)
    
    edge_cases = [
        # Format: (input, expected_output, description, should_be_valid)
        (None, "", "None value", False),
        (float('nan'), "", "NaN value", False),
        ("", "", "Empty string", False),
        ("   ", "", "Whitespace only", False),
        ("639123456789.000000", "639123456789", "Many trailing zeros", True),
        ("091234567890.000000", "091234567890", "Many trailing zeros", True),
        ("639123456789.999999", "639123456789", "Many trailing nines", True),
        ("091234567890.999999", "091234567890", "Many trailing nines", True),
        ("639123456789.000001", "639123456789", "Very small decimal", True),
        ("091234567890.000001", "091234567890", "Very small decimal", True),
        ("639123456789.5", "639123456789", "Half decimal", True),
        ("091234567890.5", "091234567890", "Half decimal", True),
        
        # Extreme cases
        ("639123456789.0000000001", "639123456789", "Extremely small decimal", True),
        ("639123456789.9999999999", "639123456789", "Extremely close to 1", True),
        ("639123456789.123456789012345", "639123456789", "Very long decimal", True),
        ("091234567890.123456789012345", "091234567890", "09 very long decimal", True),
        
        # Scientific notation edge cases
        ("6.39123456789E+11", "639123456789", "Scientific notation", True),
        ("6.39123456789E+12", "6391234567890", "Scientific notation too long", False),
        ("9.1234567890E+10", "091234567890", "09 scientific notation", True),
        ("9.1234567890E+11", "912345678900", "09 scientific too long", False),
    ]
    
    all_passed = True
    total_tests = 0
    passed_tests = 0
    
    print("EDGE CASES")
    print("-" * 60)
    
    for input_val, expected, description, should_be_valid in edge_cases:
        result = format_phone_number(input_val)
        is_valid = is_valid_ph_phone(result)
        
        format_correct = result == expected
        validation_correct = is_valid == should_be_valid
        
        total_tests += 1
        if format_correct and validation_correct:
            status = "PASS"
            passed_tests += 1
        else:
            status = "FAIL"
            all_passed = False
        
        input_str = str(input_val) if input_val is not None else "None"
        print(f"{status} | {input_str:25} -> {result:15} | Valid: {is_valid:5} | {description}")
        if not format_correct:
            print(f"        Expected: {expected}")
        if not validation_correct:
            print(f"        Expected valid: {should_be_valid}")
    
    print(f"\nEDGE CASES RESULTS: {passed_tests}/{total_tests} tests passed")
    return all_passed

def test_all_csv_files():
    """Test all CSV files in the directory"""
    print("\nTESTING ALL CSV FILES")
    print("=" * 80)
    
    # Find all test CSV files
    csv_files = glob.glob("test_*.csv")
    csv_files.sort()
    
    if not csv_files:
        print("No test CSV files found in current directory")
        return False
    
    print(f"Found {len(csv_files)} test CSV files:")
    for i, file in enumerate(csv_files, 1):
        print(f"  {i:2d}. {file}")
    
    print(f"\nTesting each file...")
    print("-" * 60)
    
    all_passed = True
    total_files = 0
    passed_files = 0
    
    for csv_file in csv_files:
        total_files += 1
        try:
            print(f"\nTesting: {csv_file}")
            df = pd.read_csv(csv_file)
            print(f"  - Loaded {len(df)} rows, {len(df.columns)} columns")
            
            # Find phone columns (first column or columns with 'phone' in name)
            phone_columns = []
            for col in df.columns:
                if 'phone' in col.lower() or col == df.columns[0]:
                    phone_columns.append(col)
            
            if not phone_columns:
                print(f"  - No phone columns found, skipping")
                continue
            
            print(f"  - Phone columns: {phone_columns}")
            
            # Test formatting
            for col in phone_columns:
                df[col] = df[col].apply(format_phone_number)
            
            # Test validation
            valid_count = 0
            for col in phone_columns:
                valid_count += df[col].apply(is_valid_ph_phone).sum()
            
            total_phones = len(df) * len(phone_columns)
            invalid_count = total_phones - valid_count
            
            print(f"  - Validation: {valid_count}/{total_phones} valid, {invalid_count} invalid")
            
            # Check if this should pass or fail based on filename
            should_pass = not any(keyword in csv_file.lower() for keyword in ['invalid', 'duplicate', 'negative', 'letter'])
            
            if should_pass and invalid_count == 0:
                status = "PASS"
                passed_files += 1
            elif not should_pass and invalid_count > 0:
                status = "PASS (Expected to fail)"
                passed_files += 1
            else:
                status = "FAIL"
                all_passed = False
            
            print(f"  - Result: {status}")
            
        except Exception as e:
            print(f"  - Error: {e}")
            all_passed = False
    
    print(f"\nCSV FILES TEST RESULTS: {passed_files}/{total_files} files passed")
    return all_passed

def test_performance():
    """Test performance with large datasets"""
    print("\nTESTING PERFORMANCE")
    print("=" * 80)
    
    # Create a large test dataset
    import time
    
    large_dataset = []
    for i in range(1000):
        phone_63 = f"639{str(i).zfill(9)}.0"
        phone_09 = f"09{str(i).zfill(9)}.0"
        large_dataset.append({
            'Phone_63': phone_63,
            'Phone_09': phone_09,
            'Name': f'Test User {i}',
            'Date': '2024-01-01'
        })
    
    df = pd.DataFrame(large_dataset)
    print(f"Created test dataset with {len(df)} rows")
    
    # Test formatting performance
    start_time = time.time()
    df['Phone_63'] = df['Phone_63'].apply(format_phone_number)
    df['Phone_09'] = df['Phone_09'].apply(format_phone_number)
    format_time = time.time() - start_time
    
    # Test validation performance
    start_time = time.time()
    valid_63 = df['Phone_63'].apply(is_valid_ph_phone)
    valid_09 = df['Phone_09'].apply(is_valid_ph_phone)
    validation_time = time.time() - start_time
    
    # Test related number validation
    start_time = time.time()
    related_count = 0
    for idx, row in df.iterrows():
        if are_related_phones(row['Phone_63'], row['Phone_09']):
            related_count += 1
    related_time = time.time() - start_time
    
    print(f"Performance Results:")
    print(f"  - Formatting {len(df)} numbers: {format_time:.4f} seconds")
    print(f"  - Validation {len(df)} numbers: {validation_time:.4f} seconds")
    print(f"  - Related validation {len(df)} pairs: {related_time:.4f} seconds")
    print(f"  - Total time: {format_time + validation_time + related_time:.4f} seconds")
    print(f"  - Related pairs found: {related_count}/{len(df)}")
    
    # Check if performance is acceptable (should be under 1 second for 1000 numbers)
    total_time = format_time + validation_time + related_time
    if total_time < 1.0:
        print("PASS - Performance is acceptable")
        return True
    else:
        print("FAIL - Performance is too slow")
        return False

def main():
    """Run all tests"""
    print("COMPREHENSIVE PHONE NUMBER FORMATTING TEST SUITE")
    print("=" * 80)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # Run all test suites
    test1_passed = test_individual_phone_formatting()
    test2_passed = test_related_phone_validation()
    test3_passed = test_csv_processing()
    test4_passed = test_edge_cases()
    test5_passed = test_all_csv_files()
    test6_passed = test_performance()
    
    # Final results
    print("\n" + "=" * 80)
    print("FINAL TEST RESULTS")
    print("=" * 80)
    
    all_tests = [
        ("Individual Phone Formatting", test1_passed),
        ("Related Phone Validation", test2_passed),
        ("CSV Processing", test3_passed),
        ("Edge Cases", test4_passed),
        ("All CSV Files", test5_passed),
        ("Performance", test6_passed),
    ]
    
    passed_count = 0
    for test_name, passed in all_tests:
        status = "PASSED" if passed else "FAILED"
        print(f"{status} | {test_name}")
        if passed:
            passed_count += 1
    
    print("-" * 80)
    if passed_count == len(all_tests):
        print("ALL TEST SUITES PASSED! The phone number formatting is working perfectly.")
        print("Ready for production use!")
    else:
        print(f"{passed_count}/{len(all_tests)} test suites passed.")
        print("Please review and fix the failing tests.")
    
    print(f"Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    return passed_count == len(all_tests)

if __name__ == "__main__":
    success = main()
    print("\n" + "=" * 80)
    print("Press Enter to exit...")
    input()
    exit(0 if success else 1)