import os
import subprocess
import time
import shutil

def run(cmd, check=True, show_output=False):
    print(f"→ {cmd}")
    if show_output:
        # Show output in real-time
        result = subprocess.run(cmd, shell=True, check=check)
        return result
    else:
        result = subprocess.run(cmd, shell=True, check=check, capture_output=True, text=True)
        return result

def run_install(cmd):
    """Run installation command with visible output"""
    print(f"→ {cmd}")
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    while True:
        line = process.stdout.readline()
        if not line and process.poll() is not None:
            break
        if line:
            print(line.rstrip())
    return process.returncode

def check_and_install_packages():
    """Check if required packages are installed, install if missing"""
    
    # Core VNC packages
    core_packages = [
        "tigervnc-standalone-server", "tigervnc-common", "novnc", "websockify",
        "xterm", "dbus-x11", "x11-xserver-utils"
    ]
    
    # Desktop environment - XFCE
    desktop_packages = [
        "xfce4", "xfce4-terminal", "xfce4-goodies", "xfce4-taskmanager",
        "thunar", "thunar-archive-plugin"
    ]
    
    # Browsers
    browser_packages = [
        "firefox-esr",       # Firefox browser
        "chromium",          # Chromium browser
    ]
    
    # File management & compression
    file_packages = [
        "file-roller",       # Archive manager
        "zip", "unzip", "p7zip-full", "rar", "unrar",
        "tar", "gzip", "bzip2", "xz-utils"
    ]
    
    # Office & productivity
    office_packages = [
        "mousepad",          # Text editor
        "libreoffice-writer", "libreoffice-calc", "libreoffice-impress",
        "evince",            # PDF viewer
        "galculator",        # Calculator
        "gnome-calculator"
    ]
    
    # Media & graphics
    media_packages = [
        "ristretto",         # Image viewer
        "gimp",              # Image editor
        "inkscape",          # Vector graphics
        "vlc",               # Media player
        "audacious",         # Music player
    ]
    
    # System utilities
    system_packages = [
        "htop",              # System monitor
        "gnome-system-monitor",
        "gnome-disk-utility",
        "gparted",           # Partition editor
        "baobab",            # Disk usage analyzer
        "xfce4-screenshooter",
        "flameshot",         # Screenshot tool
    ]
    
    # Development tools
    dev_packages = [
        "geany",             # IDE/text editor
        "meld",              # Diff/merge tool
        "gitg",              # Git GUI
        "git"
    ]
    
    # Network & internet
    network_packages = [
        "transmission-gtk",  # BitTorrent client
        "filezilla",         # FTP client
    ]
    
    # Wine for Windows apps
    wine_packages = [
        "wine", "wine64", "winetricks"
    ]
    
    # Themes and fonts
    theme_packages = [
        "fonts-noto", "fonts-noto-color-emoji",
        "fonts-dejavu", "fonts-liberation",
        "adwaita-icon-theme", "papirus-icon-theme",
        "arc-theme"
    ]
    
    # Bluetooth support
    bluetooth_packages = [
        "bluetooth", "bluez", "bluez-tools", "blueman"
    ]
    
    # Extra useful packages
    extra_packages = [
        "curl", "wget", "net-tools", "nano", "vim",
        "python3", "python3-pip", "build-essential",
        "software-properties-common", "apt-transport-https",
        "ca-certificates", "gnupg", "lsb-release"
    ]
    
    print("🔍 Checking and installing packages...")
    
    all_packages = (core_packages + desktop_packages + browser_packages + 
                   file_packages + office_packages + media_packages + 
                   system_packages + dev_packages + network_packages + 
                   wine_packages + theme_packages + bluetooth_packages + extra_packages)
    
    # Update package list first
    print("\n" + "="*60)
    print("📦 UPDATING PACKAGE LISTS...")
    print("="*60)
    run_install("sudo apt-get update -y")
    
    # Fix any broken packages first
    print("\n" + "="*60)
    print("🔧 FIXING ANY BROKEN PACKAGES...")
    print("="*60)
    run_install("sudo dpkg --configure -a")
    run_install("sudo apt-get install -f -y")
    
    # Install packages in groups for better error handling
    package_groups = [
        ("Core VNC", core_packages),
        ("Desktop Environment", desktop_packages),
        ("Browsers", browser_packages),
        ("File Management", file_packages),
        ("Office Suite", office_packages),
        ("Media Apps", media_packages),
        ("System Utilities", system_packages),
        ("Development Tools", dev_packages),
        ("Network Apps", network_packages),
        ("Wine", wine_packages),
        ("Themes & Fonts", theme_packages),
        ("Bluetooth", bluetooth_packages),
        ("Extra Tools", extra_packages),
    ]
    
    for group_name, packages in package_groups:
        print("\n" + "="*60)
        print(f"📦 INSTALLING: {group_name} ({len(packages)} packages)")
        print("="*60)
        install_cmd = f"sudo DEBIAN_FRONTEND=noninteractive apt-get install -y --fix-missing {' '.join(packages)}"
        ret = run_install(install_cmd)
        if ret != 0:
            print(f"⚠️  Some {group_name} packages may have failed, continuing...")
    
    # Final fix attempt
    print("\n" + "="*60)
    print("🔧 FINAL CLEANUP...")
    print("="*60)
    run_install("sudo apt-get install -f -y")
    
    # Verify critical apps and their actual executables
    critical_checks = {
        "vncserver": "vncserver",
        "firefox-esr": "firefox-esr",
        "chromium": ["chromium", "chromium-browser"],
        "gimp": "gimp",
        "vlc": "vlc",
        "wine": "wine",
        "filezilla": "filezilla",
        "libreoffice": "libreoffice"
    }
    
    print("\n🔎 Verifying installations...")
    missing = []
    for name, executable in critical_checks.items():
        if isinstance(executable, list):
            found = any(shutil.which(exe) for exe in executable)
        else:
            found = shutil.which(executable) is not None
        
        if not found:
            missing.append(name)
            print(f"   ❌ {name} - NOT FOUND")
        else:
            print(f"   ✅ {name} - installed")
    
    if missing:
        print(f"\n⚠️  WARNING: {len(missing)} apps failed to install: {', '.join(missing)}")
        print("💡 These apps will not work. You may need to install them manually.")
    else:
        print("\n✅ All critical packages installed successfully!")

