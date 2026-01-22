# 🖥️ Codespace Desktop Environment (Debian)

A full XFCE desktop environment running in GitHub Codespaces with tons of pre-installed applications!

**Now using Debian with full APT support!** 🎉

## 🚀 Quick Start

1. Press `Ctrl+Shift+\`` to open terminal
2. Run `python3 desktop_toggle.py`
3. Wait for it to start (first run installs packages - takes a few minutes)
4. Open Ports tab and hover over port `6080`
5. Click the globe icon (or open the link)
6. Enter password: `user123`

---

## 📦 Installed Applications

| Category | Applications |
|----------|-------------|
| 🌐 **Browsers** | Firefox ESR, Chromium |
| 📁 **File Management** | Thunar, Archive Manager (File Roller) |
| 📝 **Office** | LibreOffice Writer/Calc/Impress, PDF Viewer (Evince), Calculator |
| ✏️ **Text Editors** | Mousepad, Geany IDE |
| 🎨 **Graphics** | GIMP, Inkscape, Image Viewer (Ristretto) |
| 🎬 **Media** | VLC Media Player, Audacious Music Player |
| 🔧 **System Tools** | Task Manager, System Monitor, Disk Analyzer, GParted, Flameshot |
| 💻 **Development** | Meld (diff/merge), Gitg (Git GUI), Git |
| 🌐 **Network** | Transmission (BitTorrent), FileZilla (FTP) |
| 🍷 **Windows** | Wine + Winetricks (run .exe files) |
| 📶 **Bluetooth** | Blueman Bluetooth Manager |

### Compression Support
ZIP, 7-Zip, TAR, GZIP, BZIP2, XZ, RAR

---

## 📥 Installing More Software

**This is Debian - use APT!**

```bash
# Update package lists
sudo apt update

# Install any package
sudo apt install <package-name>

# Search for packages
apt search <keyword>

# Examples:
sudo apt install steam           # Steam gaming
sudo apt install kdenlive        # Video editor
sudo apt install obs-studio      # Screen recording
sudo apt install discord         # Discord (needs manual download)
sudo apt install spotify-client  # Spotify
```

---

## 🎮 Install Steam

```bash
# Enable 32-bit architecture (required for Steam)
sudo dpkg --add-architecture i386
sudo apt update

# Install Steam
sudo apt install steam
```

---

## 🍷 Wine - Run Windows Applications

Wine is pre-installed with Winetricks!

```bash
# Configure Wine
winecfg

# Run a Windows executable
wine /path/to/program.exe

# Install Windows components with Winetricks
winetricks

# Install common Windows libraries
winetricks vcrun2019 dotnet48 corefonts
```

---

## 🔧 Troubleshooting

### Reinstall All Packages

```bash
sudo apt update && sudo apt install -y \
    tigervnc-standalone-server tigervnc-common novnc websockify \
    xfce4 xfce4-terminal xfce4-goodies thunar \
    firefox-esr chromium \
    libreoffice-writer libreoffice-calc libreoffice-impress evince galculator \
    gimp inkscape vlc audacious ristretto \
    gnome-system-monitor gparted baobab flameshot \
    geany meld gitg transmission-gtk filezilla \
    wine wine64 winetricks \
    bluetooth bluez blueman
```

### Restart Desktop

```bash
python3 desktop_toggle.py
```

### Manual VNC Commands

```bash
# Start VNC Server
vncserver :1 -geometry 1920x1080 -depth 24

# Start noVNC
websockify --web=/usr/share/novnc 6080 localhost:5901 &

# Kill VNC
vncserver -kill :1
pkill websockify
```

---

## 💡 Tips

- **Use APT** - `sudo apt install <package>` works for everything!
- **Screen never locks** - Screensaver and lock screen are disabled
- **Reconnect anytime** - Just open the same URL again
- **Chromium note** - Runs with `--no-sandbox` flag for compatibility
- **Run Windows apps** - `wine filename.exe`

---

## ❓ FAQ

**Q: How do I install software?**  
A: Use `sudo apt install package-name` - this is Debian!

**Q: Can I install Steam?**  
A: Yes! Run `sudo dpkg --add-architecture i386 && sudo apt update && sudo apt install steam`

**Q: Apps show "Failed to run" error?**  
A: Run `python3 desktop_toggle.py` again to reinstall packages.

**Q: How to run .exe files?**  
A: Use `wine filename.exe` or configure with `winecfg`