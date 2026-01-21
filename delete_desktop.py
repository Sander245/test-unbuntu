import os
import subprocess
import shutil

def run(cmd, check=True):
    print(f"Running: {cmd}")
    subprocess.run(cmd, shell=True, check=check)

def kill_vnc():
    print("Stopping VNC server...")
    run("vncserver -kill :1", check=False)

def kill_websockify():
    print("Killing websockify (noVNC)...")
    run("pkill -f websockify", check=False)

def close_ports():
    print("Closing ports 5901 and 6080...")
    run("fuser -k 5901/tcp", check=False)
    run("fuser -k 6080/tcp", check=False)

def delete_configs():
    print("Removing VNC configuration files...")
    shutil.rmtree(os.path.expanduser("~/.vnc"), ignore_errors=True)
    novnc_log = os.path.expanduser("~/.novnc.log")
    if os.path.exists(novnc_log):
        os.remove(novnc_log)

def main():
    kill_vnc()
    kill_websockify()
    close_ports()
    delete_configs()
    print("Desktop environment has been removed. All related services stopped and files deleted.")

if __name__ == "__main__":
    main()