def kill_existing():
    print("🔻 Killing existing VNC and noVNC processes...")
    run("vncserver -kill :1 2>/dev/null", check=False)
    run("pkill -f Xvnc", check=False)
    run("pkill -f Xtightvnc", check=False)
    run("pkill -f websockify", check=False)

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
        f.write("# Disable screen blanking\n")
        f.write("xset s off\n")
        f.write("xset s noblank\n")
        f.write("xset -dpms\n\n")
        f.write("# Kill any screensaver processes\n")
        f.write("pkill -9 xfce4-screensaver 2>/dev/null\n")
        f.write("pkill -9 light-locker 2>/dev/null\n")
        f.write("pkill -9 xscreensaver 2>/dev/null\n\n")
        f.write("# Start XFCE4 desktop\n")
        f.write("startxfce4 &\n")
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
        f.write("desktop=XFCE Desktop\n")
    
    os.chmod(config_path, 0o644)

def configure_xfce_settings():
    print("🔧 Configuring XFCE settings...")
    
    # Create XFCE config directory
    xfce_config = os.path.expanduser("~/.config/xfce4/xfconf/xfce-perchannel-xml")
    os.makedirs(xfce_config, exist_ok=True)
    
    # Disable screensaver
    xfce4_screensaver = os.path.join(xfce_config, "xfce4-screensaver.xml")
    with open(xfce4_screensaver, "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<channel name="xfce4-screensaver" version="1.0">\n')
        f.write('  <property name="saver" type="empty">\n')
        f.write('    <property name="enabled" type="bool" value="false"/>\n')
        f.write('    <property name="mode" type="int" value="0"/>\n')
        f.write('  </property>\n')
        f.write('  <property name="lock" type="empty">\n')
        f.write('    <property name="enabled" type="bool" value="false"/>\n')
        f.write('  </property>\n')
        f.write('</channel>\n')
    
    # Disable power management
    xfce4_power = os.path.join(xfce_config, "xfce4-power-manager.xml")
    with open(xfce4_power, "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<channel name="xfce4-power-manager" version="1.0">\n')
        f.write('  <property name="xfce4-power-manager" type="empty">\n')
        f.write('    <property name="dpms-enabled" type="bool" value="false"/>\n')
        f.write('    <property name="blank-on-ac" type="int" value="0"/>\n')
        f.write('  </property>\n')
        f.write('</channel>\n')
    
    print("✅ XFCE configured - screensaver and lock screen disabled")

def disable_problematic_services():
    """Kill and prevent services that can cause disconnections"""
    print("🛡️  Disabling problematic services...")
    
    run("pkill -9 xfce4-screensaver", check=False)
    run("pkill -9 light-locker", check=False)
    run("pkill -9 xscreensaver", check=False)
    run("pkill -9 gnome-screensaver", check=False)
    
    # Disable screensaver autostart
    autostart_dir = os.path.expanduser("~/.config/autostart")
    os.makedirs(autostart_dir, exist_ok=True)
    
    for app in ["xfce4-screensaver", "light-locker", "gnome-screensaver", "xscreensaver"]:
        disabled_file = os.path.join(autostart_dir, f"{app}.desktop")
        with open(disabled_file, "w") as f:
            f.write(f"[Desktop Entry]\nName={app}\nHidden=true\n")
    
    print("✅ Problematic services disabled")

def create_desktop_icons():
    """Create desktop shortcuts for all installed applications"""
    print("🖼️  Creating desktop icons...")
    
    desktop_dir = os.path.expanduser("~/Desktop")
    os.makedirs(desktop_dir, exist_ok=True)
    
    desktop_entries = [
        # Browsers
        {"name": "Firefox", "exec": "firefox-esr", "check": "firefox-esr", "icon": "firefox-esr", "comment": "Web Browser"},
        {"name": "Chromium", "exec": "chromium --no-sandbox", "check": ["chromium", "chromium-browser"], "icon": "chromium", "comment": "Chromium Web Browser"},
        # File Management
        {"name": "Files", "exec": "thunar", "check": "thunar", "icon": "system-file-manager", "comment": "File Manager"},
        {"name": "Archive Manager", "exec": "file-roller", "check": "file-roller", "icon": "org.gnome.FileRoller", "comment": "Create and extract archives"},
        # Office
        {"name": "LibreOffice Writer", "exec": "libreoffice --writer", "check": "libreoffice", "icon": "libreoffice-writer", "comment": "Word Processor"},
        {"name": "LibreOffice Calc", "exec": "libreoffice --calc", "check": "libreoffice", "icon": "libreoffice-calc", "comment": "Spreadsheet"},
        {"name": "LibreOffice Impress", "exec": "libreoffice --impress", "check": "libreoffice", "icon": "libreoffice-impress", "comment": "Presentations"},
        {"name": "PDF Viewer", "exec": "evince", "check": "evince", "icon": "org.gnome.Evince", "comment": "View PDF documents"},
        {"name": "Calculator", "exec": "galculator", "check": "galculator", "icon": "galculator", "comment": "Calculator"},
        # Text Editors
        {"name": "Mousepad", "exec": "mousepad", "check": "mousepad", "icon": "mousepad", "comment": "Simple Text Editor"},
        {"name": "Geany", "exec": "geany", "check": "geany", "icon": "geany", "comment": "IDE and Text Editor"},
        # Media
        {"name": "Image Viewer", "exec": "ristretto", "check": "ristretto", "icon": "ristretto", "comment": "View Images"},
        {"name": "GIMP", "exec": "gimp", "check": "gimp", "icon": "gimp", "comment": "Image Editor"},
        {"name": "Inkscape", "exec": "inkscape", "check": "inkscape", "icon": "inkscape", "comment": "Vector Graphics Editor"},
        {"name": "VLC Media Player", "exec": "vlc", "check": "vlc", "icon": "vlc", "comment": "Play Videos and Music"},
        {"name": "Audacious", "exec": "audacious", "check": "audacious", "icon": "audacious", "comment": "Music Player"},
        # System Tools
        {"name": "Terminal", "exec": "xfce4-terminal", "check": "xfce4-terminal", "icon": "utilities-terminal", "comment": "Terminal Emulator"},
        {"name": "Task Manager", "exec": "xfce4-taskmanager", "check": "xfce4-taskmanager", "icon": "utilities-system-monitor", "comment": "Monitor System Resources"},
        {"name": "System Monitor", "exec": "gnome-system-monitor", "check": "gnome-system-monitor", "icon": "utilities-system-monitor", "comment": "View System Resources"},
        {"name": "Disk Usage", "exec": "baobab", "check": "baobab", "icon": "baobab", "comment": "Analyze Disk Usage"},
        {"name": "Disks", "exec": "gnome-disks", "check": "gnome-disks", "icon": "gnome-disks", "comment": "Disk Management"},
        {"name": "GParted", "exec": "gparted", "check": "gparted", "icon": "gparted", "comment": "Partition Editor"},
        {"name": "Screenshot", "exec": "xfce4-screenshooter", "check": "xfce4-screenshooter", "icon": "applets-screenshooter", "comment": "Take Screenshots"},
        {"name": "Flameshot", "exec": "flameshot gui", "check": "flameshot", "icon": "flameshot", "comment": "Advanced Screenshot Tool"},
        # Development
        {"name": "Meld", "exec": "meld", "check": "meld", "icon": "meld", "comment": "Diff and Merge Tool"},
        {"name": "Gitg", "exec": "gitg", "check": "gitg", "icon": "gitg", "comment": "Git Repository Viewer"},
        # Network
        {"name": "Transmission", "exec": "transmission-gtk", "check": "transmission-gtk", "icon": "transmission", "comment": "BitTorrent Client"},
        {"name": "FileZilla", "exec": "filezilla", "check": "filezilla", "icon": "filezilla", "comment": "FTP Client"},
        # Wine
        {"name": "Wine Configuration", "exec": "winecfg", "check": "winecfg", "icon": "wine", "comment": "Configure Wine"},
        {"name": "Wine File Manager", "exec": "wine explorer", "check": "wine", "icon": "wine", "comment": "Wine File Explorer"},
        # Bluetooth
        {"name": "Bluetooth Manager", "exec": "blueman-manager", "check": "blueman-manager", "icon": "bluetooth", "comment": "Manage Bluetooth Devices"},
    ]
    
    # Only create icons for apps that are actually installed
    created_count = 0
    skipped_count = 0
    
    for entry in desktop_entries:
        # Check if the app is installed
        check_cmd = entry.get('check', entry['exec'].split()[0])
        
        if isinstance(check_cmd, list):
            is_installed = any(shutil.which(cmd) for cmd in check_cmd)
        else:
            is_installed = shutil.which(check_cmd) is not None
        
        if not is_installed:
            skipped_count += 1
            continue
        
        filename = entry['name'].replace(' ', '-').replace('(', '').replace(')', '')
        desktop_file = os.path.join(desktop_dir, f"{filename}.desktop")
        with open(desktop_file, "w") as f:
            f.write("[Desktop Entry]\n")
            f.write("Version=1.0\n")
            f.write("Type=Application\n")
            f.write(f"Name={entry['name']}\n")
            f.write(f"Exec={entry['exec']}\n")
            f.write(f"Icon={entry['icon']}\n")
            f.write(f"Comment={entry['comment']}\n")
            f.write("Terminal=false\n")
            f.write("StartupNotify=true\n")
        os.chmod(desktop_file, 0o755)
        created_count += 1
    
    run("chmod +x ~/Desktop/*.desktop", check=False)
    
    # Trust desktop files for XFCE
    run("gio set ~/Desktop/*.desktop metadata::trusted true 2>/dev/null", check=False)
    
    print(f"✅ Created {created_count} desktop icons ({skipped_count} apps not installed)")

def start_vnc():
    print("🚀 Starting VNC server...")
    os.environ["USER"] = os.environ.get("USER", "root")
    
    # Start VNC server
    os.system("vncserver :1 -geometry 1920x1080 -depth 24 > /tmp/vncserver.log 2>&1 &")
    
    # Wait for VNC to be ready
    time.sleep(4)
    
    # Check if VNC is running
    check_result = run("pgrep -f 'Xvnc.*:1'", check=False)
    if check_result.returncode == 0:
        print("✅ VNC server started on display :1 (port 5901)")
    else:
        print("❌ VNC server failed to start. Check /tmp/vncserver.log")
        if os.path.exists("/tmp/vncserver.log"):
            with open("/tmp/vncserver.log") as f:
                print(f.read())
        raise Exception("VNC server failed to start")

def start_novnc():
    print("🌐 Starting noVNC web interface...")
    
    # Check if websockify is installed
    websockify_check = run("which websockify", check=False)
    if websockify_check.returncode != 0:
        print("⚠️  websockify not found, installing...")
        print("="*60)
        run_install("sudo apt-get update -y")
        run_install("sudo DEBIAN_FRONTEND=noninteractive apt-get install -y websockify python3-websockify novnc")
        print("="*60)
        
        # Verify installation
        websockify_check = run("which websockify", check=False)
        if websockify_check.returncode != 0:
            # Try pip install as fallback
            print("⚠️  Trying pip install...")
            run_install("pip3 install websockify")
            websockify_check = run("which websockify", check=False)
            if websockify_check.returncode != 0:
                raise Exception("Failed to install websockify")
    
    print("✅ websockify is available")
    
    # Find noVNC path - check multiple possible locations
    novnc_paths = [
        "/usr/share/novnc",
        "/usr/share/webapps/novnc", 
        "/usr/share/novnc/utils",
        "/snap/novnc/current"
    ]
    novnc_path = None
    for path in novnc_paths:
        if os.path.exists(path):
            print(f"✅ Found noVNC at: {path}")
            novnc_path = path
            break
    
    # If no noVNC path found, reinstall novnc
    if not novnc_path:
        print("⚠️  noVNC not found, installing...")
        print("="*60)
        run_install("sudo apt-get install -y novnc")
        print("="*60)
        
        # Check again
        for path in novnc_paths:
            if os.path.exists(path):
                print(f"✅ Found noVNC at: {path}")
                novnc_path = path
                break
        
        # If still not found, use websockify without web interface
        if not novnc_path:
            print("⚠️  noVNC path not found, using websockify without web UI")
            novnc_path = None
    
    log_path = os.path.expanduser("~/.novnc.log")
    
    # Kill any existing websockify process
    run("pkill -f websockify", check=False)
    time.sleep(1)
    
    # Start websockify in background
    if novnc_path:
        websockify_cmd = f"nohup websockify --web={novnc_path} 6080 localhost:5901 > {log_path} 2>&1 &"
        print(f"→ Starting: websockify --web={novnc_path} 6080 localhost:5901")
    else:
        # Run without --web parameter if noVNC not available
        websockify_cmd = f"nohup websockify 6080 localhost:5901 > {log_path} 2>&1 &"
        print(f"→ Starting: websockify 6080 localhost:5901 (without web UI)")
    
    os.system(websockify_cmd)
    
    # Wait and verify it started
    time.sleep(3)
    
    for attempt in range(5):
        result = run("pgrep -f websockify", check=False)
        if result.returncode == 0:
            # Double-check the port is listening
            port_check = run("netstat -tuln | grep :6080 || ss -tuln | grep :6080", check=False)
            if port_check.returncode == 0:
                print("✅ websockify started successfully on port 6080")
                if novnc_path:
                    print("✅ noVNC web interface is available")
                return
            else:
                print(f"⚠️  Attempt {attempt+1}: Port 6080 not ready yet, waiting...")
                time.sleep(2)
        else:
            print(f"⚠️  Attempt {attempt+1}: websockify process not found, waiting...")
            time.sleep(2)
    
    # If we get here, something went wrong
    print(f"❌ Warning: Could not verify websockify is running properly")
    print(f"📝 Check log file: {log_path}")
    if os.path.exists(log_path):
        print("\n--- Log output ---")
        with open(log_path) as f:
            print(f.read())
        print("--- End log ---\n")
    raise Exception("websockify failed to start properly")

def get_preview_url():
    """Get the GitHub Codespaces preview URL"""
    hostname = os.uname().nodename
    return f"https://{hostname}-6080.app.github.dev"

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
        print("      • Thunar File Manager, Archive Manager")
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
        print("   🍷 WINDOWS COMPATIBILITY:")
        print("      • Wine + Winetricks (Run Windows .exe files)")
        print("   📶 BLUETOOTH:")
        print("      • Blueman Bluetooth Manager")
        print("\n🖼️  Desktop icons have been created for all apps!")
        print("\n💡 Tips:")
        print("   • Use 'apt install <package>' to install more software")
        print("   • The desktop will NEVER disconnect or lock")
        print("   • All apps are available from the Applications menu")
        print("   • Double-click desktop icons to launch apps")
        print("="*60)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("💡 Try running the script again or check the logs")
        exit(1)

if __name__ == "__main__":
    main()
