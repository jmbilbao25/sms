# TechOps Text Blast List Formatter v0.1

A professional desktop application for formatting, validating, and preparing SMS contact lists from CSV files. Built with Python and Tkinter for a clean, modern user interface.

## 🚀 Features

### Core Functionality
- **CSV File Processing**: Drag & drop or browse to select CSV files
- **Phone Number Formatting**: Automatically formats phone numbers to digits only
- **Special Character Handling**: Replaces ñ/Ñ with n/N for compatibility
- **Duplicate Detection**: Identifies and prevents duplicate phone numbers
- **Empty Field Validation**: Ensures no empty phone numbers in the dataset
- **Preview Mode**: View before/after changes before processing
- **Custom Output**: Set custom filename and save location

### User Interface
- **Modern Design**: Clean, professional interface with card-based layout
- **Banner Support**: Custom banner image display (banner.png)
- **Responsive Layout**: Compact, lightweight window (500x750px)
- **Drag & Drop**: Intuitive file selection with visual feedback
- **Real-time Logging**: Live processing updates and validation results
- **Settings Persistence**: Remembers your preferred save location and filename

### Technical Features
- **Error Handling**: Comprehensive validation with detailed error messages
- **File Safety**: Automatic backup with numbered suffixes for existing files
- **Cross-platform**: Works on Windows, macOS, and Linux
- **Dependencies**: Minimal dependencies (pandas, PIL, tkinterdnd2)

## 📋 Requirements

### System Requirements
- **Operating System**: Windows 10/11, macOS 10.14+, or Linux
- **Python**: 3.8 or higher
- **Memory**: 100MB RAM minimum
- **Storage**: 50MB for application and dependencies

### Python Dependencies
```
pandas>=1.3.0
Pillow>=8.0.0
tkinterdnd2>=0.3.0
```

## 🛠️ Installation

### Option 1: Python Script
1. Install dependencies:
   ```bash
   pip install pandas pillow tkinterdnd2
   ```
2. Run the application:
   ```bash
   python SMS.py
   ```

### Option 2: Executable (Windows)
1. Download `TechOpsFormatter.exe` from the dist folder
2. Double-click to run (no installation required)
3. Place `banner.png` in the same folder for custom branding

## 📖 Usage Guide

### Getting Started
1. **Launch the Application**: Run `python SMS.py` or double-click the executable
2. **Set Save Location**: Click "Browse" to choose where processed files will be saved
3. **Set Output Filename**: Enter your desired filename (without .csv extension)
4. **Load CSV File**: Drag & drop a CSV file or click to browse

### File Format Requirements
Your CSV file should have:
- **First Column**: Phone numbers (any format)
- **Additional Columns**: Names, addresses, or other contact information
- **Headers**: Column names in the first row
- **Encoding**: UTF-8 recommended

### Example CSV Format
```csv
Phone,Name,Company
+1-555-123-4567,John Doe,Acme Corp
(555) 987-6543,Jane Smith,Tech Inc
555.123.4567,Bob Johnson,Startup LLC
```

### Processing Workflow
1. **File Validation**: Checks for empty phone numbers and duplicates
2. **Preview Changes**: Review what will be modified
3. **Format Processing**: Applies phone number formatting and character replacement
4. **Export**: Saves the formatted file with your custom name

## ⚠️ Edge Cases & Limitations

### Supported Phone Number Formats
- **US Numbers**: (555) 123-4567, 555-123-4567, 555.123.4567
- **International**: +1-555-123-4567, +44 20 7946 0958
- **Mixed Formats**: Any combination of parentheses, dashes, dots, spaces
- **Extension Handling**: Extensions are removed (e.g., "555-123-4567 ext 123" → "5551234567")

### Validation Rules
- **Empty Phone Numbers**: ❌ Not allowed - must be fixed before processing
- **Duplicate Numbers**: ❌ Not allowed - must be removed before processing
- **Empty Columns**: ⚠️ Allowed but logged as warnings
- **Special Characters**: ✅ Automatically converted (ñ→n, Ñ→N)

