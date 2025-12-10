import obspython as obs

# ==============================================================================
# 1. CONFIGURATION
# ==============================================================================
SOURCES = {
    "camera":   "Camera",
    "event":    "Sailor Event Seagame",
    "3d_main":  "SailorFish3D Main",
    "3d_sub":   "SailorFish3D Sub",
    "2d_main":  "2D Main",
    "2d_sub":   "2D Sub",
    "gameplay": "Gameplay Video"
}

# Camera Settings
CAM_SMALL_POS  = (1600.0, 840.0)
CAM_SMALL_SIZE = (320.0, 240.0)

# State Tracking
# 1 = Main Mode (Default)
# 2 = Sub Mode
CURRENT_MODE = 1 

# UI State
LATEST_LOG_MESSAGE = "Ready"
SAVED_SETTINGS = None

# ==============================================================================
# 2. UTILITIES
# ==============================================================================
def get_sceneitem_recursive(name):
    """Find SceneItem recursively (checks inside Groups)."""
    scene = obs.obs_frontend_get_current_scene()
    if not scene: return None
    
    scene_source = obs.obs_scene_from_source(scene)
    
    # 1. Check top level
    item = obs.obs_scene_find_source(scene_source, name)
    if item:
        obs.obs_source_release(scene)
        return item

    # 2. Check inside Groups
    items = obs.obs_scene_enum_items(scene_source)
    found_item = None
    
    for i in items:
        src = obs.obs_sceneitem_get_source(i)
        if src and obs.obs_source_is_group(src):
            group_scene = obs.obs_scene_from_source(src)
            target = obs.obs_scene_find_source(group_scene, name)
            if target:
                found_item = target
                break
    
    obs.sceneitem_list_release(items)
    obs.obs_source_release(scene)
    return found_item

def set_visible(name, visible):
    item = get_sceneitem_recursive(name)
    if item:
        obs.obs_sceneitem_set_visible(item, visible)

def is_visible(name):
    item = get_sceneitem_recursive(name)
    if item:
        return obs.obs_sceneitem_visible(item)
    return False

def apply_transform(name, width, height, x=None, y=None):
    item = get_sceneitem_recursive(name)
    if not item: return

    # Set Position
    if x is not None and y is not None:
        pos = obs.vec2()
        pos.x, pos.y = float(x), float(y)
        obs.obs_sceneitem_set_pos(item, pos)

    # Set Size (Bounds)
    bounds = obs.vec2()
    bounds.x, bounds.y = float(width), float(height)
    obs.obs_sceneitem_set_bounds_type(item, obs.OBS_BOUNDS_SCALE_INNER)
    obs.obs_sceneitem_set_bounds(item, bounds)
    obs.obs_sceneitem_set_alignment(item, 5) # Top-Left

def hide_all_except(keep_list=[]):
    """Hide all managed sources except those in keep_list."""
    for key, source_name in SOURCES.items():
        if source_name not in keep_list:
            set_visible(source_name, False)

def log_status(msg):
    """Log to script log and update UI variable."""
    global LATEST_LOG_MESSAGE
    print(f"[OBS Script] {msg}")
    LATEST_LOG_MESSAGE = msg
    # Note: We cannot force UI refresh easily from hotkey thread, 
    # but updating the variable allows it to show on next refresh.

# ==============================================================================
# 3. ACTIONS (SCENES 1-8)
# ==============================================================================
def action_1(pressed):
    if not pressed: return
    log_status("Triggered: Action 1 (Main Mode)")
    global CURRENT_MODE
    CURRENT_MODE = 1 # Set Main Mode
    
    # 1. Camera (Small) + Event + 3D Main
    hide_all_except([SOURCES["camera"], SOURCES["event"], SOURCES["3d_main"]])
    
    # Restore Transforms (in case coming from Grid)
    apply_transform(SOURCES["event"], 1920, 1080, 0, 0)
    apply_transform(SOURCES["3d_main"], 1920, 1080, 0, 0)
    
    set_visible(SOURCES["camera"], True)
    apply_transform(SOURCES["camera"], CAM_SMALL_SIZE[0], CAM_SMALL_SIZE[1], CAM_SMALL_POS[0], CAM_SMALL_POS[1])
    
    set_visible(SOURCES["event"], True)
    set_visible(SOURCES["3d_main"], True)

