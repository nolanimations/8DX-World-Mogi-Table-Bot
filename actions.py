import os
import re
import time
import base64
import pyperclip
import win32clipboard
from datetime import datetime
from io import BytesIO
import customtkinter

from PIL import Image, ImageGrab
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import pywinstyles

import obs_handler
import selenium_handler

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# --- SPEED HELPERS ---

def _normalize_scores_text(s: str) -> str:
    """Normalize Lorenzi textarea content to compare meaningfully."""
    if not s:
        return ""
    s = s.replace("\r", "").strip()
    # Trim trailing spaces per line but keep order; Lorenzi cares about lines
    return "\n".join(line.rstrip() for line in s.split("\n"))

def _get_table_img_el(driver, game_mode):
    if game_mode == "MKWorld":
        return driver.find_element(By.XPATH, "//img[starts-with(@src, 'data:image/png;base64,')]")
    else:
        images = driver.find_elements(By.TAG_NAME, "img")
        return images[7]

def get_table_image_src(app):
    try:
        img = _get_table_img_el(app.driver, app.game_mode)
        return img.get_attribute("src") or ""
    except Exception:
        return ""

def set_textarea_and_dispatch(app, new_text):
    """Make textarea editable, set value, dispatch events."""
    ta = app.driver.find_element(By.TAG_NAME, "textarea")
    app.driver.execute_script("""
        const ta = arguments[0], v = arguments[1];
        if (ta.readOnly) ta.readOnly = false;
        if (ta.disabled) ta.disabled = false;
        if (ta.value === v) {
          // No change, do nothing
          return;
        }
        ta.value = v;
        ta.dispatchEvent(new Event('input', {bubbles:true}));
        ta.dispatchEvent(new Event('change', {bubbles:true}));
    """, ta, new_text)

def wait_for_table_image_change_async(app, previous_src, timeout_ms=5000):
    """Prefer a page-side MutationObserver for instant wake-up."""
    try:
        img = _get_table_img_el(app.driver, app.game_mode)
    except Exception:
        return False
    try:
        return bool(app.driver.execute_async_script("""
            const img = arguments[0], prev = arguments[1], timeoutMs = arguments[2], done = arguments[3];
            function ready() {
              return img && img.src && img.src.startsWith('data:image/png;base64,')
                     && (!prev || img.src !== prev);
            }
            if (ready()) { done(true); return; }
            const obs = new MutationObserver(() => { if (ready()) { obs.disconnect(); done(true); }});
            obs.observe(img, { attributes: true, attributeFilter: ['src'] });
            setTimeout(() => { try { obs.disconnect(); } catch(e){} done(false); }, timeoutMs);
        """, img, previous_src, int(timeout_ms)))
    except Exception:
        return False

def wait_for_table_image_change(app, previous_src, timeout=6, poll_frequency=0.1):
    """Small timeout + fast poll; used as a fallback."""
    def changed(driver):
        try:
            img = _get_table_img_el(driver, app.game_mode)
            src = img.get_attribute("src") or ""
            if not src.startswith("data:image/png;base64,"):
                return False
            return (not previous_src) or (src != previous_src)
        except Exception:
            return False

    WebDriverWait(app.driver, timeout, poll_frequency=poll_frequency).until(changed)


