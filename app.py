import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime

# Art prices
ART_PRICES = {
    "Pencil Art": {"A4": 600, "A3": 1000},
    "Color Pencil Art": {"A4": 1000, "A3": 1800},
    "Other Art": {"A4": 0, "A3": 0}
}

FRAME_PRICES = {
    "A4": 300,
    "A3": 400
}


def get_prices(show_errors=True):
    size = size_var.get()
    art_type = art_var.get()

    # Art price
    if art_type == "Other Art":
        try:
            art_price = float(other_price_entry.get())
            if art_price < 0:
                raise ValueError
        except ValueError:
            if show_errors:
                messagebox.showerror(
                    "Invalid Price",
                    "Enter a valid Other Art price."
                )
            return None
    else:
        art_price = ART_PRICES[art_type][size]

    # Frame price
    frame_price = (
        FRAME_PRICES[size]
        if frame_var.get() == "With Frame"
        else 0
    )

    # Print price
    if print_var.get() == "Yes":
        try:
            print_price = float(print_price_entry.get())
            if print_price < 0:
                raise ValueError
        except ValueError:
            if show_errors:
                messagebox.showerror(
                    "Invalid Price",
                    "Enter a valid print price."
                )
            return None
    else:
        print_price = 0

    total = art_price + frame_price + print_price

    return art_price, frame_price, print_price, total


def calculate_total():
    prices = get_prices()

    if prices is None:
        return

    art_price, frame_price, print_price, total = prices

    art_amount_label.config(text=f"₹{art_price:,.2f}")
    frame_amount_label.config(text=f"₹{frame_price:,.2f}")
    print_amount_label.config(text=f"₹{print_price:,.2f}")
    total_label.config(text=f"₹{total:,.2f}")


def update_options(*args):
    # Keep optional fields in their correct positions
    if art_var.get() == "Other Art":
        other_price_frame.grid()
    else:
        other_price_frame.grid_remove()

    if print_var.get() == "Yes":
        print_price_frame.grid()
    else:
        print_price_frame.grid_remove()

    calculate_total()


def reset_form():
    customer_entry.delete(0, tk.END)
    size_var.set("A4")
    art_var.set("Pencil Art")
    frame_var.set("Without Frame")
    print_var.set("No")
    other_price_entry.delete(0, tk.END)
    print_price_entry.delete(0, tk.END)

    update_options()


def save_quote():
    customer = customer_entry.get().strip()

    if not customer:
        messagebox.showwarning(
            "Customer Name",
            "Please enter the customer name first."
        )
        customer_entry.focus_set()
        return

    prices = get_prices()

    if prices is None:
        return

    art_price, frame_price, print_price, total = prices

    quote = f"""
========================================
              PR ARTTZ
          ART PRICE QUOTATION
========================================

Customer Name : {customer}
Date          : {datetime.now().strftime("%d-%m-%Y %I:%M %p")}

Art Size      : {size_var.get()}
Art Type      : {art_var.get()}
Frame Option  : {frame_var.get()}
Print Required: {print_var.get()}

----------------------------------------
Art Price     : Rs. {art_price:,.2f}
Frame Charge  : Rs. {frame_price:,.2f}
Print Charge  : Rs. {print_price:,.2f}
----------------------------------------
TOTAL AMOUNT  : Rs. {total:,.2f}
========================================

Thank you for choosing PR Arttz!
"""

    filename = filedialog.asksaveasfilename(
        title="Save Art Quotation",
        defaultextension=".txt",
        initialfile=f"{customer.replace(' ', '_')}_quotation.txt",
        filetypes=[("Text Files", "*.txt")]
    )

    if not filename:
        return

    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(quote)

        messagebox.showinfo(
            "Success",
            f"Quotation saved successfully!\n\n{filename}"
        )
    except OSError as error:
        messagebox.showerror(
            "Save Error",
            f"Could not save quotation.\n{error}"
        )


# Main window
root = tk.Tk()
root.title("pr_arttz - Art Price Calculator")
root.geometry("600x850")
root.minsize(520, 750)
root.configure(bg="#fff0f5")

# Theme
style = ttk.Style()
style.theme_use("clam")

style.configure(
    "TCombobox",
    padding=6,
    font=("Arial", 10)
)

# Header
header = tk.Frame(root, bg="#c2185b", pady=15)
header.pack(fill="x")

tk.Label(
    header,
    text="PR ARTTZ",
    font=("Arial", 25, "bold"),
    bg="#c2185b",
    fg="white"
).pack()

tk.Label(
    header,
    text="Art Price Calculator",
    font=("Arial", 12),
    bg="#c2185b",
    fg="white"
).pack()

# Main content
content = tk.Frame(root, bg="#fff0f5", padx=25, pady=12)
content.pack(fill="both", expand=True)

content.columnconfigure(0, weight=1)


def add_label(text, row):
    tk.Label(
        content,
        text=text,
        font=("Arial", 10, "bold"),
        bg="#fff0f5",
        fg="#702044"
    ).grid(
        row=row,
        column=0,
        sticky="w",
        pady=(6, 2)
    )


# Customer name
add_label("Customer Name", 0)

customer_entry = tk.Entry(
    content,
    font=("Arial", 11),
    relief="solid",
    bd=1
)
customer_entry.grid(row=1, column=0, sticky="ew", ipady=5)

