import os
import subprocess
import time
import shutil

def run(cmd, check=True):
    print(f"→ {cmd}")
    result = subprocess.run(cmd, shell=True, check=check, capture_output=True, text=True)
    return result

def check_and_install_packages():
    """Check if required packages are installed, install if missing"""
    # Core VNC packages
    core_packages = [
        "tigervnc", "xfce4", "xfce4-terminal", "novnc", "websockify", "xterm",
        "dbus", "dbus-x11"
    ]
    
    # Browsers
    browser_packages = [
        "firefox",           # Web browser
        "chromium",          # Chromium browser
    ]
    
    # File management & compression
    file_packages = [
        "thunar",            # File manager
        "thunar-archive-plugin",  # Archive integration for Thunar
        "xarchiver",         # GUI archive manager
        "zip",               # ZIP compression
        "unzip",             # ZIP extraction
        "p7zip",             # 7-Zip compression
        "tar",               # TAR archives
        "gzip",              # GZIP compression
        "bzip2",             # BZIP2 compression
        "xz",                # XZ compression
        "unrar",             # RAR extraction
        "file-roller",       # GNOME archive manager (alternative)
    ]
    
    # Office & productivity
    office_packages = [
        "mousepad",          # Text editor
        "libreoffice-writer",  # Word processor
        "libreoffice-calc",    # Spreadsheet
        "libreoffice-impress", # Presentations
        "evince",            # PDF viewer
        "galculator",        # Calculator
        "gnome-calculator",  # Another calculator
    ]
    
    # Media & graphics
    media_packages = [
        "ristretto",         # Image viewer
        "gimp",              # Image editor
        "inkscape",          # Vector graphics
        "vlc",               # Media player
        "audacious",         # Music player
        "cheese",            # Webcam app
        "simple-scan",       # Scanner utility
    ]
    
    # System utilities
    system_packages = [
        "xfce4-taskmanager", # Task manager
        "htop",              # Terminal system monitor
        "gnome-system-monitor",  # GUI system monitor
        "gnome-disk-utility",    # Disk management
        "gparted",           # Partition editor
        "baobab",            # Disk usage analyzer
        "xfce4-notifyd",     # Notifications
        "xfce4-screenshooter",  # Screenshot tool
        "flameshot",         # Advanced screenshot tool
    ]
    
    # Development tools
    dev_packages = [
        "geany",             # IDE/text editor
        "meld",              # Diff/merge tool
        "gitg",              # Git GUI
    ]
    
    # Network & internet
    network_packages = [
        "transmission-gtk",  # BitTorrent client (GTK version)
        "filezilla",         # FTP client
    ]
    
    # Themes and fonts
    theme_packages = [
        "font-noto",         # Good fonts
        "font-noto-emoji",   # Emoji support
        "ttf-dejavu",        # DejaVu fonts
        "ttf-liberation",    # Liberation fonts
        "adwaita-icon-theme", # Icons
        "papirus-icon-theme", # Nice icons
        "arc-theme",         # Arc GTK theme
    ]
    
    print("🔍 Checking required packages...")
    
    all_packages = (core_packages + browser_packages + file_packages + 
                   office_packages + media_packages + system_packages + 
                   dev_packages + network_packages + theme_packages)
    
    # List of essential executables to check - if ANY are missing, reinstall all
    essential_apps = [
        "vncserver", "chromium", "filezilla", "transmission-gtk", 
        "gimp", "inkscape", "vlc", "libreoffice", "evince", 
        "galculator", "gparted", "meld", "gitg", "geany",
        "baobab", "gnome-system-monitor", "gnome-disks", "flameshot"
    ]
    
    # Check if any essential app is missing
    missing_apps = [app for app in essential_apps if not shutil.which(app)]
    
    if missing_apps:
        print(f"📦 Installing packages (this may take a few minutes)...")
        print(f"   Missing: {', '.join(missing_apps[:5])}{'...' if len(missing_apps) > 5 else ''}")
        run(f"sudo apk add --no-cache {' '.join(all_packages)}", check=False)
        print("✅ Packages installed successfully")
    else:
        print("✅ All required packages are installed")

def kill_existing():
    print("🔻 Killing existing VNC and noVNC processes...")
    run("vncserver -kill :1 2>/dev/null", check=False)
    run("pkill Xvnc", check=False)
    run("pkill Xtightvnc", check=False)
    run("pkill websockify", check=False)

    print("🧹 Removing stale lock files...")
    run("rm -f /tmp/.X1-lock", check=False)
    run("rm -f /tmp/.X11-unix/X1", check=False)

