# LudexHub

A lightweight, keyboard-driven game launcher for Windows. Searches and launches games across **Steam**, **Epic Games**, and **GOG** from a single search bar.

<p align="center">
  <img width="541" height="358" alt="LudexHub screenshot" src="https://github.com/user-attachments/assets/4248ec2d-506c-43bd-b397-512961d3fa3a" />
</p>

![Python](https://img.shields.io/badge/Python-3.12+-blue?logo=python)
![PySide6](https://img.shields.io/badge/PySide6-6.6+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Features

- **Unified Library** — Scans Steam, Epic Games, and GOG Galaxy in one place
- **Fuzzy Search** — Find games instantly with weighted fuzzy matching
- **Global Hotkey** — Open with `Alt+Space` (configurable), suppresses keystrokes
- **Favorites & Sorting** — Star your favorite games, they appear first; everything else sorted A-Z
- **Game Icons** — Async capsule art download with disk + memory cache
- **System Tray** — Lives quietly in the tray, opens on demand
- **Customizable UI** — Font, window position, size, opacity all configurable
- **Launcher Paths** — Manual path overrides for non-standard installs
- **Start with Windows** — Optional startup via Windows Startup folder shortcut
- **Fade Animations** — Smooth fade-in/fade-out transitions

## Controls

| Key | Action |
|-----|--------|
| `Alt+Space` | Open/Close launcher |
| `↑` `↓` | Navigate game list |
| `Enter` | Launch selected game |
| `Escape` | Close launcher |
| Right-click | Toggle favorite |

## Installation

### Download

Download `LudexHub.exe` from [Releases](https://github.com/Bharathraj-K/LudexHub/releases/tag/v1.0) and run it. No installation required.

### Build from Source

```bash
# Clone the repo
git clone https://github.com/Bharathraj-K/LudexHub
cd LudexHub

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run in dev mode
python main.py

# Build standalone exe
python build.py
```

Output: `dist/LudexHub.exe`

## Dependencies

| Package | Purpose |
|---------|---------|
| [PySide6](https://pypi.org/project/PySide6/) | Qt6 GUI framework |
| [vdf](https://pypi.org/project/vdf/) | Steam VDF file parsing |
| [rapidfuzz](https://pypi.org/project/rapidfuzz/) | Fuzzy string matching |
| [keyboard](https://pypi.org/project/keyboard/) | Global hotkey registration |
| [PyInstaller](https://pypi.org/project/pyinstaller/) | Standalone exe packaging |

## Project Structure

```
LudexHub/
├── main.py                 # Entry point
├── core/
│   ├── paths.py            # Path resolution (dev + frozen)
│   ├── settings.py         # Settings load/save
│   ├── scanner.py          # Unified game scanner
│   ├── steam.py            # Steam library detection
│   ├── epic.py             # Epic Games scanning
│   ├── gog.py              # GOG Galaxy scanning
│   ├── search.py           # Fuzzy search engine
│   ├── launcher.py         # Game launch by platform
│   ├── hotkey.py           # Global hotkey manager
│   ├── favorites.py        # Favorites persistence
│   ├── recents.py          # Recent launches
│   ├── icon_loader.py      # Async icon downloader
│   └── startup.py          # Windows startup shortcut
├── ui/
│   ├── window.py           # Main launcher window
│   ├── results.py          # Game list with custom items
│   ├── styles.py           # Colors, theme, stylesheet
│   ├── tray.py             # System tray icon
│   ├── settings_dialog.py  # Settings UI
│   └── hotkey_dialog.py    # Hotkey capture dialog
├── models/
│   └── game.py             # Game dataclass
├── assets/
│   └── fonts/Orbitron.ttf  # Bundled font
├── data/
│   ├── icons/tray.ico      # Tray icon
│   ├── settings.json       # (runtime, gitignored)
│   ├── games.json          # Game cache
│   ├── favorites.json      # (runtime, gitignored)
│   └── recents.json        # (runtime, gitignored)
├── LudexHub.spec           # PyInstaller spec
├── build.py                # Build script
└── requirements.txt
```

## Configuration

Settings are stored in `data/settings.json` (next to the exe in release mode):

| Key | Default | Description |
|-----|---------|-------------|
| `hotkey` | `alt+space` | Global hotkey combination |
| `font_family` | `Orbitron` | UI font |
| `position` | `center` | Window position on screen |
| `window_width` | `750` | Window width in pixels |
| `window_height` | `500` | Window height in pixels |
| `window_opacity` | `0.92` | Window opacity (0.0 - 1.0) |
| `steam_path` | `""` | Custom Steam install path (empty = auto-detect) |
| `epic_path` | `""` | Custom Epic manifest dir (empty = auto-detect) |
| `gog_path` | `""` | Custom GOG database path (empty = auto-detect) |
| `start_with_windows` | `false` | Launch on Windows login |

## Platform Support

| Platform | Status |
|----------|--------|
| Steam | Full support (registry + library folders) |
| Epic Games | Full support (LauncherInstalled.dat + manifests) |
| GOG | Full support (Galaxy 2.0 SQLite database) |

## License

MIT
