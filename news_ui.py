import tkinter as tk
from tkinter import ttk
import pandas as pd

# Load the news data from CSV
df = pd.read_csv("news_output.csv")

# Create the main application window
root = tk.Tk()
root.title("🗞️ News Headlines Viewer")
root.geometry("900x500")

# Create a Treeview to display the news
tree = ttk.Treeview(root, columns=("Title", "Date", "Summary", "Keywords"), show="headings")
tree.heading("Title", text="📰 Title")
tree.heading("Date", text="🕒 Published Date")
tree.heading("Summary", text="📄 Summary")
tree.heading("Keywords", text="🔍 Top Keywords")

# Set column widths
tree.column("Title", width=250)
tree.column("Date", width=120)
tree.column("Summary", width=350)
tree.column("Keywords", width=150)

# Add data from DataFrame to Treeview
for index, row in df.iterrows():
    tree.insert("", tk.END, values=(row["Title"], row["Published Date"], row["Summary (Shortened)"], row["Top 5 Keywords"]))

tree.pack(fill=tk.BOTH, expand=True)

# Run the application
root.mainloop()
