import ctypes
from ctypes import wintypes
import tkinter as tk
from tkinter import ttk, messagebox

# Windows API Constants
EnumWindows = ctypes.windll.user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)
GetWindowText = ctypes.windll.user32.GetWindowTextW
GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
IsWindowVisible = ctypes.windll.user32.IsWindowVisible
SetWindowText = ctypes.windll.user32.SetWindowTextW

def get_window_title(hwnd):
    length = GetWindowTextLength(hwnd)
    if length > 0:
        buff = ctypes.create_unicode_buffer(length + 1)
        GetWindowText(hwnd, buff, length + 1)
        return buff.value
    return ""

def list_windows(query=None):
    windows = []
    
    def foreach_window(hwnd, lParam):
        if IsWindowVisible(hwnd):
            title = get_window_title(hwnd)
            if title:
                if query:
                    if query.lower() in title.lower():
                        windows.append((hwnd, title))
                else:
                    windows.append((hwnd, title))
        return True
    
    EnumWindows(EnumWindowsProc(foreach_window), 0)
    # Sort by title for easier reading
    windows.sort(key=lambda x: x[1].lower())
    return windows

class WindowRenamerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Window Title Changer")
        self.root.geometry("600x500")
        
        # Store original titles: {hwnd: "Original Title"}
        self.original_titles = {}
        
        self.setup_styles()
        self.create_widgets()
        
        # Initial Load
        self.windows_cache = []
        self.refresh_list()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam') # 'clam' is usually a good base for custom styling
        
        # Colors
        bg_color = "#2b2b2b"
        fg_color = "#ffffff"
        entry_bg = "#3c3f41"
        select_bg = "#4b6eaf"
        
        self.root.configure(bg=bg_color)
        
        style.configure(".", background=bg_color, foreground=fg_color, font=("Segoe UI", 10))
        style.configure("TLabel", background=bg_color, foreground=fg_color)
        style.configure("TButton", padding=6, relief="flat", background="#3c3f41")
        style.map("TButton", background=[("active", "#4c5052")])
        
        style.configure("Treeview", 
                        background=entry_bg, 
                        foreground=fg_color, 
                        fieldbackground=entry_bg,
                        rowheight=25,
                        font=("Segoe UI", 10))
        style.map("Treeview", background=[("selected", select_bg)])
        
        style.configure("Treeview.Heading", background="#333333", foreground=fg_color, font=("Segoe UI", 10, "bold"))
        
        style.configure("TLabelframe", background=bg_color, foreground=fg_color)
        style.configure("TLabelframe.Label", background=bg_color, foreground=fg_color)

    def create_widgets(self):
        # --- Search Frame ---
        search_frame = ttk.Frame(self.root, padding="15")
        search_frame.pack(fill=tk.X)
        
        ttk.Label(search_frame, text="🔍 Search:").pack(side=tk.LEFT, padx=(0, 5))
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.on_search_change)
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, font=("Segoe UI", 10))
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        ttk.Button(search_frame, text="🔄 Refresh", command=self.refresh_list).pack(side=tk.RIGHT)
        
        # --- List Frame ---
        list_frame = ttk.Frame(self.root, padding="15")
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview
        self.tree = ttk.Treeview(list_frame, columns=("HWND", "Title"), show="headings", yscrollcommand=scrollbar.set)
        self.tree.heading("HWND", text="ID")
        self.tree.heading("Title", text="Window Title")
        self.tree.column("HWND", width=80, stretch=False)
        self.tree.column("Title", width=400)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=self.tree.yview)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        
        # --- Action Frame ---
        action_frame = ttk.LabelFrame(self.root, text="Actions", padding="15")
        action_frame.pack(fill=tk.X, padx=15, pady=15)
        
        # Grid layout for actions
        ttk.Label(action_frame, text="New Title:").grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.new_title_var = tk.StringVar()
        self.new_title_entry = ttk.Entry(action_frame, textvariable=self.new_title_var, font=("Segoe UI", 10))
        self.new_title_entry.grid(row=0, column=1, padx=10, sticky=tk.EW, pady=5)
        
        btn_frame = ttk.Frame(action_frame)
        btn_frame.grid(row=0, column=2, padx=5, pady=5)
        
        self.rename_btn = ttk.Button(btn_frame, text="✏️ Rename", command=self.rename_window, state=tk.DISABLED)
        self.rename_btn.pack(side=tk.LEFT, padx=5)
        
        self.restore_btn = ttk.Button(btn_frame, text="↩️ Restore Original", command=self.restore_window, state=tk.DISABLED)
        self.restore_btn.pack(side=tk.LEFT, padx=5)
        
        action_frame.columnconfigure(1, weight=1)

    def refresh_list(self):
        # Clear current items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        self.windows_cache = list_windows()
        self.filter_list()
        
    def filter_list(self):
        query = self.search_var.get().lower()
        
        # Clear current items first
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        for hwnd, title in self.windows_cache:
            if query in title.lower():
                self.tree.insert("", tk.END, values=(hwnd, title))

    def on_search_change(self, *args):
        self.filter_list()

    def on_select(self, event):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            hwnd, title = item['values']
            self.new_title_var.set(title)
            self.rename_btn.config(state=tk.NORMAL)
            
            # Check if we have an original title saved for this HWND
            if hwnd in self.original_titles:
                 self.restore_btn.config(state=tk.NORMAL)
            else:
                 self.restore_btn.config(state=tk.DISABLED)
        else:
            self.new_title_var.set("")
            self.rename_btn.config(state=tk.DISABLED)
            self.restore_btn.config(state=tk.DISABLED)

    def rename_window(self):
        selected = self.tree.selection()
        if not selected: return
        
        item = self.tree.item(selected[0])
        hwnd = item['values'][0] # HWND is already int from treeview insert? No, treeview stores strings mostly, but let's check.
        # Actually in previous fix we saw it was passed as int to SetWindowText.
        # Treeview values are usually strings.
        hwnd = int(hwnd)
        
        current_title = item['values'][1]
        new_title = self.new_title_var.get().strip()
        
        if not new_title:
            messagebox.showwarning("Warning", "Title cannot be empty!")
            return
            
        # Save original title if not already saved
        if hwnd not in self.original_titles:
            self.original_titles[hwnd] = current_title
            
        try:
            result = SetWindowText(hwnd, new_title)
            if result:
                # Update list
                self.refresh_list()
                # Re-select logic could go here, but refresh clears selection.
                # Let's just clear input
                self.new_title_var.set("")
                messagebox.showinfo("Success", f"Renamed to: {new_title}")
            else:
                messagebox.showerror("Error", "Failed to rename window.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def restore_window(self):
        selected = self.tree.selection()
        if not selected: return
        
        item = self.tree.item(selected[0])
        hwnd = int(item['values'][0])
        
        if hwnd in self.original_titles:
            original = self.original_titles[hwnd]
            try:
                result = SetWindowText(hwnd, original)
                if result:
                    self.refresh_list()
                    messagebox.showinfo("Success", f"Restored to: {original}")
                    # Remove from dict? No, keep it in case they want to restore again later after another rename.
                else:
                    messagebox.showerror("Error", "Failed to restore window.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = WindowRenamerApp(root)
    root.mainloop()