### File Size Limits
- **Maximum Rows**: 100,000 contacts (recommended)
- **Maximum Columns**: 50 columns
- **File Size**: Up to 100MB CSV files
- **Memory Usage**: ~2MB per 1,000 contacts

### Error Handling
- **Invalid CSV**: Clear error messages with row numbers
- **Missing Files**: Graceful fallback to text title if banner.png missing
- **Permission Issues**: Detailed error messages for file access problems
- **Memory Issues**: Automatic cleanup and garbage collection

## 🔧 Configuration

### Settings File
The application saves settings in:
- **Windows**: `%USERPROFILE%\.sms_csv_formatter_config.json`
- **macOS/Linux**: `~/.sms_csv_formatter_config.json`

### Customizable Settings
```json
{
  "output_dir": "C:/Users/Username/Desktop",
  "filename_prefix": "sms_contacts"
}
```

### Banner Customization
- **File**: `banner.png` in the same directory as the executable
- **Format**: PNG, JPG, or ICO
- **Size**: Automatically resized to fit (max 500px width, 120px height)
- **Fallback**: Text title if image not found

## 🐛 Troubleshooting

### Common Issues

#### "PIL not found" Error
```bash
pip install Pillow
```

#### "tkinterdnd2 not found" Error
```bash
pip install tkinterdnd2
```

#### Application Won't Start
- Check Python version: `python --version`
- Verify all dependencies: `pip list`
- Try running from command line for error messages

#### Drag & Drop Not Working
- Ensure CSV file has .csv extension
- Try clicking "browse files" instead
- Check file permissions

#### Banner Image Not Showing
- Verify `banner.png` exists in the same folder
- Check image format (PNG recommended)
- Ensure PIL/Pillow is installed

### Performance Optimization
- **Large Files**: Process in batches of 10,000 contacts
- **Memory Usage**: Close other applications for large files
- **Processing Time**: Allow 1-2 minutes per 10,000 contacts

## 📊 Output Format

### Processed CSV Structure
- **Phone Numbers**: Digits only (e.g., "5551234567")
- **Special Characters**: Converted (ñ→n, Ñ→N)
- **Headers**: Preserved exactly as input
- **Empty Columns**: Kept but logged as warnings
- **Encoding**: UTF-8 with BOM for Excel compatibility

### File Naming
- **Default**: `sms_contacts.csv`
- **Custom**: User-specified name + `.csv`
- **Duplicates**: Automatic numbering (`filename_1.csv`, `filename_2.csv`)

## 🔒 Security & Privacy

### Data Handling
- **Local Processing**: All data processed locally, never sent to external servers
- **Temporary Files**: No temporary files created during processing
- **Settings**: Stored locally in user profile directory
- **Logs**: Displayed in application only, not saved to disk

### File Permissions
- **Read Access**: Required for input CSV files
- **Write Access**: Required for output directory
- **No Network**: Application does not require internet connection

## 🚀 Advanced Usage

### Batch Processing
For multiple files, process them individually:
1. Load first CSV file
2. Process and save
3. Load next CSV file
4. Repeat process

### Integration with SMS Platforms
The formatted output is compatible with:
- **Twilio**: Direct CSV import
- **SendGrid**: Contact list upload
- **AWS SNS**: Bulk SMS sending
- **Custom APIs**: Standard CSV format

### Custom Validation
Extend the application by modifying validation rules in the `validate_file()` method.

## 📝 Changelog

### Version 0.1 (Current)
- ✅ Initial release
- ✅ CSV file processing
- ✅ Phone number formatting
- ✅ Duplicate detection
- ✅ Preview functionality
- ✅ Custom banner support
- ✅ Settings persistence
- ✅ Executable build support

## 🤝 Support

### Getting Help
- **Documentation**: This README file
- **Error Messages**: Check the Processing Log for detailed information
- **File Issues**: Verify CSV format and encoding

### Reporting Issues
When reporting issues, include:
- Operating system and version
- Python version (if using script)
- Error messages from Processing Log
- Sample CSV file (if possible)
- Steps to reproduce the issue

## 📄 License

This application is provided as-is for internal use. All rights reserved.

---

**TechOps Text Blast List Formatter v0.1**  
*Professional CSV formatting for SMS campaigns*
