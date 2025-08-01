import os
import cv2
import customtkinter
from pygrabber.dshow_graph import FilterGraph
from datetime import datetime
import re
from PIL import Image, ImageGrab, ImageTk
from io import BytesIO
import base64

placeholder_2v2_data = b"""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"""
placeholder_3v3_data = b"""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"""
placeholder_4v4_data = b"""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"""

placeholder_2v2_imagetk = None
placeholder_3v3_imagetk = None
placeholder_4v4_imagetk = None

def load_placeholders():
    global placeholder_2v2_imagetk, placeholder_3v3_imagetk, placeholder_4v4_imagetk
    placeholder_2v2_imagetk = ImageTk.PhotoImage(Image.open(BytesIO(base64.b64decode(placeholder_2v2_data))))
    placeholder_3v3_imagetk = ImageTk.PhotoImage(Image.open(BytesIO(base64.b64decode(placeholder_3v3_data))))
    placeholder_4v4_imagetk = ImageTk.PhotoImage(Image.open(BytesIO(base64.b64decode(placeholder_4v4_data))))

def get_obs_virtual_cam_index():
    try:
        graph = FilterGraph()
        devices = graph.get_input_devices()
        for index, name in enumerate(devices):
            if "OBS Virtual Camera" in name:
                return index
        raise ValueError("OBS Virtual Camera not found (make sure OBS is installed and running)")
    except Exception as e:
        print(f"Error accessing camera devices: {e}")
        raise ValueError("Could not find camera devices. Pygrabber might have issues.")

def capture_image_from_obs_virtual_camera(app):
    if not app.cap:
        raise ValueError("OBS Capture device not initialized.")
    
    # Read a few frames to clear the buffer and get the latest image
    for _ in range(3):
        app.cap.read()

    ret, frame = app.cap.read()
    if not ret:
        raise ValueError("Couldn't capture frame from OBS Virtual Camera.")

    height, width, _ = frame.shape
    if width != 1920 or height != 1080:
        raise ValueError(f"Screenshot is not 1920x1080 (it's {width}x{height}). Check OBS settings.")

    temp_screenshot_path = os.path.join(os.path.expanduser("~"), datetime.now().strftime("%Y-%m-%d_%H-%M-%S.png"))
    cv2.imwrite(temp_screenshot_path, frame)
    return temp_screenshot_path

def toggle_obs(app):
    if not app.obs_overlay_active:
        app.obs_overlay_window = customtkinter.CTkToplevel()
        app.obs_overlay_window.geometry("780x125")
        app.obs_overlay_window.title("Scores Overlay")
        app.obs_overlay_window.resizable(False, False)
        app.obs_overlay_window.configure(fg_color="green")
        app.obs_overlay_window.iconphoto(True, app.ui.icon)
        
        app.obs_overlay_window.protocol("WM_DELETE_WINDOW", app.close_obs_action)
        
        app.obs_overlay_active = True
        app.ui.obs_overlay_checkbox.select()
        
        if app.currentimg != 0:
            scores_text = app.driver.find_element("tag name", "textarea").get_attribute("value")
            update_obs_overlay(app, scores_text)
        else: 
            reset_obs_overlay(app)
            
    else:
        close_obs(app)

def close_obs(app):
    if app.obs_overlay_window:
        app.obs_overlay_window.destroy()
    app.obs_overlay_window = None
    app.obs_overlay_active = False
    app.ui.obs_overlay_checkbox.deselect()

