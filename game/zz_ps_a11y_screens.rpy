# Pale Spectrum Accessibility Mod - screens
# The game's own screens are left as they are. One mod screen above them
# (ps_a11y_global) works out which game screen is showing, reads it, and
# drives it from the keyboard.

init -80 python:
    import functools

    A11Y_CHOICE_NAMES = {
        "prude": "Prude",
        "bel": "Belinda",
        "hek": "Hektor",
        "ash": "Ash",
        "aku": "Aku",
        "terra": "Terra",
        "sword": "Sword",
        "aelf": "Aelfnod",
    }

    def a11y_choice_intro(items):
        who = A11Y_CHOICE_NAMES.get(getattr(store, "screen_choice", "none"))
        parts = [u"{0}'s choice.".format(who) if who else u"Choice."]
        for caption, action, chosen in items:
            if not action:
                parts.append(a11y.clean(caption))
        count = len([1 for caption, action, chosen in items if action])
        parts.append(u"{0} options.".format(count))
        return u" ".join(parts)

    def a11y_main_intro():
        if a11y.welcomed:
            return "Main menu."
        a11y.welcomed = True
        engine = a11y.prism.name if a11y.prism.available else "Ren'Py text to speech"
        return ("Pale Spectrum, Part Two of the Book of Gray Magic. Accessibility mod active, "
                "speaking through {0}. Use the arrow keys and Enter. Main menu.").format(engine)

    def a11y_lis_unlocked():
        p = persistent
        return bool(p.banish_unlock or p.res_trust_truth or p.res_trust_lie or p.mountain_aelf_end_unlock or
                    p.banish_reveal_unlock or p.banish_wait_and_see_unlock or p.banish_pursue_unlock or
                    p.res_grudge_death_unlock or p.nores_summon_unlock or p.nores_summon_late_unlock)

    # -- Save and load -----------------------------------------------------

    def a11y_file_pages(mode):
        pages = [str(i) for i in range(1, 8)]
        if mode == "load":
            pages = ["auto", "quick"] + pages
        return pages

    def a11y_page_name(page):
        if page == "auto":
            return "Automatic saves"
        if page == "quick":
            return "Quick saves"
        return "Page {0} of 7".format(page)

    def a11y_slot_label(slot):
        when = FileTime(slot, empty="")
        if not when:
            return "Slot {0}, empty.".format(slot)
        name = a11y.clean(FileSaveName(slot))
        if name:
            return "Slot {0}, {1}, {2}.".format(slot, when, name)
        return "Slot {0}, {1}.".format(slot, when)

    def a11y_file_page_change(mode, slot, delta):
        pages = a11y_file_pages(mode)
        current = FileCurrentPage()
        idx = pages.index(current) if current in pages else pages.index("1")
        page = pages[(idx + delta) % len(pages)]
        a11y_run(FilePage(page))
        a11y.speak(a11y_page_name(page) + ". " + a11y_slot_label(slot))

    def a11y_file_intro(mode):
        current = FileCurrentPage()
        return "{0} game. {1}.".format("Save" if mode == "save" else "Load", a11y_page_name(current))

    def a11y_after_save(slot):
        # An overwrite asks for confirmation first; the prompt announces itself.
        if renpy.get_screen("yesno_prompt") is None:
            a11y.speak("Saved in slot {0}.".format(slot))

    def a11y_file_items(mode):
        items = []
        for slot in range(1, 5):
            if mode == "save":
                action = FileSave(slot)
                after = functools.partial(a11y_after_save, slot)
            else:
                action = FileLoad(slot)
                after = None
            items.append(A11yItem(a11y_slot_label, action,
                                  adjust=functools.partial(a11y_file_page_change, mode, slot),
                                  delete=FileDelete(slot), after=after, label_args=(slot,)))
        items.append(A11yItem("Next page", Function(a11y_file_page_change, mode, 1, 1)))
        items.append(A11yItem("Previous page", Function(a11y_file_page_change, mode, 1, -1)))
        items.append(A11yItem("Return", a11y_back()))
        return items

    # -- Yes / no prompt -----------------------------------------------------

    def a11y_yesno_text(message):
        known = {
            layout.ARE_YOU_SURE: "Are you sure?",
            layout.DELETE_SAVE: "Do you want to delete this save?",
            layout.OVERWRITE_SAVE: "Do you want to overwrite this save?",
            layout.LOADING: "Do you want to load this game?",
            layout.QUIT: "Are you sure you want to quit?",
            layout.MAIN_MENU: "Go to the main menu? Any unsaved progress will be lost.",
        }
        return known.get(message, a11y.clean(message))

    def a11y_yesno_after(message):
        if message == layout.OVERWRITE_SAVE:
            a11y.speak("Saved.")
        elif message == layout.DELETE_SAVE:
            a11y.speak("Save deleted.")

    # -- Preferences ---------------------------------------------------------

    def _a11y_selected_index(options, current=None):
        if current is not None:
            return current()
        for i, (name, action) in enumerate(options):
            try:
                if action.get_selected():
                    return i
            except Exception:
                pass
        return -1

    def a11y_pref_label(title, options, current=None):
        idx = _a11y_selected_index(options, current)
        value = options[idx][0] if idx >= 0 else "not set"
        return u"{0}: {1}.".format(title, value)

    def a11y_pref_cycle(title, options, current, delta):
        idx = _a11y_selected_index(options, current)
        idx = 0 if idx < 0 else (idx + delta) % len(options)
        a11y_run(options[idx][1])
        a11y.speak(a11y_pref_label(title, options, current))

    def a11y_pref_item(title, options, current=None):
        # current: optional function returning the selected option's index,
        # for settings whose actions cannot report it themselves.
        return A11yItem(a11y_pref_label, Function(a11y_pref_cycle, title, options, current, 1),
                        adjust=functools.partial(a11y_pref_cycle, title, options, current),
                        label_args=(title, options, current))

    def a11y_display_index():
        return 0 if _preferences.fullscreen else 1

    def a11y_volume_label(title, mixer):
        return "{0}: {1} percent.".format(title, int(round(_preferences.get_volume(mixer) * 100)))

    def a11y_volume_adjust(title, mixer, delta):
        volume = _preferences.get_volume(mixer) + 0.1 * delta
        _preferences.set_volume(mixer, round(max(0.0, min(1.0, volume)), 1))
        renpy.restart_interaction()
        a11y.speak(a11y_volume_label(title, mixer))

    def a11y_volume_item(title, mixer):
        return A11yItem(a11y_volume_label, None,
                        adjust=functools.partial(a11y_volume_adjust, title, mixer),
                        label_args=(title, mixer))

    def a11y_text_speed_label():
        cps = _preferences.text_cps
        if cps == 0:
            return "Text speed: instant."
        return "Text speed: {0} characters per second.".format(cps)

    def a11y_text_speed_adjust(delta):
        # Same scale as the game's slider: 1 to 200, where 0 means instant.
        cps = _preferences.text_cps
        if delta > 0:
            if cps != 0:
                cps += 20
                if cps >= 200:
                    cps = 0
        else:
            cps = 180 if cps == 0 else max(20, cps - 20)
        _preferences.text_cps = cps
        renpy.restart_interaction()
        a11y.speak(a11y_text_speed_label())

    def a11y_pref_items():
        return [
            a11y_pref_item("Display", [("fullscreen", Preference("display", "fullscreen")),
                                       ("windowed", Preference("display", "window"))],
                           current=a11y_display_index),
            a11y_pref_item("Skip", [("seen text only", Preference("skip", "seen")),
                                    ("all text", Preference("skip", "all"))]),
            a11y_pref_item("After choices", [("stop skipping", Preference("after choices", "stop")),
                                             ("keep skipping", Preference("after choices", "skip"))]),
            a11y_pref_item("Transitions", [("all", Preference("transitions", "all")),
                                           ("none", Preference("transitions", "none"))]),
            A11yItem(a11y_text_speed_label, None, adjust=a11y_text_speed_adjust),
            a11y_volume_item("Music volume", "music"),
            a11y_volume_item("Voice volume", "voice"),
            a11y_volume_item("Sound volume", "sfx"),
            a11y_pref_item("Read voice acted lines", [("off", SetField(persistent, "a11y_read_voiced", False)),
                                                      ("on", SetField(persistent, "a11y_read_voiced", True))]),
            A11yItem("Return", a11y_back()),
        ]

    # -- Reading the game's own screens --------------------------------------
    # Text and buttons are read from the shown screen while the game runs, so
    # nothing from the game is copied into the mod.

    def a11y_walk(d, out, seen=None):
        """Every displayable under d, in drawing order."""
        if seen is None:
            seen = set()
        if d is None or id(d) in seen:
            return out
        seen.add(id(d))
        out.append(d)
        try:
            children = d.visit()
        except Exception:
            children = []
        for c in children or []:
            a11y_walk(c, out, seen)
        return out

    def a11y_screen_widgets(screen_name):
        s = renpy.get_screen(screen_name)
        if s is None:
            return []
        return a11y_walk(getattr(s, "child", None), [])

    def a11y_screen_texts(screen_name):
        """The text shown on a screen, one entry per paragraph."""
        lines = []
        for d in a11y_screen_widgets(screen_name):
            if isinstance(d, renpy.text.text.Text):
                raw = u"".join(t for t in d.text if isinstance(t, basestring))
                for part in raw.split("{p}"):
                    part = a11y.clean(part)
                    if part and part not in lines:
                        lines.append(part)
        return lines

    # -- Extras: credits, gallery, progress map ------------------------------

    A11Y_CREDIT_SCREENS = ("credits", "credits_2", "credits_3")

    def a11y_credits_page(page, delta):
        target = page + delta
        if 1 <= target <= len(A11Y_CREDIT_SCREENS):
            return a11y_run(ShowMenu(A11Y_CREDIT_SCREENS[target - 1]))
        a11y.speak("First page." if delta < 0 else "Last page.")

    def a11y_credits_items(page):
        screen_name = A11Y_CREDIT_SCREENS[page - 1]
        items = [A11yItem(line, adjust=functools.partial(a11y_credits_page, page))
                 for line in a11y_screen_texts(screen_name)]
        if page < len(A11Y_CREDIT_SCREENS):
            items.append(A11yItem("Next page", ShowMenu(A11Y_CREDIT_SCREENS[page])))
        if page > 1:
            items.append(A11yItem("Previous page", ShowMenu(A11Y_CREDIT_SCREENS[page - 2])))
        items.append(A11yItem("Return", Return()))
        return items

    def a11y_cg_screen(page):
        return "cg_gallery" if page == 1 else "cg_gallery{0}".format(page)

    def a11y_cg_page_count():
        page = 1
        while renpy.has_screen(a11y_cg_screen(page + 1)):
            page += 1
        return page

    def a11y_cg_name_for_index(index):
        for name, b in g.buttons.items():
            if getattr(b, "index", None) == index:
                return name
        return None

    def a11y_cg_entries(page):
        """The gallery buttons on a page, in screen order: a button name, or
        None for a locked picture. Locked buttons have no action, so their
        names can't be known (and aren't needed)."""
        entries = []
        for d in a11y_screen_widgets(a11y_cg_screen(page)):
            if not isinstance(d, renpy.display.behavior.Button):
                continue
            action = getattr(d, "action", None)
            if action is None:
                entries.append(None)
            elif type(action).__name__.endswith("GalleryAction"):
                entries.append(a11y_cg_name_for_index(action.index))
        return entries

    def a11y_cg_label(name, number, total):
        if name is None:
            return "Picture {0} of {1}. Locked.".format(number, total)
        count = len(g.buttons[name].images)
        return "Picture {0} of {1}. {2}. {3} {4}.".format(number, total, a11y_gallery_title(name), count,
                                                         "image" if count == 1 else "images")

    def a11y_cg_view(name, label):
        a11y.gallery_button = name
        a11y.gallery_last = None
        a11y_run(g.Action(name))
        a11y.gallery_button = None
        a11y.speak("Back to the gallery. " + label)

    def a11y_cg_page_change(page, delta):
        target = page + delta
        if 1 <= target <= a11y_cg_page_count():
            return a11y_run(ShowMenu(a11y_cg_screen(target)))
        a11y.speak("First page." if delta < 0 else "Last page.")

    def a11y_cg_items(page):
        entries = a11y_cg_entries(page)
        items = []
        for i, name in enumerate(entries):
            label = a11y_cg_label(name, i + 1, len(entries))
            action = Function(a11y_cg_view, name, label) if name else None
            items.append(A11yItem(label, action, adjust=functools.partial(a11y_cg_page_change, page)))
        pages = a11y_cg_page_count()
        if page < pages:
            items.append(A11yItem("Next page", ShowMenu(a11y_cg_screen(page + 1))))
        if page > 1:
            items.append(A11yItem("Previous page", ShowMenu(a11y_cg_screen(page - 1))))
        items.append(A11yItem("Return", Return()))
        return items

    def a11y_cg_intro(page):
        entries = a11y_cg_entries(page)
        unlocked = len([e for e in entries if e])
        return "Gallery page {0} of {1}. {2} of {3} unlocked. Left and Right change pages.".format(
            page, a11y_cg_page_count(), unlocked, len(entries))

    def a11y_gallery_announce(locked, index, count, force=False):
        # The viewer screen is re-shown for each image, so this is called
        # repeatedly and speaks when the image changes.
        key = (a11y.gallery_button, index, locked)
        if not force and a11y.gallery_last == key:
            return
        a11y.gallery_last = key
        if locked:
            text = "Image {0} of {1}. Locked.".format(index, count)
        else:
            text = "Image {0} of {1}. {2}".format(index, count,
                                                 a11y_gallery_description(a11y.gallery_button, index - 1))
        if index == 1 and not force:
            text += " Enter for the next image, Escape to go back."
        a11y.speak(text)

    def a11y_endings_items():
        found = [title for flag, title in A11Y_ENDINGS if getattr(persistent, flag)]
        items = [A11yItem("Endings found: {0} of {1}.".format(len(found), len(A11Y_ENDINGS)))]
        items += [A11yItem("Ending: {0}.".format(title)) for title in found]
        items.append(A11yItem("Return", Return()))
        return items

    # -- Which game screen is up ----------------------------------------------

    A11Y_MOD_POPUPS = ("ps_a11y_settings", "ps_a11y_scene_buttons")

    def a11y_scope(screen_name, key, default=None):
        s = renpy.get_screen(screen_name)
        if s is None:
            return default
        try:
            return s.scope.get(key, default)
        except Exception:
            return default

    def a11y_mode():
        """Name of the game screen the keyboard should drive, top-most first."""
        try:
            for name in A11Y_MOD_POPUPS:
                if renpy.get_screen(name) is not None:
                    return None
            if renpy.get_screen("_gallery") is not None:
                return "_gallery"
            if renpy.get_screen("yesno_prompt") is not None:
                return "yesno_prompt"
            pages = a11y_cg_page_count()
            for page in range(1, pages + 1):
                if renpy.get_screen(a11y_cg_screen(page)) is not None:
                    return a11y_cg_screen(page)
            for name in ("credits", "credits_2", "credits_3", "progress_map", "gallery", "preferences",
                         "save", "load", "esc_menu", "story_picker", "main_menu"):
                if renpy.get_screen(name) is not None:
                    return name
            if renpy.get_screen("choice") is not None:
                return "choice"
            if renpy.get_screen("nvl") is not None:
                return "nvl"
            if renpy.get_screen("say") is not None:
                return "say"
        except Exception:
            a11y_log_exc("a11y_mode")
        return None

    def a11y_cg_page_of(mode):
        if mode == "cg_gallery":
            return 1
        try:
            return int(mode[len("cg_gallery"):])
        except Exception:
            return 0

    # -- Story lines ----------------------------------------------------------
    # A new line is read a moment after it appears, so the voice clip for the
    # line has already started and voiced lines can be told apart.

    def a11y_story_tick():
        try:
            if renpy.get_screen("nvl") is not None:
                dialogue = a11y_scope("nvl", "dialogue") or []
                who, what = (dialogue[-1][0], dialogue[-1][1]) if dialogue else (None, None)
            else:
                who, what = a11y_scope("say", "who"), a11y_scope("say", "what")
            if what is None:
                return
            now = time.time()
            if what != a11y.story_seen:
                a11y.story_seen = what
                a11y.story_seen_at = now
                return
            if what != a11y.story_read and now - a11y.story_seen_at >= 0.12:
                a11y.story_read = what
                a11y_read_line(who, what)
        except Exception:
            a11y_log_exc("a11y_story_tick")

    # Shown in every context, so the menus Ren'Py opens with ShowMenu get it too.
    def a11y_ensure_global():
        try:
            if renpy.get_screen("ps_a11y_global") is None:
                renpy.show_screen("ps_a11y_global")
        except Exception:
            a11y_log_exc("a11y_ensure_global")

    config.start_interact_callbacks.append(a11y_ensure_global)


