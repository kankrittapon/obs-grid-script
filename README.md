# OBS Grid Script

A custom Python script for OBS Studio that manages scene visibility, transforms, and grid layouts with hotkey support.

## Features

- **Scene Switching (Keys 1-7)**: Instantly switch between different source configurations (Camera, Event, 3D Models, 2D Models).
- **Grid Layout (Key 8)**: Automatically arranges sources into a 4-quadrant grid.
- **State Tracking**: Remembers if you are in "Main Mode" or "Sub Mode" and adapts the Grid Layout accordingly.
- **UI Feedback**: Displays the last triggered action and a hotkey reference table directly in the OBS Scripts window.

## Hotkeys

| Key | Action | Description |
| :--- | :--- | :--- |
| **1** | Main Mode | Camera (Small) + Event + 3D Main |
| **2** | Sub Mode | Camera (Small) + Event + 3D Sub |
| **3** | 2D Main | Show 2D Main Model only |
| **4** | 2D Sub | Show 2D Sub Model only |
| **5** | Camera Full | Show Camera Full Screen |
| **6** | Gameplay | Show Gameplay Video |
| **7** | Toggle Event | Toggle Event visibility |
| **8** | Grid Layout | Show 4-Quadrant Grid (Content depends on Mode 1/2) |

## Installation

1.  Open OBS Studio.
2.  Go to **Tools** -> **Scripts**.
3.  Click the **+** button and select `obs-script-v3.py`.
4.  Go to **Settings** -> **Hotkeys**.
5.  Search for "Scene" and assign keys 1-8 to the corresponding script actions.

## Requirements

Ensure your OBS Scene has sources named exactly as follows:
- `Camera`
- `Sailor Event Seagame`
- `SailorFish3D Main`
- `SailorFish3D Sub`
- `2D Main`
- `2D Sub`
- `Gameplay Video`

## Window Title Changer Tool

Included is a helper tool `window-title-changer.py` to help you rename application windows so OBS can distinguish between multiple instances of the same program.

### Usage
1.  Run the script:
    ```bash
    python window-title-changer.py
    ```
2.  **Search**: Type to filter the list of open windows.
3.  **Select**: Click on the window you want to rename.
4.  **Rename**: Enter a new title and click **Rename**.
5.  **Restore**: Click **Restore Original** to revert changes (only available if you renamed it in the current session).

