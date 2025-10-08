#!/usr/bin/env python3
"""
Debug script to understand phone number formatting issues
"""

import re

def format_phone_number_debug(phone):
    """Debug version of phone number formatting"""
    print(f"\n🔍 DEBUGGING: {phone}")
    
    if phone is None:
        print("  → None value, returning empty string")
        return ""
    
    # Convert to string and remove all non-digit characters
    phone_str = str(phone)
    print(f"  → Original string: '{phone_str}'")
    
    # Check if original string starts with 0 (for 09 format preservation)
    starts_with_zero = phone_str.startswith('0')
    print(f"  → Starts with zero: {starts_with_zero}")
    
    # Handle decimal numbers more carefully
    if '.' in phone_str:
        print(f"  → Contains decimal point")
        try:
            # Try to parse as float to check if it's a whole number
            float_val = float(phone_str)
            print(f"  → Float value: {float_val}")
            
            if float_val == int(float_val):  # It's a whole number
                print(f"  → Is whole number, removing decimal part")
                # For whole numbers, just remove the decimal part without converting to int
                phone_str = phone_str.split('.')[0]
                print(f"  → After removing decimal: '{phone_str}'")
            else:
                print(f"  → Is decimal number, truncating to int")
                # It's a decimal number, truncate to integer part
                phone_str = str(int(float_val))
                print(f"  → After truncating: '{phone_str}'")
        except ValueError:
            print(f"  → ValueError, splitting on decimal")
            # If it's not a valid number, just remove the decimal part
            phone_str = phone_str.split('.')[0]
            print(f"  → After splitting: '{phone_str}'")
    else:
        print(f"  → No decimal point")
    
    # Extract digits while preserving the original structure for 09 numbers
    digits = re.sub(r'\D', '', phone_str)
    print(f"  → After removing non-digits: '{digits}'")
    
    # Special handling for 09 format numbers that might have lost their leading zero
    if starts_with_zero and len(digits) == 10:
        print(f"  → Adding leading zero back")
        digits = '0' + digits
        print(f"  → Final result: '{digits}'")
    else:
        print(f"  → No leading zero needed (starts_with_zero: {starts_with_zero}, len: {len(digits)})")
        print(f"  → Final result: '{digits}'")
    
    return digits

# Test cases that are failing
test_cases = [
    "099999999999.0",
    "091234567890.0", 
    "091234567890.5",
    "091234567890.25",
    "091234567890.99",
    "091234567890.01",
    "091234567890.000",
    "091234567890.999",
    "091234567890.000000",
    "091234567890.999999",
    "091234567890.000001",
]

print("🐛 DEBUGGING PHONE NUMBER FORMATTING")
print("=" * 60)

for test_case in test_cases:
    result = format_phone_number_debug(test_case)
    expected = test_case.replace('.0', '').replace('.5', '').replace('.25', '').replace('.99', '').replace('.01', '').replace('.000', '').replace('.999', '').replace('.000000', '').replace('.999999', '').replace('.000001', '')
    print(f"  Expected: {expected}")
    print(f"  Match: {'✅' if result == expected else '❌'}")
    print("-" * 60)
