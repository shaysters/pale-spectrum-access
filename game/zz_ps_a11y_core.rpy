# Pale Spectrum Accessibility Mod - core
# Speech output through Prism, dialogue reading, hotkeys and the shared
# keyboard menu engine used by zz_ps_a11y_screens.rpy.

init -100 python:
    import __builtin__
    import os
    import re
    import time
    import traceback as _a11y_traceback

    # ------------------------------------------------------------------
    # Logging: a11y_log.txt next to the game executable.
    # ------------------------------------------------------------------

    def a11y_log(msg):
        try:
            path = os.path.join(config.basedir, "a11y_log.txt")
            with open(path, "a") as f:
                f.write("[{0}] {1}\n".format(time.strftime("%Y-%m-%d %H:%M:%S"), msg))
        except Exception:
            pass

    def a11y_log_exc(context):
        a11y_log("EXCEPTION in {0}:\n{1}".format(context, _a11y_traceback.format_exc()))

    A11Y_VERSION = "1.0.0"

    a11y_log("=" * 60)
    a11y_log("Pale Spectrum accessibility mod {0} loading.".format(A11Y_VERSION))

    # ------------------------------------------------------------------
    # Prism wrapper. prism.dll sits next to the game executable and picks
    # the best speech output available (NVDA, JAWS, SAPI, ...).
    # ------------------------------------------------------------------

    PRISM_OK = 0
    PRISM_ERROR_ALREADY_INITIALIZED = 15

    class A11yPrism(__builtin__.object):
        def __init__(self):
            self.available = False
            self.name = "none"
            self._dll = None
            self._ctx = None
            self._backend = None
            self._failed_speaks = 0
            try:
                self._load()
            except Exception:
                a11y_log_exc("A11yPrism._load")

        def _load(self):
            import ctypes

            path = None
            for d in (config.basedir, config.gamedir):
                candidate = os.path.join(d, "prism.dll")
                if os.path.exists(candidate):
                    path = candidate
                    break
            if path is None:
                a11y_log("Prism: prism.dll not found.")
                return

            class PrismConfig(ctypes.Structure):
                _fields_ = [
                    ("version", ctypes.c_uint8),
                    ("registry", ctypes.c_void_p),
                    ("availability_callback", ctypes.c_void_p),
                    ("availability_userdata", ctypes.c_void_p),
                    ("availability_poll_interval_ms", ctypes.c_uint32),
                    ("availability_debounce_samples", ctypes.c_uint32),
                    ("availability_backoff_max_ms", ctypes.c_uint32),
                    ("availability_auto_power_manage", ctypes.c_bool),
                    ("availability_baseline_callback", ctypes.c_void_p),
                ]

            dll = ctypes.CDLL(path)
            dll.prism_config_init.restype = PrismConfig
            dll.prism_config_init.argtypes = []
            dll.prism_init.restype = ctypes.c_void_p
            dll.prism_init.argtypes = [ctypes.POINTER(PrismConfig)]
            dll.prism_registry_acquire_best.restype = ctypes.c_void_p
            dll.prism_registry_acquire_best.argtypes = [ctypes.c_void_p]
            dll.prism_backend_initialize.restype = ctypes.c_int
            dll.prism_backend_initialize.argtypes = [ctypes.c_void_p]
            dll.prism_backend_name.restype = ctypes.c_char_p
            dll.prism_backend_name.argtypes = [ctypes.c_void_p]
            dll.prism_backend_output.restype = ctypes.c_int
            dll.prism_backend_output.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_bool]
            dll.prism_backend_speak.restype = ctypes.c_int
            dll.prism_backend_speak.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_bool]
            dll.prism_backend_stop.restype = ctypes.c_int
            dll.prism_backend_stop.argtypes = [ctypes.c_void_p]

            self._cfg = dll.prism_config_init()
            ctx = dll.prism_init(ctypes.byref(self._cfg))
            if not ctx:
                a11y_log("Prism: prism_init failed.")
                return
            backend = dll.prism_registry_acquire_best(ctx)
            if not backend:
                a11y_log("Prism: no speech backend available.")
                return
            err = dll.prism_backend_initialize(backend)
            if err not in (PRISM_OK, PRISM_ERROR_ALREADY_INITIALIZED):
                a11y_log("Prism: backend initialize returned error {0}.".format(err))
                return

            self._dll = dll
            self._ctx = ctx
            self._backend = backend
            self.name = dll.prism_backend_name(backend) or "Prism"
            self.available = True
            a11y_log("Prism ready from {0}. Backend: {1}".format(path, self.name))

        def speak(self, text, interrupt=True):
            if not self.available:
                return False
            try:
                if not isinstance(text, unicode):
                    text = text.decode("utf-8", "replace")
                data = text.encode("utf-8")
                err = self._dll.prism_backend_output(self._backend, data, bool(interrupt))
                if err != PRISM_OK:
                    err = self._dll.prism_backend_speak(self._backend, data, bool(interrupt))
                if err != PRISM_OK:
                    self._failed_speaks += 1
                    if self._failed_speaks <= 5:
                        a11y_log("Prism: speak failed with error {0}.".format(err))
                    return False
                return True
            except Exception:
                a11y_log_exc("A11yPrism.speak")
                return False

        def stop(self):
            if self.available:
                try:
                    self._dll.prism_backend_stop(self._backend)
                except Exception:
                    pass

    # ------------------------------------------------------------------
    # Speech state shared by the whole mod.
    # ------------------------------------------------------------------

    class A11yState(__builtin__.object):
        def __init__(self):
            self.prism = A11yPrism()
            if not self.prism.available:
                a11y_log("Falling back to Ren'Py's built-in text to speech.")
            self.history = []
            self.review_index = -1
            self.last_line = ""
            self.last_voice_file = None
            self.last_skipping = False
            self.last_show_text = ""
            self.last_show_time = 0.0
            self.nav_index = {}
            self.nav_screen = {}
            self.nav_screen_name = {}
            self.nav_items = {}
            self.nav_last = None
            self.gallery_button = None
            self.gallery_last = None
            self.welcomed = False
            self.reread_pending = False
            # Story line tracking for ps_a11y_global.
            self.story_seen = None
            self.story_seen_at = 0.0
            self.story_read = None
            # When anything was last spoken, so the update notice can wait for a pause.
            self.last_speech_time = time.time()

        def clean(self, text):
            if text is None:
                return u""
            if not isinstance(text, unicode):
                text = unicode(str(text), "utf-8", "replace")
            text = re.sub(r"\{p[^}]*\}", u" ", text)
            text = re.sub(r"\{[^}]*\}", u"", text)
            text = text.replace(u"’", u"'").replace(u"‘", u"'")
            text = text.replace(u"“", u'"').replace(u"”", u'"')
            return re.sub(r"\s+", u" ", text).strip()

        def speak(self, text, interrupt=True):
            text = self.clean(text)
            if not text:
                return
            self.last_speech_time = time.time()
            if self.prism.available:
                self.prism.speak(text, interrupt)
            else:
                try:
                    renpy.display.tts.tts(text)
                except Exception:
                    pass

        def remember(self, text):
            text = self.clean(text)
            if not text:
                return
            self.last_line = text
            if not self.history or self.history[-1] != text:
                self.history.append(text)
                if len(self.history) > 500:
                    self.history = self.history[-500:]
            self.review_index = len(self.history) - 1

        def say_story(self, text, interrupt=True):
            # Story text is remembered for R and history review.
            self.remember(text)
            self.speak(text, interrupt)

    a11y = A11yState()

    def a11y_speak(text, interrupt=True):
        a11y.speak(text, interrupt)

    # ------------------------------------------------------------------
    # Dialogue reading. Called from the say screen a moment after each new
    # line appears, so the voice clip for that line has already started.
    # ------------------------------------------------------------------

    def a11y_voice_file():
        try:
            return renpy.music.get_playing("voice")
        except Exception:
            return None

    def a11y_spoken_what(what):
        # A line that is only dots (someone says nothing) would be skipped by
        # most screen readers, so it's read as "ellipsis".
        text = a11y.clean(what)
        if text and not re.sub(u"[.\u2026\s]", u"", text):
            return u"ellipsis"
        return text

    def a11y_read_line(who, what):
        try:
            if config.skipping:
                return
            text = a11y_spoken_what(what)
            if who:
                text = u"{0}. {1}".format(a11y.clean(who), text)
            a11y.remember(text)

            # A line counts as voiced when a new clip started on the voice
            # channel. A clip still playing from the previous line does not.
            voice = a11y_voice_file()
            voiced = bool(voice) and voice != a11y.last_voice_file
            a11y.last_voice_file = voice

            if voiced and who and not persistent.a11y_read_voiced:
                return
            # Don't cut off a chapter title or text card announced just before.
            a11y.speak(text, interrupt=time.time() - a11y.last_show_time > 2.0)
        except Exception:
            a11y_log_exc("a11y_read_line")

    def a11y_repeat():
        if a11y.last_line:
            a11y.speak(a11y.last_line)
        else:
            a11y.speak("Nothing to repeat yet.")

    def a11y_review(delta):
        if not a11y.history:
            a11y.speak("No history yet.")
            return
        idx = a11y.review_index
        if idx < 0:
            idx = len(a11y.history) - 1
        idx = max(0, min(len(a11y.history) - 1, idx + delta))
        a11y.review_index = idx
        prefix = u""
        if delta < 0 and idx == 0:
            prefix = u"Oldest line. "
        elif delta > 0 and idx == len(a11y.history) - 1:
            prefix = u"Latest line. "
        a11y.speak(prefix + a11y.history[idx])

    # ------------------------------------------------------------------
    # Announce text and title cards shown as images.
    # ------------------------------------------------------------------

    A11Y_IMAGE_TEXT = {
        "prologue": "Prologue.",
        "chap1header": "Chapter 1. The Shadow and the Light.",
        "chap2header": "Chapter 2.",
        "chap3header": "Chapter 3.",
        "chap4header": "Chapter 4.",
        "epilogueheader": "Epilogue.",
        "keeping_up_appearances": "Keeping Up Appearances.",
        "fireandchaos": "Fire and Chaos.",
        "resurrectionheader": "Resurrection.",
        "ending_shot": "Picture: the whole cast of Pale Spectrum gathered above the game's logo.",
    }

    def a11y_announce_shown(text):
        now = time.time()
        if text == a11y.last_show_text and now - a11y.last_show_time < 1.0:
            return
        a11y.last_show_text = text
        a11y.last_show_time = now
        a11y.say_story(text, interrupt=False)

    a11y_orig_config_show = config.show

    def a11y_show_proxy(name, *args, **kwargs):
        try:
            if isinstance(name, basestring):
                parts = tuple(name.split())
            else:
                parts = tuple(name)
            if parts and not config.skipping:
                head = parts[0]
                if head == "text":
                    spoken = u" ".join(parts[1:]).strip(u'"')
                    if not spoken:
                        what = kwargs.get("what", None)
                        spoken = getattr(what, "text", u"")
                        if isinstance(spoken, (list, tuple)):
                            spoken = u" ".join(s for s in spoken if isinstance(s, basestring))
                    if spoken:
                        a11y_announce_shown(spoken)
                elif head in A11Y_IMAGE_TEXT:
                    a11y_announce_shown(A11Y_IMAGE_TEXT[head])
        except Exception:
            a11y_log_exc("a11y_show_proxy")
        return a11y_orig_config_show(name, *args, **kwargs)

    config.show = a11y_show_proxy

    # ------------------------------------------------------------------
    # Hotkey helpers.
    # ------------------------------------------------------------------

    def a11y_run(action):
        return renpy.display.behavior.run(action)

    def a11y_toggle_voiced():
        persistent.a11y_read_voiced = not persistent.a11y_read_voiced
        if persistent.a11y_read_voiced:
            a11y.speak("Voice acted lines will be read aloud.")
        else:
            a11y.speak("Voice acted lines will not be read. Narration is still read.")

    def a11y_toggle_fullscreen():
        if _preferences.fullscreen:
            a11y_run(Preference("display", "window"))
            a11y.speak("Windowed.")
        else:
            a11y_run(Preference("display", "fullscreen"))
            a11y.speak("Fullscreen.")

    def a11y_hide_interface():
        # HideInterface waits until H, Enter, Space or a click, then returns.
        a11y.speak("Text window hidden. Press H, Enter or Space to show it again.")
        a11y_run(HideInterface())
        a11y.speak("Text window shown.")

    def a11y_screenshot():
        a11y_run(Screenshot())
        a11y.speak("Screenshot saved.")

    def a11y_mark_return():
        # Leaving a menu for the story: read the current line once back.
        if not renpy.context()._main_menu:
            a11y.reread_pending = True

    def a11y_back():
        # Action for Return / Escape in menus that can lead back to the story.
        return [Function(a11y_mark_return), Return()]

    def a11y_poll():
        # Runs twice a second from the hotkey overlay, which only shows
        # during the story.
        if a11y.reread_pending:
            a11y.reread_pending = False
            if renpy.get_screen("say") is not None and a11y.last_line:
                a11y.speak(a11y.last_line)
        try:
            _preferences.self_voicing = False
        except Exception:
            pass
        skipping = bool(config.skipping)
        if skipping != a11y.last_skipping:
            a11y.last_skipping = skipping
            a11y.speak("Skipping." if skipping else "Skipping stopped.")

    # ------------------------------------------------------------------
    # Keyboard menu engine. A screen passes a list of A11yItem objects to
    # the a11y_nav screen, which handles arrows, Enter, Home/End and Delete.
    # ------------------------------------------------------------------

    class A11yItem(__builtin__.object):
        """One entry in a keyboard menu.

        label   text, or a function returning text (called with label_args)
        action  Ren'Py action run on Enter, or None for read-only entries
        adjust  function(delta) run on Left/Right; Left/Right move otherwise
        delete  action run on the Delete key
        after   function run after the action succeeds
        """
        def __init__(self, label, action=None, adjust=None, delete=None, after=None, label_args=()):
            self.label = label
            self.action = action
            self.adjust = adjust
            self.delete = delete
            self.after = after
            self.label_args = label_args

        def text(self):
            if callable(self.label):
                return self.label(*self.label_args)
            return self.label

    # Menus shown on top of something else. Closing one announces what was
    # selected underneath, so they are not remembered as the menu in use.
    A11Y_POPUP_MENUS = ("yesno", "mod_settings", "scene_buttons")

    def _a11y_nav_touch(menu_id, items):
        # Remember the menu in use, so it can be announced again when a
        # prompt shown over it closes. Prompts themselves don't count.
        if menu_id not in A11Y_POPUP_MENUS:
            a11y.nav_items[menu_id] = items
            a11y.nav_last = menu_id

    def a11y_after_prompt():
        # Like a screen reader returning focus: say what was selected before
        # the prompt opened.
        try:
            menu_id = a11y.nav_last
            name = a11y.nav_screen_name.get(menu_id)
            if menu_id and name and renpy.get_screen(name) is not None:
                items = a11y.nav_items.get(menu_id)
                if items:
                    a11y.speak(items[_a11y_nav_clamp(menu_id, items)].text())
                    return
            if renpy.get_screen("say") is not None and a11y.last_line:
                a11y.speak(a11y.last_line)
        except Exception:
            a11y_log_exc("a11y_after_prompt")

    def _a11y_nav_clamp(menu_id, items):
        idx = a11y.nav_index.get(menu_id, 0)
        if not items:
            return 0
        if idx >= len(items):
            idx = len(items) - 1
        if idx < 0:
            idx = 0
        a11y.nav_index[menu_id] = idx
        return idx

    def a11y_nav_open(menu_id, screen_name, items, intro, start, queue):
        # The screen's timer can fire again after a re-render, so only
        # announce once per shown screen.
        try:
            shown = renpy.get_screen(screen_name)
            if shown is not None and a11y.nav_screen.get(menu_id) is shown:
                return
            a11y.nav_screen[menu_id] = shown
            a11y.nav_screen_name[menu_id] = screen_name
            _a11y_nav_touch(menu_id, items)
            a11y.nav_index[menu_id] = start
            idx = _a11y_nav_clamp(menu_id, items)
            if callable(intro):
                intro = intro()
            parts = []
            if intro:
                parts.append(intro)
            if items:
                parts.append(items[idx].text())
            a11y.speak(u" ".join(parts), interrupt=not queue)
        except Exception:
            a11y_log_exc("a11y_nav_open({0})".format(menu_id))

    def a11y_nav_current(menu_id, items):
        if not items:
            return None
        return items[_a11y_nav_clamp(menu_id, items)]

    def a11y_nav_move(menu_id, items, delta):
        if not items:
            return
        _a11y_nav_touch(menu_id, items)
        idx = (_a11y_nav_clamp(menu_id, items) + delta) % len(items)
        a11y.nav_index[menu_id] = idx
        a11y.speak(items[idx].text())

    def a11y_nav_jump(menu_id, items, idx):
        if not items:
            return
        a11y.nav_index[menu_id] = idx % len(items)
        a11y.speak(items[a11y.nav_index[menu_id]].text())

    def a11y_nav_adjust(menu_id, items, delta):
        _a11y_nav_touch(menu_id, items)
        item = a11y_nav_current(menu_id, items)
        if item is None:
            return
        if item.adjust is None:
            return a11y_nav_move(menu_id, items, delta)
        try:
            return item.adjust(delta)
        except Exception:
            a11y_log_exc("a11y_nav_adjust({0})".format(menu_id))

    def a11y_nav_activate(menu_id, items):
        _a11y_nav_touch(menu_id, items)
        item = a11y_nav_current(menu_id, items)
        if item is None:
            return
        if item.action is None:
            a11y.speak(item.text())
            return
        try:
            if not renpy.display.behavior.is_sensitive(item.action):
                a11y.speak("Unavailable.")
                return
            rv = a11y_run(item.action)
            if item.after is not None:
                item.after()
            return rv
        except renpy.game.CONTROL_EXCEPTIONS:
            raise
        except Exception:
            a11y_log_exc("a11y_nav_activate({0})".format(menu_id))
            a11y.speak("That did not work.")

    def a11y_nav_delete(menu_id, items):
        item = a11y_nav_current(menu_id, items)
        if item is None or item.delete is None:
            return
        return a11y_run(item.delete)

    def a11y_nav_say_current(menu_id, items):
        item = a11y_nav_current(menu_id, items)
        if item is not None:
            a11y.speak(item.text())

    # ------------------------------------------------------------------
    # Stuck modifier keys. Alt+Tab or Alt+F4 can leave SDL thinking Alt is
    # still held, and then every plain key is ignored. Clear any modifier
    # that no key is actually holding down.
    # ------------------------------------------------------------------

    import pygame_sdl2 as _a11y_pygame

    _A11Y_MODIFIERS = (
        ((_a11y_pygame.K_LALT, _a11y_pygame.K_RALT), _a11y_pygame.KMOD_ALT),
        ((_a11y_pygame.K_LCTRL, _a11y_pygame.K_RCTRL), _a11y_pygame.KMOD_CTRL),
        ((_a11y_pygame.K_LSHIFT, _a11y_pygame.K_RSHIFT), _a11y_pygame.KMOD_SHIFT),
        ((_a11y_pygame.K_LGUI, _a11y_pygame.K_RGUI), _a11y_pygame.KMOD_META),
    )
    _A11Y_ALL_MODIFIERS = (_a11y_pygame.KMOD_ALT | _a11y_pygame.KMOD_CTRL |
                           _a11y_pygame.KMOD_SHIFT | _a11y_pygame.KMOD_META)

    def a11y_unstick_modifiers():
        try:
            mods = _a11y_pygame.key.get_mods()
            if not mods & _A11Y_ALL_MODIFIERS:
                return
            pressed = _a11y_pygame.key.get_pressed()
            held = 0
            for keys, flag in _A11Y_MODIFIERS:
                if any(pressed[k] for k in keys):
                    held |= mods & flag
            if held != mods & _A11Y_ALL_MODIFIERS:
                _a11y_pygame.key.set_mods((mods & ~_A11Y_ALL_MODIFIERS) | held)
        except Exception:
            if not getattr(a11y, "unstick_failed", False):
                a11y.unstick_failed = True
                a11y_log_exc("a11y_unstick_modifiers")

    config.periodic_callbacks.append(a11y_unstick_modifiers)

    # ------------------------------------------------------------------
    # Keymap changes.
    # ------------------------------------------------------------------

    def _a11y_remove_keys(binding, keys):
        config.keymap[binding] = [k for k in config.keymap.get(binding, []) if k not in keys]

    # V is used for the voiced-lines toggle, so Ren'Py's own self-voicing
    # (which would talk over the screen reader) is switched off.
    _a11y_remove_keys("self_voicing", ["v", "V", "alt_K_v"])
    _a11y_remove_keys("clipboard_voicing", ["C", "shift_K_c"])


