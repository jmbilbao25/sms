import tkinter as tk
from tkinter import ttk, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
import pandas as pd
import re
from datetime import datetime
import os
import json
import sys
import time
import random

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    import pkg_resources
    RESOURCE_AVAILABLE = True
except ImportError:
    RESOURCE_AVAILABLE = False


class CSVFormatterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TechOps Text Blast List Formater v0.1")
        self.root.geometry("500x850")
        self.root.minsize(500, 850)  # Set minimum window size
        self.root.configure(bg="#f5f7fa")
        
        # Config file path
        self.config_file = os.path.join(os.path.expanduser("~"), ".sms_csv_formatter_config.json")
        
        # Load saved settings
        self.load_settings()
        
        # Default output directory and filename prefix if not loaded
        if not hasattr(self, 'output_dir'):
            self.output_dir = os.path.join(os.path.expanduser("~"), "Desktop")
        if not hasattr(self, 'filename_prefix'):
            self.filename_prefix = "sms_contacts"
        
        # Bind window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Main container with padding
        main_container = tk.Frame(root, bg="#f5f7fa")
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header with banner image
        header_frame = tk.Frame(main_container, bg="#f5f7fa")
        header_frame.pack(pady=(0, 20))
        
        # Load and display banner image
        banner_loaded = False
        if PIL_AVAILABLE:
            try:
                # Try to load banner from multiple sources
                banner_image = None
                
                # Method 1: Try embedded resource (for PyInstaller)
                if RESOURCE_AVAILABLE:
                    try:
                        banner_path = pkg_resources.resource_filename(__name__, 'banner.png')
                        if os.path.exists(banner_path):
                            banner_image = Image.open(banner_path)
                    except:
                        pass
                
                # Method 1b: Try PyInstaller temp directory
                if banner_image is None:
                    try:
                        # PyInstaller creates a temp directory and stores path in _MEIPASS
                        base_path = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
                        banner_path = os.path.join(base_path, 'banner.png')
                        if os.path.exists(banner_path):
                            banner_image = Image.open(banner_path)
                    except:
                        pass
                
                # Method 2: Try local file (for development)
                if banner_image is None and os.path.exists("banner.png"):
                    banner_image = Image.open("banner.png")
                
                # Method 3: Try in same directory as executable
                if banner_image is None:
                    exe_dir = os.path.dirname(os.path.abspath(__file__))
                    banner_path = os.path.join(exe_dir, "banner.png")
                    if os.path.exists(banner_path):
                        banner_image = Image.open(banner_path)
                
                if banner_image is not None:
                    # Get the original dimensions
                    original_width, original_height = banner_image.size
                    
                    # Calculate the maximum width (window width minus padding)
                    max_width = 600  # Adjust this to fit your window better
                    max_height = 120  # Maximum height for the banner
                    
                    # Calculate scaling factor to fit within bounds while maintaining aspect ratio
                    width_scale = max_width / original_width
                    height_scale = max_height / original_height
                    scale = min(width_scale, height_scale)  # Use the smaller scale to fit both dimensions
                    
                    # Calculate new dimensions
                    new_width = int(original_width * scale)
                    new_height = int(original_height * scale)
                    
                    # Resize the image
                    banner_image = banner_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    self.banner_photo = ImageTk.PhotoImage(banner_image)
                    
                    header = tk.Label(
                        header_frame, 
                        image=self.banner_photo,
                        bg="#f5f7fa"
                    )
                    header.pack()
                    banner_loaded = True
                    
            except Exception as e:
                # Fallback to text if image fails to load
                pass
        
        if not banner_loaded:
            # Use text title if banner couldn't be loaded
            header = tk.Label(
                header_frame, 
                text="TechOps Text Blast List Formatter", 
                font=("Segoe UI", 22, "bold"),
                bg="#f5f7fa",
                fg="#2c3e50"
            )
            header.pack()
        
        subtitle = tk.Label(
            header_frame,
            text="Format, validate, and prepare .csv files for Text Blast (Smart Messaging Suite)",
            font=("Segoe UI", 10),
            bg="#f5f7fa",
            fg="#7f8c8d"
        )
        subtitle.pack()
        
        # Output directory card
        dir_card = tk.Frame(main_container, bg="white", relief=tk.FLAT)
        dir_card.pack(fill=tk.X, pady=(0, 15))
        
        dir_inner = tk.Frame(dir_card, bg="white")
        dir_inner.pack(fill=tk.X, padx=15, pady=12)
        
        tk.Label(
            dir_inner,
            text="Save Location:",
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg="#2c3e50"
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.dir_label = tk.Label(
            dir_inner,
            text=self.output_dir,
            font=("Segoe UI", 9),
            bg="#ecf0f1",
            fg="#34495e",
            relief=tk.FLAT,
            anchor="w",
            padx=10,
            pady=6,
            borderwidth=1
        )
        self.dir_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        self.browse_dir_btn = tk.Button(
            dir_inner,
            text="Browse",
            command=self.select_output_directory,
            font=("Segoe UI", 9, "bold"),
            bg="#3498db",
            fg="white",
            relief=tk.FLAT,
            padx=15,
            pady=6,
            cursor="hand2",
            activebackground="#2980b9",
            activeforeground="white"
        )
        self.browse_dir_btn.pack(side=tk.LEFT)
        
        # Filename prefix card
        filename_card = tk.Frame(main_container, bg="white", relief=tk.FLAT)
        filename_card.pack(fill=tk.X, pady=(0, 15))
        
        filename_inner = tk.Frame(filename_card, bg="white")
        filename_inner.pack(fill=tk.X, padx=15, pady=12)
        
        tk.Label(
            filename_inner,
            text="Output Filename:",
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg="#2c3e50"
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.filename_entry = tk.Entry(
            filename_inner,
            font=("Segoe UI", 10),
            bg="#ecf0f1",
            fg="#34495e",
            relief=tk.FLAT,
            borderwidth=1
        )
        self.filename_entry.insert(0, self.filename_prefix)
        self.filename_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10), ipady=4)
        
        tk.Label(
            filename_inner,
            text=".csv",
            font=("Segoe UI", 9),
            bg="white",
            fg="#95a5a6"
        ).pack(side=tk.LEFT)
        
        # Info label for filename
        filename_info = tk.Label(
            filename_card,
            text="Tip: Enter your desired filename (no need for extension)",
            font=("Segoe UI", 8),
            bg="white",
            fg="#7f8c8d",
            anchor="w"
        )
        filename_info.pack(fill=tk.X, padx=15, pady=(0, 8))
        
        # Drop zone card
        drop_card = tk.Frame(main_container, bg="white", relief=tk.FLAT)
        drop_card.pack(fill=tk.X, pady=(0, 15))
        
        self.drop_frame = tk.Frame(
            drop_card, 
            bg="#f8f9fa",
            highlightbackground="#3498db",
            highlightcolor="#3498db",
            highlightthickness=2,
            height=120
        )
        self.drop_frame.pack(fill=tk.X, padx=15, pady=15)
        
        drop_content = tk.Frame(self.drop_frame, bg="#f8f9fa")
        drop_content.place(relx=0.5, rely=0.5, anchor="center")
        
        self.drop_icon = tk.Label(
            drop_content,
            text="📄",
            font=("Segoe UI", 32),
            bg="#f8f9fa",
            fg="#3498db"
        )
        self.drop_icon.pack()
        
        self.drop_label = tk.Label(
            drop_content,
            text="Drag & Drop CSV File Here",
            font=("Segoe UI", 12, "bold"),
            bg="#f8f9fa",
            fg="#2c3e50"
        )
        self.drop_label.pack(pady=(10, 5))
        
        self.drop_sublabel = tk.Label(
            drop_content,
            text="or click to browse files",
            font=("Segoe UI", 9),
            bg="#f8f9fa",
            fg="#95a5a6"
        )
        self.drop_sublabel.pack()
        
        # Enable drag and drop
        self.drop_frame.drop_target_register(DND_FILES)
        self.drop_frame.dnd_bind('<<Drop>>', self.drop_file)
        self.drop_frame.bind('<Button-1>', self.browse_file)
        self.drop_label.bind('<Button-1>', self.browse_file)
        self.drop_sublabel.bind('<Button-1>', self.browse_file)
        self.drop_icon.bind('<Button-1>', self.browse_file)
        
        # Status area card
        status_card = tk.Frame(main_container, bg="white", relief=tk.FLAT)
        status_card.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        status_header = tk.Frame(status_card, bg="white")
        status_header.pack(fill=tk.X, padx=15, pady=(12, 8))
        
        tk.Label(
            status_header,
            text="Processing Log",
            font=("Segoe UI", 11, "bold"),
            bg="white",
            fg="#2c3e50"
        ).pack(side=tk.LEFT)
        
        # Preview button positioned on the right side of the Processing Log header
        self.preview_btn = tk.Button(
            status_header,
            text="Preview",
            command=self.show_preview,
            font=("Segoe UI", 8),
            bg="#95a5a6",
            fg="white",
            relief=tk.FLAT,
            padx=8,
            pady=4,
            cursor="hand2",
            activebackground="#7f8c8d",
            activeforeground="white",
            state=tk.DISABLED
        )
        self.preview_btn.pack(side=tk.RIGHT)
        
        self.status_text = tk.Text(
            status_card, 
            height=12, 
            font=("Consolas", 9),
            bg="#f8f9fa",
            fg="#2c3e50",
            relief=tk.FLAT,
            padx=10,
            pady=10,
            wrap=tk.WORD
        )
        self.status_text.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        # Scrollbar for status text
        scrollbar = tk.Scrollbar(self.status_text)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.status_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.status_text.yview)
        
        # Button frame
        btn_frame = tk.Frame(main_container, bg="#f5f7fa")
        btn_frame.pack(fill=tk.X, pady=(0, 5))
        
        # Create a frame for the main format button (centered)
        format_container = tk.Frame(btn_frame, bg="#f5f7fa")
        format_container.pack(fill=tk.X)
        
        # Main format button (centered)
        self.format_btn = tk.Button(
            format_container,
            text="Format File",
            command=self.format_file,
            font=("Segoe UI", 11, "bold"),
            bg="#27ae60",
            fg="white",
            relief=tk.FLAT,
            padx=30,
            pady=10,
            cursor="hand2",
            activebackground="#229954",
            activeforeground="white",
            state=tk.DISABLED
        )
        self.format_btn.pack(fill=tk.X, padx=20)
        
        # Store file path for processing
        self.current_file_path = None
        self.validation_passed = False
        self.preview_df = None
        
        # Hover effects
        self.setup_hover_effects()
        
    def setup_hover_effects(self):
        """Add hover effects to buttons"""
        def on_enter(e, btn, color):
            if btn['state'] != tk.DISABLED:
                btn['background'] = color
            
        def on_leave(e, btn, color):
            if btn['state'] != tk.DISABLED:
                btn['background'] = color
        
        self.browse_dir_btn.bind("<Enter>", lambda e: on_enter(e, self.browse_dir_btn, "#2980b9"))
        self.browse_dir_btn.bind("<Leave>", lambda e: on_leave(e, self.browse_dir_btn, "#3498db"))
        
        self.preview_btn.bind("<Enter>", lambda e: on_enter(e, self.preview_btn, "#7f8c8d"))
        self.preview_btn.bind("<Leave>", lambda e: on_leave(e, self.preview_btn, "#95a5a6"))
        
        self.format_btn.bind("<Enter>", lambda e: on_enter(e, self.format_btn, "#229954"))
        self.format_btn.bind("<Leave>", lambda e: on_leave(e, self.format_btn, "#27ae60"))
    
    def load_settings(self):
        """Load saved settings from config file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    self.output_dir = config.get('output_dir', os.path.join(os.path.expanduser("~"), "Desktop"))
                    self.filename_prefix = config.get('filename_prefix', 'sms_contacts')
                    
                    # Verify directory still exists
                    if not os.path.exists(self.output_dir):
                        self.output_dir = os.path.join(os.path.expanduser("~"), "Desktop")
        except Exception as e:
            # If config file is corrupted, use defaults
            self.output_dir = os.path.join(os.path.expanduser("~"), "Desktop")
            self.filename_prefix = 'sms_contacts'
    
    def save_settings(self):
        """Save current settings to config file"""
        try:
            config = {
                'output_dir': self.output_dir,
                'filename_prefix': self.filename_entry.get().strip() or 'sms_contacts'
            }
            with open(self.config_file, 'w') as f:
                json.dump(config, f)
        except Exception as e:
            # Silently fail if we can't save settings
            pass
    
    def on_closing(self):
        """Handle window closing event"""
        self.save_settings()
        self.root.destroy()
        
    def log(self, message):
        """Add message to status log"""
        self.status_text.insert(tk.END, f"{message}\n")
        self.status_text.see(tk.END)
        self.root.update()
        
    def clear_log(self):
        """Clear the status log"""
        self.status_text.delete(1.0, tk.END)
    
    def select_output_directory(self):
        """Open directory browser to select output location"""
        from tkinter import filedialog
        directory = filedialog.askdirectory(
            title="Select Output Directory",
            initialdir=self.output_dir
        )
        if directory:
            self.output_dir = directory
            self.dir_label.config(text=directory)
            self.log(f"✓ Output directory changed to: {directory}\n")
            self.save_settings()  # Save immediately when changed
        
    def browse_file(self, event):
        """Open file browser"""
        from tkinter import filedialog
        filename = filedialog.askopenfilename(
            title="Select CSV file",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            self.process_file(filename)
    
    def drop_file(self, event):
        """Handle dropped file"""
        file_path = event.data.strip('{}')
        if file_path.lower().endswith('.csv'):
            self.validate_file(file_path)
        else:
            messagebox.showerror("Error", "Please drop a CSV file")
    
    def detect_column_type(self, series):
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

    def format_phone_number(self, phone):
        """Format phone number to digits only"""
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
    
    def replace_special_chars(self, text, track_replacements=False):
        """Replace special characters with their ASCII equivalents"""
        if pd.isna(text):
            return text, {} if track_replacements else text
        text = str(text)
        original_text = text
        
        # Comprehensive character mapping for common special characters
        char_map = {
            
            'ñ': 'n', 'Ñ': 'N',

            'à': 'a', 'á': 'a', 'â': 'a', 'ã': 'a', 'ä': 'a', 'å': 'a',
            'À': 'A', 'Á': 'A', 'Â': 'A', 'Ã': 'A', 'Ä': 'A', 'Å': 'A',
            'è': 'e', 'é': 'e', 'ê': 'e', 'ë': 'e',
            'È': 'E', 'É': 'E', 'Ê': 'E', 'Ë': 'E',
            'ì': 'i', 'í': 'i', 'î': 'i', 'ï': 'i',
            'Ì': 'I', 'Í': 'I', 'Î': 'I', 'Ï': 'I',
            'ò': 'o', 'ó': 'o', 'ô': 'o', 'õ': 'o', 'ö': 'o',
            'Ò': 'O', 'Ó': 'O', 'Ô': 'O', 'Õ': 'O', 'Ö': 'O',
            'ù': 'u', 'ú': 'u', 'û': 'u', 'ü': 'u',
            'Ù': 'U', 'Ú': 'U', 'Û': 'U', 'Ü': 'U',
            'ý': 'y', 'ÿ': 'y',
            'Ý': 'Y', 'Ÿ': 'Y',
            'ç': 'c', 'Ç': 'C',
            
        }
        
        # Track replacements if requested
        replacements_made = {}
        if track_replacements:
            for special_char, replacement in char_map.items():
                if special_char in text:
                    count = text.count(special_char)
                    replacements_made[special_char] = {'replacement': replacement, 'count': count}
                    text = text.replace(special_char, replacement)
        else:
            # Apply character mapping
            for special_char, replacement in char_map.items():
                text = text.replace(special_char, replacement)
        
        return (text, replacements_made) if track_replacements else text
    
    def validate_file(self, file_path):
        """Validate the CSV file and show what will be changed"""
        try:
            self.clear_log()
            self.current_file_path = file_path
            self.validation_passed = False
            self.format_btn.config(state=tk.DISABLED, bg="#95a5a6")
            self.preview_btn.config(state=tk.DISABLED, bg="#bdc3c7")
            
            self.log(f"{'='*60}")
            self.log(f"FILE VALIDATION")
            self.log(f"{'='*60}")
            self.log(f"File: {os.path.basename(file_path)}\n")
            
            
            # Read CSV
            df = pd.read_csv(file_path)
            original_rows = len(df)
            self.log(f"✓ Loaded {original_rows} rows")
            
            # Get headers
            headers = df.columns.tolist()
            self.log(f"✓ Found {len(headers)} columns: {', '.join(headers)}\n")
            
            # Detect likely Name and Date columns (based on headers)
            def detect_column(headers_list, phone_header, patterns):
                for h in headers_list:
                    if h == phone_header:
                        continue
                    if re.search(patterns, str(h), flags=re.IGNORECASE):
                        return h
                return None
            
            if len(df.columns) == 0:
                raise ValueError("CSV file is empty")
            
            phone_col = df.columns[0]
            name_col = detect_column(headers, phone_col, r"\b(name|full\s*name|contact|recipient)\b")
            date_col = detect_column(headers, phone_col, r"\b(date|send\s*date|scheduled?\s*date|dob|birth)\b")
            
            # A column is considered required only if it has at least one non-empty value anywhere
            def column_has_values(series):
                if series is None:
                    return False
                # Convert to string and strip whitespace
                s = series.astype(str).str.strip()
                # Remove NaN values
                s = s[~series.isna()]
                # Check for non-empty values, excluding common formula results that evaluate to empty
                # This handles Google Sheets formulas that might return empty strings, 0, or other "empty" values
                non_empty = s.ne('').any()
                if non_empty:
                    # Additional check: make sure we have actual meaningful content
                    # Exclude values that are just "0", "0.0", or other numeric representations of empty
                    meaningful_values = s[~s.isin(['0', '0.0', '0.00', 'nan', 'NaN', 'None', 'null'])]
                    return len(meaningful_values) > 0
                return False
            
            name_required = bool(name_col and name_col in df.columns and column_has_values(df[name_col]))
            date_required = bool(date_col and date_col in df.columns and column_has_values(df[date_col]))
            
            self.log(f"{'─'*60}")
            self.log(f"VALIDATION CHECKS")
            self.log(f"{'─'*60}\n")
            
            # Check for empty phone numbers BEFORE formatting
            # Handle Google Sheets formulas and decimal formats
            def is_phone_empty(phone_value):
                if pd.isna(phone_value):
                    return True
                phone_str = str(phone_value).strip()
                if phone_str == '' or phone_str in ['0', '0.0', '0.00', 'nan', 'NaN', 'None', 'null']:
                    return True
                # Check if it's a decimal number that represents a whole number
                if '.' in phone_str:
                    try:
                        float_val = float(phone_str)
                        if float_val == int(float_val):  # It's a whole number with decimal
                            # This is a valid phone number in decimal format, not empty
                            return False
                    except ValueError:
                        pass
                return False
            
            empty_phone_mask = df[phone_col].apply(is_phone_empty)
            empty_phone_rows = df[empty_phone_mask]
            if len(empty_phone_rows) > 0:
                self.log(f"VALIDATION FAILED: Found {len(empty_phone_rows)} empty phone number(s)\n")
                self.log("Rows with empty phone numbers:")
                for idx in empty_phone_rows.index:
                    row_num = idx + 2  # +2 because Excel starts at 1 and has header
                    display_name = empty_phone_rows.loc[idx, name_col] if name_col and name_col in empty_phone_rows.columns else "N/A"
                    self.log(f"  • Row {row_num}: {display_name}")
                
                self.log(f"\nPlease fix empty phone numbers before formatting.")
                messagebox.showwarning(
                    "Validation Failed",
                    f"Found {len(empty_phone_rows)} row(s) with empty phone numbers.\n\n"
                    "Please fix the file and try again."
                )
                return
            
            self.log("✓ No empty phone numbers found")
            
            # Fail if phone column contains any letters
            phone_with_letters = df[df[phone_col].astype(str).str.contains(r"[A-Za-z]", na=False)]
            if len(phone_with_letters) > 0:
                self.log(f"VALIDATION FAILED: Found {len(phone_with_letters)} phone number(s) containing letters\n")
                self.log("Rows with invalid phone numbers:")
                for idx in phone_with_letters.index:
                    row_num = idx + 2  # account for header
                    raw_phone = df.loc[idx, phone_col]
                    display_name = df.loc[idx, name_col] if name_col and name_col in df.columns else "N/A"
                    self.log(f"  • Row {row_num}: {raw_phone} (Name: {display_name})")
                self.log("\nPlease remove letters from phone numbers before formatting.")
                messagebox.showwarning(
                    "Validation Failed",
                    f"Found {len(phone_with_letters)} phone number(s) containing letters.\n\nPlease fix the file and try again."
                )
                return
            
            # Fail if phone number is incomplete (must be 11 digits starting with 09 or 12 digits starting with 63)
            df_digits = df[phone_col].astype(str).apply(self.format_phone_number)
            
            # Check for valid Philippine phone number formats
            def is_valid_ph_phone(digits):
                if len(digits) == 11 and digits.startswith('09'):
                    return True
                elif len(digits) == 12 and digits.startswith('63'):
                    return True
                return False
            
            invalid_mask = ~df_digits.apply(is_valid_ph_phone)
            invalid_phone_rows = df[invalid_mask]
            if len(invalid_phone_rows) > 0:
                self.log(f"VALIDATION FAILED: Found {len(invalid_phone_rows)} phone number(s) not matching required format\n")
                self.log("Valid formats: 09xxxxxxxxx (11 digits) or 63xxxxxxxxxx (12 digits)")
                self.log("Rows with invalid phone numbers:")
                for idx in invalid_phone_rows.index:
                    row_num = idx + 2
                    raw_phone = df.loc[idx, phone_col]
                    digits = df_digits.loc[idx]
                    display_name = df.loc[idx, name_col] if name_col and name_col in df.columns else "N/A"
                    reason_parts = []
                    if len(digits) not in [11, 12]:
                        reason_parts.append(f"len={len(digits)}")
                    if not (digits.startswith('09') or digits.startswith('63')):
                        reason_parts.append("invalid prefix")
                    reason = ", ".join(reason_parts) if reason_parts else "format"
                    self.log(f"  • Row {row_num}: {raw_phone} → {digits} ({reason}) (Name: {display_name})")
                self.log("\nPhone numbers must be 11 digits starting with '09' or 12 digits starting with '63'.")
                messagebox.showwarning(
                    "Validation Failed",
                    "Phone numbers must be 11 digits starting with '09' or 12 digits starting with '63'. Please fix the highlighted rows and try again."
                )
                return
            
            # Fail if a row has a phone number but missing required fields (only enforce for columns that have data elsewhere)
            phone_present = ~(df[phone_col].isna() | (df[phone_col].astype(str).str.strip() == ''))
            invalid_rows_mask = pd.Series(False, index=df.index)
            if name_required:
                name_missing = (df[name_col].isna() | (df[name_col].astype(str).str.strip() == ''))
                invalid_rows_mask = invalid_rows_mask | (phone_present & name_missing)
            if date_required:
                date_missing = (df[date_col].isna() | (df[date_col].astype(str).str.strip() == ''))
                invalid_rows_mask = invalid_rows_mask | (phone_present & date_missing)
            invalid_rows = df[invalid_rows_mask]
            if len(invalid_rows) > 0:
                self.log(f"VALIDATION FAILED: Found {len(invalid_rows)} row(s) with phone number but missing required fields\n")
                for idx in invalid_rows.index:
                    row_num = idx + 2
                    missing_fields = []
                    if name_required and (df.loc[idx, name_col] is None or str(df.loc[idx, name_col]).strip() == ''):
                        missing_fields.append('Name')
                    if date_required and (df.loc[idx, date_col] is None or str(df.loc[idx, date_col]).strip() == ''):
                        missing_fields.append('Date')
                    which = ' & '.join(missing_fields) if missing_fields else 'Unknown'
                    self.log(f"  • Row {row_num}: missing {which}")
                self.log("\nPlease fill in the missing required fields (columns that have values elsewhere) for rows that have a phone number.")
                messagebox.showwarning(
                    "Validation Failed",
                    f"Found {len(invalid_rows)} row(s) with a phone number but missing required fields (based on headers in use).\n\nPlease fix the file and try again."
                )
                return
            
            # Check duplicates BEFORE formatting
            # Create a temporary formatted version to check for duplicates
            df_temp = df.copy()
            df_temp[phone_col] = df_temp[phone_col].apply(self.format_phone_number)
            
            duplicates = df_temp[df_temp.duplicated(subset=[phone_col], keep=False)]
            duplicate_count = len(duplicates)
            
            if duplicate_count > 0:
                self.log(f"VALIDATION FAILED: Found duplicate phone numbers\n")
                
                # Get duplicate numbers and their rows
                dup_groups = df_temp[df_temp.duplicated(subset=[phone_col], keep=False)].groupby(phone_col)
                
                self.log("Duplicate phone numbers found:")
                for phone_num, group in dup_groups:
                    self.log(f"\n  {phone_num} appears {len(group)} times:")
                    for idx in group.index:
                        row_num = idx + 2  # +2 because Excel starts at 1 and has header
                        display_name = df.loc[idx, name_col] if name_col and name_col in df.columns else "N/A"
                        self.log(f"    • Row {row_num}: {display_name}")
                
                self.log(f"\nPlease remove duplicates before formatting.")
                messagebox.showwarning(
                    "Validation Failed",
                    f"Found duplicate phone numbers!\n\n"
                    f"Unique numbers duplicated: {len(dup_groups)}\n"
                    f"Total rows affected: {duplicate_count}\n\n"
                    "Please fix the file and try again."
                )
                return
            
            self.log("✓ No duplicates found\n")
            
            # Show what will be changed
            self.log(f"{'─'*60}")
            self.log(f"PREVIEW OF CHANGES")
            self.log(f"{'─'*60}\n")
            
            # Show headers information with column type detection
            self.log(f"Headers found: {len(headers)}")
            for idx, header in enumerate(headers, 1):
                non_empty_count = df[header].notna().sum()
                column_type = self.detect_column_type(df[header])
                self.log(f"  {idx}. {header} ({non_empty_count} records) - Type: {column_type}")
            self.log("")
            
            # Check for empty columns
            empty_columns = []
            for col in df.columns:
                if df[col].isna().all():
                    empty_columns.append(col)
            
            if empty_columns:
                self.log(f"Warning: {len(empty_columns)} header(s) with no records:")
                for col in empty_columns:
                    self.log(f"  • {col}")
                self.log("  (These columns will be kept in the output)\n")
            
            # Count phone numbers that will be formatted
            formatted_count = 0
            decimal_format_count = 0
            self.log("Phone number formatting preview (showing first 5):")
            for idx, phone in enumerate(df[phone_col].head(5)):
                original_phone = str(phone)
                formatted = self.format_phone_number(phone)
                
                # Track special formatting cases
                if '.' in original_phone:
                    try:
                        float_val = float(original_phone)
                        if float_val == int(float_val):  # It's a whole number with decimal
                            decimal_format_count += 1
                    except ValueError:
                        pass
                
                if original_phone != formatted:
                    self.log(f"  {phone} → {formatted}")
                    formatted_count += 1
                else:
                    self.log(f"  {phone} (no change)")
            
            if len(df) > 5:
                self.log(f"  ... and {len(df) - 5} more rows")
            
            self.log(f"\n✓ {len(df)} phone numbers will be formatted")
            
            # Show special formatting statistics
            if decimal_format_count > 0:
                self.log("Special formatting applied:")
                self.log(f"  • {decimal_format_count} decimal format numbers (.0 suffix removed)")
            
            # Check for special characters
            special_char_count = 0
            special_char_columns = []
            special_chars_found = set()
            
            for col in df.columns:
                if df[col].dtype == 'object':
                    has_special = False
                    for val in df[col]:
                        if pd.notna(val):
                            val_str = str(val)
                            # Check for any special characters that will be replaced
                            for char in val_str:
                                if ord(char) > 127:  # Non-ASCII characters
                                    has_special = True
                                    special_chars_found.add(char)
                                    break
                    if has_special:
                        special_char_count += 1
                        special_char_columns.append(col)
            
            if special_char_count > 0:
                self.log(f"✓ Special characters found in {special_char_count} column(s):")
                for col in special_char_columns:
                    self.log(f"  • {col}")
                if special_chars_found:
                    self.log(f"  Special characters detected: {', '.join(sorted(special_chars_found))}")
            else:
                self.log("✓ No special characters found")
            
            self.log(f"\n{'='*60}")
            self.log("VALIDATION PASSED")
            self.log(f"{'='*60}\n")
            self.log("Summary:")
            self.log(f"  • All validation checks passed!")
            self.log(f"  • Total recipients: {len(df)}")

            # self.log(f"\nClick 'Format File' to proceed or 'Preview Changes' to see before/after.\n")
            
            # Store dataframe for preview
            self.preview_df = df.copy()
            
            # Enable format button
            self.validation_passed = True
            self.format_btn.config(state=tk.NORMAL, bg="#27ae60")
            self.preview_btn.config(state=tk.NORMAL, bg="#95a5a6")
            
        except Exception as e:
            self.log(f"\n{'='*60}")
            self.log(f"ERROR OCCURRED")
            self.log(f"{'='*60}\n")
            self.log(f"Error: {str(e)}\n")
            messagebox.showerror("Error", f"Failed to validate file:\n{str(e)}")
    
    def show_preview(self):
        """Show before/after preview in a new window"""
        if not self.validation_passed or self.preview_df is None:
            messagebox.showwarning("No File", "Please drag and drop a CSV file first.")
            return
        
        # Create preview window
        preview_window = tk.Toplevel(self.root)
        preview_window.title("Preview Changes - Before & After")
        preview_window.geometry("1200x700")
        preview_window.minsize(1200, 700)
        preview_window.configure(bg="#f5f7fa")
        
        # Header
        header = tk.Label(
            preview_window,
            text="Preview Changes",
            font=("Segoe UI", 16, "bold"),
            bg="#f5f7fa",
            fg="#2c3e50"
        )
        header.pack(pady=15)
        
        # Create main frame with two columns
        main_frame = tk.Frame(preview_window, bg="#f5f7fa")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # BEFORE column
        before_frame = tk.Frame(main_frame, bg="white", relief=tk.FLAT)
        before_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        before_header = tk.Label(
            before_frame,
            text="BEFORE (Original)",
            font=("Segoe UI", 12, "bold"),
            bg="#e74c3c",
            fg="white",
            pady=10
        )
        before_header.pack(fill=tk.X)
        
        # AFTER column
        after_frame = tk.Frame(main_frame, bg="white", relief=tk.FLAT)
        after_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        after_header = tk.Label(
            after_frame,
            text="AFTER (Formatted)",
            font=("Segoe UI", 12, "bold"),
            bg="#27ae60",
            fg="white",
            pady=10
        )
        after_header.pack(fill=tk.X)
        
        # Create Text widgets with scrollbars for BEFORE
        before_text_frame = tk.Frame(before_frame, bg="white")
        before_text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        before_scrollbar_y = tk.Scrollbar(before_text_frame)
        before_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        before_scrollbar_x = tk.Scrollbar(before_text_frame, orient=tk.HORIZONTAL)
        before_scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        before_text = tk.Text(
            before_text_frame,
            font=("Consolas", 9),
            bg="#fff5f5",
            fg="#2c3e50",
            wrap=tk.NONE,
            yscrollcommand=before_scrollbar_y.set,
            xscrollcommand=before_scrollbar_x.set
        )
        before_text.pack(fill=tk.BOTH, expand=True)
        # y-scroll command will be set after both text widgets are created, to sync scroll
        before_scrollbar_x.config(command=before_text.xview)
        
        # Create Text widgets with scrollbars for AFTER
        after_text_frame = tk.Frame(after_frame, bg="white")
        after_text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        after_scrollbar_y = tk.Scrollbar(after_text_frame)
        after_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        after_scrollbar_x = tk.Scrollbar(after_text_frame, orient=tk.HORIZONTAL)
        after_scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        after_text = tk.Text(
            after_text_frame,
            font=("Consolas", 9),
            bg="#f0fff4",
            fg="#2c3e50",
            wrap=tk.NONE,
            yscrollcommand=after_scrollbar_y.set,
            xscrollcommand=after_scrollbar_x.set
        )
        after_text.pack(fill=tk.BOTH, expand=True)
        # y-scroll command will be set to sync both panes
        after_scrollbar_x.config(command=after_text.xview)

        # Synchronize vertical scrolling between BEFORE and AFTER panes
        def _sync_y_scroll(*args):
            before_text.yview(*args)
            after_text.yview(*args)
        def _on_text_yscroll(first, last):
            before_scrollbar_y.set(first, last)
            after_scrollbar_y.set(first, last)
        before_scrollbar_y.config(command=_sync_y_scroll)
        after_scrollbar_y.config(command=_sync_y_scroll)
        before_text.config(yscrollcommand=_on_text_yscroll)
        after_text.config(yscrollcommand=_on_text_yscroll)

        # Sync mouse wheel scrolling on Windows
        def _on_mousewheel(event):
            delta = -1 if event.delta > 0 else 1
            before_text.yview_scroll(delta, "units")
            after_text.yview_scroll(delta, "units")
            return "break"
        before_text.bind("<MouseWheel>", _on_mousewheel)
        after_text.bind("<MouseWheel>", _on_mousewheel)

        # Populate BEFORE data (original)
        df_before = self.preview_df.copy()
        before_text.insert("1.0", "Row | " + " | ".join(df_before.columns) + "\n")
        before_text.insert(tk.END, "─" * 80 + "\n")
        
        for idx, row in df_before.iterrows():
            row_data = f"{idx+2:3d} | " + " | ".join([str(val)[:20] for val in row.values])
            before_text.insert(tk.END, row_data + "\n")
        
        
        # Populate AFTER data (formatted)
        df_after = self.preview_df.copy()
        phone_col = df_after.columns[0]
        df_after[phone_col] = df_after[phone_col].apply(self.format_phone_number)
        
        for col in df_after.columns:
            if df_after[col].dtype == 'object':
                df_after[col] = df_after[col].apply(self.replace_special_chars)
        
        after_text.insert("1.0", "Row | " + " | ".join(df_after.columns) + "\n")
        after_text.insert(tk.END, "─" * 80 + "\n")
        
        for idx, row in df_after.iterrows():
            row_data = f"{idx+2:3d} | " + " | ".join([str(val)[:20] for val in row.values])
            after_text.insert(tk.END, row_data + "\n")
        
        
        # Highlight changed rows in BOTH panes with yellow background
        before_text.tag_configure("changed", background="#fff59d")
        after_text.tag_configure("changed", background="#fff59d")
        max_rows_to_compare = min(len(df_before), len(df_after))
        for i, idx in enumerate(df_before.index[:max_rows_to_compare]):
            row_changed = False
            for col in df_after.columns:
                before_val = df_before.loc[idx, col] if col in df_before.columns else None
                after_val = df_after.loc[idx, col] if col in df_after.columns else None
                if str(before_val) != str(after_val):
                    row_changed = True
                    break
            if row_changed:
                line_no = 3 + i  # header=1, separator=2, first row starts at 3
                before_text.tag_add("changed", f"{line_no}.0", f"{line_no}.end")
                after_text.tag_add("changed", f"{line_no}.0", f"{line_no}.end")

        # Disable editing after applying highlights
        before_text.config(state=tk.DISABLED)
        after_text.config(state=tk.DISABLED)
        
        # Close button
        close_btn = tk.Button(
            preview_window,
            text="Close Preview",
            command=preview_window.destroy,
            font=("Segoe UI", 10, "bold"),
            bg="#95a5a6",
            fg="white",
            relief=tk.FLAT,
            padx=20,
            pady=8,
            cursor="hand2"
        )
        close_btn.pack(pady=(0, 15))
    
    def format_file(self):
        """Format and export the validated file"""
        if not self.validation_passed or not self.current_file_path:
            messagebox.showwarning("No File", "Please drag and drop a CSV file first.")
            return
        
        try:
            self.log(f"{'='*60}")
            self.log(f"FORMATTING FILE")
            self.log(f"{'='*60}\n")
            # Artificial loading (quick, non-blocking feel)
            try:
                spinner_frames = ['⠋','⠙','⠹','⠸','⠼','⠴','⠦','⠧','⠇','⠏']
                total_frames = 5  # ~0.4s with 0.08s per frame
                # Seed the line once
                self.status_text.insert(tk.END, "⠋ Preparing .csv file...\n")
                self.status_text.see(tk.END)
                self.root.update()
                for i in range(total_frames):
                    frame = spinner_frames[i % len(spinner_frames)]
                    # Replace the last line in-place
                    start_idx = self.status_text.index('end-1l linestart')
                    end_idx = self.status_text.index('end-1l lineend')
                    self.status_text.delete(start_idx, end_idx)
                    self.status_text.insert(start_idx, f"{frame} Preparing .csv file...")
                    self.root.update()
                    time.sleep(0.08)
                # Finalize line
                start_idx = self.status_text.index('end-1l linestart')
                end_idx = self.status_text.index('end-1l lineend')
                self.status_text.delete(start_idx, end_idx)
                self.status_text.insert(start_idx, "✓ .csv file ready")
                self.status_text.insert(tk.END, "\n")
                self.status_text.see(tk.END)
                self.root.update()
            except Exception:
                pass
            
            # Read CSV again
            df = pd.read_csv(self.current_file_path)
            phone_col = df.columns[0]

            # Additional artificial checks with randomized, faster durations (single-line updates)
            try:
                def animate_step(base_label, min_ms=5, max_ms=20):
                    frames = ['⠋','⠙','⠹','⠸','⠼','⠴','⠦','⠧','⠇','⠏']
                    duration = random.randint(min_ms, max_ms) / 1000.0
                    frame_time = 0.02
                    steps = max(2, int(duration / frame_time))
                    self.status_text.insert(tk.END, f"{frames[0]} {base_label}...\n")
                    self.status_text.see(tk.END)
                    self.root.update()
                    for i in range(steps):
                        start_idx = self.status_text.index('end-1l linestart')
                        end_idx = self.status_text.index('end-1l lineend')
                        self.status_text.delete(start_idx, end_idx)
                        self.status_text.insert(start_idx, f"{frames[i % len(frames)]} {base_label}...")
                        self.root.update()
                        time.sleep(frame_time)
                    start_idx = self.status_text.index('end-1l linestart')
                    end_idx = self.status_text.index('end-1l lineend')
                    self.status_text.delete(start_idx, end_idx)
                    self.status_text.insert(start_idx, f"✓ {base_label} passed.")
                    self.status_text.insert(tk.END, "\n")
                    self.status_text.see(tk.END)
                    self.root.update()
 
                animate_step("Checking special characters")
                animate_step("Detecting duplicates")
                animate_step("Verifying required headers")
            except Exception:
                pass
            
            # Format phone numbers
            self.log("Formatting phone numbers...")
            
            # Track special formatting cases during actual formatting
            decimal_format_count = 0
            
            def format_and_track(phone):
                nonlocal decimal_format_count
                original = str(phone)
                formatted = self.format_phone_number(phone)
                
                # Track special cases
                if '.' in original:
                    try:
                        float_val = float(original)
                        if float_val == int(float_val):  # It's a whole number with decimal
                            decimal_format_count += 1
                    except ValueError:
                        pass
                
                return formatted
            
            df[phone_col] = df[phone_col].apply(format_and_track)
            formatted_count = len(df[df[phone_col] != ""])
            self.log(f"✓ Formatted {formatted_count} phone numbers")
            
            # Show special formatting statistics
            if decimal_format_count > 0:
                self.log("Special formatting applied:")
                self.log(f"  • {decimal_format_count} decimal format numbers (.0 suffix removed)")
            self.log("")
            
            # Replace special characters in all columns and track statistics
            self.log("Replacing special characters (accented letters, symbols, etc.)...")
            
            # Track special character replacements
            total_replacements = 0
            replacement_stats = {}
            columns_with_replacements = 0
            
            for col in df.columns:
                if df[col].dtype == 'object':  # Only string columns
                    col_replacements = 0
                    for idx, value in df[col].items():
                        if pd.notna(value):
                            result = self.replace_special_chars(value, track_replacements=True)
                            if isinstance(result, tuple):
                                text, replacements = result
                                df.loc[idx, col] = text
                                if replacements:
                                    col_replacements += sum(r['count'] for r in replacements.values())
                                    for char, info in replacements.items():
                                        if char not in replacement_stats:
                                            replacement_stats[char] = {'replacement': info['replacement'], 'count': 0}
                                        replacement_stats[char]['count'] += info['count']
                            else:
                                df.loc[idx, col] = result
                    
                    if col_replacements > 0:
                        columns_with_replacements += 1
                        total_replacements += col_replacements
                        self.log(f"  • {col}: {col_replacements} characters replaced")
            
            if total_replacements > 0:
                self.log(f"✓ Special characters replaced: {total_replacements} total")

                
                # Show detailed breakdown of replacements
                if replacement_stats:
                    self.log("  Replacement breakdown:")
                    for char, info in sorted(replacement_stats.items(), key=lambda x: x[1]['count'], reverse=True):
                        self.log(f"    {char} → {info['replacement']}: {info['count']} times")
            else:
                self.log("✓ No special characters found to replace")
            self.log("")
            
            # Generate output filename
            self.log("Generating output file...")
            
            # Get custom filename from entry
            custom_name = self.filename_entry.get().strip()
            if not custom_name:
                custom_name = "sms_contacts"
            
            # Remove any file extension if user added one
            custom_name = os.path.splitext(custom_name)[0]
            
            # Remove any invalid filename characters
            custom_name = re.sub(r'[<>:"/\\|?*]', '_', custom_name)
            
            output_filename = f"{custom_name}.csv"
            output_path = os.path.join(self.output_dir, output_filename)
            
            # Check if file exists and add number suffix if needed
            counter = 1
            while os.path.exists(output_path):
                output_filename = f"{custom_name}_{counter}.csv"
                output_path = os.path.join(self.output_dir, output_filename)
                counter += 1
            
            # Export to CSV
            df.to_csv(output_path, index=False, encoding='utf-8')
            
            final_rows = len(df)
            self.log("✓ File exported successfully\n")
            self.log(f"{'='*60}")
            self.log(f"FORMATTING COMPLETE")
            self.log(f"{'='*60}\n")
            self.log(f"FINAL SUMMARY:")
            
            # Show all headers with record counts
            self.log(f"\nHeaders and Record Counts:")
            for idx, col in enumerate(df.columns, 1):
                non_empty_count = df[col].notna().sum()
                if non_empty_count == 0:
                    self.log(f"  {idx}. {col} - NO RECORDS")
                else:
                    self.log(f"  {idx}. {col} - {non_empty_count} records")
            
            
            self.log(f"OUTPUT:")
            self.log(f"  • Filename: {output_filename}")
            self.log(f"  • Location: {self.output_dir}\n")
            self.log(f"{'='*60}\n")
            self.log(f"  • File saved successfully ✓\n")
            if total_replacements > 0:
                self.log(f"  • Special characters replaced: {total_replacements}")
            else:
                self.log(f"  • Special characters: None found")
            self.log(f"  • Total recipients ready: {final_rows}")
 
            #self.log("Ready for SMS blast!\n")
            
            # Reset state
            self.validation_passed = False
            self.current_file_path = None
            self.preview_df = None
            self.format_btn.config(state=tk.DISABLED, bg="#95a5a6")
            self.preview_btn.config(state=tk.DISABLED, bg="#bdc3c7")
            
            # Highlight the 'Total recipients ready' line in the log
            try:
                highlight_text = f"  • Total recipients ready: {final_rows}"
                start_index = self.status_text.search(highlight_text, "1.0", tk.END)
                if start_index:
                    end_index = f"{start_index}+{len(highlight_text)}c"
                    self.status_text.tag_configure("success_line", background="#e8f5e9", foreground="#1b5e20")
                    self.status_text.tag_add("success_line", start_index, end_index)
            except Exception:
                pass
            
        except Exception as e:
            self.log(f"\n{'='*60}")
            self.log(f"ERROR OCCURRED")
            self.log(f"{'='*60}\n")
            self.log(f"Error: {str(e)}\n")
            self.validation_passed = False
            self.preview_df = None
            self.format_btn.config(state=tk.DISABLED, bg="#95a5a6")
            self.preview_btn.config(state=tk.DISABLED, bg="#bdc3c7")
            messagebox.showerror("Error", f"Failed to format file:\n{str(e)}")

def main():
    root = TkinterDnD.Tk()
    app = CSVFormatterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()