#!/usr/bin/env python3

import tkinter as tk
import subprocess
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from tkinter import filedialog, messagebox

# Create the main window
root = tk.Tk()
root.title("IoT Security Analysis")

# Set the size of the window
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = screen_width // 2
window_height = screen_height // 2
root.geometry(f"{window_width}x{window_height}")

# Create a frame for the buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=50)

# Function to run the network scan shell script
def run_network_scan():
    try: 
        subprocess.run(["./network_scan.sh"], check=True)
        with open("netscan_result.txt", "r") as file:
            result = file.read()
        
        display_result_window(result, "Network Scan")

    except subprocess.CalledProcessError as e:
        message_label.config(text=f"Error: {e.stderr.strip()}")

# Function to run the port and version scan script
def run_pv_scan():
    try: 
        subprocess.run(["python3", "pvscan.py"], check=True)
        with open("pvscan_results.txt", "r") as file:
            result = file.read()
        
        display_result_window(result, "Port/Version Scan")

    except subprocess.CalledProcessError as e:
        message_label.config(text=f"Error: {e.stderr.strip()}")

# Function to save the results as a PDF report
def save_report(result, btname):
    # Open a file dialog to save the file as PDF
    file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")],
            title=f"Save {btname} Report"
    )
    if file_path:
        # Create a PDF document using ReportLab
        pdf = canvas.Canvas(file_path, pagesize=letter)
        pdf.setTitle(f"{btname} Report")

        # Set initial cursor position and line height
        width, height = letter
        cursor_y = height - 40
        line_height =12

        # Add title
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(40, cursor_y, f"{btname} Report")
        cursor_y -= 30

        # Add the result content
        pdf.setFont("Helvetica", 10)
        for line in result.splitlines():
            if cursor_y < 40:
                pdf.showpage()
                pdf.setFont("Helvetica", 10)
                cursor_y = height - 40
            pdf.drawString(40, cursor_y, line)
            cursor_y -= line_height

        # Save and close the PDF
        pdf.save()
        messagebox.showinfo("Save Report", f"{btname} report saved successfully as PDF!")
        
# Function to display result in a new window
def display_result_window(result, btname):
    result_window = tk.Toplevel(root) 
    result_window.title(f"{btname} Results")
    
    # Create a Text widget to display results
    text_widget = tk.Text(result_window, wrap=tk.NONE)
    text_widget.insert(tk.END, result)
    text_widget.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Create a scroll bar for the Text widget
    scrollbar = tk.Scrollbar(result_window, command=text_widget.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    text_widget.config(yscrollcommand=scrollbar.set)

    # Create a frame for the "Save Report" and "Close" buttons
    button_frame = tk.Frame(result_window)
    button_frame.pack(pady=(10,10))

    # Create a button to save the result as a report
    save_button = tk.Button(button_frame, text="Save Report", command=lambda: save_report(result, btname))
    save_button.pack(side=tk.LEFT, padx=(0,5))

    # Create a button to close the results window
    close_button = tk.Button(result_window, text="Close", command=result_window.destroy)
    close_button.pack(side=tk.RIGHT)

# Function for each button
def on_button_click(btname):
    if btname == "Network Scan":
        run_network_scan()
    elif btname == "Port/Version Scan":
        run_pv_scan()
    else:
         message_label.config(text=f"{btname} clicked!")

# Create buttons
buttons = [
        "Network Scan", 
        "Port/Version Scan",
        "Vulnerability Scan",
        "Network Traffic Analysis"
]

for button_name in buttons:

    button = tk.Button(button_frame, text=button_name, command=lambda name=button_name: on_button_click(name))
    button.pack(side=tk.TOP, pady=5)

root.mainloop()

