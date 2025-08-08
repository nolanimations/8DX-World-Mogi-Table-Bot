import re
import customtkinter
from selenium.webdriver.common.by import By


LINE_RE = re.compile(r"^(.*?) (?:\[\w{2}\] )?(\d+(?:\+\d+)*)$")

def _norm_tag(ch):
    if ch == "8":
        return "B"
    return (ch or " ").upper()

def parse_textarea(text):
    out = []
    for raw in (text or "").replace("\r", "").split("\n"):
        raw = raw.strip()
        if not raw:
            continue
        m = LINE_RE.match(raw)
        if not m:
            continue
        name = m.group(1).lstrip()
        scores = m.group(2)
        chunks = [int(x) for x in scores.split("+")] if scores else []
        out.append((name, chunks, raw))
    return out

def is_clean_12p(text):
    rows = parse_textarea(text)
    if len(rows) < 12:
        return False
    counts = { len(ch) for _, ch, _ in rows }
    return len(counts) == 1

# ----- Roster cache -----

def cache_12p_roster(app, textarea_text):
    """If textarea shows a clean 12p race, cache roster, tags, and per-player totals on app._dcw_cache."""
    rows = parse_textarea(textarea_text)
    if len(rows) < 12:
        return
    counts = { len(ch) for _, ch, _ in rows }
    if len(counts) != 1:
        return

    # Take the first 12 rows as the roster snapshot
    names = [name for name, _, _ in rows][:12]
    tag_of = { name: _norm_tag(name[:1]) for name in names }

    # Per-player totals at this snapshot
    sum_of = {}
    for name, chunks, _ in rows:
        if name in tag_of:  # only keep the 12p roster entries
            sum_of[name] = sum(chunks)

    tags = sorted({ tag_of[n] for n in names })
    app._dcw_cache = {
        "names": names,
        "tag_of": tag_of,
        "sum_of": sum_of,
        "tags": tags,
    }


# ----- DC math -----

def compute_dc_increments(cache, dc_name, first_name, second_name):
    """
    Per-player additions then rolled up per-tag.
    Rules:
      - All present players (11) +1
      - 1st +2 extra (total +3 for that player)
      - 2nd +1 extra (total +2 for that player)
      - DC +1 (assume 12th)
    Returns dict: {TAG: points}
    """
    names = list(cache["names"])
    tag_of = cache["tag_of"]

    if dc_name not in names or first_name not in names or second_name not in names:
        raise ValueError("Selections must be from cached roster names.")

    if len({dc_name, first_name, second_name}) < 3:
        # Don't allow overlap; the UI should already prevent this
        raise ValueError("DC, 1st and 2nd must be different players.")

    inc_player = { n: 0 for n in names }
    present = [n for n in names if n != dc_name]

    # baseline +1 for all present
    for p in present:
        inc_player[p] += 1

    # bonuses
    inc_player[first_name] += 2  # now +3 total
    inc_player[second_name] += 1 # now +2 total

    # DC special +1
    inc_player[dc_name] += 1

    # roll-up per tag
    inc_tag = {}
    for n, pts in inc_player.items():
        if pts == 0:
            continue
        t = tag_of[n]
        inc_tag[t] = inc_tag.get(t, 0) + pts

    return inc_tag

def parse_dc_points_field(s):
    """'A6 B10 C2' -> dict {'A':6,'B':10,'C':2}"""
    out = {}
    if not s:
        return out
    parts = s.strip().split()
    for token in parts:
        if not token:
            continue
        t = _norm_tag(token[:1])
        num = token[1:]
        if not num.isdigit():
            continue
        out[t] = out.get(t, 0) + int(num)
    return out

def merge_dc_points_str(old_str, inc_tag):
    base = parse_dc_points_field(old_str)
    for t, add in inc_tag.items():
        base[t] = base.get(t, 0) + int(add)
    # return tokens sorted by tag letter
    tokens = [f"{t}{base[t]}" for t in sorted(base.keys())]
    return " ".join(tokens)

# ----- Wizard UI -----

