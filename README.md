# Desktop Environment Setup

## How to Run

### Step 1: Open Terminal
Press
```bash 
Ctrl+shift+`
```
to open terminal

### Step 2: Update APT
```bash
sudo apt update
```

### Step 3: Install Python3
```bash
sudo apt install -y python3
```

### Step 4: Install Required Packages
```bash
sudo apt install -y tigervnc-standalone-server tigervnc-common novnc websockify
```

### Step 5: Start the Desktop
```bash
python3 desktop_toggle.py
```
Wait for it to complete (this may take a few minutes on first run)

### Step 6: Access the Desktop
1. Click on the **Ports** tab
2. Hover over the correct port (port `6080`)
3. Click the **globe icon** to open the link (<small> thats just to open the link, you can also just ctrl+click it or whatever to just open link
</small>)
### Step 7: Connect to VNC
1. Select **vnc.html** (NOT the lite version cause that can break more and less features)
2. Click **Connect**
3. Enter password: `user123`

### EXTRA SETUP
there might be some glitched and theese are some fixes to them.

Screen sizing broken: click the arrow on left side bar them click options, find scaling and set it to local scaling, this should fix that issue.

clipboard not working: the clipboard is currently not good at syncing(for now probaly), so on the side bar there is a clipboard button that you can view to see the current clipboard in an input where you can paste your stuff or transfer it to your real clipboard.

Not connection anymore: if it works then later you go back on and its broken, an easy way to fix this is to restart the desktop by hovering above every port number then clicking the X button to close, then running the python script
```bash
python3 desktop_toggle.py
```
 again and try to fix it, a last resort option is to just delete this codespace and make a new one