##############################################################################
# One screen above the game's own screens. It works out which game screen is
# showing and drives it from the keyboard; the game's screens are untouched.

screen ps_a11y_global():
    # Above the game's screens (so it gets the keys first), below the mod's
    # own pop-ups.
    zorder 250
    $ a11y_m = a11y_mode()

    if a11y_m == "say" or a11y_m == "nvl" or a11y_m == "choice":
        timer 0.05 repeat True action Function(a11y_story_tick)

    if a11y_m == "say":
        key "K_UP" action Function(a11y_review, -1)
        key "repeat_K_UP" action Function(a11y_review, -1)
        key "K_DOWN" action Function(a11y_review, 1)
        key "repeat_K_DOWN" action Function(a11y_review, 1)
        # Keep the arrow keys from moving focus onto the hidden in-game buttons.
        key "K_LEFT" action NullAction()
        key "K_RIGHT" action NullAction()
        # Advance even if the mouse pointer is resting on an in-game button.
        key "K_RETURN" action Return()
        key "K_KP_ENTER" action Return()
        key "K_SPACE" action Return()

    elif a11y_m == "choice":
        $ a11y_items = a11y_scope("choice", "items") or []
        # Wait for the question to be read first (it's read after 0.12s).
        use a11y_nav("choice", "choice", [A11yItem(caption, action) for caption, action, chosen in a11y_items if action],
                     intro=a11y_choice_intro(a11y_items), queue=True, delay=0.3)

    elif a11y_m == "nvl":
        $ a11y_items = a11y_scope("nvl", "items")
        if a11y_items:
            use a11y_nav("nvl_choice", "nvl", [A11yItem(caption, action) for caption, action, chosen in a11y_items if action],
                         intro="Choice.", queue=True, delay=0.3)

    elif a11y_m == "main_menu":
        use a11y_nav("main_menu", "main_menu", [
            A11yItem("Start", ShowMenu('story_picker')),
            A11yItem("Load", ShowMenu('load')),
            A11yItem("Preferences", ShowMenu('preferences')),
            A11yItem("Extras", ShowMenu('gallery')),
            A11yItem("Quit", Quit()),
            ], intro=a11y_main_intro)

    elif a11y_m == "story_picker":
        if a11y_lis_unlocked():
            $ a11y_lis_item = A11yItem("Lost in Shadow, Continued.", [SetVariable("startDestination", "4"), Start()])
        else:
            $ a11y_lis_item = A11yItem("Lost in Shadow, Continued. Locked. It unlocks after you reach one of the main story's endings.")
        use a11y_nav("story_picker", "story_picker", [
            A11yItem("Pale Spectrum. The main story.", [SetVariable("startDestination", "1"), Start()]),
            a11y_lis_item,
            A11yItem("Return", Return()),
            ], intro="Choose a story.", escape=Return())

    elif a11y_m == "esc_menu":
        use a11y_nav("esc_menu", "esc_menu", [
            A11yItem("Return to game", a11y_back()),
            A11yItem("Save", ShowMenu('save')),
            A11yItem("Load", ShowMenu('load')),
            A11yItem("Main menu", MainMenu()),
            A11yItem("Settings", ShowMenu('preferences')),
            A11yItem("Quit", Quit()),
            ], intro="Game menu.", escape=a11y_back())

    elif a11y_m == "save" or a11y_m == "load":
        use a11y_nav(a11y_m, a11y_m, a11y_file_items(a11y_m), intro=a11y_file_intro(a11y_m), escape=a11y_back())

    elif a11y_m == "preferences":
        use a11y_nav("preferences", "preferences", a11y_pref_items(),
            intro="Preferences. Left and Right change a setting.", escape=a11y_back())

    elif a11y_m == "yesno_prompt":
        $ a11y_message = a11y_scope("yesno_prompt", "message")
        $ a11y_yes = a11y_scope("yesno_prompt", "yes_action")
        $ a11y_no = a11y_scope("yesno_prompt", "no_action")
        use a11y_nav("yesno", "yesno_prompt", [
            A11yItem("Yes", a11y_yes, after=functools.partial(a11y_yesno_after, a11y_message)),
            A11yItem("No", [a11y_no, Function(a11y_after_prompt)]),
            ], intro=a11y_yesno_text(a11y_message), escape=[a11y_no, Function(a11y_after_prompt)])

    elif a11y_m == "gallery":
        use a11y_nav("extras", "gallery", [
            A11yItem("Credits", ShowMenu("credits")),
            A11yItem("Gallery", ShowMenu("cg_gallery")),
            A11yItem("Progress map", ShowMenu("progress_map")),
            A11yItem("Ithaqua Labs website. Opens your web browser.", OpenURL("http://ithaqualabs.com/")),
            A11yItem("Return", Return()),
            ], intro="Extras.", escape=Return())

    elif a11y_m in A11Y_CREDIT_SCREENS:
        $ a11y_page = A11Y_CREDIT_SCREENS.index(a11y_m) + 1
        use a11y_nav("credits", a11y_m, a11y_credits_items(a11y_page),
            intro="Credits, page {0} of {1}. Up and Down read each line.".format(a11y_page, len(A11Y_CREDIT_SCREENS)),
            escape=Return())

    elif a11y_m == "progress_map":
        use a11y_nav("progress_map", "progress_map", a11y_endings_items(), intro="Progress map.", escape=Return())

    elif a11y_m and a11y_m.startswith("cg_gallery"):
        $ a11y_page = a11y_cg_page_of(a11y_m)
        use a11y_nav("cg_gallery", a11y_m, a11y_cg_items(a11y_page), intro=a11y_cg_intro(a11y_page), escape=Return())

    elif a11y_m == "_gallery":
        # Ren'Py's own full-screen gallery viewer.
        $ a11y_gal = a11y_scope("_gallery", "gallery")
        $ a11y_args = (a11y_scope("_gallery", "locked"), a11y_scope("_gallery", "index"), a11y_scope("_gallery", "count"))
        timer 0.1 repeat True action Function(a11y_gallery_announce, *a11y_args)
        if a11y_gal is not None:
            key "K_RIGHT" action a11y_gal.Next()
            key "K_DOWN" action a11y_gal.Next()
            key "K_LEFT" action a11y_gal.Previous()
            key "K_UP" action a11y_gal.Previous()
        key "K_r" action Function(a11y_gallery_announce, *(a11y_args + (True,)))