def action_2(pressed):
    if not pressed: return
    log_status("Triggered: Action 2 (Sub Mode)")
    global CURRENT_MODE
    CURRENT_MODE = 2 # Set Sub Mode
    
    # 2. Camera (Small) + Event + 3D Sub
    hide_all_except([SOURCES["camera"], SOURCES["event"], SOURCES["3d_sub"]])
    
    # Restore Transforms
    apply_transform(SOURCES["event"], 1920, 1080, 0, 0)
    apply_transform(SOURCES["3d_sub"], 1920, 1080, 0, 0)
    
    set_visible(SOURCES["camera"], True)
    apply_transform(SOURCES["camera"], CAM_SMALL_SIZE[0], CAM_SMALL_SIZE[1], CAM_SMALL_POS[0], CAM_SMALL_POS[1])
    
    set_visible(SOURCES["event"], True)
    set_visible(SOURCES["3d_sub"], True)

def action_3(pressed):
    if not pressed: return
    log_status("Triggered: Action 3 (2D Main)")
    # 3. 2D Main Only
    hide_all_except([SOURCES["2d_main"]])
    
    # Restore Transforms
    apply_transform(SOURCES["2d_main"], 1920, 1080, 0, 0)
    
    set_visible(SOURCES["2d_main"], True)

def action_4(pressed):
    if not pressed: return
    log_status("Triggered: Action 4 (2D Sub)")
    # 4. 2D Sub Only
    hide_all_except([SOURCES["2d_sub"]])
    
    # Restore Transforms
    apply_transform(SOURCES["2d_sub"], 1920, 1080, 0, 0)
    
    set_visible(SOURCES["2d_sub"], True)

def action_5(pressed):
    if not pressed: return
    log_status("Triggered: Action 5 (Camera Full)")
    # 5. Camera Full Screen
    hide_all_except([SOURCES["camera"]])
    
    set_visible(SOURCES["camera"], True)
    apply_transform(SOURCES["camera"], 1920, 1080, 0, 0)

def action_6(pressed):
    if not pressed: return
    log_status("Triggered: Action 6 (Gameplay)")
    # 6. Gameplay Video
    hide_all_except([SOURCES["gameplay"]])
    
    # Restore Transforms
    apply_transform(SOURCES["gameplay"], 1920, 1080, 0, 0)
    
    set_visible(SOURCES["gameplay"], True)

def action_7(pressed):
    if not pressed: return
    log_status("Triggered: Action 7 (Toggle Event)")
    # 7. Toggle Event (Independent)
    current = is_visible(SOURCES["event"])
    set_visible(SOURCES["event"], not current)
    # Ensure it's full screen if we toggle it on
    if not current:
        apply_transform(SOURCES["event"], 1920, 1080, 0, 0)

def action_8(pressed):
    if not pressed: return
    log_status(f"Triggered: Action 8 (Grid Layout) [Mode: {CURRENT_MODE}]")
    # 8. GRID LAYOUT (4 Quadrants)
    # Q1 (TL): Event + (3D Main/Sub)
    # Q2 (TR): Camera
    # Q3 (BL): (2D Main/Sub)
    # Q4 (BR): Gameplay
    
    # Determine sources based on Mode
    s_3d = SOURCES["3d_main"] if CURRENT_MODE == 1 else SOURCES["3d_sub"]
    s_2d = SOURCES["2d_main"] if CURRENT_MODE == 1 else SOURCES["2d_sub"]
    
    hide_all_except([SOURCES["event"], s_3d, SOURCES["camera"], s_2d, SOURCES["gameplay"]])
    
    # Q1: Event + 3D (0, 0)
    set_visible(SOURCES["event"], True)
    apply_transform(SOURCES["event"], 960, 540, 0, 0)
    set_visible(s_3d, True)
    apply_transform(s_3d, 960, 540, 0, 0)
    
    # Q2: Camera (960, 0)
    set_visible(SOURCES["camera"], True)
    apply_transform(SOURCES["camera"], 960, 540, 960, 0)
    
    # Q3: 2D (0, 540)
    set_visible(s_2d, True)
    apply_transform(s_2d, 960, 540, 0, 540)
    
    # Q4: Gameplay (960, 540)
    set_visible(SOURCES["gameplay"], True)
    apply_transform(SOURCES["gameplay"], 960, 540, 960, 540)