def upload_screenshot(app):
    temp_screenshot_path = None
    try:
        if app.using_obs_virtual_cam:
            temp_screenshot_path = obs_handler.capture_image_from_obs_virtual_camera(app)
        else:
            screenshot = ImageGrab.grab()
            temp_screenshot_path = os.path.join(os.path.expanduser("~"), f"mogi_bot_temp_{datetime.now().strftime('%H%M%S')}.png")
            screenshot.save(temp_screenshot_path, format="PNG")

        if game_mode_needs_screenshot_button(app.game_mode):
            try:
                app.driver.find_element(By.CSS_SELECTOR, "input[type='file']")
            except NoSuchElementException:
                from_screenshot_button = WebDriverWait(app.driver, 10).until(
                    lambda d: d.find_element(By.XPATH, "//button[contains(., 'From screenshot')]")
                )
                app.driver.execute_script("arguments[0].click();", from_screenshot_button)
        
        upload_element = app.driver.find_element(By.CSS_SELECTOR, "input[type='file']")
        upload_element.send_keys(temp_screenshot_path)
        pywinstyles.set_opacity(app.ui.image_label, value=0.2)
        
        try:
            scores_area = WebDriverWait(app.driver, 12).until(
                lambda d: d.find_element(By.TAG_NAME, "textarea") if d.find_element(By.TAG_NAME, "textarea").get_attribute("value").strip() != "" else False
            )

            if app.game_mode == "MKWorld":
                wait_for_mkworld_stability(app.driver, scores_area)
            
            initial_scores_text = scores_area.get_attribute("value")

        except TimeoutException:
            print("OCR timed out or failed. Resetting view.")
            reset_main_image(app.ui)
            return

        scoresvalue = calculate_dc_points(app.dc_points, initial_scores_text)
        
        # Only force a re-render if the DC math actually changes the text
        if _normalize_scores_text(scoresvalue) != _normalize_scores_text(initial_scores_text):
            try:
                previous_src = get_table_image_src(app)
                set_textarea_and_dispatch(app, scoresvalue)
                changed = wait_for_table_image_change_async(app, previous_src, timeout_ms=5000)
                if not changed:
                    try:
                        wait_for_table_image_change(app, previous_src, timeout=5, poll_frequency=0.1)
                    except TimeoutException:
                        pass
            except NoSuchElementException:
                pass

        broke = "ÍÍÍ''Ý!|¡¡įįį [au] 0" in scoresvalue.replace("\n", "")
        if broke:
            pywinstyles.set_opacity(app.ui.image_label, value=1)
        else:
            update_main_image_from_driver(app)
            if app.autocopy == "Table":
                send_to_clipboard(app.currentimg)
            elif app.autocopy == "Scores":
                copy_scores_to_clipboard(scoresvalue, app.my_tag)

        update_screenshot_previews(app, temp_screenshot_path)
        
        if not broke:
            if app.obs_overlay_active:
                obs_handler.update_obs_overlay(app, scoresvalue)
            check_for_dc_points(app, scoresvalue)

    except (ValueError, FileNotFoundError) as e:
        print(f"Error during screenshot processing: {e}")
        reset_main_image(app.ui)
    finally:
        if temp_screenshot_path and os.path.exists(temp_screenshot_path):
            os.remove(temp_screenshot_path)

def game_mode_needs_screenshot_button(game_mode):
    return game_mode == "MKWorld"

def wait_for_mkworld_stability(driver, scores_area):
    last_line_count = -1
    stability_counter = 0
    required_stable_checks = 3
    for _ in range(10): 
        current_text = scores_area.get_attribute("value")
        current_line_count = len([line for line in current_text.split('\n') if line.strip()])
        if current_line_count == last_line_count and current_line_count > 0:
            stability_counter += 1
        else:
            stability_counter = 0
            last_line_count = current_line_count
        if stability_counter >= required_stable_checks:
            break
        time.sleep(1.5)

def update_main_image_from_driver(app):
    if app.game_mode == "MKWorld":
        image_element = app.driver.find_element(By.XPATH, "//img[starts-with(@src, 'data:image/png;base64,')]")
    else:
        images = app.driver.find_elements(By.TAG_NAME, "img")
        image_element = images[7]
    
    image_url = image_element.get_attribute("src")
    if image_url and image_url.startswith("data:image/png;base64,"):
        base64_data = image_url.split(",")[1]
        image_data = base64.b64decode(base64_data)
        img = Image.open(BytesIO(image_data))
        app.currentimg = img
        
        img_copy = img.copy()
        img_copy.thumbnail((600, 363))
        
        app.ui.tableimg.configure(dark_image=img_copy)
        pywinstyles.set_opacity(app.ui.image_label, value=1)