init 1 python:
    if persistent.a11y_read_voiced is None:
        persistent.a11y_read_voiced = False


# Hotkeys available during the story. Ren'Py hides overlays while a menu is
# open, so menu screens get their own keys from a11y_nav.
screen ps_a11y_hotkeys():
    zorder 200
    timer 0.5 repeat True action Function(a11y_poll)

    key "K_r" action Function(a11y_repeat)
    key "K_v" action Function(a11y_toggle_voiced)
    key "K_f" action Function(a11y_toggle_fullscreen)
    key "K_h" action Function(a11y_hide_interface)
    key "K_s" action Function(a11y_screenshot)
    key "K_q" action Show("ps_a11y_scene_buttons")
    key "K_F1" action Show("ps_a11y_settings")


# Shared keyboard navigation, included at the end of each menu screen so its
# keys are checked before the screen's own image buttons.
#   menu_id      name used to remember the selected entry
#   screen_name  the top-level screen, used to detect a fresh showing
#   items        list of A11yItem
#   intro        spoken before the first entry when the screen opens
#   start        index selected when the screen opens
#   queue        True to wait for current speech instead of cutting it off
#   escape       action for Escape / right click, or None to leave it alone
#   delay        seconds to wait before the opening announcement
screen a11y_nav(menu_id, screen_name, items, intro="", start=0, queue=False, escape=None, delay=0.05):
    # Repeats so a screen shown again in the same place is announced again;
    # a11y_nav_open speaks once per shown screen.
    timer delay repeat True action Function(a11y_nav_open, menu_id, screen_name, items, intro, start, queue)

    key "K_UP" action Function(a11y_nav_move, menu_id, items, -1)
    key "repeat_K_UP" action Function(a11y_nav_move, menu_id, items, -1)
    key "K_DOWN" action Function(a11y_nav_move, menu_id, items, 1)
    key "repeat_K_DOWN" action Function(a11y_nav_move, menu_id, items, 1)
    key "K_LEFT" action Function(a11y_nav_adjust, menu_id, items, -1)
    key "repeat_K_LEFT" action Function(a11y_nav_adjust, menu_id, items, -1)
    key "K_RIGHT" action Function(a11y_nav_adjust, menu_id, items, 1)
    key "repeat_K_RIGHT" action Function(a11y_nav_adjust, menu_id, items, 1)
    key "K_HOME" action Function(a11y_nav_jump, menu_id, items, 0)
    key "K_END" action Function(a11y_nav_jump, menu_id, items, -1)
    key "K_RETURN" action Function(a11y_nav_activate, menu_id, items)
    key "K_KP_ENTER" action Function(a11y_nav_activate, menu_id, items)
    key "K_SPACE" action Function(a11y_nav_activate, menu_id, items)
    key "K_DELETE" action Function(a11y_nav_delete, menu_id, items)
    key "K_r" action Function(a11y_nav_say_current, menu_id, items)
    key "K_F1" action Show("ps_a11y_settings")
    if escape is not None:
        key "game_menu" action escape