def setup_vnc_password(password="user123"):
    passwd_file = os.path.expanduser("~/.vnc/passwd")
    print("🔐 Setting VNC password...")
    os.makedirs(os.path.expanduser("~/.vnc"), exist_ok=True)
    
    # Use vncpasswd with password input
    proc = subprocess.Popen(
        ["vncpasswd", "-f"], 
        stdin=subprocess.PIPE, 
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, _ = proc.communicate(input=f"{password}\n{password}\n".encode())
    
    with open(passwd_file, "wb") as f:
        f.write(stdout)
    os.chmod(passwd_file, 0o600)

def create_xstartup():
    print("📝 Creating VNC startup script...")
    xstartup_path = os.path.expanduser("~/.vnc/xstartup")
    with open(xstartup_path, "w") as f:
        f.write("#!/bin/bash\n\n")
        f.write("# Prevent session manager issues\n")
        f.write("unset SESSION_MANAGER\n")
        f.write("unset DBUS_SESSION_BUS_ADDRESS\n\n")
        f.write("# Set up environment\n")
        f.write("export XDG_SESSION_TYPE=x11\n")
        f.write("export XDG_CURRENT_DESKTOP=XFCE\n")
        f.write("export XDG_SESSION_DESKTOP=xfce\n")
        f.write("export DISPLAY=:1\n\n")
        f.write("# Start D-Bus for the session\n")
        f.write("if [ -z \"$DBUS_SESSION_BUS_ADDRESS\" ]; then\n")
        f.write("    eval $(dbus-launch --sh-syntax)\n")
        f.write("    export DBUS_SESSION_BUS_ADDRESS\n")
        f.write("fi\n\n")
        f.write("# Disable screen blanking at X level\n")
        f.write("xset s off\n")
        f.write("xset s noblank\n")
        f.write("xset -dpms\n\n")
        f.write("# Kill any screensaver processes\n")
        f.write("pkill -9 xfce4-screensaver 2>/dev/null\n")
        f.write("pkill -9 light-locker 2>/dev/null\n")
        f.write("pkill -9 xscreensaver 2>/dev/null\n\n")
        f.write("# Start XFCE4 panel and desktop directly (skip session manager user switch)\n")
        f.write("xfwm4 --replace &\n")
        f.write("xfdesktop &\n")
        f.write("xfce4-panel &\n")
        f.write("thunar --daemon &\n")
        f.write("\n# Keep the session alive\n")
        f.write("wait\n")
    os.chmod(xstartup_path, 0o755)

def create_vnc_config():
    print("⚙️  Creating VNC configuration...")
    vnc_dir = os.path.expanduser("~/.vnc")
    config_path = os.path.join(vnc_dir, "config")
    
    with open(config_path, "w") as f:
        f.write("# TigerVNC Configuration\n")
        f.write("geometry=1920x1080\n")
        f.write("depth=24\n")
        f.write("localhost=no\n")
        f.write("alwaysshared=yes\n")
        f.write("# Keep session alive\n")
        f.write("desktop=XFCE Desktop\n")
        f.write("# Disable screen blanking\n")
        f.write("neverShared=no\n")
        f.write("disconnectClients=no\n")
    
    os.chmod(config_path, 0o644)

def configure_xfce_settings():
    print("🔧 Configuring XFCE settings...")
    
    # Create XFCE config directory
    xfce_config = os.path.expanduser("~/.config/xfce4/xfconf/xfce-perchannel-xml")
    os.makedirs(xfce_config, exist_ok=True)
    
    # Completely disable screensaver
    xfce4_screensaver = os.path.join(xfce_config, "xfce4-screensaver.xml")
    with open(xfce4_screensaver, "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<channel name="xfce4-screensaver" version="1.0">\n')
        f.write('  <property name="saver" type="empty">\n')
        f.write('    <property name="enabled" type="bool" value="false"/>\n')
        f.write('    <property name="mode" type="int" value="0"/>\n')
        f.write('    <property name="idle-activation" type="empty">\n')
        f.write('      <property name="enabled" type="bool" value="false"/>\n')
        f.write('    </property>\n')
        f.write('  </property>\n')
        f.write('  <property name="lock" type="empty">\n')
        f.write('    <property name="enabled" type="bool" value="false"/>\n')
        f.write('    <property name="saver-activation" type="empty">\n')
        f.write('      <property name="enabled" type="bool" value="false"/>\n')
        f.write('    </property>\n')
        f.write('    <property name="user-switching" type="empty">\n')
        f.write('      <property name="enabled" type="bool" value="false"/>\n')
        f.write('    </property>\n')
        f.write('  </property>\n')
        f.write('</channel>\n')
    
    # Completely disable power management
    xfce4_power = os.path.join(xfce_config, "xfce4-power-manager.xml")
    with open(xfce4_power, "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<channel name="xfce4-power-manager" version="1.0">\n')
        f.write('  <property name="xfce4-power-manager" type="empty">\n')
        f.write('    <property name="show-tray-icon" type="bool" value="false"/>\n')
        f.write('    <property name="blank-on-ac" type="int" value="0"/>\n')
        f.write('    <property name="blank-on-battery" type="int" value="0"/>\n')
        f.write('    <property name="dpms-on-ac-sleep" type="uint" value="0"/>\n')
        f.write('    <property name="dpms-on-ac-off" type="uint" value="0"/>\n')
        f.write('    <property name="dpms-on-battery-sleep" type="uint" value="0"/>\n')
        f.write('    <property name="dpms-on-battery-off" type="uint" value="0"/>\n')
        f.write('    <property name="dpms-enabled" type="bool" value="false"/>\n')
        f.write('    <property name="lock-screen-suspend-hibernate" type="bool" value="false"/>\n')
        f.write('    <property name="logind-handle-lid-switch" type="bool" value="false"/>\n')
        f.write('    <property name="inactivity-on-ac" type="uint" value="0"/>\n')
        f.write('    <property name="inactivity-on-battery" type="uint" value="0"/>\n')
        f.write('    <property name="inactivity-sleep-mode-on-ac" type="uint" value="0"/>\n')
        f.write('    <property name="inactivity-sleep-mode-on-battery" type="uint" value="0"/>\n')
        f.write('  </property>\n')
        f.write('</channel>\n')
    
    # Disable session lock and user switching completely
    xfce4_session = os.path.join(xfce_config, "xfce4-session.xml")
    with open(xfce4_session, "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<channel name="xfce4-session" version="1.0">\n')
        f.write('  <property name="general" type="empty">\n')
        f.write('    <property name="LockCommand" type="string" value=""/>\n')
        f.write('    <property name="SaveOnExit" type="bool" value="false"/>\n')
        f.write('    <property name="AutoSave" type="bool" value="false"/>\n')
        f.write('    <property name="PromptOnLogout" type="bool" value="false"/>\n')
        f.write('  </property>\n')
        f.write('  <property name="splash" type="empty">\n')
        f.write('    <property name="Engine" type="string" value=""/>\n')
        f.write('  </property>\n')
        f.write('  <property name="shutdown" type="empty">\n')
        f.write('    <property name="ShowSuspend" type="bool" value="false"/>\n')
        f.write('    <property name="ShowHibernate" type="bool" value="false"/>\n')
        f.write('    <property name="ShowHybridSleep" type="bool" value="false"/>\n')
        f.write('    <property name="ShowSwitchUser" type="bool" value="false"/>\n')
        f.write('  </property>\n')
        f.write('</channel>\n')
    
    # Configure panel to remove problematic items
    xfce4_panel = os.path.join(xfce_config, "xfce4-panel.xml")
    with open(xfce4_panel, "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<channel name="xfce4-panel" version="1.0">\n')
        f.write('  <property name="configver" type="int" value="2"/>\n')
        f.write('  <property name="panels" type="array">\n')
        f.write('    <value type="int" value="1"/>\n')
        f.write('    <property name="panel-1" type="empty">\n')
        f.write('      <property name="position" type="string" value="p=6;x=0;y=0"/>\n')
        f.write('      <property name="length" type="uint" value="100"/>\n')
        f.write('      <property name="position-locked" type="bool" value="true"/>\n')
        f.write('      <property name="size" type="uint" value="30"/>\n')
        f.write('      <property name="plugin-ids" type="array">\n')
        f.write('        <value type="int" value="1"/>\n')
        f.write('        <value type="int" value="2"/>\n')
        f.write('        <value type="int" value="3"/>\n')
        f.write('        <value type="int" value="4"/>\n')
        f.write('        <value type="int" value="5"/>\n')
        f.write('        <value type="int" value="6"/>\n')
        f.write('      </property>\n')
        f.write('    </property>\n')
        f.write('  </property>\n')
        f.write('  <property name="plugins" type="empty">\n')
        f.write('    <property name="plugin-1" type="string" value="applicationsmenu"/>\n')
        f.write('    <property name="plugin-2" type="string" value="tasklist"/>\n')
        f.write('    <property name="plugin-3" type="string" value="separator">\n')
        f.write('      <property name="expand" type="bool" value="true"/>\n')
        f.write('      <property name="style" type="uint" value="0"/>\n')
        f.write('    </property>\n')
        f.write('    <property name="plugin-4" type="string" value="systray"/>\n')
        f.write('    <property name="plugin-5" type="string" value="clock"/>\n')
        f.write('    <property name="plugin-6" type="string" value="showdesktop"/>\n')
        f.write('  </property>\n')
        f.write('</channel>\n')
    
    print("✅ XFCE configured - screensaver, lock screen, and user switching disabled")

def disable_problematic_services():
    """Kill and prevent services that can cause disconnections"""
    print("🛡️  Disabling problematic services...")
    
    # Kill any running screensavers or lock managers
    run("pkill -9 xfce4-screensaver", check=False)
    run("pkill -9 light-locker", check=False)
    run("pkill -9 xscreensaver", check=False)
    run("pkill -9 gnome-screensaver", check=False)
    
    # Remove screensaver autostart
    autostart_dir = os.path.expanduser("~/.config/autostart")
    os.makedirs(autostart_dir, exist_ok=True)
    
    # Create disabled autostart files for screensavers
    disabled_apps = [
        "xfce4-screensaver",
        "light-locker", 
        "gnome-screensaver",
        "xscreensaver"
    ]
    
    for app in disabled_apps:
        disabled_file = os.path.join(autostart_dir, f"{app}.desktop")
        with open(disabled_file, "w") as f:
            f.write(f"[Desktop Entry]\n")
            f.write(f"Name={app}\n")
            f.write(f"Hidden=true\n")
            f.write(f"X-GNOME-Autostart-enabled=false\n")
    
    print("✅ Problematic services disabled")

def create_desktop_icons():
    """Create desktop shortcuts for all installed applications"""
    print("🖼️  Creating desktop icons...")
    
    desktop_dir = os.path.expanduser("~/Desktop")
    os.makedirs(desktop_dir, exist_ok=True)
    
    # Define all desktop shortcuts
    desktop_entries = [
        # Browsers
        {
            "name": "Firefox",
            "exec": "firefox",
            "icon": "firefox",
            "comment": "Web Browser",
            "categories": "Network;WebBrowser;"
        },
        {
            "name": "Chromium",
            "exec": "chromium",
            "icon": "chromium",
            "comment": "Chromium Web Browser",
            "categories": "Network;WebBrowser;"
        },
        # File Management
        {
            "name": "Files (Thunar)",
            "exec": "thunar",
            "icon": "system-file-manager",
            "comment": "File Manager",
            "categories": "System;FileTools;FileManager;"
        },
        {
            "name": "Archive Manager",
            "exec": "xarchiver",
            "icon": "xarchiver",
            "comment": "Create and extract archives",
            "categories": "Utility;Archiving;"
        },
        # Office
        {
            "name": "LibreOffice Writer",
            "exec": "libreoffice --writer",
            "icon": "libreoffice-writer",
            "comment": "Word Processor",
            "categories": "Office;WordProcessor;"
        },
        {
            "name": "LibreOffice Calc",
            "exec": "libreoffice --calc",
            "icon": "libreoffice-calc",
            "comment": "Spreadsheet",
            "categories": "Office;Spreadsheet;"
        },
        {
            "name": "LibreOffice Impress",
            "exec": "libreoffice --impress",
            "icon": "libreoffice-impress",
            "comment": "Presentations",
            "categories": "Office;Presentation;"
        },
        {
            "name": "PDF Viewer",
            "exec": "evince",
            "icon": "evince",
            "comment": "View PDF documents",
            "categories": "Office;Viewer;"
        },
        {
            "name": "Calculator",
            "exec": "galculator",
            "icon": "galculator",
            "comment": "Calculator",
            "categories": "Utility;Calculator;"
        },
        # Text Editors
        {
            "name": "Mousepad",
            "exec": "mousepad",
            "icon": "mousepad",
            "comment": "Simple Text Editor",
            "categories": "Utility;TextEditor;"
        },
        {
            "name": "Geany",
            "exec": "geany",
            "icon": "geany",
            "comment": "IDE and Text Editor",
            "categories": "Development;IDE;"
        },
        # Media
        {
            "name": "Image Viewer",
            "exec": "ristretto",
            "icon": "ristretto",
            "comment": "View Images",
            "categories": "Graphics;Viewer;"
        },
        {
            "name": "GIMP",
            "exec": "gimp",
            "icon": "gimp",
            "comment": "Image Editor",
            "categories": "Graphics;2DGraphics;"
        },
        {
            "name": "Inkscape",
            "exec": "inkscape",
            "icon": "inkscape",
            "comment": "Vector Graphics Editor",
            "categories": "Graphics;VectorGraphics;"
        },
        {
            "name": "VLC Media Player",
            "exec": "vlc",
            "icon": "vlc",
            "comment": "Play Videos and Music",
            "categories": "AudioVideo;Player;"
        },
        {
            "name": "Audacious",
            "exec": "audacious",
            "icon": "audacious",
            "comment": "Music Player",
            "categories": "AudioVideo;Audio;Player;"
        },
        # System Tools
        {
            "name": "Terminal",
            "exec": "xfce4-terminal",
            "icon": "utilities-terminal",
            "comment": "Terminal Emulator",
            "categories": "System;TerminalEmulator;"
        },
        {
            "name": "Task Manager",
            "exec": "xfce4-taskmanager",
            "icon": "utilities-system-monitor",
            "comment": "Monitor System Resources",
            "categories": "System;Monitor;"
        },
        {
            "name": "System Monitor",
            "exec": "gnome-system-monitor",
            "icon": "utilities-system-monitor",
            "comment": "View System Resources",
            "categories": "System;Monitor;"
        },
        {
            "name": "Disk Usage Analyzer",
            "exec": "baobab",
            "icon": "baobab",
            "comment": "Analyze Disk Usage",
            "categories": "System;Filesystem;"
        },
        {
            "name": "Disks",
            "exec": "gnome-disks",
            "icon": "gnome-disks",
            "comment": "Disk Management",
            "categories": "System;"
        },
        {
            "name": "GParted",
            "exec": "gparted",
            "icon": "gparted",
            "comment": "Partition Editor",
            "categories": "System;"
        },
        {
            "name": "Screenshot",
            "exec": "xfce4-screenshooter",
            "icon": "applets-screenshooter",
            "comment": "Take Screenshots",
            "categories": "Utility;"
        },
        {
            "name": "Flameshot",
            "exec": "flameshot gui",
            "icon": "flameshot",
            "comment": "Advanced Screenshot Tool",
            "categories": "Utility;"
        },
        # Development
        {
            "name": "Meld",
            "exec": "meld",
            "icon": "meld",
            "comment": "Diff and Merge Tool",
            "categories": "Development;"
        },
        {
            "name": "Gitg",
            "exec": "gitg",
            "icon": "gitg",
            "comment": "Git Repository Viewer",
            "categories": "Development;"
        },
        # Network
        {
            "name": "Transmission",
            "exec": "transmission-gtk",
            "icon": "transmission",
            "comment": "BitTorrent Client",
            "categories": "Network;P2P;"
        },
        {
            "name": "FileZilla",
            "exec": "filezilla",
            "icon": "filezilla",
            "comment": "FTP Client",
            "categories": "Network;FileTransfer;"
        },
    ]
    
    for entry in desktop_entries:
        desktop_file = os.path.join(desktop_dir, f"{entry['name'].replace(' ', '-').replace('(', '').replace(')', '')}.desktop")
        with open(desktop_file, "w") as f:
            f.write("[Desktop Entry]\n")
            f.write("Version=1.0\n")
            f.write("Type=Application\n")
            f.write(f"Name={entry['name']}\n")
            f.write(f"Exec={entry['exec']}\n")
            f.write(f"Icon={entry['icon']}\n")
            f.write(f"Comment={entry['comment']}\n")
            f.write(f"Categories={entry['categories']}\n")
            f.write("Terminal=false\n")
            f.write("StartupNotify=true\n")
        os.chmod(desktop_file, 0o755)
    
    # Also mark all desktop files as trusted (XFCE specific)
    run("chmod +x ~/Desktop/*.desktop", check=False)
    
    print(f"✅ Created {len(desktop_entries)} desktop icons")

def start_vnc():
    print("🚀 Starting VNC server...")
    os.environ["USER"] = os.environ.get("USER", "root")
    
    # Start VNC server - vncserver will read options from ~/.vnc/config
    # Run in background and redirect output
    os.system("vncserver :1 > /tmp/vncserver.log 2>&1 &")
    
    # Wait for VNC to be ready
    time.sleep(4)
    
    # Check if VNC is running
    check_result = run("pgrep -f 'Xvnc.*:1'", check=False)
    if check_result.returncode == 0:
        print("✅ VNC server started on display :1 (port 5901)")
    else:
        print("❌ VNC server failed to start. Check /tmp/vncserver.log for details")
        # Show the log
        if os.path.exists("/tmp/vncserver.log"):
            with open("/tmp/vncserver.log") as f:
                print(f.read())
        raise Exception("VNC server failed to start")

def start_novnc():
    print("🌐 Starting noVNC web interface...")
    
    # Find websockify and novnc paths
    novnc_path = "/usr/share/novnc"
    if not os.path.exists(novnc_path):
        novnc_path = "/usr/share/webapps/novnc"
    
    log_path = os.path.expanduser("~/.novnc.log")
    
    # Start websockify in background
    cmd = f"websockify --web={novnc_path} 6080 localhost:5901 > {log_path} 2>&1 &"
    run(cmd, check=False)
    
    # Wait and verify it started
    time.sleep(3)
    result = run("pgrep -f websockify", check=False)
    if result.returncode == 0:
        print("✅ noVNC web interface started on port 6080")
    else:
        print("⚠️  Warning: Could not verify websockify is running")
        print(f"Check log at: {log_path}")

def get_preview_url():
    """Get the GitHub Codespaces preview URL"""
    hostname = os.uname().nodename
    return f"https://{hostname}-6080.githubpreview.dev"

def main():
    try:
        check_and_install_packages()
        kill_existing()
        setup_vnc_password()
        disable_problematic_services()
        configure_xfce_settings()
        create_xstartup()
        create_vnc_config()
        create_desktop_icons()
        start_vnc()
        start_novnc()
        
        print("\n" + "="*60)
        print("✅ Desktop is running!")
        print("="*60)
        print(f"🌐 Open in browser: {get_preview_url()}")
        print("🔐 VNC password: user123")
        print("\n📦 Installed Applications:")
        print("   🌐 BROWSERS:")
        print("      • Firefox, Chromium")
        print("   📁 FILE MANAGEMENT:")
        print("      • Thunar File Manager, Archive Manager (Xarchiver)")
        print("      • Supports: ZIP, 7z, TAR, GZIP, BZIP2, XZ, RAR")
        print("   📝 OFFICE & PRODUCTIVITY:")
        print("      • LibreOffice (Writer, Calc, Impress)")
        print("      • PDF Viewer (Evince), Calculator")
        print("   ✏️  TEXT EDITORS:")
        print("      • Mousepad, Geany IDE")
        print("   🎨 GRAPHICS & MEDIA:")
        print("      • GIMP, Inkscape, Image Viewer")
        print("      • VLC Media Player, Audacious Music Player")
        print("   🔧 SYSTEM TOOLS:")
        print("      • Task Manager, System Monitor")
        print("      • Disk Usage Analyzer, GParted")
        print("      • Screenshot Tools (Flameshot)")
        print("   💻 DEVELOPMENT:")
        print("      • Meld (diff/merge), Gitg (Git GUI)")
        print("   🌐 NETWORK:")
        print("      • Transmission (BitTorrent), FileZilla (FTP)")
        print("\n🖼️  Desktop icons have been created for all apps!")
        print("\n💡 Tips:")
        print("   • The desktop will NEVER disconnect or lock")
        print("   • All apps are available from the Applications menu")
        print("   • Double-click desktop icons to launch apps")
        print("   • Reconnect anytime using the same URL")
        print("="*60)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("💡 Try running the script again or check the logs")
        exit(1)

if __name__ == "__main__":
    main()
