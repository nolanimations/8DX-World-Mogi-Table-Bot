import customtkinter
import keyboard
import cv2
from PIL import Image

import config
import gui
import selenium_handler
import obs_handler
import actions
import mkw_dc_wizard

class MogiTableBot:
    def __init__(self):
        self.root = customtkinter.CTk()
        
        self.driver = None
        self.cap = None
        self.obs_overlay_window = None
        self.currentimg = 0
        self.dc_points = ""
        self.dc_score = 0
        
        self.load_and_apply_settings()
        
        customtkinter.set_appearance_mode("dark")
        theme_path = config.extract_theme()
        customtkinter.set_default_color_theme(theme_path)
        
        self.ui = gui.UIBuilder(self.root, self)
        self.ui.sync_settings()
        
        obs_handler.load_placeholders()

        self.driver = selenium_handler.reinitialize_driver(None, self.game_mode)
        self.update_main_table_image_on_startup()
        
        self.setup_hotkeys()
        self.initial_toggle_checks()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def load_and_apply_settings(self):
        settings = config.load_settings()
        self.hotkey = settings.get("hotkey", "Down")
        self.autocopy = settings.get("autocopy", "Disabled")
        self.using_obs_virtual_cam = settings.get("using_obs_virtual_cam", False)
        self.obs_overlay_active = settings.get("obs_overlay_active", False)
        self.game_mode = "MKWorld"
        self.my_tag = settings.get("my_tag", "")

    def update_main_table_image_on_startup(self):
        if self.game_mode == "MK8DX":
            try:
                actions.update_main_image_from_driver(self)
            except Exception as e:
                print(f"Could not get initial table image for MK8DX: {e}")
                actions.reset_main_image(self.ui)
        else:
            actions.reset_main_image(self.ui)

    def setup_hotkeys(self):
        try:
            if self.hotkey:
                keyboard.add_hotkey(self.hotkey, self.upload_screenshot_action)
        except ValueError:
            print(f"Failed to register hotkey '{self.hotkey}', resetting to default.")
            self.reset_and_apply_settings()
            keyboard.add_hotkey(self.hotkey, self.upload_screenshot_action)
            
    def initial_toggle_checks(self):
        if self.obs_overlay_active:
            obs_handler.toggle_obs(self)
        if self.using_obs_virtual_cam:
            self._update_virtual_cam_resource()

    def run(self):
        self.root.mainloop()

    def on_closing(self):
        config.save_settings(self)
        if self.driver:
            self.driver.quit()
        if self.cap:
            self.cap.release()
        self.root.destroy()

    def upload_screenshot_action(self):
        actions.upload_screenshot(self)
        
    def set_autocopy_action(self, choice):
        self.autocopy = choice
        
    def set_my_tag_action(self):
        self.my_tag = self.ui.my_tag_field.get().strip().upper()
        if self.obs_overlay_active:
            scores_text = self.driver.find_element("tag name", "textarea").get_attribute("value")
            obs_handler.update_obs_overlay(self, scores_text)

    def set_dc_points_action(self):
        actions.set_dc_points(self)
        
    def clear_all_scores_action(self):
        actions.clear_all_scores(self)

    def roomcrash_action(self):
        actions.roomcrash(self)
        
    def fill_in_tags_action(self):
        actions.fill_in_tags(self)
        
    def copy_table_action(self):
        actions.send_to_clipboard(self.currentimg)

    def copy_scores_action(self):
        scores_text = self.driver.find_element("tag name", "textarea").get_attribute("value")
        actions.copy_scores_to_clipboard(scores_text, self.my_tag)
        
    def reset_table_action(self):
        actions.reset_table(self)

    def change_hotkey_action(self):
        self.ui.update_hotkey_status("Listening...")
        self.root.bind("<Key>", self.set_hotkey_event)

    def set_hotkey_event(self, event):
        self.root.unbind("<Key>")
        if self.hotkey:
            keyboard.remove_hotkey(self.hotkey)
        
        if event.keysym == "Escape":
            self.hotkey = None
        else:
            self.hotkey = event.keysym
            keyboard.add_hotkey(self.hotkey, self.upload_screenshot_action)
            
        self.ui.update_hotkey_status(self.hotkey)

    def toggle_obs_action(self):
        obs_handler.toggle_obs(self)

    def close_obs_action(self):
        obs_handler.close_obs(self)
        
    def toggle_obs_virtual_cam_action(self):
        self.using_obs_virtual_cam = not self.using_obs_virtual_cam
        self._update_virtual_cam_resource()
    
    def _update_virtual_cam_resource(self):
        if self.using_obs_virtual_cam:
            try:
                obs_cam_index = obs_handler.get_obs_virtual_cam_index()
                self.cap = cv2.VideoCapture(obs_cam_index)
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
                print("OBS Virtual Camera enabled and resource created.")
            except (ValueError, Exception) as e:
                print(f"Error enabling OBS Virtual Cam: {e}")
                self.using_obs_virtual_cam = False
                self.ui.using_obs_virtual_cam_checkbox.deselect()
        else:
            if self.cap:
                self.cap.release()
                self.cap = None
                print("OBS Virtual Camera disabled and resource released.")

    def reset_and_apply_settings(self):
        settings = config.reset_settings_file()
        self.load_and_apply_settings()
        self.ui.sync_settings()
    
    def open_dc_wizard_action(self):
        mkw_dc_wizard.open_dc_wizard(self)



if __name__ == "__main__":
    app = MogiTableBot()
    app.run()