# ==============================================================================
# 4. HOTKEY REGISTRATION
# ==============================================================================
hotkeys = {}

def register_hotkey(settings, id_name, desc, callback):
    hk = obs.obs_hotkey_register_frontend(id_name, desc, callback)
    saved = obs.obs_data_get_array(settings, id_name)
    obs.obs_hotkey_load(hk, saved)
    obs.obs_data_array_release(saved)
    hotkeys[id_name] = hk

def script_load(settings):
    global SAVED_SETTINGS
    SAVED_SETTINGS = settings
    
    register_hotkey(settings, "htk_1", "Scene 1: Cam(S) + Event + 3D Main", action_1)
    register_hotkey(settings, "htk_2", "Scene 2: Cam(S) + Event + 3D Sub",  action_2)
    register_hotkey(settings, "htk_3", "Scene 3: 2D Main",                  action_3)
    register_hotkey(settings, "htk_4", "Scene 4: 2D Sub",                   action_4)
    register_hotkey(settings, "htk_5", "Scene 5: Camera Full",              action_5)
    register_hotkey(settings, "htk_6", "Scene 6: Gameplay Video",           action_6)
    register_hotkey(settings, "htk_7", "Scene 7: Toggle Event",             action_7)
    register_hotkey(settings, "htk_8", "Scene 8: Grid Layout (4 Views)",    action_8)

def script_save(settings):
    for name, hk in hotkeys.items():
        saved = obs.obs_hotkey_save(hk)
        obs.obs_data_set_array(settings, name, saved)
        obs.obs_data_array_release(saved)

# ==============================================================================
# 5. UI PROPERTIES
# ==============================================================================
def script_description():
    return """
    <h2>OBS Custom Switcher V3</h2>
    <p><b>Hotkeys & Actions:</b></p>
    <table border="1" style="border-collapse: collapse; width: 100%;">
      <tr style="background-color: #333; color: white;"><th>Key</th><th>Action</th></tr>
      <tr><td><b>1</b></td><td>Cam(S) + Event + 3D Main (Set Main Mode)</td></tr>
      <tr><td><b>2</b></td><td>Cam(S) + Event + 3D Sub (Set Sub Mode)</td></tr>
      <tr><td><b>3</b></td><td>2D Main</td></tr>
      <tr><td><b>4</b></td><td>2D Sub</td></tr>
      <tr><td><b>5</b></td><td>Camera Full</td></tr>
      <tr><td><b>6</b></td><td>Gameplay Video</td></tr>
      <tr><td><b>7</b></td><td>Toggle Event</td></tr>
      <tr><td><b>8</b></td><td>Grid Layout (4 Quadrants)</td></tr>
    </table>
    <br/>
    """

def script_properties():
    props = obs.obs_properties_create()
    
    # Status Log (Read-only Text)
    obs.obs_properties_add_text(props, "status_log", "Last Action:", obs.OBS_TEXT_DEFAULT)
    
    # Refresh Button (To manually update UI if needed)
    obs.obs_properties_add_button(props, "btn_refresh", "Refresh Status", lambda p,s: True)
    
    return props

def script_update(settings):
    # Called when settings change (e.g. user types in text field)
    # We can use this to sync our variable if needed, but here we just write TO settings
    obs.obs_data_set_string(settings, "status_log", LATEST_LOG_MESSAGE)