def update_obs_overlay(app, scores_text):
    if not app.obs_overlay_active or not app.obs_overlay_window:
        return

    scoresfr = {}
    pattern = re.compile(r"^(.*?) (?:\[\w{2}\] )?(\d+(\+\d+)*)$")
    for line in scores_text.split("\n"):
        match = pattern.match(line)
        if match:
            name = match.group(1).lstrip()
            score_str = match.group(2)
            score = sum(int(x) for x in score_str.split("+"))

            initial = name[0].upper()
            if initial == "8":
                initial = "B"
            scoresfr[initial] = scoresfr.get(initial, 0) + score

    sortedscores = sorted(scoresfr.items(), key=lambda x: x[1], reverse=True)
    total_score = sum(scoresfr.values())
    
    if total_score == 0:
        races_left = "@12"
        missingpoints = 0
    elif total_score % 82 == 0:
        races_left = f"@{12 - int(total_score / 82)}"
        missingpoints = 0
    else:
        races_left = f"@{12 - (int(total_score / 82) + 1)}"
        missingpoints = 82 - (total_score % 82)

    tags = [k for k, _ in sortedscores]
    teamscores = [v for _, v in sortedscores]
    if len(tags) > 6:
        tags, teamscores = tags[:6], teamscores[:6]
    elif len(tags) == 5:
        tags, teamscores = tags[:4], teamscores[:4]

    if len(tags) >= 5: bg_img, width, pos_count = placeholder_2v2_imagetk, 780, 6
    elif len(tags) == 4: bg_img, width, pos_count = placeholder_3v3_imagetk, 520, 4
    elif len(tags) == 3: bg_img, width, pos_count = placeholder_4v4_imagetk, 390, 3
    elif len(tags) == 2: bg_img, width, pos_count = placeholder_4v4_imagetk, 390, 2
    else:
        reset_obs_overlay(app)
        return

    positions = [(((i * (width / pos_count)) + (width / pos_count / 2)), 22, 67) for i in range(pos_count)]
    if pos_count == 3 or pos_count == 2:
        xs = [65, 195, 325]
        positions = [(xs[i], 22, 67) for i in range(pos_count)]


    canvas = customtkinter.CTkCanvas(master=app.obs_overlay_window, width=780, height=125, bg="green", highlightthickness=0)
    canvas.place(x=0, y=0)
    
    x_off = (780 - width) // 2
    canvas.create_image((x_off, 0), image=bg_img, anchor="nw")

    for i in range(len(tags)):
        tag = tags[i]
        x, y_tag, y_score = positions[i]
        color = "magenta" if tag == app.my_tag else "white"
        display_tag = f"*{tag}*" if tag == app.my_tag else tag
        canvas.create_text((x_off + x, y_tag), text=display_tag, font=app.ui.tagsfont, anchor="center", fill=color)
        canvas.create_text((x_off + x, y_score), text=str(teamscores[i]), font=app.ui.scoresfont, anchor="center", fill="white")

    for i in range(len(tags) - 1):
        x1, _, _ = positions[i]
        x2, _, _ = positions[i+1]
        diff = abs(teamscores[i] - teamscores[i+1])
        canvas.create_text((x_off + (x1 + x2) / 2, 90 + 35 // 2), text=f"+{diff}", font=app.ui.smallerfont, anchor="center", fill="white")

    canvas.create_text((x_off + width - 60, 90 + 35 // 2), text=races_left, font=app.ui.smallerfont, anchor="center", fill="medium purple")
    if missingpoints:
        canvas.create_text((x_off + 40, 90 + 35 // 2), text=f"-{missingpoints}", font=app.ui.smallerfont, anchor="center", fill="red")

def reset_obs_overlay(app):
    if not app.obs_overlay_active or not app.obs_overlay_window:
        return
        
    canvas = customtkinter.CTkCanvas(master=app.obs_overlay_window, width=780, height=125, bg="green", highlightthickness=0)
    canvas.place(x=0, y=0)
    canvas.create_image((0, 0), image=placeholder_2v2_imagetk, anchor="nw")
    
    for i in range(6):
        x_position = (i * 130) + 65
        canvas.create_text((x_position, 22), text="-", font=app.ui.tagsfont, anchor="center", fill="white")
        canvas.create_text((x_position, 67), text="0", font=app.ui.scoresfont, anchor="center", fill="white")
    
    for i in range(5):
        x1 = (i * 130) + 65
        x2 = ((i + 1) * 130) + 65
        diff_x = (x1 + x2) / 2
        canvas.create_text((diff_x, 90 + 17), text="+0", font=app.ui.smallerfont, anchor="center", fill="white")
    
    canvas.create_text((720, 90 + 17), text="@12", font=app.ui.smallerfont, anchor="center", fill="medium purple")