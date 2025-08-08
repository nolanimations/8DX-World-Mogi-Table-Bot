# Mogi Table Bot

## Mario Kart World (MKWorld) Support

This fork of the Mogi Table Bot introduces experimental support for generating tables from *Mario Kart World* screenshots.

To use this, you **must** use the `MKWorld-MogiTableBot.exe` file in the [latest release](https://github.com/nolanimations/8DX-World-Mogi-Table-Bot/releases).
You can use the old MK8DX version with `MK8DX-MogiTableBot.exe`.

### Important Notes & Limitations for MKWorld Mode:

*   **12-Player Rooms Only:** Support is currently limited to standard 12-player rooms.
*   **Team Mode is NOT Supported:** Due to the different colouring on the team scoreboard which interferes with OCR, team mode is not supported. This is also generally unnecessary as the game already provides final team scores.
*   **Table Generation is Slow:** Be patient! It can take 15-20 seconds or more for the website to fully process the screenshot and generate the final table.
*   **OCR Isn't Perfect:** The technology for reading MKW screenshots is still new. **Always double-check the generated scores for mistakes.** The bot relies entirely on the accuracy of Lorenzi's OCR.

## DC Wizard (11-player race corrections)

The bot includes a **DC Wizard** to fix scores for races where **exactly one player disconnects** (so the results screen shows **11 players**). It does not modify screenshots; instead it adds compensation to your **DC Points** field so corrections apply to **all future screenshots** until you clear them.

### What it does
- Works with **12-player rooms** only and **one DC per race** (11 players shown on results).
- Uses your last **clean 12-player** screenshot (same number of `+` chunks on every line) to cache the roster.
- You tell it:
  - **Who disconnected**
  - **Who got 1st**
  - **Who got 2nd**
- Applies MKWorld-style correction **per player**, rolls it up **per tag**, and **adds** those totals to the **DC Points** field (cumulative—never replace).
- Option to **carry the DC’d player’s pre-DC total** from the last 12p snapshot (ON by default), so when they rejoin with 0 shown in-game, their earlier points are still accounted for.

### When you **don’t** need the wizard
If a **bot races for the disconnected player** and the room still shows **12 players**, you can skip the wizard. Just use **manual DC Points** in Settings for that one player’s tag if needed—the normal flow handles it.

### Requirements
- You must have taken **at least one 12-player screenshot** this session so the wizard can cache the roster.  
  If you open the wizard without that, you’ll see: *“I don’t have a 12-player roster yet. Capture a 12p screenshot first.”*

### How to use
1. Take a normal **12-player** screenshot at some point (this caches the roster).
2. If a race has **11 players** (one DC), open **Settings → DC Wizard (11-player race)**.
3. Pick:
   - **Disconnected player** (1)
   - **1st place player** (1)
   - **2nd place player** (1)
4. Review the **per-tag** additions. Leave **“Also add DC’s pre-DC total”** checked (recommended).
5. Click **Apply**. The wizard **merges** these additions into your **DC Points** field and the bot auto-applies them to the table/overlay.

> The DC Points field is persistent for the session. Every new screenshot (12p or 11p) uses the **current** field value, so corrections keep applying automatically until you clear them.

### The math (per player → per tag)
For a **single-DC** race:
- All **present** players (11 of them): **+1**  
- **1st place** player: **+2 extra** (so **+3** total)  
- **2nd place** player: **+1 extra** (so **+2** total)  
- **DC’d** player: **+1** (assume 12th in a full room)  

These are summed **per tag** and added to your DC Points field.

**Examples**
- Team gets **1st & 3rd** → that tag gets **+4** (3 + 1).  
- Team gets **top 2** → that tag gets **+5** (3 + 2).  
- Duo with one DC and partner 11th → that tag gets **+2** this race (+1 DC, +1 partner).

### Tips & limitations
- **One DC per race** only (11-player result). Multi-DC in the same race isn’t supported yet.
- If you **skip screenshots**, that’s fine—the wizard works off the cached 12p roster and updates your DC Points field; future screenshots will include the cumulative corrections.
- If you run the wizard **twice for the same race**, it will double-add (because it’s cumulative). If that happens, just edit/clear the DC field.
- Names shown in the wizard come from Lorenzi’s **textarea** (full names), not the PNG abbreviations. Tags are inferred from the **first character** (`'8'` is treated as `'B'`).
- To discard all corrections, **clear the DC Points field** in Settings.

If you encounter any issues or have suggestions regarding the MKWorld implementation, contact me on Discord: @nolanimations

## Highlight Tag

This fork also adds the ability to submit your own Tag, and it will be highlighted in magenta and surrounded by "*" signs on the OBS overlay. It will also be highlighted by asterisks in the clipboard output.

![Highlight](https://github.com/user-attachments/assets/acc78ef2-2740-4a24-b73b-6f8546b68721)

This feature is not thoroughly tested, use at your own risk

## Tutorial
I strongly advise to follow and read the whole instructions, to prevent confusion. (It won't take long)
## First Time Setup:
Download MogiTableBot.exe from https://github.com/nolanimations/8DX-Mogi-Table-Bot/releases.

If you're planning to use the OBS Overlay, download the 2 fonts aswell, and install them.

Fonts needed for OBS Overlay:

[DS-Digital Bold](https://github.com/lisophorm/dreamteam/raw/master/src/assets/fonts/Digital/DS-DIGIB.TTF)

[New Rodin Pro](https://archive.org/download/Fontworks/Fonts/FOT-NewRodin%20Pro%20B.otf)

Run both, and press Install on the top left.

Go to the Settings tab and check the "Using OBS Virtual Camera" if you're using it for your own game, leave it disabled if you're watching a Stream. (Leaving it disabled will take a Screenshot from your PC, rather than your Capture Card).

Check the OBS Overlay checkbox if you want to use the Overlay.

<p align="center">
  <img src="https://github.com/user-attachments/assets/c8b2650e-b389-4917-883d-5c77162b6751" alt="Bild 1" width="400"/>
  <img src="https://github.com/user-attachments/assets/9897ee2b-1a23-4cdd-86de-cc59656104d0" alt="Bild 2" width="397"/>
</p> 


If you activated OBS Overlay this window should pop up.

![image](https://github.com/user-attachments/assets/2f78c3f0-f9c8-478e-87b9-9a230976188e)

Don't minimize this window, you can click a window behind it, to make it disappear. (Windows doesn't render it, if you minimize it)

Go to OBS and press on the gear icon next to "Start Virtual Camera", under Controls.

<p align="center">
  <img src="https://github.com/user-attachments/assets/fc9d8faf-8f0d-42c3-95f0-9d01f4c61921" alt="Bild 1" width="200"/>
  <img src="https://github.com/user-attachments/assets/81dc61b4-5332-4cec-b878-564431b2c116" alt="Bild 2" width="800"/>
</p> 

Set it to Source, and then select your Capture Card Source.

Under Sources, add a new Window Capture, name it whatever you want, and set the Window to the Scores Overlay. Under Window Match Priority, apply Window title must match, and disable Capture Cursor.

![image](https://github.com/user-attachments/assets/cdcb41a4-996f-445e-916a-e15ac3e2adc3)

Move the Overlay, to where you want it. (pressing Ctrl while dragging, unlocks it)

Right-click the Window Capture, press on Filters, and add a Chroma Key. Set the Opacity to 0.5 and Contrast to 2.5

![image](https://github.com/user-attachments/assets/0c333730-2e1e-41b4-b153-c8e48c15f5a7)

This finished the Setup.

## How to Use:

Every time you use the Bot you have to Start your Virtual Camera in OBS, so the Bot can get the Image from the Switch.

![image](https://github.com/user-attachments/assets/1e760b1c-4856-4200-aec3-71aedb1b4a55)

Whenever you're at the end of a race, wait until the Points finished adding up and press the Hotkey, you can alternatively wait until the scoreboard sorts itself and press it then. 

<p align="center">
  <img src="https://github.com/user-attachments/assets/f74d7f0a-ba37-44e2-a58f-e8b0902985ba" alt="Bild 2" width="400"/>
  <img src="https://github.com/user-attachments/assets/18587502-2051-46c5-a535-f1c989fbc050" alt="Bild 1" width="400"/>
  Left = Good, Right = Bad
</p> 

In case of a Disconnect, enter the first Letter of the Tag, and the amount the Person disconnected with, (shows in Overlay and next to Table). If more than one person disconnected in a single race, you can check on the Screenshots Tab, to see how much each one disconnected with.

![image](https://github.com/user-attachments/assets/3ce4b612-a5a1-4eb6-b2e7-37d9b21af3d1)

If it's a Japanese Tag or a Symbol, press the Insert Tags button, so you can get the Tag.

If the room crashes, press the Room Crash button, and it will add the Points to the following Tables/Scores. 

Press Clear after a mogi with DC Points/Room Crash finished.

Bind a Key to ESC to unbind it.

## Disclaimer:

It does not work if somebody has the tag at the end of the name.

If the Table / Scores don't update, check the Screenshots tab.

![image](https://github.com/user-attachments/assets/c2b88cb4-3824-46d3-a246-267b5061774e)

If this image shows up, you forgot to start the Virtual Camera

The Twitch Hotkey is experimental, I don't recommend using it.





