# 📋 SMS CSV Formatter Test Files

This directory contains comprehensive test CSV files for testing the SMS CSV Formatter application. Each file tests different scenarios and edge cases.

## 🧪 Test Files Overview

### Basic Format Tests
- **`test_01_basic_63_format.csv`** - Basic 63 format phone numbers (12 digits starting with 63)
- **`test_02_basic_09_format.csv`** - Basic 09 format phone numbers (11 digits starting with 09)
- **`test_03_mixed_formats.csv`** - Mixed 63 and 09 formats in the same file

### Decimal Format Tests
- **`test_04_decimal_formats.csv`** - Phone numbers with decimal formats (.0, .5, .25, .99)
- **`test_05_related_63_09_columns.csv`** - Separate columns for 63 and 09 formats with related numbers
- **`test_07_edge_cases.csv`** - Edge cases with many trailing zeros/nines, very small decimals

### Google Sheets Integration Tests
- **`test_06_google_sheets_formulas.csv`** - Simulates Google Sheets formulas that might evaluate to empty

### Validation Tests
- **`test_08_invalid_formats.csv`** - Invalid phone number formats (too short, too long, wrong prefixes, letters)
- **`test_09_duplicates.csv`** - Duplicate phone numbers (should fail validation)

### Special Cases
- **`test_10_special_characters.csv`** - Names with special characters (accented letters, etc.)
- **`test_11_large_dataset.csv`** - Large dataset with 20 phone numbers
- **`test_12_comprehensive_mixed.csv`** - Comprehensive test with all scenarios combined

### Advanced Format Tests
- **`test_13_phone_with_spaces.csv`** - Phone numbers with spaces, dashes, dots, parentheses
- **`test_14_very_long_decimals.csv`** - Very long decimal numbers (many decimal places)
- **`test_15_scientific_notation.csv`** - Phone numbers in scientific notation format
- **`test_16_negative_numbers.csv`** - Negative phone numbers (should fail validation)
- **`test_17_leading_zeros_63.csv`** - 63 format numbers with leading zeros
- **`test_18_phone_with_letters.csv`** - Phone numbers containing letters (should fail validation)

### Unicode and Special Characters
- **`test_19_unicode_characters.csv`** - Names with extensive Unicode characters
- **`test_20_mixed_separators.csv`** - Phone numbers with mixed separators (dashes, dots, spaces)
- **`test_21_phone_with_plus.csv`** - Phone numbers with plus signs
- **`test_22_phone_with_parentheses.csv`** - Phone numbers with parentheses formatting
- **`test_23_very_small_numbers.csv`** - Very small decimal numbers
- **`test_24_phone_with_commas.csv`** - Phone numbers with comma separators
- **`test_25_phone_with_special_chars.csv`** - Phone numbers with special character separators
- **`test_26_phone_with_quotes.csv`** - Phone numbers with quote marks
- **`test_27_phone_with_brackets.csv`** - Phone numbers with square brackets
- **`test_28_phone_with_underscores.csv`** - Phone numbers with underscore separators
- **`test_29_phone_with_slashes.csv`** - Phone numbers with slash separators
- **`test_30_comprehensive_edge_cases.csv`** - Comprehensive edge cases with all decimal variations

## 🎯 How to Use These Test Files

1. **Open the SMS CSV Formatter application**
2. **Drag and drop any test file** onto the application
3. **Review the validation results** in the processing log
4. **Use the Preview button** to see before/after changes
5. **Format the file** if validation passes

## 📊 Expected Results

### ✅ Should Pass Validation
- `test_01_basic_63_format.csv` - All 63 format numbers
- `test_02_basic_09_format.csv` - All 09 format numbers  
- `test_03_mixed_formats.csv` - Mixed valid formats
- `test_04_decimal_formats.csv` - Decimal formats (should be cleaned)
- `test_05_related_63_09_columns.csv` - Related number pairs
- `test_06_google_sheets_formulas.csv` - Should handle formulas correctly
- `test_07_edge_cases.csv` - Edge cases should be handled
- `test_10_special_characters.csv` - Special characters should be replaced
- `test_11_large_dataset.csv` - Large dataset should process
- `test_12_comprehensive_mixed.csv` - Comprehensive test
- `test_13_phone_with_spaces.csv` - Should clean separators
- `test_14_very_long_decimals.csv` - Should truncate long decimals
- `test_15_scientific_notation.csv` - Should handle scientific notation
- `test_17_leading_zeros_63.csv` - Should handle leading zeros
- `test_19_unicode_characters.csv` - Should replace Unicode characters
- `test_20_mixed_separators.csv` - Should clean mixed separators
- `test_21_phone_with_plus.csv` - Should remove plus signs
- `test_22_phone_with_parentheses.csv` - Should clean parentheses
- `test_23_very_small_numbers.csv` - Should truncate small decimals
- `test_24_phone_with_commas.csv` - Should remove commas
- `test_25_phone_with_special_chars.csv` - Should clean special chars
- `test_26_phone_with_quotes.csv` - Should remove quotes
- `test_27_phone_with_brackets.csv` - Should clean brackets
- `test_28_phone_with_underscores.csv` - Should remove underscores
- `test_29_phone_with_slashes.csv` - Should remove slashes
- `test_30_comprehensive_edge_cases.csv` - Should handle all edge cases

### ❌ Should Fail Validation
- `test_08_invalid_formats.csv` - Invalid formats should be rejected
- `test_09_duplicates.csv` - Duplicates should be detected
- `test_16_negative_numbers.csv` - Negative numbers should be rejected
- `test_18_phone_with_letters.csv` - Letters in phone numbers should be rejected

## 🔍 What to Look For

### Phone Number Formatting
- **63 format**: `639123456789.0` → `639123456789`
- **09 format**: `091234567890.0` → `091234567890`
- **Decimals**: `639123456789.5` → `639123456789` (truncated)
- **Related numbers**: 63 and 09 formats should be recognized as related

### Special Character Handling
- **Accented letters**: `José` → `Jose`
- **Special symbols**: `Müller` → `Muller`
- **Non-ASCII characters**: Should be converted to ASCII equivalents

### Validation Features
- **Empty detection**: `0`, `0.0` should be detected as empty
- **Format validation**: Only 11-digit (09) and 12-digit (63) formats accepted
- **Duplicate detection**: Same phone numbers should be flagged
- **Column type detection**: Numeric vs text columns should be identified

## 🚀 Testing Workflow

1. **Start with basic tests** (`test_01`, `test_02`, `test_03`)
2. **Test decimal handling** (`test_04`, `test_05`, `test_07`)
3. **Test edge cases** (`test_06`, `test_08`, `test_09`)
4. **Test special features** (`test_10`, `test_11`, `test_12`)

## 📝 Notes

- All test files use realistic Philippine phone number formats
- Names include various special characters to test character replacement
- Dates are included to test multi-column processing
- Some files intentionally contain invalid data to test validation
- Related number tests verify that 63 and 09 formats are handled correctly

## 🐛 Troubleshooting

If a test file doesn't work as expected:
1. Check the processing log for specific error messages
2. Verify the phone number formats in the file
3. Ensure the file is properly formatted as CSV
4. Check for any hidden characters or encoding issues

---

**Happy Testing! 🎉**
