import os
import subprocess
import getpass

def run(cmd, check=True):
    print(f"Running: {cmd}")
    subprocess.run(cmd, shell=True, check=check)

def install_packages():
    run("sudo apt update")
    run("sudo apt install -y xfce4 xfce4-goodies tightvncserver dbus-x11 novnc websockify")

def setup_vnc_password(password="user123"):
    os.makedirs(os.path.expanduser("~/.vnc"), exist_ok=True)
    passwd_file = os.path.expanduser("~/.vnc/passwd")
    if not os.path.exists(passwd_file):
        print("Setting VNC password...")
        proc = subprocess.Popen(["vncpasswd", "-f"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        stdout, _ = proc.communicate(input=f"{password}\n".encode())
        with open(passwd_file, "wb") as f:
            f.write(stdout)
        os.chmod(passwd_file, 0o600)

def create_xstartup():
    xstartup_path = os.path.expanduser("~/.vnc/xstartup")
    with open(xstartup_path, "w") as f:
        f.write("#!/bin/bash\nxrdb $HOME/.Xresources\nstartxfce4 &\n")
    os.chmod(xstartup_path, 0o755)

def start_vnc():
    run("vncserver -kill :1", check=False)
    run("vncserver :1")

def start_novnc():
    log_path = os.path.expanduser("~/.novnc.log")
    run(f"nohup websockify --web=/usr/share/novnc/ 6080 localhost:5901 > {log_path} 2>&1 &")

def main():
    install_packages()
    setup_vnc_password()
    create_xstartup()
    start_vnc()
    start_novnc()
    print("Desktop is ready!")
    print(f"Open in browser: https://{os.uname().nodename}-6080.githubpreview.dev")
    print("VNC password: user123")

if __name__ == "__main__":
    main()
