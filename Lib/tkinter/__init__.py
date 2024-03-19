import os
import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ResourceMonitorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Resource Monitor")
        
        self.selected_directory = ""
        self.file_data = {}
        
        self.create_widgets()
    
    def create_widgets(self):
        self.select_dir_button = tk.Button(self.master, text="Select Directory", command=self.select_directory)
        self.select_dir_button.pack(pady=10)
        
        self.plot_button = tk.Button(self.master, text="Plot Graphs", command=self.plot_graphs, state=tk.DISABLED)
        self.plot_button.pack(pady=5)
        
        self.canvas = None
    
    def select_directory(self):
        self.selected_directory = filedialog.askdirectory(title="Select Directory")
        if self.selected_directory:
            self.read_files()
            self.plot_button.config(state=tk.NORMAL)
    
    def read_files(self):
        self.file_data = {}
        for filename in os.listdir(self.selected_directory):
            if filename.endswith(".txt"):
                filepath = os.path.join(self.selected_directory, filename)
                with open(filepath, "r") as file:
                    data = file.readlines()
                    self.file_data[filename] = data
    
    def plot_graphs(self):
        for filename, data in self.file_data.items():
            time_points = []
            cpu_usage = []
            internet_status = []
            for line in data:
                # Predpostavimo, da podatki v datoteki izgledajo nekako tako: "Čas CPU% Internet"
                parts = line.strip().split()
                time_points.append(parts[0])
                cpu_usage.append(float(parts[1]))
                internet_status.append(parts[2])
            
            plt.figure(figsize=(8, 6))
            plt.plot(time_points, cpu_usage, marker='o', linestyle='-')
            plt.title(f"CPU Usage Over Time ({filename})")
            plt.xlabel("Time")
            plt.ylabel("CPU Usage (%)")
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            for i, status in enumerate(internet_status):
                if status == "Disconnected":
                    plt.axvline(x=time_points[i], color='r', linestyle='--', linewidth=0.5)
            
            canvas = FigureCanvasTkAgg(plt.gcf(), master=self.master)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            if self.canvas:
                self.canvas.get_tk_widget().pack_forget()
            self.canvas = canvas

def main():
    root = tk.Tk()
    app = ResourceMonitorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