# Art size
add_label("Select Art Size", 2)

size_var = tk.StringVar(value="A4")

size_box = ttk.Combobox(
    content,
    textvariable=size_var,
    values=["A4", "A3"],
    state="readonly"
)
size_box.grid(row=3, column=0, sticky="ew")

# Art type
add_label("Select Art Type", 4)

art_var = tk.StringVar(value="Pencil Art")

art_box = ttk.Combobox(
    content,
    textvariable=art_var,
    values=["Pencil Art", "Color Pencil Art", "Other Art"],
    state="readonly"
)
art_box.grid(row=5, column=0, sticky="ew")

# Other art price
other_price_frame = tk.Frame(content, bg="#fff0f5")
other_price_frame.grid(row=6, column=0, sticky="ew", pady=4)
other_price_frame.columnconfigure(0, weight=1)

tk.Label(
    other_price_frame,
    text="Other Art Price (₹)",
    bg="#fff0f5",
    fg="#702044"
).grid(row=0, column=0, sticky="w")

other_price_entry = tk.Entry(other_price_frame, font=("Arial", 10))
other_price_entry.grid(row=1, column=0, sticky="ew", ipady=4)

# Frame
add_label("Frame Option", 7)

frame_var = tk.StringVar(value="Without Frame")

frame_box = ttk.Combobox(
    content,
    textvariable=frame_var,
    values=["Without Frame", "With Frame"],
    state="readonly"
)
frame_box.grid(row=8, column=0, sticky="ew")

# Print option
add_label("Print Required?", 9)

print_var = tk.StringVar(value="No")

print_box = ttk.Combobox(
    content,
    textvariable=print_var,
    values=["No", "Yes"],
    state="readonly"
)
print_box.grid(row=10, column=0, sticky="ew")

# Print price
print_price_frame = tk.Frame(content, bg="#fff0f5")
print_price_frame.grid(row=11, column=0, sticky="ew", pady=4)
print_price_frame.columnconfigure(0, weight=1)

tk.Label(
    print_price_frame,
    text="Print Price (₹)",
    bg="#fff0f5",
    fg="#702044"
).grid(row=0, column=0, sticky="w")

print_price_entry = tk.Entry(print_price_frame, font=("Arial", 10))
print_price_entry.grid(row=1, column=0, sticky="ew", ipady=4)

# Price summary
summary = tk.LabelFrame(
    content,
    text="Price Summary",
    font=("Arial", 11, "bold"),
    bg="white",
    fg="#c2185b",
    padx=12,
    pady=8
)
summary.grid(row=12, column=0, sticky="ew", pady=10)
summary.columnconfigure(0, weight=1)


def summary_row(text, row):
    tk.Label(
        summary,
        text=text,
        font=("Arial", 10),
        bg="white"
    ).grid(row=row, column=0, sticky="w", pady=3)

    amount = tk.Label(
        summary,
        text="₹0.00",
        font=("Arial", 10, "bold"),
        bg="white"
    )
    amount.grid(row=row, column=1, sticky="e", pady=3)

    return amount


art_amount_label = summary_row("Art Price", 0)
frame_amount_label = summary_row("Frame Charge", 1)
print_amount_label = summary_row("Print Charge", 2)

tk.Label(
    summary,
    text="TOTAL AMOUNT",
    font=("Arial", 13, "bold"),
    bg="white",
    fg="#c2185b"
).grid(row=3, column=0, sticky="w", pady=(8, 2))

total_label = tk.Label(
    summary,
    text="₹600.00",
    font=("Arial", 15, "bold"),
    bg="white",
    fg="#c2185b"
)
total_label.grid(row=3, column=1, sticky="e", pady=(8, 2))

# Buttons
buttons = tk.Frame(content, bg="#fff0f5")
buttons.grid(row=13, column=0, sticky="ew", pady=5)
buttons.columnconfigure((0, 1), weight=1)

tk.Button(
    buttons,
    text="Calculate Total",
    command=calculate_total,
    bg="#c2185b",
    fg="white",
    font=("Arial", 10, "bold"),
    relief="flat",
    padx=8,
    pady=9,
    cursor="hand2"
).grid(row=0, column=0, sticky="ew", padx=(0, 5))

tk.Button(
    buttons,
    text="Save Quote",
    command=save_quote,
    bg="#7b1fa2",
    fg="white",
    font=("Arial", 10, "bold"),
    relief="flat",
    padx=8,
    pady=9,
    cursor="hand2"
).grid(row=0, column=1, sticky="ew", padx=(5, 0))

tk.Button(
    content,
    text="Reset",
    command=reset_form,
    bg="#ead1dc",
    fg="#702044",
    font=("Arial", 10, "bold"),
    relief="flat",
    pady=7,
    cursor="hand2"
).grid(row=14, column=0, sticky="ew", pady=4)

# Hide optional fields initially
other_price_frame.grid_remove()
print_price_frame.grid_remove()

# Update display when selections change
size_var.trace_add("write", update_options)
art_var.trace_add("write", update_options)
frame_var.trace_add("write", update_options)
print_var.trace_add("write", update_options)

# Start application
update_options()
root.mainloop()