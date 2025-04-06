import tkinter as tk
from tkinter import ttk
import pandas as pd


df = pd.read_csv("news_output.csv")


root = tk.Tk()
root.title("🗞️ News Headlines Viewer")
root.geometry("900x500")


tree = ttk.Treeview(root, columns=("Title", "Date", "Summary", "Keywords"), show="headings")
tree.heading("Title", text="📰 Title")
tree.heading("Date", text="🕒 Published Date")
tree.heading("Summary", text="📄 Summary")
tree.heading("Keywords", text="🔍 Top Keywords")


tree.column("Title", width=250)
tree.column("Date", width=120)
tree.column("Summary", width=350)
tree.column("Keywords", width=150)


for index, row in df.iterrows():
    tree.insert("", tk.END, values=(row["Title"], row["Published Date"], row["Summary (Shortened)"], row["Top 5 Keywords"]))

tree.pack(fill=tk.BOTH, expand=True)


root.mainloop()