import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, simpledialog
import subprocess

# Function to run shell commands and return output
def run_command(cmd):
    print(f"Running command: {cmd}")  # Print command to terminal
    try:
        result = subprocess.check_output(cmd, shell=True, text=True)
        print(result.strip())  # Print result
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.output.strip()}")
        return f"Error: {e.output.strip()}"

# Refresh and display list of Docker containers with optional filter
def refresh_containers(filter_term=""):
    output = run_command("docker ps -a --format '{{.ID}} {{.Names}} {{.Status}}'")
    container_list.delete(*container_list.get_children())  # Clear existing entries

    for line in output.strip().split('\n'):
        parts = line.strip().split(maxsplit=2)
        # Filter by container name or status
        if len(parts) == 3 and (filter_term.lower() in parts[1].lower() or filter_term.lower() in parts[2].lower()):
            container_list.insert("", "end", values=(parts[0], parts[1], parts[2]))

    status_var.set("Refreshed containers.")

# Get the container ID of the selected item in the treeview
def get_selected_container():
    selected = container_list.selection()
    if not selected:
        messagebox.showwarning("No Selection", "Please select a container.")
        return None
    return container_list.item(selected[0])["values"][0]

# Perform start, stop, or restart operation on a container
def act_on_container(action):
    container = get_selected_container()
    if container:
        output = run_command(f"docker {action} {container}")
        status_var.set(output.strip() or f"{action.title()} command sent to {container}")
        refresh_containers(search_var.get())  # Refresh list after action

# Remove a container after confirmation
def remove_container():
    container = get_selected_container()
    if container and messagebox.askyesno("Confirm", f"Remove container {container}?"):
        output = run_command(f"docker rm {container}")
        status_var.set(output.strip())
        refresh_containers(search_var.get())

# Show logs of selected container in a new window
def view_logs():
    container = get_selected_container()
    if container:
        logs = run_command(f"docker logs {container}")
        logs_window = tk.Toplevel(root)
        logs_window.title(f"Logs - {container}")
        logs_window.geometry("800x500")

        # Text display area with scroll
        frame = ttk.Frame(logs_window)
        frame.pack(fill='both', expand=True)
        text_area = scrolledtext.ScrolledText(frame, wrap=tk.WORD, font=("Courier", 10))
        text_area.pack(expand=True, fill="both", padx=10, pady=10)
        text_area.insert(tk.END, logs)
        text_area.config(state='disabled')

        # Copy and clear buttons
        btns = ttk.Frame(logs_window)
        btns.pack(fill='x', pady=5)
        ttk.Button(btns, text="Copy", command=lambda: root.clipboard_append(logs)).pack(side='left', padx=10)
        ttk.Button(btns, text="Clear", command=lambda: text_area.config(state='normal') or text_area.delete(1.0, tk.END) or text_area.config(state='disabled')).pack(side='left')

# Inspect container and show full details in a new window
def inspect_container():
    container = get_selected_container()
    if container:
        inspect = run_command(f"docker inspect {container}")
        info_window = tk.Toplevel(root)
        info_window.title(f"Inspect - {container}")
        info_window.geometry("800x500")

        # Show inspection info
        text = scrolledtext.ScrolledText(info_window, wrap=tk.WORD, font=("Courier", 10))
        text.pack(expand=True, fill="both", padx=10, pady=10)
        text.insert(tk.END, inspect)
        text.config(state='disabled')

# Create new container from image interactively
def create_container():
    image = simpledialog.askstring("Run Container", "Enter image name (e.g. ubuntu):")
    if image:
        # Run the container in a new terminal window interactively
        terminal_command = f'gnome-terminal -- bash -c "sudo docker run -it {image}; exec bash"'
        subprocess.Popen(terminal_command, shell=True)
        status_var.set(f"Launching interactive container: {image}")

# GUI Setup
root = tk.Tk()
root.title("Docker Manager UI")
root.geometry("1000x600")
root.configure(bg="#f0f0f0")

# Set styles for widgets
style = ttk.Style(root)
style.configure("Treeview", font=("Arial", 11), rowheight=30)
style.configure("Treeview.Heading", font=("Arial", 12, "bold"))
style.configure("TButton", font=("Arial", 11))

# Header label
tk.Label(root, text="🛠️ Docker Container Manager", font=("Helvetica", 20, "bold"), bg="#f0f0f0").pack(pady=10)

# Search Bar
search_frame = ttk.Frame(root)
search_frame.pack(pady=5, padx=10, fill='x')
search_var = tk.StringVar()
ttk.Label(search_frame, text="Search: ").pack(side='left')
ttk.Entry(search_frame, textvariable=search_var, width=30).pack(side='left', padx=5)
ttk.Button(search_frame, text="Filter", command=lambda: refresh_containers(search_var.get())).pack(side='left')
ttk.Button(search_frame, text="Clear", command=lambda: search_var.set("") or refresh_containers()).pack(side='left', padx=5)

# Container list table
columns = ("ID", "Name", "Status")
container_list = ttk.Treeview(root, columns=columns, show="headings", height=12)
for col in columns:
    container_list.heading(col, text=col)
    container_list.column(col, anchor='center')
container_list.pack(padx=15, fill="both", expand=True)

# Button panel for actions
btn_frame = ttk.Frame(root)
btn_frame.pack(pady=10)

# Define buttons and bind to respective functions
buttons = [
    ("Start", lambda: act_on_container("start")),
    ("Stop", lambda: act_on_container("stop")),
    ("Restart", lambda: act_on_container("restart")),
    ("Remove", remove_container),
    ("View Logs", view_logs),
    ("Inspect", inspect_container),
    ("Create New", create_container),
    ("Refresh", lambda: refresh_containers(search_var.get()))
]

# Add buttons to frame
for i, (label, cmd) in enumerate(buttons):
    ttk.Button(btn_frame, text=label, command=cmd).grid(row=0, column=i, padx=8)

# Status bar at the bottom
status_var = tk.StringVar()
status_bar = tk.Label(root, textvariable=status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W, bg="white")
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

# Initial load of containers
refresh_containers()

# Run the application
root.mainloop()