init 999 python:
    if "ps_a11y_hotkeys" not in config.overlay_screens:
        config.overlay_screens.append("ps_a11y_hotkeys")


# ----------------------------------------------------------------------
# Update check. Once per game start, asks GitHub for the latest release
# and says so if it's newer than A11Y_VERSION. Reads the release manifest
# the installer itself uses (a plain redirect, no API token or rate
# limit). This Python has no SSL support, so the request goes through
# Windows' own curl.exe in the background, polled from a periodic
# callback. The notice waits for the main menu and a moment of silence,
# so it neither cuts off the start-up speech nor gets cut off by it.
# Nothing is sent except the request itself, and a failed check is only
# logged.
# ----------------------------------------------------------------------

init 2 python:
    A11Y_UPDATE_URL = "https://github.com/shaysters/pale-spectrum-access/releases/latest/download/loadstone-release.json"
    A11Y_UPDATE_QUIET = 2.0

    a11y_update = {"proc": None, "latest": None, "done": False}

    def a11y_version_tuple(s):
        try:
            return tuple(int(p) for p in s.split("."))
        except Exception:
            return None

    def a11y_update_tick():
        u = a11y_update
        if u["done"]:
            return
        try:
            if u["latest"]:
                if renpy.get_screen("main_menu") is not None and time.time() - a11y.last_speech_time >= A11Y_UPDATE_QUIET:
                    u["done"] = True
                    text = u"Pale Spectrum Access version {0} is available. Run the installer to update.".format(u["latest"])
                    a11y_log("Update announced.")
                    # R repeats it until the story starts.
                    if not a11y.last_line:
                        a11y.last_line = text
                    a11y.speak(text, False)
                return
            if u["proc"] is None:
                import subprocess
                curl = os.path.join(os.environ.get("SystemRoot", r"C:\Windows"), "System32", "curl.exe")
                if not os.path.exists(curl):
                    curl = "curl"
                startupinfo = None
                if hasattr(subprocess, "STARTUPINFO"):
                    startupinfo = subprocess.STARTUPINFO()
                    startupinfo.dwFlags |= 1  # STARTF_USESHOWWINDOW: keep the console hidden
                u["proc"] = subprocess.Popen(
                    [curl, "-s", "-L", "--max-time", "15", A11Y_UPDATE_URL],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=startupinfo)
                return
            if u["proc"].poll() is None:
                return
            out = u["proc"].stdout.read()
            m = re.search(r'"version"\s*:\s*"v?([0-9.]+)"', out or "")
            if not m:
                u["done"] = True
                a11y_log("Update check skipped (exit code {0}).".format(u["proc"].returncode))
                return
            latest = m.group(1)
            a11y_log("Update check: installed {0}, latest {1}".format(A11Y_VERSION, latest))
            lv, iv = a11y_version_tuple(latest), a11y_version_tuple(A11Y_VERSION)
            if lv and iv and lv > iv:
                u["latest"] = latest
            else:
                u["done"] = True
        except Exception:
            u["done"] = True
            a11y_log_exc("update check")

    config.periodic_callbacks.append(a11y_update_tick)
