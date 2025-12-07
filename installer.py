import ctypes
import sys
import os
import subprocess
import tkinter as tk
from tkinter import messagebox

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{os.path.abspath(__file__)}"', None, 1)
    sys.exit(0)

class Installer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Claudifi Installer")
        self.root.geometry("500x450")
        self.root.resizable(False, False)
        self.root.configure(bg="white")
        
        try:
            self.root.iconbitmap(default='')
        except:
            pass
        
        self.cmd_name = tk.StringVar(value="claudify")
        self.custom_name = tk.StringVar()
        self.api_key = tk.StringVar()
        self.show_key = tk.BooleanVar(value=False)
        self.final_name = "claudify"
        
        self.header = tk.Frame(self.root, bg="#0078d4", height=60)
        self.header.pack(fill="x")
        self.header.pack_propagate(False)
        
        self.header_label = tk.Label(self.header, text="Claudify Installer", 
                                     font=("Segoe UI", 14, "bold"), bg="#0078d4", fg="white")
        self.header_label.pack(pady=15)
        
        self.content = tk.Frame(self.root, bg="white")
        self.content.pack(fill="both", expand=True, padx=30, pady=20)
        
        self.footer = tk.Frame(self.root, bg="#f5f5f5", height=50)
        self.footer.pack(fill="x", side="bottom")
        self.footer.pack_propagate(False)
        
        self.show_page1()
    
    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        for widget in self.footer.winfo_children():
            widget.destroy()
    
    def create_button(self, parent, text, command, primary=False):
        bg = "#0078d4" if primary else "#e1e1e1"
        fg = "white" if primary else "black"
        btn = tk.Button(parent, text=text, command=command, font=("Segoe UI", 10),
                       bg=bg, fg=fg, relief="flat", width=12, height=1, cursor="hand2",
                       activebackground="#005a9e" if primary else "#c1c1c1",
                       activeforeground="white" if primary else "black")
        return btn
    
    def show_page1(self):
        self.clear_content()
        self.header_label.config(text="Claudify Installer")
        
        tk.Label(self.content, text="Select command name", 
                font=("Segoe UI", 12, "bold"), bg="white", anchor="w").pack(fill="x", pady=(0, 5))
        tk.Label(self.content, text="Choose how you want to launch Claude Code:", 
                font=("Segoe UI", 9), bg="white", fg="#666", anchor="w").pack(fill="x", pady=(0, 15))
        
        columns_frame = tk.Frame(self.content, bg="white")
        columns_frame.pack(fill="x")
        
        left_col = tk.Frame(columns_frame, bg="white")
        left_col.pack(side="left", anchor="n")
        
        right_col = tk.Frame(columns_frame, bg="white")
        right_col.pack(side="left", anchor="n", padx=(40, 0))
        
        left_options = ["cude", "claudify", "claudee", "claode"]
        right_options = ["ccode", "cclaude", "cllaude"]
        
        for opt in left_options:
            rb = tk.Radiobutton(left_col, text=opt, variable=self.cmd_name, value=opt,
                               font=("Segoe UI", 10), bg="white", activebackground="white",
                               selectcolor="white", command=self.on_option_change, cursor="hand2")
            rb.pack(anchor="w", pady=2)
        
        for opt in right_options:
            rb = tk.Radiobutton(right_col, text=opt, variable=self.cmd_name, value=opt,
                               font=("Segoe UI", 10), bg="white", activebackground="white",
                               selectcolor="white", command=self.on_option_change, cursor="hand2")
            rb.pack(anchor="w", pady=2)
        
        custom_frame = tk.Frame(right_col, bg="white")
        custom_frame.pack(anchor="w", pady=2)
        
        rb_custom = tk.Radiobutton(custom_frame, text="Custom:", variable=self.cmd_name, value="custom",
                                   font=("Segoe UI", 10), bg="white", activebackground="white",
                                   selectcolor="white", command=self.on_option_change, cursor="hand2")
        rb_custom.pack(side="left")
        
        self.custom_entry = tk.Entry(custom_frame, textvariable=self.custom_name, 
                                     font=("Segoe UI", 10), width=15, state="disabled",
                                     relief="solid", bd=1)
        self.custom_entry.pack(side="left", padx=5)
        
        sep = tk.Frame(self.footer, bg="#ddd", height=1)
        sep.pack(fill="x", side="top")
        
        btn_container = tk.Frame(self.footer, bg="#f5f5f5")
        btn_container.pack(fill="x", pady=12, padx=20)
        
        self.create_button(btn_container, "Cancel", self.root.destroy).pack(side="right", padx=(10, 0))
        self.create_button(btn_container, "Next →", self.go_page2, primary=True).pack(side="right")
    
    def on_option_change(self):
        if self.cmd_name.get() == "custom":
            self.custom_entry.config(state="normal")
            self.custom_entry.focus()
        else:
            self.custom_entry.config(state="disabled")
    
    def go_page2(self):
        name = self.cmd_name.get()
        if name == "custom":
            name = self.custom_name.get().strip()
            if not name:
                messagebox.showerror("Error", "Please enter a custom command name.")
                return
        
        if name.lower() == "claude":
            messagebox.showerror("Error", "Command name cannot be 'claude'. Please choose another name.")
            return
        
        self.final_name = name
        self.show_page2()
    
    def show_page2(self):
        self.clear_content()
        self.header_label.config(text="API Configuration")
        
        tk.Label(self.content, text="Enter your API Key", 
                font=("Segoe UI", 12, "bold"), bg="white", anchor="w").pack(fill="x", pady=(0, 5))
        tk.Label(self.content, text="Get your API key from the Claudifi panel:", 
                font=("Segoe UI", 9), bg="white", fg="#666", anchor="w").pack(fill="x", pady=(0, 20))
        
        tk.Label(self.content, text="API Key:", font=("Segoe UI", 10), bg="white", anchor="w").pack(fill="x", pady=(0, 5))
        
        self.key_entry = tk.Entry(self.content, textvariable=self.api_key, 
                                  font=("Consolas", 10), show="•", relief="solid", bd=1)
        self.key_entry.pack(fill="x", pady=(0, 10), ipady=8)
        
        show_frame = tk.Frame(self.content, bg="white")
        show_frame.pack(fill="x")
        
        cb = tk.Checkbutton(show_frame, text="Show API key", variable=self.show_key,
                           font=("Segoe UI", 9), bg="white", activebackground="white",
                           command=self.toggle_key, cursor="hand2")
        cb.pack(anchor="w")
        
        sep = tk.Frame(self.footer, bg="#ddd", height=1)
        sep.pack(fill="x", side="top")
        
        btn_container = tk.Frame(self.footer, bg="#f5f5f5")
        btn_container.pack(fill="x", pady=12, padx=20)
        
        self.create_button(btn_container, "Install", self.do_install, primary=True).pack(side="right", padx=(10, 0))
        self.create_button(btn_container, "← Back", self.show_page1).pack(side="right")
    
    def toggle_key(self):
        self.key_entry.config(show="" if self.show_key.get() else "•")
    
    def do_install(self):
        api_key = self.api_key.get().strip()
        if not api_key:
            messagebox.showerror("Error", "Please enter your API key.")
            return
        
        try:
            scripts_dir = "C:\\scripts"
            if not os.path.exists(scripts_dir):
                os.makedirs(scripts_dir)
            
            bat_content = f'''@echo off

set ANTHROPIC_BASE_URL=https://claudecode.epsiloncode.pl/api/
set ANTHROPIC_AUTH_TOKEN={api_key}
set ANTHROPIC_API_KEY={api_key}

set CURRENT_DIR=%CD%

echo ========================================
echo     Claude Code - Claudify.dev 
echo ========================================
echo Current dir: %CURRENT_DIR%
echo.

claude

pause
'''
            
            bat_path = os.path.join(scripts_dir, f"{self.final_name}.bat")
            with open(bat_path, 'w') as f:
                f.write(bat_content)
            
            result = subprocess.run(
                ['powershell', '-Command', '[Environment]::GetEnvironmentVariable("Path", "Machine")'],
                capture_output=True, text=True
            )
            current_path = result.stdout.strip()
            
            if scripts_dir.lower() not in current_path.lower():
                new_path = current_path + ";" + scripts_dir if current_path else scripts_dir
                subprocess.run([
                    'powershell', '-Command',
                    f'[Environment]::SetEnvironmentVariable("Path", "{new_path}", "Machine")'
                ], check=True)
            
            self.show_page3()
            
        except Exception as e:
            messagebox.showerror("Error", f"Installation failed:\n{str(e)}")
    
    def show_page3(self):
        self.clear_content()
        self.header_label.config(text="Installation Complete")
        
        success_frame = tk.Frame(self.content, bg="white")
        success_frame.pack(expand=True)
        
        tk.Label(success_frame, text="✓", font=("Segoe UI", 60), fg="#0078d4", bg="white").pack(pady=(20, 10))
        tk.Label(success_frame, text="Installation Successful!", 
                font=("Segoe UI", 14, "bold"), bg="white").pack(pady=(0, 20))
        
        info_frame = tk.Frame(success_frame, bg="#f0f7ff", relief="solid", bd=1)
        info_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(info_frame, text=f"Command '{self.final_name}' is now available.", 
                font=("Segoe UI", 10), bg="#f0f7ff", pady=10).pack()
        tk.Label(info_frame, text="Open a new terminal and type:", 
                font=("Segoe UI", 9), bg="#f0f7ff", fg="#666").pack()
        tk.Label(info_frame, text=self.final_name, font=("Consolas", 14, "bold"), 
                bg="#f0f7ff", fg="#0078d4", pady=10).pack()
        
        sep = tk.Frame(self.footer, bg="#ddd", height=1)
        sep.pack(fill="x", side="top")
        
        btn_container = tk.Frame(self.footer, bg="#f5f5f5")
        btn_container.pack(fill="x", pady=12, padx=20)
        
        self.create_button(btn_container, "Finish", self.root.destroy, primary=True).pack(side="right")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = Installer()
    app.run()
