import os
import subprocess
import time

def run(cmd, check=True):
    print(f"→ {cmd}")
    subprocess.run(cmd, shell=True, check=check)

def kill_existing():
    print("🔻 Killing existing VNC and noVNC processes...")
    run("vncserver -kill :1", check=False)
    run("pkill Xtightvnc", check=False)
    run("pkill websockify", check=False)

    print("🧹 Removing stale lock files...")
    run("rm -f /tmp/.X1-lock", check=False)
    run("rm -f /tmp/.X11-unix/X1", check=False)

def setup_vnc_password(password="user123"):
    passwd_file = os.path.expanduser("~/.vnc/passwd")
    if not os.path.exists(passwd_file):
        print("🔐 Setting VNC password...")
        os.makedirs(os.path.expanduser("~/.vnc"), exist_ok=True)
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
    os.environ["USER"] = "root"
    run("vncserver :1")

def start_novnc():
    log_path = os.path.expanduser("~/.novnc.log")
    run(f"nohup websockify --web=/usr/share/novnc/ 6080 localhost:5901 > {log_path} 2>&1 &")
    time.sleep(2)

def main():
    kill_existing()
    setup_vnc_password()
    create_xstartup()
    start_vnc()
    start_novnc()
    print("\n✅ Desktop is running!")
    print(f"🌐 Open in browser: https://{os.uname().nodename}-6080.githubpreview.dev")
    print("🔐 VNC password: user123")

if __name__ == "__main__":
    main()