class _Stepper:
    def __init__(self, root, title="DC Wizard (11-player race)"):
        self.top = customtkinter.CTkToplevel(root)
        self.top.title(title)
        self.top.grab_set()
        self.top.geometry("+420+260")
        self.frame = customtkinter.CTkFrame(self.top)
        self.frame.pack(padx=14, pady=14, fill="both", expand=True)

        self.header = customtkinter.CTkLabel(self.frame, text=title, font=("Segoe UI", 16, "bold"))
        self.header.pack(anchor="w", pady=(0,8))

        self.body = customtkinter.CTkFrame(self.frame)
        self.body.pack(fill="both", expand=True)

        self.btns = customtkinter.CTkFrame(self.frame)
        self.btns.pack(fill="x", pady=(8,0))

        self.prev_btn = customtkinter.CTkButton(self.btns, text="Back", state="disabled", command=self.on_prev)
        self.next_btn = customtkinter.CTkButton(self.btns, text="Next", command=self.on_next)
        self.cancel_btn = customtkinter.CTkButton(self.btns, text="Cancel", fg_color="#444444", command=self.on_cancel)
        self.prev_btn.pack(side="left")
        self.cancel_btn.pack(side="right")
        self.next_btn.pack(side="right", padx=(8,8))

        self.step = 0
        self.steps = []
        self.result = None

    def set_steps(self, steps):
        self.steps = steps
        self.step = 0
        self._render()

    def _clear_body(self):
        for w in self.body.winfo_children():
            w.destroy()

    def _render(self):
        self._clear_body()
        self.prev_btn.configure(state="normal" if self.step > 0 else "disabled")
        if self.step == len(self.steps) - 1:
            self.next_btn.configure(text="Apply")
        else:
            self.next_btn.configure(text="Next")
        self.steps[self.step]["render"](self.body)

    def on_prev(self):
        if self.step > 0:
            self.step -= 1
            self._render()

    def on_next(self):
        ok = self.steps[self.step]["validate"]()
        if not ok:
            return
        if self.step == len(self.steps) - 1:
            self.result = True
            self.top.destroy()
        else:
            self.step += 1
            self._render()

    def on_cancel(self):
        self.result = False
        self.top.destroy()

