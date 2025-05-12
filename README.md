# Docker Manager UI 

This is a **Linux-based GUI tool** built using **Python Tkinter** to manage Docker containers easily through an interactive desktop interface.

> Developed as part of a **Linux-based systems project** to simplify Docker container operations with a visual interface.

---

##  Features

- View all Docker containers (running and stopped)
- Filter/search containers by name or status
- Start, Stop, Restart containers
- View real-time container logs
- Inspect container metadata
- Remove containers safely with confirmation
- Launch new interactive containers using GNOME Terminal
- Copy logs to clipboard
- Lightweight and easy to use on most Linux distros

---

##  Technologies Used

-  **Python 3.12.3**
-  **Docker** installed and running
-  Python standard libraries:
  - `tkinter`
  - `subprocess`
-  **GNOME Terminal** (used to launch interactive containers)

---

##  Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/docker-manager-ui.git
   cd docker-manager-ui

2. **Run the Script**:
  ```bash
   python3 docker_gui.py
```


##  Usage Instructions
- Launch the application using python3 docker_gui.py

- Use the search bar to filter containers by name or status.

- Select a container from the list to:

  - Start, Stop, or Restart

  - View logs

  - Inspect details

  - Remove the container

- Use "Create New" to launch a container interactively in a GNOME terminal.

- Use the Refresh button to reload the container list anytime.

- Watch the status bar for updates and messages.

## Docker Commands Used
Internally, the following Docker commands are executed using Python’s subprocess module:

- docker ps -a --format

- docker start <container>

- docker stop <container>

- docker restart <container>

- docker logs <container>

- docker inspect <container>

- docker rm <container>

- docker run -it <image> (in GNOME Terminal)


