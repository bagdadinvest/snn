import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import subprocess

class ScraperConfig:
    def __init__(self, root):
        self.root = root
        self.root.title("Scraper Configuration")

        # URL
        tk.Label(root, text="URL:").grid(row=0, column=0, padx=10, pady=5)
        self.url_entry = tk.Entry(root, width=50)
        self.url_entry.grid(row=0, column=1, padx=10, pady=5)

        # Max Items
        tk.Label(root, text="Max Items:").grid(row=1, column=0, padx=10, pady=5)
        self.max_items_entry = tk.Entry(root, width=50)
        self.max_items_entry.grid(row=1, column=1, padx=10, pady=5)
        self.max_items_entry.insert(0, "100")

        # Price Range
        tk.Label(root, text="Price Range (min-max):").grid(row=2, column=0, padx=10, pady=5)
        self.price_range_entry = tk.Entry(root, width=50)
        self.price_range_entry.grid(row=2, column=1, padx=10, pady=5)

        # Categories
        tk.Label(root, text="Categories (comma-separated):").grid(row=3, column=0, padx=10, pady=5)
        self.category_entry = tk.Entry(root, width=50)
        self.category_entry.grid(row=3, column=1, padx=10, pady=5)

        # Preview Option
        tk.Label(root, text="Preview Option:").grid(row=4, column=0, padx=10, pady=5)
        self.preview_var = tk.StringVar(value="tabular")
        tk.Radiobutton(root, text="Tabular", variable=self.preview_var, value="tabular").grid(row=4, column=1, padx=10, pady=5, sticky='w')
        tk.Radiobutton(root, text="HTML", variable=self.preview_var, value="html").grid(row=4, column=1, padx=10, pady=5)

        # Driver Path
        tk.Label(root, text="ChromeDriver Path:").grid(row=5, column=0, padx=10, pady=5)
        self.driver_path_entry = tk.Entry(root, width=50)
        self.driver_path_entry.grid(row=5, column=1, padx=10, pady=5)
        tk.Button(root, text="Browse", command=self.browse_driver_path).grid(row=5, column=2, padx=10, pady=5)

        # Headless Option
        self.headless_var = tk.BooleanVar()
        tk.Checkbutton(root, text="Headless", variable=self.headless_var).grid(row=6, column=1, padx=10, pady=5)

        # Submit Button
        tk.Button(root, text="Run Scraper", command=self.run_scraper).grid(row=7, column=1, padx=10, pady=10)

    def browse_driver_path(self):
        filename = filedialog.askopenfilename(filetypes=[("Executable Files", "*.exe")])
        if filename:
            self.driver_path_entry.delete(0, tk.END)
            self.driver_path_entry.insert(0, filename)

    def run_scraper(self):
        url = self.url_entry.get()
        max_items = self.max_items_entry.get()
        price_range = self.price_range_entry.get()
        category = self.category_entry.get()
        preview = self.preview_var.get()
        driver_path = self.driver_path_entry.get()
        headless = self.headless_var.get()

        if not url or not driver_path:
            messagebox.showerror("Error", "URL and ChromeDriver Path are required.")
            return
        
        command = [
            'python', 'scrape_products.py',
            url,
            '--max_items', max_items,
            '--price_range', price_range,
            '--category', category,
            '--preview', preview,
            '--driver_path', driver_path
        ]
        
        if headless:
            command.append('--headless')

        subprocess.run(command)

if __name__ == "__main__":
    root = tk.Tk()
    app = ScraperConfig(root)
    root.mainloop()
