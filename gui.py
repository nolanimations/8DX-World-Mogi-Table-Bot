import customtkinter
from PIL import Image, ImageTk
from io import BytesIO
import base64

class UIBuilder:
    def __init__(self, root, app):
        self.root = root
        self.app = app 
        
        self.icon_data = b"""AAABAAEAICAAAAEAIACoEAAAFgAAACgAAAAgAAAAQAAAAAEAIAAAAAAAABAAAMMOAADDDgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJgoUACRFkwAliJPIpMYTICEFlDKdC9n0l9hnXNFkNULTn/BAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAlBBHAJMQRRSXEkmuqA5P/LwDUv++BE3/myxu8GxxsmcA//8BWJDTAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKYACwCUAj0AkgI5PaIBP+7DAEz/1wBV/+AAV//YBFf/lkCG00p4tSReb64AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAWQAAAJcANACPADAxpQA45cIARv/RAE3/2QBS/+EAVv+5FV/8W0uEeADV/wE4X5gAQ2mfAEFnnQdFbKAeRWygGUFlngRDaJ8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAjQAsAI8AJAmMADSPigA6+4kAPP+KADr/lAA5/54COP9mJ1DcOFCFOFdMXgByDTwMSl+Re0t0o9hMdaPQSG+hdD9imQxCZ5wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAogAAALsAAAC8EwsArJwZAJ72GACm/xkAqv8iAJ7/OAB7/00KUf8xJWnFAgSQZGIIRn5JS3n0TXek/1F8pv9MdKLzRWmeaDBGjwFBY5sAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADgAAAAsAAAALIXAAC9uwAA0f8AAOD/AADr/wAA9f8AAPX/CQHZ/w0Ikf8HAVP5TQE09kgoTf9DZ5j/T3ml/1B5pf9JcKDhQmebSd///wA7XpQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACvAAAA/wAAAL8oAADGwQAA1f8AAOj/AAD2/wAA/v8AAP//AADz/wQAk/8/ACb/VQkk/z9Kd/9KcqL/UHqk/012of9FapzPPmGVLEFkmQAlXHoAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB/AAAAjgMBAHKKAACi/wAA1f8AAOj/AAD1/wAA/v8AAP7/AADu/x8Aev9TABv/RypP/0FlmP9Lc6H/S3Of/0Rqmv89Y5d/haz/ADZbiwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA3AAAAJQAAAC2TgEAbeQBAEf/AQCH/wAA0v8AAPb/AAD//wAA/v8AAPT/AwDb/z0ATv9nDC7/TUx9/0duo/9FbqD/Rmea/1RUiJDJAAABZTVkAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAuwAAAMBoAACu/AAAi/8CAF3/BABj/wQAlf8DAMf/AQ3o/wAd9f8AC/X/IACy/4kAPP+OE0X/eEN7/21Ujv+CPXf/pBdSenVYmQCyADgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA3gAAAP8AAADXHQAAxJwAALv9AADT/wAA2/8BALf/AwCH/wYAbf8DUJr/CMr3/weg8/8IGdH/ZQB5/8AATP/KAlH/ygZV/9UCUtPfAFAw3gBOAMsAdAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAM0AAADOCAAAy1QAAMjFAADA+wAAvP8AANH/AADi/wAA3v8CAtf/CAfM/wsrzf8Kaef/A2/Z/wMSnP8RAKD/ZQWm89sUgLr5EHaZ+wZzPP8AbQH/AHIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADIAAAAyhIAAMWGAADC7gAAwv8AAMD/AAC//wAAvv8EBLP/JiWi/1VUo/91dLn/fnvN/2Vi2P8tK+P/BAPy/wAA+f8CAf3XPRTgKf99ewT///8A/7X3AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAxgAAAMYQAADGlgAAy/kAAN3/AADi/wAAyf8AAMD/Bgav/0hHn/+NjKP/q6u1/7y8xP+5ucH/vr7J/7Ox1f9WVen/BQX+/wAA/vYAAPpiAAD/AAAA8QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADLAAAAxjsAANroAADy/wAA/PkAAOLxAAC++QEBsv9CQqD/lpeg/7GytP/Fxsj/09PW/5eXmv+qqa3/393i/8nG3/9BQPL/AAD//wAA/L8AAPYVAAD4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOEAAADXEAAA9V0AAP5yAAD5XgUTumYFFJjkHB6a/4aHnv+sraz/x8jI/9nZ2f/j4uP/2tnb/+Hg4v/u7O7/7+3t/5uZ7f8JCf3/AAD/9AAA/VIAAP0AAAD/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFWpsAAVSQAIhfY0/InmenxNKi/lNXYr/oaGi/7+/v//c3N3/6urq/+7u7v/y8vL/9/b3//r5+v/7+vr/1dPy/yEh9/8AAP//AAD+mwAA/wYAAP8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAARX3wAAAAAAiqKppA5pL7/HXGU/16Im/+trq3/0dHR/6ysrf+cnJz/5OTk//n5+f/7+vv/7e3t//v7+v/08/r0R0ftwQAA/fEAAP+1AAD/DgAA/wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAxbeAAAAAAAGnGORRx6mc0cmLX/ZJuk/7y7u/+qqqr/Hx8f/wgICP+NjY3//f39/7Ozs/9BQUH/rq6u/////uvKyvREAAD9SQAA/0AAAP8DAAD/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGmmEABFeexdBmK1fMpizzRunzP9slaL/wsHA/25ubv8AAAD/AAAA/1tbW//k5OT/Q0ND/wAAAP9qamr/9/f33fv7+yP5+fkAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD01PABYbEAAAcGgEFYmtWEfE3O8xst3/E6Hd/1SsyP+9xMT/aGdn/wAAAP8AAAD/a2tr/8XGxv8WFhb/AAAA/1tna//Y4uaq////Cvb39wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIjLwACI6/EQaFsY0LiLnOIq7i/SGp4/8kndL/HbHh/27N5f+PoKP/HRsZ/x8eHf+4uLf/wcHB/xIQEP8SHR7/MICO9V6ZrFgJaYQA6e/wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAia1AAHoNoUCInAlhJ5pqsRfrL4QrbZ/1Cy0f8SktP/F7Ds/0vD6v9rq7v/n77C/+/5+//j6ur/gYiI/1aPlf8ho7rZEnmXIhSEoQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABYm/AAWPxAEAh8gGFGmVcAt4q/0pnsn/KKDT/w2k6f8Nr/T/FKPj/zC87v9Iz/j/Xdb4/2fb9/9f2fX/L7jc/xyQrc0phpUYJ5WlAA4bUQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD5C8ABaUvQcLh7OGCo7F/Aue1/8PmND/Dafe/xir5f9PwM//NafO/xSk7P8PqvD/Fq7q/xe07f8Pksv/QZqn5mG5uS5cu7wAWoB/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB/nwASms4AE5PEIQ+azcodjrnyD1mm/wEWeP8GZqX/GqTc/1zH3/82pM3/DaXt/w2v9P9Bwef/TM3r/w6W0v8jia/rNJCtNDKPrgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA2VzAAMlMoGDpPHNCeOtlYNSp7aAAeO/wQvpv8MnOL/FZ7d/w6T1f8Mf7v/EZ7e/zW+5f87v+H/CoXH/QaDveQKfqVAA4XPAA91gQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGbZwAComiAgRemEwCQJq9CVqy/RCWzv8Rhs3/BDOa/wMSbv8NXKX/Dajk/w6Z0P8feKnZDn60ugmLuqAPhaYKDYetAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAWepoAGXGIBg+Aq2oUotfwEKfc/xBxuf8EHZL9ARSL/w9Yov8PjML/EpfJ40ObsV0WkcdWEJnSXQp2pQYNg7YAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAx+rQALd6UOC4CzURSWzqgNoN3kDo/Hvw1ppnoGY6WUH4e6hRSVx9wMndGhBnmcCBM+YQAAyvoAAMr6AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABijAAAAAABB3uvXgd+tVIMhLNqEYqvERqLnAQEdKYEDp/aQwyd2DT1//8AAILFAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA/8D///+Af///gH///4Aw//+AIH//gAA//4AAP//AAB//wAAf/8AAD//AAB//gAAf/gAAH/wAAH/4AAD/+AAAf/gAAH/+AAA//gAAP/8AAD/+AAH//AAB//gAA//4AAP/+AAD//wAA//8AAP//AAD//8AAf//gAH//4AP///AH/8="""
        
        self.tagsfont = customtkinter.CTkFont(family="FOT-NewRodin Pro B", size=32)
        self.scoresfont = customtkinter.CTkFont(family="DS-Digital", size=42, weight="bold")
        self.smallerfont = customtkinter.CTkFont(family="DS-Digital", size=30, weight="bold")
        
        self.setup_window()
        self.create_tabs()
        self.create_table_bot_tab()
        self.create_settings_tab()
        self.create_screenshots_tab()
        self.create_info_tab()

    def setup_window(self):
        self.root.geometry("820x700")
        self.root.minsize(820, 700)
        self.root.title("Mogi Table Bot")
        self.root.resizable(False, False)
        
        icon_image = Image.open(BytesIO(base64.b64decode(self.icon_data)))
        self.icon = ImageTk.PhotoImage(icon_image)
        self.root.wm_iconbitmap()
        self.root.iconphoto(True, self.icon)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def create_tabs(self):
        self.tabview = customtkinter.CTkTabview(self.root)
        self.tabview.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.tabview.add("Table Bot")
        self.tabview.add("Settings")
        self.tabview.add("Screenshots")
        self.tabview.add("Info")

    def create_table_bot_tab(self):
        tab = self.tabview.tab("Table Bot")
        self.image_label = customtkinter.CTkLabel(tab, text="")
        self.image_label.grid(row=0, column=0, padx=(25,0), pady=10)

        black_img = Image.new("RGB", (600, 363), color="black")
        self.tableimg = customtkinter.CTkImage(dark_image=black_img, size=(600, 363))
        self.image_label.configure(image=self.tableimg)

        button_frame = customtkinter.CTkFrame(tab)
        button_frame.grid(row=1, column=0, padx=(0, 0), pady=10)

        copy_button = customtkinter.CTkButton(button_frame, text="Copy Table", command=self.app.copy_table_action)
        copy_button.grid(row=0, column=0, padx=20, pady=0)

        copy_scores_button = customtkinter.CTkButton(button_frame, text="Copy Scores", command=self.app.copy_scores_action)
        copy_scores_button.grid(row=0, column=1, pady=0)

        self.missing_points_label = customtkinter.CTkLabel(tab, text="")
        self.missing_points_label.grid(row=1, padx=(500,0), pady=(0,0))

    def create_settings_tab(self):
        tab = self.tabview.tab("Settings")
        tab.grid_columnconfigure((0, 2), weight=1)
        
        game_mode_label = customtkinter.CTkLabel(tab, text="Game Mode", anchor="center")
        game_mode_label.grid(row=0, column=1, pady=(5, 0))
        self.game_mode_switcher = customtkinter.CTkSegmentedButton(tab, values=["MK8DX", "MKWorld"], command=self.app.switch_game_mode_action)
        self.game_mode_switcher.grid(row=1, column=1, pady=(0, 10))

        auto_copy_label = customtkinter.CTkLabel(tab, text="Auto Copy to Clipboard", anchor="center")
        auto_copy_label.grid(row=2, column=1, pady=(5, 0))
        self.auto_copy_menu = customtkinter.CTkOptionMenu(tab, values=["Disabled", "Table", "Scores"], command=self.app.set_autocopy_action)
        self.auto_copy_menu.grid(row=3, column=1, pady=(0, 0))

        my_tag_label = customtkinter.CTkLabel(tab, text="My Tag (single letter)", anchor="center")
        my_tag_label.grid(row=4, column=1, pady=(10, 0))
        self.my_tag_field = customtkinter.CTkEntry(tab, placeholder_text="e.g. A")
        self.my_tag_field.grid(row=5, column=1, pady=(0, 0))
        my_tag_button = customtkinter.CTkButton(tab, text="Submit Tag", command=self.app.set_my_tag_action)
        my_tag_button.grid(row=6, column=1, pady=(10, 0))

        dc_points_label = customtkinter.CTkLabel(tab, text="DC Points")
        dc_points_label.grid(row=7, column=1, pady=(10, 0))
        self.dc_points_field = customtkinter.CTkEntry(tab, placeholder_text="e.g. A6 B10 C2")
        self.dc_points_field.grid(row=8, column=1, pady=(0, 0))

        btn_frame_settings = customtkinter.CTkFrame(tab)
        btn_frame_settings.grid(row=9, column=1, pady=(10, 0))
        fill_tags_btn = customtkinter.CTkButton(btn_frame_settings, text="Insert Tags", command=self.app.fill_in_tags_action)
        fill_tags_btn.grid(row=4, column=1, pady=(10, 0))
        dc_clear_btn = customtkinter.CTkButton(btn_frame_settings, text="Clear All", command=self.app.clear_all_scores_action)
        dc_clear_btn.grid(row=3, column=0, padx=5)
        roomcrash_btn = customtkinter.CTkButton(btn_frame_settings, text="Room Crash", command=self.app.roomcrash_action)
        roomcrash_btn.grid(row=3, column=2, padx=5)
        dc_submit_btn = customtkinter.CTkButton(btn_frame_settings, text="Submit", command=self.app.set_dc_points_action)
        dc_submit_btn.grid(row=3, column=1, padx=5)

        hotkeys_label = customtkinter.CTkLabel(tab, text="Hotkeys")
        hotkeys_label.grid(row=10, column=1, pady=(10, 0))
        btn_frame_hotkeys = customtkinter.CTkFrame(tab)
        btn_frame_hotkeys.grid(row=11, column=1, pady=0)
        change_hotkey_button = customtkinter.CTkButton(btn_frame_hotkeys, text="Change Hotkey", command=self.app.change_hotkey_action)
        change_hotkey_button.grid(row=0, column=0, padx=5)
        self.status_label = customtkinter.CTkLabel(btn_frame_hotkeys, text=f"Current: {self.app.hotkey or 'None'}", anchor="w")
        self.status_label.grid(row=3, column=0, pady=0)

        reset_button = customtkinter.CTkButton(tab, text="Reset Scores", command=self.app.reset_table_action) 
        reset_button.grid(row=12, column=1, pady=(10,0))
        
        self.obs_overlay_checkbox = customtkinter.CTkCheckBox(tab, text="OBS Overlay", command=self.app.toggle_obs_action)
        self.obs_overlay_checkbox.grid(row=13, column=1, pady=(15, 0))
        
        self.using_obs_virtual_cam_checkbox = customtkinter.CTkCheckBox(tab, text="Using OBS Virtual Camera", command=self.app.toggle_obs_virtual_cam_action)
        self.using_obs_virtual_cam_checkbox.grid(row=14, column=1, pady=(15, 0))

    def create_screenshots_tab(self):
        tab = self.tabview.tab("Screenshots")
        currentss_label = customtkinter.CTkLabel(tab, text="Current Screenshot", anchor="center")
        recentss_label = customtkinter.CTkLabel(tab, text="Recent Screenshot", anchor="center")
        currentss_label.grid(row=0, column=0, pady=(25, 0))
        recentss_label.grid(row=0, column=1, pady=(25, 0))

        self.currentss_image_label = customtkinter.CTkLabel(tab, text="", anchor="nw")
        self.recentss_image_label = customtkinter.CTkLabel(tab, text="", anchor="nw")
        self.currentss_image_label.grid(row=1, column=0, padx=(14,20), pady=10)
        self.recentss_image_label.grid(row=1, column=1, padx=0, pady=10)

        black_img = Image.new("RGB", (300, 300), color="black")
        ss_img = customtkinter.CTkImage(dark_image=black_img, size=(300, 300))
        self.currentss_image_label.configure(image=ss_img)
        self.recentss_image_label.configure(image=ss_img)

    def create_info_tab(self):
        tab = self.tabview.tab("Info")
        infotext_content = (
            "Press Hotkey once you're on the sorted race results screen or the points finished adding up\n"
            "Only enter the first Letter of Tag for DC Points (in this format: A10 B10 C10 D10 E10 F10)\n"
            "Use the normal Hotkey if youre using OBS method or watching Fullscreen (recommended)\n"
            "Use the Twitch Hotkey if youre watching twitch with chat opened (highly experimental)\n"
            "Twitch Mode might not work if youre not on Chrome and dont have something in your bookmarks \n"
            "(might not even work then)\n\n"
            "Made by tarek, fork by Nolanimations\n"
            "using https://gb.hlorenzi.com/table and https://gb2.hlorenzi.com/table\n\n"
            "v0.3"
        )
        infotext = customtkinter.CTkTextbox(tab, width=620, height=250)
        infotext.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        infotext.insert("0.0", infotext_content)
        infotext.configure(state="disabled")

    def update_hotkey_status(self, new_hotkey):
        self.status_label.configure(text=f"Current: {new_hotkey or 'None'}")

    def sync_settings(self):
        self.game_mode_switcher.set(self.app.game_mode)
        self.auto_copy_menu.set(self.app.autocopy)
        self.my_tag_field.delete(0, "end")
        if self.app.my_tag:
            self.my_tag_field.insert(0, self.app.my_tag)
        if self.app.obs_overlay_active:
            self.obs_overlay_checkbox.select()
        else:
            self.obs_overlay_checkbox.deselect()
        if self.app.using_obs_virtual_cam:
            self.using_obs_virtual_cam_checkbox.select()
        else:
            self.using_obs_virtual_cam_checkbox.deselect()