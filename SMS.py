import tkinter as tk
from tkinter import ttk, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
import pandas as pd
import re
from datetime import datetime
import os
import json
import sys

# Try to import PIL, but make it optional
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# Try to import pkg_resources for embedded resources
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
                    max_width = 500  # Adjust this to fit your window better
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
            text="Format, validate, and prepare your SMS contact lists",
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
    
    def format_phone_number(self, phone):
        """Format phone number to digits only"""
        if pd.isna(phone):
            return ""
        # Convert to string and remove all non-digit characters
        phone_str = str(phone)
        digits = re.sub(r'\D', '', phone_str)
        return digits
    
    def replace_special_chars(self, text, track_replacements=False):
        """Replace special characters with their ASCII equivalents"""
        if pd.isna(text):
            return text, {} if track_replacements else text
        text = str(text)
        original_text = text
        
        # Comprehensive character mapping for common special characters
        char_map = {
            # Spanish characters
            'ñ': 'n', 'Ñ': 'N',
            
            # French characters
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
            
            # German characters
            'ß': 'ss',
            
            # Polish characters
            'ą': 'a', 'ć': 'c', 'ę': 'e', 'ł': 'l', 'ń': 'n', 'ó': 'o', 'ś': 's', 'ź': 'z', 'ż': 'z',
            'Ą': 'A', 'Ć': 'C', 'Ę': 'E', 'Ł': 'L', 'Ń': 'N', 'Ó': 'O', 'Ś': 'S', 'Ź': 'Z', 'Ż': 'Z',
            
            # Czech characters
            'č': 'c', 'ď': 'd', 'ě': 'e', 'ň': 'n', 'ř': 'r', 'š': 's', 'ť': 't', 'ů': 'u', 'ž': 'z',
            'Č': 'C', 'Ď': 'D', 'Ě': 'E', 'Ň': 'N', 'Ř': 'R', 'Š': 'S', 'Ť': 'T', 'Ů': 'U', 'Ž': 'Z',
            
            # Romanian characters
            'ă': 'a', 'â': 'a', 'î': 'i', 'ș': 's', 'ț': 't',
            'Ă': 'A', 'Â': 'A', 'Î': 'I', 'Ș': 'S', 'Ț': 'T',
            
            # Hungarian characters
            'ő': 'o', 'ű': 'u',
            'Ő': 'O', 'Ű': 'U',
            
            # Turkish characters
            'ğ': 'g', 'ı': 'i', 'ş': 's',
            'Ğ': 'G', 'İ': 'I', 'Ş': 'S',
            
            # Scandinavian characters
            'æ': 'ae', 'ø': 'o', 'å': 'a',
            'Æ': 'AE', 'Ø': 'O', 'Å': 'A',
            
            # Other common special characters
            'œ': 'oe', 'Œ': 'OE',
            'ð': 'd', 'Ð': 'D',
            'þ': 'th', 'Þ': 'TH',
            
            # Currency and symbols
            '€': 'EUR', '£': 'GBP', '¥': 'JPY',
            '°': 'deg', '±': '+/-', '×': 'x', '÷': '/',
            '©': '(c)', '®': '(R)', '™': '(TM)',
            
            # Quotation marks and punctuation
            '"': '"', '"': '"', ''': "'", ''': "'",
            '–': '-', '—': '-', '…': '...',
            
            # Mathematical symbols
            '≤': '<=', '≥': '>=', '≠': '!=', '≈': '~=',
            '∞': 'inf', '√': 'sqrt', '∑': 'sum',
            
            # Greek letters (common ones)
            'α': 'alpha', 'β': 'beta', 'γ': 'gamma', 'δ': 'delta', 'ε': 'epsilon',
            'ζ': 'zeta', 'η': 'eta', 'θ': 'theta', 'ι': 'iota', 'κ': 'kappa',
            'λ': 'lambda', 'μ': 'mu', 'ν': 'nu', 'ξ': 'xi', 'ο': 'omicron',
            'π': 'pi', 'ρ': 'rho', 'σ': 'sigma', 'τ': 'tau', 'υ': 'upsilon',
            'φ': 'phi', 'χ': 'chi', 'ψ': 'psi', 'ω': 'omega',
            'Α': 'Alpha', 'Β': 'Beta', 'Γ': 'Gamma', 'Δ': 'Delta', 'Ε': 'Epsilon',
            'Ζ': 'Zeta', 'Η': 'Eta', 'Θ': 'Theta', 'Ι': 'Iota', 'Κ': 'Kappa',
            'Λ': 'Lambda', 'Μ': 'Mu', 'Ν': 'Nu', 'Ξ': 'Xi', 'Ο': 'Omicron',
            'Π': 'Pi', 'Ρ': 'Rho', 'Σ': 'Sigma', 'Τ': 'Tau', 'Υ': 'Upsilon',
            'Φ': 'Phi', 'Χ': 'Chi', 'Ψ': 'Psi', 'Ω': 'Omega'
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
            
            # Assume first column is phone number
            if len(df.columns) == 0:
                raise ValueError("CSV file is empty")
            
            phone_col = df.columns[0]
            self.log(f"{'─'*60}")
            self.log(f"VALIDATION CHECKS")
            self.log(f"{'─'*60}\n")
            
            # Check for empty phone numbers BEFORE formatting
            empty_phone_rows = df[df[phone_col].isna() | (df[phone_col].astype(str).str.strip() == '')]
            if len(empty_phone_rows) > 0:
                self.log(f"VALIDATION FAILED: Found {len(empty_phone_rows)} empty phone number(s)\n")
                self.log("Rows with empty phone numbers:")
                for idx in empty_phone_rows.index:
                    row_num = idx + 2  # +2 because Excel starts at 1 and has header
                    name = empty_phone_rows.loc[idx, df.columns[1]] if len(df.columns) > 1 else "N/A"
                    self.log(f"  • Row {row_num}: {name}")
                
                self.log(f"\nPlease fix empty phone numbers before formatting.")
                messagebox.showwarning(
                    "Validation Failed",
                    f"Found {len(empty_phone_rows)} row(s) with empty phone numbers.\n\n"
                    "Please fix the file and try again."
                )
                return
            
            self.log("✓ No empty phone numbers found")
            
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
                        name = df.loc[idx, df.columns[1]] if len(df.columns) > 1 else "N/A"
                        self.log(f"    • Row {row_num}: {name}")
                
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
            
            # Show headers information
            self.log(f"Headers found: {len(headers)}")
            for idx, header in enumerate(headers, 1):
                non_empty_count = df[header].notna().sum()
                self.log(f"  {idx}. {header} ({non_empty_count} records)")
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
            self.log("Phone number formatting preview (showing first 5):")
            for idx, phone in enumerate(df[phone_col].head(5)):
                formatted = self.format_phone_number(phone)
                if str(phone) != formatted:
                    self.log(f"  {phone} → {formatted}")
                    formatted_count += 1
                else:
                    self.log(f"  {phone} (no change)")
            
            if len(df) > 5:
                self.log(f"  ... and {len(df) - 5} more rows")
            
            self.log(f"\n✓ {len(df)} phone numbers will be formatted")
            
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
            self.log(f"  • Total rows: {len(df)}")
            self.log(f"  • Total columns: {len(headers)}")
            self.log(f"  • All validation checks passed ✓")
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
        preview_window.geometry("1000x600")
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
        before_scrollbar_y.config(command=before_text.yview)
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
        after_scrollbar_y.config(command=after_text.yview)
        after_scrollbar_x.config(command=after_text.xview)
        
        # Populate BEFORE data (original)
        df_before = self.preview_df.copy()
        before_text.insert("1.0", "Row | " + " | ".join(df_before.columns) + "\n")
        before_text.insert(tk.END, "─" * 80 + "\n")
        
        for idx, row in df_before.head(20).iterrows():
            row_data = f"{idx+2:3d} | " + " | ".join([str(val)[:20] for val in row.values])
            before_text.insert(tk.END, row_data + "\n")
        
        if len(df_before) > 20:
            before_text.insert(tk.END, f"\n... and {len(df_before) - 20} more rows\n")
        
        before_text.config(state=tk.DISABLED)
        
        # Populate AFTER data (formatted)
        df_after = self.preview_df.copy()
        phone_col = df_after.columns[0]
        df_after[phone_col] = df_after[phone_col].apply(self.format_phone_number)
        
        for col in df_after.columns:
            if df_after[col].dtype == 'object':
                df_after[col] = df_after[col].apply(self.replace_special_chars)
        
        after_text.insert("1.0", "Row | " + " | ".join(df_after.columns) + "\n")
        after_text.insert(tk.END, "─" * 80 + "\n")
        
        for idx, row in df_after.head(20).iterrows():
            row_data = f"{idx+2:3d} | " + " | ".join([str(val)[:20] for val in row.values])
            after_text.insert(tk.END, row_data + "\n")
        
        if len(df_after) > 20:
            after_text.insert(tk.END, f"\n... and {len(df_after) - 20} more rows\n")
        
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
            
            # Read CSV again
            df = pd.read_csv(self.current_file_path)
            phone_col = df.columns[0]
            
            # Format phone numbers
            self.log("Formatting phone numbers...")
            df[phone_col] = df[phone_col].apply(self.format_phone_number)
            formatted_count = len(df[df[phone_col] != ""])
            self.log(f"✓ Formatted {formatted_count} phone numbers\n")
            
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
                self.log(f"✓ Affected columns: {columns_with_replacements}")
                
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
            self.log(f"\n  • Phone numbers formatted: {formatted_count}")
            self.log(f"  • Total recipients ready: {final_rows}")
            if total_replacements > 0:
                self.log(f"  • Special characters replaced: {total_replacements}")
                self.log(f"  • Affected columns: {columns_with_replacements}")
            else:
                self.log(f"  • Special characters: None found")
            #self.log("Ready for SMS blast!\n")
            
            # Reset state
            self.validation_passed = False
            self.current_file_path = None
            self.preview_df = None
            self.format_btn.config(state=tk.DISABLED, bg="#95a5a6")
            self.preview_btn.config(state=tk.DISABLED, bg="#bdc3c7")
            
            # Prepare success message with special character stats
            success_message = f"File formatted successfully!\n\nSummary:\n"
            success_message += f"  • Phone numbers formatted: {formatted_count}\n"
            
            
            if total_replacements > 0:
                success_message += f"  • Special characters replaced: {total_replacements}\n"
                success_message += f"  • Affected columns: {columns_with_replacements}\n"
                success_message += f"  • Total recipients: {final_rows}\n"
            else:
                success_message += f"  • Special characters: None found\n"
            
            success_message += f"\nSaved as:\n{output_filename}\n\n"
            success_message += f"Location:\n{self.output_dir}"
            
            messagebox.showinfo("Success", success_message)
            
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