##############################################################################
# Mod menus: F1 opens the mod settings, Q the in-scene buttons. Both sit on
# top of whatever is showing and announce it again when closed.

init -80 python:
    def a11y_speech_label():
        return "Speech output: {0}.".format(a11y.prism.name if a11y.prism.available else "Ren'Py text to speech")

screen ps_a11y_settings():
    modal True
    zorder 300
    frame:
        xalign 0.5
        yalign 0.5
        has vbox
        text "Accessibility settings"
        text "Up and Down choose, Left, Right or Enter change, Escape closes." size 20

    $ a11y_close = [Hide("ps_a11y_settings"), Function(a11y_after_prompt)]
    use a11y_nav("mod_settings", "ps_a11y_settings", [
        a11y_pref_item("Read voice acted lines", [("off", SetField(persistent, "a11y_read_voiced", False)),
                                                  ("on", SetField(persistent, "a11y_read_voiced", True))]),
        A11yItem(a11y_speech_label),
        A11yItem("Close", a11y_close),
        ], intro="Accessibility settings.", escape=a11y_close)

screen ps_a11y_scene_buttons():
    modal True
    zorder 300
    frame:
        xalign 0.5
        yalign 0.5
        has vbox
        text "In-scene buttons"
        text "Up and Down choose, Enter presses, Escape closes." size 20

    $ a11y_close = [Hide("ps_a11y_scene_buttons"), Function(a11y_after_prompt)]
    use a11y_nav("scene_buttons", "ps_a11y_scene_buttons", [
        A11yItem("Rewind. Go back one line.", [Hide("ps_a11y_scene_buttons"), Rollback()]),
        A11yItem("Skip. Fast forward through lines you have read.", [Hide("ps_a11y_scene_buttons"), Skip()]),
        A11yItem("Game menu.", [Hide("ps_a11y_scene_buttons"), ShowMenu("esc_menu", transition=dissolve)]),
        A11yItem("Close", a11y_close),
        ], intro="In-scene buttons.", escape=a11y_close)
    key "K_q" action a11y_close


