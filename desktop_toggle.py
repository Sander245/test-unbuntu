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
    
    # Browser and useful apps
    app_packages = [
        "firefox",           # Web browser
        "mousepad",          # Text editor
        "thunar",            # File manager (usually comes with xfce4)
        "ristretto",         # Image viewer
        "xfce4-taskmanager", # Task manager
        "htop",              # Terminal system monitor
        "font-noto",         # Good fonts
        "adwaita-icon-theme", # Icons
        "papirus-icon-theme", # Nice icons
    ]
    
    print("🔍 Checking required packages...")
    
    all_packages = core_packages + app_packages
    
    # Check if vncserver is available
    if not shutil.which("vncserver") or not shutil.which("firefox"):
        print(f"📦 Installing packages...")
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
        start_vnc()
        start_novnc()
        
        print("\n" + "="*60)
        print("✅ Desktop is running!")
        print("="*60)
        print(f"🌐 Open in browser: {get_preview_url()}")
        print("🔐 VNC password: user123")
        print("\n📦 Installed Apps:")
        print("   • Firefox - Web Browser")
        print("   • Mousepad - Text Editor")
        print("   • Thunar - File Manager")
        print("   • Ristretto - Image Viewer")
        print("   • Task Manager - System Monitor")
        print("\n💡 Tips:")
        print("   • The desktop will NEVER disconnect or lock")
        print("   • Screen saver and user switching are completely disabled")
        print("   • Reconnect anytime using the same URL")
        print("="*60)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("💡 Try running the script again or check the logs")
        exit(1)

if __name__ == "__main__":
    main()