def open_dc_wizard(app):
    cache = getattr(app, "_dcw_cache", None)
    if not cache or not cache.get("names"):
        ta = None
        try:
            ta = app.driver.find_element(By.TAG_NAME, "textarea")
        except Exception:
            pass
        if ta:
            val = ta.get_attribute("value") or ""
            if is_clean_12p(val):
                cache_12p_roster(app, val)
                cache = getattr(app, "_dcw_cache", None)

    if not cache or not cache.get("names"):
        _toast(app.root, "I don't have a 12-player roster yet. Capture a 12p screenshot first.")
        return

    names = list(cache["names"])
    tag_of = cache["tag_of"]

    # State
    sel = {"dc": None, "first": None, "second": None}

    # Step factories
    def _make_list_step(title, key, forbid=None):
        def forbid_set():
            try:
                return set(forbid()) if callable(forbid) else set(forbid or [])
            except Exception:
                return set()

        def render(parent):
            hdr = customtkinter.CTkLabel(parent, text=title, font=("Segoe UI", 14, "bold"))
            hdr.pack(anchor="w", pady=(0,6))

            radio_var = customtkinter.StringVar(value=sel[key] or "")

            list_frame = customtkinter.CTkScrollableFrame(parent, height=280)
            list_frame.pack(fill="both", expand=True)

            fset = forbid_set()
            for n in names:
                state = "disabled" if n in fset else "normal"
                label = f"{n}  [{tag_of[n]}]"
                rb = customtkinter.CTkRadioButton(list_frame, text=label, value=n, variable=radio_var, state=state)
                rb.pack(anchor="w", pady=2)

            def on_change(*_):
                sel[key] = radio_var.get() or None
            radio_var.trace_add("write", on_change)

        def validate():
            return sel[key] is not None

        return {"render": render, "validate": validate}

    def _make_review_step():
        def render(parent):
            hdr = customtkinter.CTkLabel(parent, text="Review → Per-tag additions to apply", font=("Segoe UI", 14, "bold"))
            hdr.pack(anchor="w", pady=(0,6))

            try:
                inc = compute_dc_increments(cache, sel["dc"], sel["first"], sel["second"])
            except Exception as e:
                msg = customtkinter.CTkLabel(parent, text=f"Selection error: {e}", text_color="red")
                msg.pack(anchor="w")
                return

            # base per-tag table
            body = customtkinter.CTkFrame(parent)
            body.pack(fill="x", pady=(6,0))
            for t in sorted(inc.keys()):
                row = customtkinter.CTkFrame(body)
                row.pack(fill="x", pady=2)
                customtkinter.CTkLabel(row, text=f"Tag {t}", width=60, anchor="w").pack(side="left")
                customtkinter.CTkLabel(row, text=f"+{inc[t]}").pack(side="left")

            # Carry the DC player's pre-DC total (from last clean 12p)
            dc_name = sel["dc"]
            carry_val = cache.get("sum_of", {}).get(dc_name, 0)
            dc_tag = tag_of.get(dc_name, "?")

            # Store toggle in sel so it persists when navigating steps
            if "carry_pre_dc" not in sel:
                sel["carry_pre_dc"] = True  # default ON

            carry_var = customtkinter.BooleanVar(value=sel["carry_pre_dc"])
            chk = customtkinter.CTkCheckBox(
                parent,
                text=f"Also add {dc_name}'s pre-DC total (+{carry_val}) to tag {dc_tag}",
                variable=carry_var
            )
            chk.pack(anchor="w", pady=(10,6))

            def on_toggle(*_):
                sel["carry_pre_dc"] = carry_var.get()
            carry_var.trace_add("write", on_toggle)

            # Merge preview (what will land in the DC field)
            old = (app.ui.dc_points_field.get() or "").strip()
            inc_preview = dict(inc)
            if sel["carry_pre_dc"] and carry_val:
                inc_preview[dc_tag] = inc_preview.get(dc_tag, 0) + carry_val
            merged = merge_dc_points_str(old, inc_preview)

            prev = customtkinter.CTkLabel(parent, text=f"DC field will become:\n{merged}", justify="left")
            prev.pack(anchor="w", pady=(8,4))

        def validate():
            return True

        return {"render": render, "validate": validate}

    stepper = _Stepper(app.root)
    stepper.set_steps([
        _make_list_step("Who disconnected?", "dc"),
        _make_list_step("Who got 1st place?", "first", forbid=lambda: {sel["dc"]} if sel["dc"] else set()),
        _make_list_step("Who got 2nd place?", "second", forbid=lambda: {x for x in [sel["dc"], sel["first"]] if x}),
        _make_review_step(),
    ])

    app.root.wait_window(stepper.top)

    if not stepper.result:
        return

    # Apply
    inc = compute_dc_increments(cache, sel["dc"], sel["first"], sel["second"])

    if sel.get("carry_pre_dc", True):
        carry_val = cache.get("sum_of", {}).get(sel["dc"], 0)
        if carry_val:
            dc_tag = tag_of.get(sel["dc"])
            inc[dc_tag] = inc.get(dc_tag, 0) + carry_val

    old = (app.ui.dc_points_field.get() or "").strip()
    new_field = merge_dc_points_str(old, inc)
    app.ui.dc_points_field.delete(0, "end")
    app.ui.dc_points_field.insert(0, new_field)

    # call existing apply flow
    if hasattr(app, "set_dc_points_action"):
        app.set_dc_points_action()
    else:
        try:
            import actions
            actions.set_dc_points(app)
        except Exception:
            pass


def _toast(root, message):
    top = customtkinter.CTkToplevel(root)
    top.title("Notice")
    top.geometry("+480+320")
    lbl = customtkinter.CTkLabel(top, text=message, wraplength=380, justify="left")
    lbl.pack(padx=16, pady=16)
    btn = customtkinter.CTkButton(top, text="OK", command=top.destroy)
    btn.pack(pady=(0,10))
    top.after(100, lambda: top.lift())
