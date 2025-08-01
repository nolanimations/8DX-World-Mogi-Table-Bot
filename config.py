import os
import json

def get_config_path():
    home_dir = os.path.expanduser("~")
    config_file = ".mogi_table_bot_v2_config.json"
    return os.path.join(home_dir, config_file)

def get_theme_path():
    home_dir = os.path.expanduser("~")
    return os.path.join(home_dir, ".mogi_table_bot_theme.json")

def extract_theme():
    theme_path = get_theme_path()
    
    if not os.path.exists(theme_path):
        theme = """
            {
        "CTk": {
            "fg_color": ["gray92", "gray14"]
        },
        "CTkToplevel": {
            "fg_color": ["gray92", "gray14"]
        },
        "CTkFrame": {
            "corner_radius": 6,
            "border_width": 0,
            "fg_color": ["gray86", "gray17"],
            "top_fg_color": ["gray81", "gray20"],
            "border_color": ["gray65", "gray28"]
        },
        "CTkButton": {
            "corner_radius": 6,
            "border_width": 0,
            "fg_color": ["#B288DA", "#9F7DB7"],
            "hover_color": ["#7E4B9C", "#693D82"],
            "border_color": ["#3E454A", "#949A9F"],
            "text_color": ["gray98", "#DCE4EE"],
            "text_color_disabled": ["gray78", "gray68"]
        },
        "CTkLabel": {
            "corner_radius": 0,
            "fg_color": "transparent",
            "text_color": ["gray10", "#DCE4EE"]
        },
        "CTkEntry": {
            "corner_radius": 6,
            "border_width": 2,
            "fg_color": ["#F9F9FA", "#343638"],
            "border_color": ["#979DA2", "#565B5E"],
            "text_color":["gray10", "#DCE4EE"],
            "placeholder_text_color": ["gray52", "gray62"]
        },
        "CTkCheckBox": {
            "corner_radius": 6,
            "border_width": 3,
            "fg_color": ["#B288DA", "#9F7DB7"],
            "border_color": ["#3E454A", "#949A9F"],
            "hover_color": ["#7E4B9C", "#693D82"],
            "checkmark_color": ["#DCE4EE", "gray90"],
            "text_color": ["gray10", "#DCE4EE"],
            "text_color_disabled": ["gray60", "gray45"]
        },
        "CTkSwitch": {
            "corner_radius": 1000,
            "border_width": 3,
            "button_length": 0,
            "fg_color": ["#939BA2", "#4A4D50"],
            "progress_color": ["#B288DA", "#9F7DB7"],
            "button_color": ["gray36", "#D5D9DE"],
            "button_hover_color": ["gray20", "gray100"],
            "text_color": ["gray10", "#DCE4EE"],
            "text_color_disabled": ["gray60", "gray45"]
        },
        "CTkRadioButton": {
            "corner_radius": 1000,
            "border_width_checked": 6,
            "border_width_unchecked": 3,
            "fg_color": ["#B288DA", "#9F7DB7"],
            "border_color": ["#3E454A", "#949A9F"],
            "hover_color":["#7E4B9C", "#693D82"],
            "text_color": ["gray10", "#DCE4EE"],
            "text_color_disabled": ["gray60", "gray45"]
        },
        "CTkProgressBar": {
            "corner_radius": 1000,
            "border_width": 0,
            "fg_color": ["#939BA2", "#4A4D50"],
            "progress_color": ["#B288DA", "#9F7DB7"],
            "border_color": ["gray", "gray"]
        },
        "CTkSlider": {
            "corner_radius": 1000,
            "button_corner_radius": 1000,
            "border_width": 6,
            "button_length": 0,
            "fg_color": ["#939BA2", "#4A4D50"],
            "progress_color": ["gray40", "#AAB0B5"],
            "button_color": ["#B288DA", "#9F7DB7"],
            "button_hover_color": ["#7E4B9C", "#693D82"]
        },
        "CTkOptionMenu": {
            "corner_radius": 6,
            "fg_color": ["#B288DA", "#9F7DB7"],
            "button_color": ["#9B75C1", "#8C6DA7"],
            "button_hover_color": ["#7E4B9C", "#693D82"],
            "text_color": ["gray98", "#DCE4EE"],
            "text_color_disabled": ["gray78", "gray68"]
        },
        "CTkComboBox": {
            "corner_radius": 6,
            "border_width": 2,
            "fg_color": ["#F9F9FA", "#343638"],
            "border_color": ["#979DA2", "#565B5E"],
            "button_color": ["#979DA2", "#565B5E"],
            "button_hover_color": ["#6E7174", "#7A848D"],
            "text_color": ["gray10", "#DCE4EE"],
            "text_color_disabled": ["gray50", "gray45"]
        },
        "CTkScrollbar": {
            "corner_radius": 1000,
            "border_spacing": 4,
            "fg_color": "transparent",
            "button_color": ["gray55", "gray41"],
            "button_hover_color": ["gray40", "gray53"]
        },
        "CTkSegmentedButton": {
            "corner_radius": 6,
            "border_width": 2,
            "fg_color": ["#979DA2", "gray29"],
            "selected_color": ["#B288DA", "#9F7DB7"],
            "selected_hover_color": ["#7E4B9C", "#693D82"],
            "unselected_color": ["#979DA2", "gray29"],
            "unselected_hover_color": ["gray70", "gray41"],
            "text_color": ["gray98", "#DCE4EE"],
            "text_color_disabled": ["gray78", "gray68"]
        },
        "CTkTextbox": {
            "corner_radius": 6,
            "border_width": 0,
            "fg_color": ["#F9F9FA", "gray23"],
            "border_color": ["#979DA2", "#565B5E"],
            "text_color":["gray10", "#DCE4EE"],
            "scrollbar_button_color": ["gray55", "gray41"],
            "scrollbar_button_hover_color": ["gray40", "gray53"]
        },
        "CTkScrollableFrame": {
            "label_fg_color": ["gray78", "gray23"]
        },
        "DropdownMenu": {
            "fg_color": ["gray90", "gray20"],
            "hover_color": ["gray75", "gray28"],
            "text_color": ["gray10", "gray90"]
        },
        "CTkFont": {
            "macOS": {
            "family": "SF Display",
            "size": 13,
            "weight": "normal"
            },
            "Windows": {
            "family": "Roboto",
            "size": 13,
            "weight": "normal"
            },
            "Linux": {
            "family": "Roboto",
            "size": 13,
            "weight": "normal"
            }
        }
        }"""
        with open(theme_path, "w") as theme_file:
            theme_file.write(theme)
    return theme_path

def get_default_settings():
    return {
        "hotkey": "Down",
        "autocopy": "Disabled",
        "using_obs_virtual_cam": False,
        "obs_overlay_active": False,
        "game_mode": "MKWorld",
        "my_tag": ""
    }

def load_settings():
    config_path = get_config_path()
    defaults = get_default_settings()
    
    if not os.path.exists(config_path):
        return defaults

    try:
        with open(config_path, "r") as file:
            settings = json.load(file)
            for key, value in defaults.items():
                if key not in settings:
                    settings[key] = value
            return settings
    except (json.JSONDecodeError, Exception):
        return defaults

def save_settings(app_state):
    config_path = get_config_path()
    settings = {
        "hotkey": app_state.hotkey,
        "autocopy": app_state.autocopy,
        "using_obs_virtual_cam": app_state.using_obs_virtual_cam,
        "obs_overlay_active": app_state.obs_overlay_active,
        "game_mode": app_state.game_mode,
        "my_tag": app_state.my_tag
    }
    with open(config_path, "w") as file:
        json.dump(settings, file)

def reset_settings_file():
    config_path = get_config_path()
    settings = get_default_settings()
    with open(config_path, "w") as file:
        json.dump(settings, file)
    return settings