def update_screenshot_previews(app, temp_screenshot_path):
    with Image.open(temp_screenshot_path) as screenshot_image:
        cropped_image = screenshot_image.crop((795, 0, 1875, 1080))
        
    ss_ctk_image = customtkinter.CTkImage(dark_image=cropped_image, size=(300, 300))
    app.ui.recentss_image_label.configure(image=app.ui.currentss_image_label.cget("image"))
    app.ui.currentss_image_label.configure(image=ss_ctk_image)

def reset_main_image(ui):
    black_img = Image.new("RGB", (600, 363), color="black")
    ui.tableimg.configure(dark_image=black_img)
    pywinstyles.set_opacity(ui.image_label, value=1)

def set_dc_points(app):
    app.dc_points = app.ui.dc_points_field.get()
    
    if app.currentimg == 0:
        print("Cannot apply DC points, no table is active.")
        return

    pywinstyles.set_opacity(app.ui.image_label, value=0.2)

    scores_area = app.driver.find_element(By.TAG_NAME, "textarea")
    current_scores_text = scores_area.get_attribute("value")
    final_scores_text = calculate_dc_points(app.dc_points, current_scores_text)

    # FAST PATH: if nothing changes, skip re-render/waits
    if _normalize_scores_text(final_scores_text) == _normalize_scores_text(current_scores_text):
        # Keep downstream behavior consistent (overlay/clipboard/DC check)
        if app.obs_overlay_active:
            obs_handler.update_obs_overlay(app, final_scores_text)
        check_for_dc_points(app, final_scores_text)
        if app.autocopy == "Scores":
            copy_scores_to_clipboard(final_scores_text, app.my_tag)
        if app.autocopy == "Table":
            # Table PNG is already current; just copy it if requested
            send_to_clipboard(app.currentimg)
        pywinstyles.set_opacity(app.ui.image_label, value=1)
        return

    # SLOW PATH: apply text, wait for PNG to actually update
    previous_src = get_table_image_src(app)
    set_textarea_and_dispatch(app, final_scores_text)

    # First try MutationObserver wait (snappy), then fallback polling
    changed = wait_for_table_image_change_async(app, previous_src, timeout_ms=5000)
    if not changed:
        try:
            wait_for_table_image_change(app, previous_src, timeout=5, poll_frequency=0.1)
        except TimeoutException:
            pass

    update_main_image_from_driver(app)


    if app.obs_overlay_active:
        obs_handler.update_obs_overlay(app, final_scores_text)
    check_for_dc_points(app, final_scores_text)
    if app.autocopy == "Scores":
        copy_scores_to_clipboard(final_scores_text, app.my_tag)
    if app.autocopy == "Table":
        send_to_clipboard(app.currentimg)

def clear_all_scores(app):
    print("Clearing DC points and resetting table...")
    app.ui.dc_points_field.delete(0, "end")
    app.dc_points = ""
    reset_table(app)

def roomcrash(app):
    scores = app.driver.find_element(By.TAG_NAME, "textarea")
    scoresvalue = scores.get_attribute("value")
    scoresfr = {}
    pattern = re.compile(r"^(.*?) (?:\[\w{2}\] )?(\d+(\+\d+)*)$")
    for line in scoresvalue.split("\n"):
        match = pattern.match(line)
        if match:
            name = match.group(1).lstrip()
            score_str = match.group(2)
            score = sum(int(x) for x in score_str.split("+"))
            initial = name[0].upper()
            scoresfr[initial] = scoresfr.get(initial, 0) + score
            
    sortedscores = sorted(scoresfr.items(), key=lambda x: x[1], reverse=True)
    out = " ".join([f"{key}{value}" for key, value in sortedscores])
    app.ui.dc_points_field.delete(0, "end") 
    app.ui.dc_points_field.insert(0, out)
    app.dc_points = out

