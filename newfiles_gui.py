import os
import sys
import json
import threading
import time
import customtkinter as ctk
from tkinter import filedialog, messagebox
import tkinter as tk
from pathlib import Path

from config.settings import Settings
from core.processor import FileProcessor
from core.monitor import FileMonitor
from utils.logger import default_logger

class NewfilesGUI:
    def __init__(self):
        # Initialize CustomTkinter
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        
        # Create the main window
        self.root = ctk.CTk()
        self.root.title("Newfiles - Automatic Content Generator")
        self.root.geometry("1000x750")
        self.root.minsize(900, 650)
        
        # Set window icon
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass
        
        # Initialize variables
        self.monitor = None
        self.monitor_thread = None
        self.is_monitoring = False
        self.config_path = "config/config.json"
        
        # Ensure config directory exists
        os.makedirs("config", exist_ok=True)
        os.makedirs("logs", exist_ok=True)
        
        # Load settings
        self.load_settings()
        
        # Create UI
        self.create_widgets()
        self.load_config_values()
        
        # Handle closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Start log monitoring
        self.start_log_monitoring()
    
    def load_settings(self):
        """Load settings from config file or create default if not exists"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    self.config_data = json.load(f)
            else:
                self.config_data = self.create_default_config()
                self.save_config()
        except Exception as e:
            print(f"Error loading config: {e}")
            self.config_data = self.create_default_config()
    
    def create_default_config(self):
        """Create default configuration"""
        return {
            "monitored_directory": str(Path.home() / "Desktop"),
            "delay": 0.5,
            "monitor_subdirectories": True,
            "default_text_prompt_file": "prompts/default_text.md",
            "default_image_prompt_file": "prompts/default_image.md",
            "extension_settings": {
                "txt": {
                    "model": "gpt-4.1-nano",
                    "prompt_file": "prompts/default_text.md"
                },
                "md": {
                    "model": "gpt-4.1-nano",
                    "prompt_file": "prompts/default_text.md"
                },
                "py": {
                    "model": "gpt-4.1-nano",
                    "prompt_file": "prompts/default_text.md"
                },
                "java": {
                    "model": "gpt-4.1-nano",
                    "prompt_file": "prompts/default_text.md"
                },
                "png": {
                    "model": "dall-e-3",
                    "prompt_file": "prompts/image.md"
                },
                "jpg": {
                    "model": "dall-e-3",
                    "prompt_file": "prompts/image.md"
                }
            }
        }
    
    def save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.config_data, f, indent=2)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save config: {str(e)}")
            return False
    
    def create_widgets(self):
        # Create tabview
        self.tabview = ctk.CTkTabview(self.root)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create tabs
        self.settings_tab = self.tabview.add("Settings")
        self.models_tab = self.tabview.add("AI Models")
        self.monitoring_tab = self.tabview.add("Monitoring")
        self.logs_tab = self.tabview.add("Logs")
        
        # Create widgets for each tab
        self.create_settings_widgets()
        self.create_models_widgets()
        self.create_monitoring_widgets()
        self.create_logs_widgets()
    
    def create_settings_widgets(self):
        # Main frame for settings
        settings_frame = ctk.CTkFrame(self.settings_tab)
        settings_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Directory selection
        dir_label = ctk.CTkLabel(settings_frame, text="Monitored Directory:", font=ctk.CTkFont(size=14, weight="bold"))
        dir_label.pack(anchor="w", padx=20, pady=(20, 5))
        
        dir_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        dir_frame.pack(fill="x", padx=20, pady=5)
        
        self.dir_var = tk.StringVar()
        dir_entry = ctk.CTkEntry(dir_frame, textvariable=self.dir_var, width=500)
        dir_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        dir_button = ctk.CTkButton(dir_frame, text="Browse...", command=self.browse_directory, width=100)
        dir_button.pack(side="right")
        
        # Delay setting
        delay_label = ctk.CTkLabel(settings_frame, text="Processing Delay (seconds):", font=ctk.CTkFont(size=14, weight="bold"))
        delay_label.pack(anchor="w", padx=20, pady=(20, 5))
        
        delay_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        delay_frame.pack(fill="x", padx=20, pady=5)
        
        self.delay_var = tk.DoubleVar()
        delay_entry = ctk.CTkEntry(delay_frame, textvariable=self.delay_var, width=100)
        delay_entry.pack(side="left", padx=(0, 10))
        
        delay_info = ctk.CTkLabel(delay_frame, text="Delay before processing new files", text_color="gray")
        delay_info.pack(side="left")
        
        # Monitor subdirectories
        sub_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        sub_frame.pack(fill="x", padx=20, pady=(20, 5))
        
        self.sub_var = tk.BooleanVar()
        sub_check = ctk.CTkCheckBox(sub_frame, text="Monitor subdirectories", variable=self.sub_var)
        sub_check.pack(anchor="w")
        
        # Save button
        save_button = ctk.CTkButton(settings_frame, text="Save Settings", command=self.save_settings, width=200, height=40)
        save_button.pack(pady=30)
    
    def create_models_widgets(self):
        # Main frame for models
        models_frame = ctk.CTkFrame(self.models_tab)
        models_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Models info label
        info_label = ctk.CTkLabel(models_frame, text="Configure AI models for different file extensions", 
                                 font=ctk.CTkFont(size=14, weight="bold"))
        info_label.pack(pady=(20, 10))
        
        # Create a frame for the treeview and scrollbars
        tree_frame = ctk.CTkFrame(models_frame)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Create treeview for extension settings
        columns = ("Extension", "Model", "Prompt File")
        self.models_tree = tk.ttk.Treeview(tree_frame, columns=columns, show="headings", height=10)
        
        # Define headings
        for col in columns:
            self.models_tree.heading(col, text=col)
            self.models_tree.column(col, width=200)
        
        # Add scrollbars
        v_scrollbar = ctk.CTkScrollbar(tree_frame, orientation="vertical", command=self.models_tree.yview)
        h_scrollbar = ctk.CTkScrollbar(tree_frame, orientation="horizontal", command=self.models_tree.xview)
        self.models_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack treeview and scrollbars
        self.models_tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Add button frame
        button_frame = ctk.CTkFrame(models_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=10)
        
        # Add extension button
        add_button = ctk.CTkButton(button_frame, text="Add Extension", command=self.add_extension, width=120)
        add_button.pack(side="left", padx=(0, 10))
        
        # Edit extension button
        edit_button = ctk.CTkButton(button_frame, text="Edit Extension", command=self.edit_extension, width=120)
        edit_button.pack(side="left", padx=10)
        
        # Remove extension button
        remove_button = ctk.CTkButton(button_frame, text="Remove Extension", command=self.remove_extension, width=120)
        remove_button.pack(side="left", padx=10)
        
        # Model suggestions
        model_frame = ctk.CTkFrame(models_frame)
        model_frame.pack(fill="x", padx=20, pady=10)
        
        model_label = ctk.CTkLabel(model_frame, text="Suggested Models:", font=ctk.CTkFont(size=12, weight="bold"))
        model_label.pack(anchor="w", pady=(5, 5))
        
        models_text = ctk.CTkLabel(model_frame, 
                                 text="Text: gpt-4.1-nano, gpt-4.1-mini, gpt-4.1, gpt-4o-mini\n" +
                                      "Images: dall-e-3, dall-e-2", 
                                 font=ctk.CTkFont(size=11), text_color="gray")
        models_text.pack(anchor="w")
        
        # Save models button
        save_models_button = ctk.CTkButton(models_frame, text="Save Models", command=self.save_models, width=200, height=40)
        save_models_button.pack(pady=20)
    
    def create_monitoring_widgets(self):
        # Main frame for monitoring
        monitoring_frame = ctk.CTkFrame(self.monitoring_tab)
        monitoring_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Status frame
        status_frame = ctk.CTkFrame(monitoring_frame)
        status_frame.pack(fill="x", padx=20, pady=20)
        
        status_label = ctk.CTkLabel(status_frame, text="Monitoring Status:", font=ctk.CTkFont(size=14, weight="bold"))
        status_label.pack(anchor="w", padx=10, pady=10)
        
        self.status_var = tk.StringVar(value="Not monitoring")
        status_value = ctk.CTkLabel(status_frame, textvariable=self.status_var, font=ctk.CTkFont(size=16, weight="bold"))
        status_value.pack(anchor="w", padx=10, pady=(0, 10))
        
        # Control buttons
        control_frame = ctk.CTkFrame(monitoring_frame)
        control_frame.pack(fill="x", padx=20, pady=20)
        
        self.start_button = ctk.CTkButton(control_frame, text="Start Monitoring", command=self.start_monitoring, 
                                         width=200, height=50, font=ctk.CTkFont(size=14))
        self.start_button.pack(side="left", padx=(0, 20), pady=20)
        
        self.stop_button = ctk.CTkButton(control_frame, text="Stop Monitoring", command=self.stop_monitoring, 
                                        width=200, height=50, font=ctk.CTkFont(size=14), state="disabled")
        self.stop_button.pack(side="left", padx=20, pady=20)
        
        # Directory info
        dir_info_frame = ctk.CTkFrame(monitoring_frame)
        dir_info_frame.pack(fill="x", padx=20, pady=20)
        
        dir_info_label = ctk.CTkLabel(dir_info_frame, text="Monitoring Information:", font=ctk.CTkFont(size=14, weight="bold"))
        dir_info_label.pack(anchor="w", padx=10, pady=10)
        
        self.monitoring_dir_var = tk.StringVar()
        dir_info_value = ctk.CTkLabel(dir_info_frame, textvariable=self.monitoring_dir_var, font=ctk.CTkFont(size=12))
        dir_info_value.pack(anchor="w", padx=10, pady=(0, 5))
        
        self.sub_info_var = tk.StringVar()
        sub_info_value = ctk.CTkLabel(dir_info_frame, textvariable=self.sub_info_var, font=ctk.CTkFont(size=12))
        sub_info_value.pack(anchor="w", padx=10, pady=(0, 10))
    
    def create_logs_widgets(self):
        # Main frame for logs
        logs_frame = ctk.CTkFrame(self.logs_tab)
        logs_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Logs text area
        logs_label = ctk.CTkLabel(logs_frame, text="Application Logs:", font=ctk.CTkFont(size=14, weight="bold"))
        logs_label.pack(anchor="w", padx=20, pady=(20, 10))
        
        # Create text widget for logs
        logs_text_frame = ctk.CTkFrame(logs_frame)
        logs_text_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.log_text = tk.Text(logs_text_frame, wrap=tk.WORD, bg="#1f1f1f", fg="white", font=("Consolas", 10))
        self.log_text.pack(side="left", fill="both", expand=True)
        
        # Scrollbar for logs
        log_scrollbar = ctk.CTkScrollbar(logs_text_frame, orientation="vertical", command=self.log_text.yview)
        log_scrollbar.pack(side="right", fill="y")
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        # Control buttons
        button_frame = ctk.CTkFrame(logs_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        clear_button = ctk.CTkButton(button_frame, text="Clear Logs", command=self.clear_logs, width=120)
        clear_button.pack(side="left", padx=(0, 10))
        
        refresh_button = ctk.CTkButton(button_frame, text="Refresh Logs", command=self.refresh_logs, width=120)
        refresh_button.pack(side="left")
        
        # Redirect logs to text widget
        self.refresh_logs()
    
    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.dir_var.set(directory)
    
    def load_config_values(self):
        # Load directory
        self.dir_var.set(self.config_data.get("monitored_directory", str(Path.home() / "Desktop")))
        
        # Load delay
        self.delay_var.set(self.config_data.get("delay", 0.5))
        
        # Load subdirectory monitoring
        self.sub_var.set(self.config_data.get("monitor_subdirectories", True))
        
        # Load extension settings
        self.load_extension_settings()
    
    def load_extension_settings(self):
        # Clear existing items
        for item in self.models_tree.get_children():
            self.models_tree.delete(item)
        
        # Load extension settings
        extension_settings = self.config_data.get("extension_settings", {})
        for extension, settings in extension_settings.items():
            model = settings.get("model", "gpt-4.1-nano")
            prompt_file = settings.get("prompt_file", "prompts/default_text.md")
            self.models_tree.insert("", tk.END, values=(extension, model, prompt_file))
    
    def save_settings(self):
        try:
            # Update config data
            self.config_data["monitored_directory"] = self.dir_var.get()
            self.config_data["delay"] = self.delay_var.get()
            self.config_data["monitor_subdirectories"] = self.sub_var.get()
            
            if self.save_config():
                messagebox.showinfo("Success", "Settings saved successfully!")
                self.log_text.insert(tk.END, "Settings saved successfully\n")
                self.log_text.see(tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")
            self.log_text.insert(tk.END, f"Error saving settings: {str(e)}\n")
            self.log_text.see(tk.END)
    
    def add_extension(self):
        dialog = ExtensionDialog(self.root, "Add Extension")
        self.root.wait_window(dialog.top)
        
        if dialog.result:
            extension, model, prompt_file = dialog.result
            self.models_tree.insert("", tk.END, values=(extension, model, prompt_file))
    
    def edit_extension(self):
        selected = self.models_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an extension to edit.")
            return
        
        item = selected[0]
        values = self.models_tree.item(item, "values")
        extension, model, prompt_file = values
        
        dialog = ExtensionDialog(self.root, "Edit Extension", extension, model, prompt_file)
        self.root.wait_window(dialog.top)
        
        if dialog.result:
            new_extension, new_model, new_prompt_file = dialog.result
            self.models_tree.item(item, values=(new_extension, new_model, new_prompt_file))
    
    def remove_extension(self):
        selected = self.models_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an extension to remove.")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to remove this extension?"):
            self.models_tree.delete(selected[0])
    
    def save_models(self):
        try:
            # Update extension settings
            extension_settings = {}
            for child in self.models_tree.get_children():
                values = self.models_tree.item(child, "values")
                extension, model, prompt_file = values
                extension_settings[extension] = {
                    "model": model,
                    "prompt_file": prompt_file
                }
            
            self.config_data["extension_settings"] = extension_settings
            
            if self.save_config():
                messagebox.showinfo("Success", "Models saved successfully!")
                self.log_text.insert(tk.END, "Models saved successfully\n")
                self.log_text.see(tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save models: {str(e)}")
            self.log_text.insert(tk.END, f"Error saving models: {str(e)}\n")
            self.log_text.see(tk.END)
    
    def start_monitoring(self):
        try:
            # Save current settings
            self.config_data["monitored_directory"] = self.dir_var.get()
            self.config_data["delay"] = self.delay_var.get()
            self.config_data["monitor_subdirectories"] = self.sub_var.get()
            
            if not self.save_config():
                return
            
            # Create new settings object
            settings = Settings(self.config_path)
            
            # Create processor and monitor
            processor = FileProcessor(settings)
            self.monitor = FileMonitor(settings, processor)
            
            # Start monitoring in a separate thread
            self.monitor_thread = threading.Thread(target=self._run_monitor, daemon=True)
            self.monitor_thread.start()
            
            # Update UI
            self.is_monitoring = True
            self.start_button.configure(state="disabled")
            self.stop_button.configure(state="normal")
            self.status_var.set("Monitoring...")
            self.monitoring_dir_var.set(f"Monitoring directory: {settings.monitored_directory}")
            self.sub_info_var.set(f"Monitor subdirectories: {settings.monitor_subdirectories}")
            
            messagebox.showinfo("Success", "Monitoring started successfully!")
            self.log_text.insert(tk.END, f"Monitoring started: {settings.monitored_directory}\n")
            self.log_text.see(tk.END)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start monitoring: {str(e)}")
            self.log_text.insert(tk.END, f"Error starting monitoring: {str(e)}\n")
            self.log_text.see(tk.END)
    
    def _run_monitor(self):
        """Run the monitor in a separate thread"""
        try:
            # Create event handler
            from core.monitor import NewFileHandler
            event_handler = NewFileHandler(self.monitor.settings, self.monitor.processor)
            
            # Schedule the observer
            self.monitor.observer.schedule(
                event_handler, 
                self.monitor.settings.monitored_directory, 
                recursive=self.monitor.settings.monitor_subdirectories
            )
            
            # Start the observer
            self.monitor.observer.start()
            default_logger.info(f"Started monitoring directory: {self.monitor.settings.monitored_directory}")
            
            try:
                while self.is_monitoring:
                    time.sleep(1)
            except KeyboardInterrupt:
                self.monitor.stop()
        except Exception as e:
            default_logger.error(f"Error in monitor thread: {str(e)}")
            self.log_text.insert(tk.END, f"Error in monitor thread: {str(e)}\n")
            self.log_text.see(tk.END)
    
    def stop_monitoring(self):
        try:
            if self.monitor:
                self.monitor.stop()
            
            self.is_monitoring = False
            self.start_button.configure(state="normal")
            self.stop_button.configure(state="disabled")
            self.status_var.set("Not monitoring")
            
            messagebox.showinfo("Success", "Monitoring stopped successfully!")
            self.log_text.insert(tk.END, "Monitoring stopped\n")
            self.log_text.see(tk.END)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop monitoring: {str(e)}")
            self.log_text.insert(tk.END, f"Error stopping monitoring: {str(e)}\n")
            self.log_text.see(tk.END)
    
    def start_log_monitoring(self):
        """Start monitoring log file for updates"""
        self.log_monitor_thread = threading.Thread(target=self._monitor_logs, daemon=True)
        self.log_monitor_thread.start()
    
    def _monitor_logs(self):
        """Monitor log file for new entries"""
        log_file = "logs/newfiles.log"
        if not os.path.exists(log_file):
            return
        
        with open(log_file, 'r') as f:
            f.seek(0, 2)  # Go to end of file
            while True:
                line = f.readline()
                if line:
                    self.root.after(0, self.add_log_line, line.strip())
                else:
                    time.sleep(0.5)
    
    def add_log_line(self, line):
        """Add a log line to the text widget"""
        self.log_text.insert(tk.END, line + "\n")
        self.log_text.see(tk.END)
    
    def refresh_logs(self):
        """Refresh logs from file"""
        self.log_text.delete(1.0, tk.END)
        try:
            with open("logs/newfiles.log", 'r') as f:
                content = f.read()
                self.log_text.insert(tk.END, content)
            self.log_text.see(tk.END)
        except:
            self.log_text.insert(tk.END, "No logs found\n")
    
    def clear_logs(self):
        """Clear logs"""
        try:
            with open("logs/newfiles.log", 'w') as f:
                f.write("")
            self.refresh_logs()
        except:
            pass
    
    def on_closing(self):
        """Handle window closing"""
        if self.is_monitoring:
            if messagebox.askyesno("Confirm", "Monitoring is active. Do you want to stop monitoring and exit?"):
                self.stop_monitoring()
                self.root.destroy()
        else:
            self.root.destroy()
    
    def run(self):
        """Run the application"""
        self.root.mainloop()

class ExtensionDialog:
    def __init__(self, parent, title, extension="", model="", prompt_file=""):
        self.result = None
        
        self.top = ctk.CTkToplevel(parent)
        self.top.title(title)
        self.top.geometry("450x300")
        self.top.resizable(False, False)
        
        # Center the dialog
        self.top.transient(parent)
        self.top.grab_set()
        
        # Create widgets
        main_frame = ctk.CTkFrame(self.top)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Extension
        ext_label = ctk.CTkLabel(main_frame, text="Extension (without dot):")
        ext_label.grid(row=0, column=0, sticky="w", pady=5)
        self.extension_var = tk.StringVar(value=extension)
        ext_entry = ctk.CTkEntry(main_frame, textvariable=self.extension_var, width=200)
        ext_entry.grid(row=0, column=1, sticky="w", pady=5, padx=(10, 0))
        
        # Model
        model_label = ctk.CTkLabel(main_frame, text="Model:")
        model_label.grid(row=1, column=0, sticky="w", pady=5)
        self.model_var = tk.StringVar(value=model)
        model_entry = ctk.CTkEntry(main_frame, textvariable=self.model_var, width=200)
        model_entry.grid(row=1, column=1, sticky="w", pady=5, padx=(10, 0))
        
        # Prompt file
        prompt_label = ctk.CTkLabel(main_frame, text="Prompt File:")
        prompt_label.grid(row=2, column=0, sticky="w", pady=5)
        self.prompt_var = tk.StringVar(value=prompt_file)
        prompt_entry = ctk.CTkEntry(main_frame, textvariable=self.prompt_var, width=200)
        prompt_entry.grid(row=2, column=1, sticky="w", pady=5, padx=(10, 0))
        
        # Browse button for prompt file
        browse_button = ctk.CTkButton(main_frame, text="Browse...", command=self.browse_prompt_file, width=80)
        browse_button.grid(row=2, column=2, sticky="w", padx=(5, 0))
        
        # Model suggestions
        suggestions_label = ctk.CTkLabel(main_frame, text="Suggested Models:", font=ctk.CTkFont(size=11, weight="bold"))
        suggestions_label.grid(row=3, column=0, columnspan=3, sticky="w", pady=(10, 5))
        
        suggestions_text = ctk.CTkLabel(main_frame, 
                                      text="Text: gpt-4.1-nano, gpt-4.1-mini, gpt-4.1, gpt-4o-mini\n" +
                                           "Images: dall-e-3, dall-e-2", 
                                      font=ctk.CTkFont(size=10), text_color="gray")
        suggestions_text.grid(row=4, column=0, columnspan=3, sticky="w")
        
        # Buttons
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.grid(row=5, column=0, columnspan=3, pady=20)
        
        ok_button = ctk.CTkButton(button_frame, text="OK", command=self.ok, width=100)
        ok_button.pack(side="left", padx=5)
        cancel_button = ctk.CTkButton(button_frame, text="Cancel", command=self.cancel, width=100)
        cancel_button.pack(side="left", padx=5)
    
    def browse_prompt_file(self):
        filename = filedialog.askopenfilename(
            title="Select Prompt File",
            filetypes=[("Markdown files", "*.md"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            # Make path relative if possible
            try:
                rel_path = os.path.relpath(filename)
                self.prompt_var.set(rel_path)
            except:
                self.prompt_var.set(filename)
    
    def ok(self):
        extension = self.extension_var.get().strip()
        model = self.model_var.get().strip()
        prompt_file = self.prompt_var.get().strip()
        
        if not extension or not model or not prompt_file:
            messagebox.showwarning("Warning", "All fields are required.")
            return
        
        # Remove leading dot if present
        if extension.startswith('.'):
            extension = extension[1:]
        
        self.result = (extension, model, prompt_file)
        self.top.destroy()
    
    def cancel(self):
        self.top.destroy()

def main():
    """Main function"""
    # Ensure required directories exist
    os.makedirs("config", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    os.makedirs("prompts", exist_ok=True)
    
    # Create default prompt files if they don't exist
    default_text_prompt = """# Default Text Prompt

Generate helpful content for this file based on its name and extension.

File: {filename}
Extension: {extension}

Please provide relevant content that would be useful for this type of file."""
    
    default_image_prompt = """# Default Image Prompt

Create an image based on the filename: {filename}"""
    
    if not os.path.exists("prompts/default_text.md"):
        with open("prompts/default_text.md", "w") as f:
            f.write(default_text_prompt)
    
    if not os.path.exists("prompts/default_image.md"):
        with open("prompts/default_image.md", "w") as f:
            f.write(default_image_prompt)
    
    if not os.path.exists("prompts/image.md"):
        with open("prompts/image.md", "w") as f:
            f.write(default_image_prompt)
    
    app = NewfilesGUI()
    app.run()

if __name__ == "__main__":
    main()