def fill_in_tags(app):
    scores = app.driver.find_element(By.TAG_NAME, "textarea")
    scoresvalue = scores.get_attribute("value")
    tags = set()
    pattern = re.compile(r"^(.*?) (?:\[\w{2}\] )?(\d+(\+\d+)*)$")
    for line in scoresvalue.split("\n"):
        match = pattern.match(line)
        if match:
            name = match.group(1).lstrip()
            initial = name[0].upper()
            tags.add(initial)
    
    out = "".join(sorted(list(tags)))
    app.ui.dc_points_field.insert("end", out)

def send_to_clipboard(currentimg):
    if not isinstance(currentimg, Image.Image):
        print("Cannot copy to clipboard, no valid image.")
        return
        
    output = BytesIO()
    currentimg.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]
    output.close()
    
    try:
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()
        print("Table image copied to clipboard.")
    except Exception as e:
        print(f"Failed to copy to clipboard: {e}")

def copy_scores_to_clipboard(scores_text, my_tag):
    scoresfr = {}
    pattern = re.compile(r"^(.*?) (?:\[\w{2}\] )?(\d+(\+\d+)*)$")
    for line in scores_text.split("\n"):
        match = pattern.match(line)
        if match:
            name = match.group(1).lstrip()
            score_str = match.group(2)
            score = sum(int(x) for x in score_str.split("+"))
            initial = name[0].upper()
            if initial == "8": initial = "B"
            scoresfr[initial] = scoresfr.get(initial, 0) + score
            
    sortedscores = sorted(scoresfr.items(), key=lambda x: x[1], reverse=True)
    total_score = sum(scoresfr.values())

    out = " || ".join([f"{'**' + key +'**' if key == my_tag else key} {value}" for key, value in sortedscores])
    if total_score > 0 and total_score % 82 == 0:
        out += f" || @{12 - int(total_score / 82)}"
    else:
        races_left = 12 - (int(total_score / 82) + (1 if total_score % 82 else 0))
        missing_pts = 82 - (total_score % 82) if total_score % 82 else 0
        if races_left < 12:
            out += f" || @{races_left} (missing {missing_pts} pts)"

    pyperclip.copy(out)
    print("Scores copied to clipboard.")

def check_for_dc_points(app, scores_text):
    total = 0
    pattern = re.compile(r"^(.*?) (?:\[\w{2}\] )?(\d+(\+\d+)*)$")
    for line in scores_text.split("\n"):
        match = pattern.match(line)
        if match:
            score_str = match.group(2)
            total += sum(int(x) for x in score_str.split("+"))
    
    if total <= 990 and total >= 910:
        app.dc_points = ""
        app.ui.dc_points_field.delete(0, "end")
        
    if total % 82 == 0:
        app.dc_score = 0
        app.ui.missing_points_label.configure(text="")
    else:
        app.dc_score = 82 - (total % 82)
        app.ui.missing_points_label.configure(text=f"Missing: {app.dc_score}pts")

def calculate_dc_points(dc_points_str, scoresvalue):
    dc_scores = dc_points_str.split()
    lines = scoresvalue.splitlines()
    dc_helper = {}
    for team in dc_scores:
        tag = team[0].upper()
        points = team[1:]
        dc_helper[tag] = points
        
    new_html = []
    added_tags = set()

    for line in lines:
        stripped_line = line.lstrip()
        if not stripped_line:
            continue
            
        processed_line = re.sub(r'\+\d+$', '', stripped_line)
        
        if dc_points_str:
            initial = processed_line[0].upper()
            if initial in dc_helper and initial not in added_tags:
                processed_line += "+" + dc_helper[initial]
                added_tags.add(initial)
        
        new_html.append(processed_line)

    return "\n".join(new_html)

def reset_table(app):
    try:
        scores = app.driver.find_element(By.TAG_NAME, "textarea")
        if app.game_mode == "MKWorld":
            app.driver.execute_script("arguments[0].value = ' ';", scores)
        else:
            scores.clear()
            scores.send_keys(" ")
    except NoSuchElementException:
        print("Textarea not found on page to reset.")

    reset_main_image(app.ui)
    
    if app.obs_overlay_active:
        obs_handler.reset_obs_overlay(app)
            
    app.currentimg = 0
    check_for_dc_points(app, " ")