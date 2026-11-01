# Pale Spectrum Accessibility Mod - descriptions
# Spoken titles and descriptions for the CG gallery, plus the ending titles
# that the progress map only shows as pictures.

init -90 python:

    # Gallery button name -> (title, [description of each image in order]).
    A11Y_GALLERY = {
        "ash terra tavern": ("Ash and Terra at the tavern", [
            "A wide view of a cozy, dim tavern with stone pillars and strings of fairy lights. Ash, green skinned, shares a small table with Terra, who is disguised as a red haired trader in a feathered cap.",
            "The same tavern scene, a moment later.",
        ]),
        "ash terra trader": ("Terra's disguises", [
            "Close up at the table. Ash, with green skin, dark green hair and glowing green eyes, sits beside Terra in the form of a fiery red haired trader with a feathered cap. Mugs of ale sit in front of them.",
            "Terra now wears the form of a buxom barmaid with long golden curls. She leans toward Ash with a playful smile, gesturing, as she sets down the ale.",
            "The golden haired barmaid again, now blushing.",
        ]),
        "bel closeup": ("Belinda training", [
            "Close up of Belinda, a dark skinned young woman with a cloud of curly purple brown hair and a cloth headband. Her arms stretch overhead as she pulls herself up, teeth gritted, light sparkling through a window behind her.",
            "Belinda again, now grinning with confidence mid pull-up.",
        ]),
        "bel pullup2": ("Pull-ups with an audience", [
            "Seen from behind, Belinda hangs from a bar doing pull-ups. Below her sit a large blue and green lizard creature and a small orange creature in goggles, watching. A sword leans nearby.",
        ]),
        "sword eye1": ("Sword awakens", [
            "Close up of a grey steel sword's crossguard, shaped like curving horns, against a blurry reddish background.",
            "A rounded metal lid has appeared at the center of the crossguard.",
            "The lid opens, revealing a large round eye in the hilt. The sword is alive.",
            "The sword's eyelid droops half closed as it peers at you.",
        ]),
        "aelf 1": ("Aelfnod at tea", [
            "Aelfnod, a bearded man with long braided hair, a jeweled circlet and a blue scarf, sits at a wooden table holding a steaming teacup. The view starts at the cup and rises to his face.",
            "The full portrait of Aelfnod with his tea, in a cozy room lit by a window.",
            "Aelfnod at tea, his expression shifting slightly.",
            "Aelfnod at tea, with another subtle change of expression.",
        ]),
        "marm 1": ("Madame Marm", [
            "Madame Marm, an elderly woman with a tall white hairdo, a high collared teal robe with red ribbons, and closed eyes shadowed in purple, sits with her hands folded before a red curtain. The view rises from her hands to her face.",
            "The full portrait of Madame Marm.",
        ]),
        "marm dance": ("Madame Marm dances", [
            "Madame Marm spins in a whirling dance, her teal robes flying, laughing with a gap toothed grin.",
        ]),
        "prude room": ("Prude in her room", [
            "A dim blue bedroom with ornate curtains. Prude, a red haired girl in armor, sits hunched on the edge of her bed.",
        ]),
        "prude sword": ("Reflection in the blade", [
            "Prude's terrified, tear streaked face is reflected in a bloodied sword blade. Glowing motes drift through the darkness around it.",
        ]),
        "prude room closeup": ("Prude startled", [
            "Close up of Prude, freckled with long red hair, staring wide eyed over her shoulder as sparkling light washes over her face.",
            "Prude, mouth open in shock, as dark curling shapes gather around her.",
            "Prude's frightened face once more, the dark shapes still around her.",
        ]),
        "ash terra hold tavern": ("An embrace", [
            "In a dark, misty tavern lit by drifting green sparks, Ash and the white haired Terra hold each other close.",
        ]),
        "soldier squire cook": ("Soldiers at the door", [
            "A smirking blond soldier in red armor strides through an arched doorway with his young squire, who has his arms crossed. The tavern cook peeks nervously around the door frame.",
            "The same doorway, with the cook ducked out of sight.",
        ]),
        "ash sword swing": ("A blade meets magic", [
            "A pale hand, marked with a black tattoo, rises against a swinging sword as green magic curls from its fingers through red smoke.",
        ]),
        "ash hair adjust": ("Ash's smirk", [
            "Close up of Ash, green skinned with glowing green eyes, smirking as she sweeps a hand back through her hair.",
        ]),
        "soldier eyes red": ("Red eyes", [
            "In near darkness, the soldier's face appears with glowing red eyes and dark streaks running down his cheeks.",
        ]),
        "ash ribs scales": ("Scales like iron", [
            "A sword strikes Ash's side, but under her torn green coat, purple scales as hard as iron turn the blade aside.",
        ]),
        "ash soldier nose": ("A fight in shadow", [
            "Two silhouettes grapple inside a circle of hazy green and gold light, one landing a blow on the other.",
        ]),
        "terra kerfuffle": ("After the scuffle", [
            "Terra, a dark skinned elf with long white hair, crouches over the unconscious squire on the tavern floor. A dagger lies nearby. The view rises from the floor.",
            "The full view of Terra crouched over the fallen squire.",
        ]),
        "terra door": ("Caught at the door", [
            "Terra glances back over her shoulder in surprise, green eyes wide. Ash stands in the tavern doorway behind her, and someone's hand reaches toward Terra in the foreground.",
        ]),
        "ellena enter": ("Ellena", [
            "Close up of Ellena, a woman with dark hair pulled back, a cool blue gaze and a faint, knowing look. Green sparks drift behind her.",
        ]),
        "terra tavern vrayis": ("Wearing the soldier's face", [
            "A blurry view of a back room. The soldier and his squire lie slumped against the wall while a figure in red armor kneels beside them.",
            "In focus now: Terra, wearing the soldier's own face and armor, pours a bottle of liquor over the unconscious soldier and squire.",
        ]),
        "terra tavern leap": ("Into the forest", [
            "A tall, narrow view of a dark forest. A small figure leaps down between towering trees. The view moves down the trunks.",
            "The full view of the figure leaping through the forest.",
        ]),
        "beljump cg": ("Belinda leaps", [
            "Belinda leaps from a high wall into an open dusk sky, above tall cypress trees and green hills. The view rises with her.",
            "The full view of Belinda in mid air above the hills.",
        ]),
        "terragrin": ("Terra's grin", [
            "Close up of Terra, a dark skinned elf with wild white hair and long pointed ears, grinning wide with sharp teeth, her green eyes bright against a sunset sky.",
        ]),
        "terra ash shapeshift": ("A lesson in the meadow", [
            "Ash and Terra kneel facing each other in a sunny meadow dotted with yellow flowers. Ash watches closely while Terra smiles with her eyes closed.",
        ]),
        "ash shapeshift": ("Changing faces", [
            "A split panel. Terra grins on the left, while Ash, mid transformation, takes on the face of a freckled red haired girl with green eyes.",
        ]),
        "ash terra kiss": ("A kiss at sunset", [
            "Terra and Ash share a kiss against a blazing sunset, both with their eyes closed.",
            "The kiss continues, Ash's tattooed hand resting against Terra's cheek.",
        ]),
        "tent2": ("The young officer", [
            "A soft, sketch like scene inside a tent. A young man with short hair and stripe markings on his cheek looks down grimly.",
        ]),
        "tent1": ("The lord's tent", [
            "Inside a tent, a dark silhouette with pointed ears stands holding a wine glass.",
            "The same silhouette, the glass gone and a splash of red spilled on the floor at his feet.",
        ]),
        "tent3": ("The lord's smile", [
            "The back of the pointed eared silhouette's head, against a bright haze.",
            "Close up of a white haired figure with pointed ears and a shadowed face, grinning wide with sharp teeth.",
        ]),
        "vrayisspiders": ("Battle with the spiders", [
            "Ink splash silhouettes. A figure swings a long blade in a wide arc, cutting through a swarm of giant spiders. The view pulls back.",
        ]),
        "vrayiswingsash1": ("Vrayis's wings", [
            "The silhouette of Vrayis, with pointed ears and enormous tattered wings spread wide, stands over a meadow.",
            "The winged silhouette again, with Ash's wide, glowing green eye staring at it from a corner panel.",
        ]),
        "vrayismeltcg": ("Watching it burn", [
            "A silhouetted woman with a long braid stands with her back to us, watching a dark spire of smoke and flame rise across a valley at sunset. The view moves down the scene.",
        ]),
        "ashwatchvrayburn": ("Ash watches", [
            "Ash stares wide eyed, a hand raised, her face lit an eerie green in a haze of purple light.",
        ]),
        "vrayisflyaway": ("Vrayis escapes", [
            "A storm of swirling wind. A huge dark winged shape soars up into the clouds while a small figure with a sword watches from a ledge below.",
        ]),
        "terra horse": ("Terra the horse", [
            "Terra, shapeshifted into a black stallion with a flowing white mane and green eyes, gallops across a purple sky with Ellena riding on her back.",
        ]),
        "carriage": ("Inside the royal coach", [
            "The plush interior of a royal coach, with velvet seats, gold trim, stained glass windows and a hanging banner showing a white heron. Countryside passes outside.",
        ]),
        "rhes intro1": ("Rheswenn", [
            "A hulking silhouette in a top hat, a monocle glinting, stalks down a rain soaked, green lit street with a cane in hand.",
        ]),
        "flashback": ("Terra's memory: the ball", [
            "A pale, dreamlike memory. Young Terra, with white ringlets and a white ball gown, stands at a glittering ball as a servant's silhouette passes with a tray.",
            "A large mustached face, cracked like a mask, looms in the foreground over young Terra.",
        ]),
        "flashback2": ("Terra's memory: fear", [
            "Close up of a wide, frightened eye, with dark streaks dripping down like ink.",
            "A dark figure looms over young Terra, who has fallen in her white dress. A glint of steel flashes in the air.",
        ]),
        "flashback4": ("Darkness", [
            "Near total darkness. Faint, twisting shapes of faces and bodies writhe in the shadows.",
        ]),
        "flashback5": ("Terra awakens", [
            "Young Terra's face in deep blue darkness, eyes closed, framed by white ringlets.",
            "Still darkness, her eyes still closed.",
            "Terra's eyes snap open, a bright icy blue, her face now lit in warm color.",
        ]),
        "bunny": ("The rabbit", [
            "A soft watercolor scene. A frightened white rabbit lies tangled in a snare among grass and lavender.",
            "The same patch of grass, now empty. The rabbit is gone.",
        ]),
        "barmaid": ("Terra the barmaid", [
            "A blurry view. A buxom blonde barmaid with pointed ears blushes while two tavern patrons gawk behind her.",
            "In focus now: the blonde elf barmaid, Terra in disguise, blushes and glances sideways holding a tray, as the patrons stare.",
        ]),
        "terra ambig": ("On the road", [
            "Terra in a boyish disguise, with short white hair, a loose tunic, trousers and a sword at her hip, looks off into the distance.",
            "Closer on Terra, blushing, her green eyes wide.",
            "A cheerful blonde girl in a blue dress appears beside the blushing Terra, smiling with rosy cheeks.",
            "Terra turns away in profile while the blonde girl keeps smiling at her.",
            "A full view of the blonde girl in her short blue dress, hands clasped happily near her chin.",
        ]),
        "goddess": ("The goddess", [
            "A stained glass style image of a goddess with many purple arms, holding glowing orbs, with a radiant crown above her head and flowing white robes.",
        ]),
        "prudevrayislap": ("On the throne", [
            "Prude, in blue armor, curls up in the lap of Vrayis, a tall blond elf who lounges on a stone throne beneath dark banners.",
            "Looking far up a tall, dark hall. A winged shape hovers high in a swirling ceiling.",
        ]),
        "vr_town_1": ("Vrayis transforms", [
            "A monstrous silhouette with huge clawed talons rises in a purple haze. Small figures stand far away.",
            "More figures gather in the distance as the monster's talons spread wider.",
        ]),
        "ashskewer": ("Ash is struck", [
            "A huge shadowy beast lunges, and Ash is caught on its spiked talons, thrown back in a burst of light.",
        ]),
        "ashskewer2": ("Ash in agony", [
            "Ash cries out in agony, head thrown back, a talon piercing her chest and blood at her mouth.",
            "The same moment again, flickering like a memory.",
        ]),
        "vr_town_3": ("The nightmare", [
            "Vrayis has become a nightmare of shadow, with jagged spikes and whipping tendrils, grinning out of the swirling purple.",
            "Closer on Vrayis's shadowy face, long haired, with a wide and sinister grin, as tendrils lash around him.",
        ]),
        "vr_bel_jump_1": ("Belinda dodges", [
            "A sweeping, stylized panel. Belinda leaps and twists three times across the picture, dodging dark tendrils, with a burst of golden magic behind her.",
        ]),
        "krok swing": ("Krok's blow", [
            "Krok, a muscular, spiked lizard man, grins as he brings a huge jagged blade around in a two handed blow.",
        ]),
        "belindaweapon": ("Belinda in flight", [
            "Seen from high above a cobbled town square, Belinda soars with her arm flung out as a huge jagged blade sweeps past her. A small figure stands far below.",
        ]),
        "vrayiswing": ("Striking the monster", [
            "A small figure darts above the rooftops, slashing at a huge purple shadow monster with a gaping, fanged mouth.",
        ]),
        "belfloatbehind": ("Belinda floats", [
            "Belinda floats in the air above a ruined city, arms raised, eyes closed, her hair drifting upward.",
        ]),
        "prude_ash_fb1": ("A childhood memory", [
            "A sketchy flashback. Young Ash, with dark hair and green eyes, hugs a crying young Prude with orange pigtails.",
            "A wider view. A tall white haired figure dressed in red and gold stands over the two girls.",
        ]),
        "luci_ash_fb": ("Head Luciana", [
            "A flashback. Young Ash, pale with long black pigtails and green eyes, faces Head Luciana, a dark skinned woman with her hair in a bun and glowing eyes.",
        ]),
        "prude sword chap1": ("Prude and Sword", [
            "Prude, with a long red braid and armor, smiles with her eyes closed as she hugs Sword to her chest. The sword's eye peers out from its hilt.",
            "A sketched panel slashes in: a close up of Prude's determined face.",
            "A second sketched panel joins it, showing another face looking up beside Prude's.",
        ]),
        "sword cackle": ("Sword laughs", [
            "Sword, its single big eye wide open in its hilt, stands propped against a parchment colored wall.",
            "Sword narrows its eye halfway, as if cackling.",
            "Sword squints, its lid low over its eye, looking smug.",
        ]),
        "chap_end_ash_terra": ("End of the chapter", [
            "Ash lies in bed under a blue blanket, winking, as Terra lovingly feeds her from a spoon.",
        ]),
    }

    # Progress map endings in the order the map shows them:
    # (persistent flag, title shown on the map).
    A11Y_ENDINGS = [
        ("res_trust_truth", "Dude, Where's My Core"),
        ("res_heaven_death", "Mother Knows Best"),
        ("res_trust_lie", "Order from Chaos"),
        ("res_trust_ogland_unlock", "Mustache Ride"),
        ("res_trust_ogland_untrained_unlock", "Give Her a Hand"),
        ("res_trust_ogland_trained_unlock", "Take a Bao"),
        ("res_trust_priamos_unlock", "Fish Sticks"),
        ("res_trust_priamos_untrained_unlock", "Catch of the Day"),
        ("res_trust_priamos_trained_unlock", "Catch and Release"),
        ("res_trust_gwen_unlock", "Uteruses Before Duderuses"),
        ("res_trust_gwen_hand_unlock", "Gwen Will I See You Again"),
        ("mountain_aelf_end_unlock", "Too Old For This"),
        ("mountain_nyssa_end_unlock", "The Goggles Do Nothing"),
        ("mountain_students_end_unlock", "Teacher's Pets"),
        ("mountain_fel_lives_end_unlock", "Perfect Attendance"),
        ("mountain_aku_gray_unlock", "Together At Last"),
        ("mountain_lyrael_gray_unlock", "Inside Out"),
        ("banish_reveal_unlock", "A Changeling of Heart"),
        ("banish_wait_and_see_unlock", "Whine and Cheese"),
        ("banish_pursue_unlock", "In-Terra-Gation"),
        ("res_grudge_death_unlock", "The Fine Print"),
        ("nores_summon_unlock", "Boy's Night Out"),
        ("nores_summon_late_unlock", "Road Trip"),
        ("evil_ash_golem_unlock", "Revenge is Fun"),
        ("evil_ash_headless_unlock", "Truly Lost in Shadow"),
        ("evil_ash_terra_unlock", "New Beginnings"),
    ]

    def a11y_gallery_title(name):
        return A11Y_GALLERY.get(name, (name, []))[0]

    def a11y_gallery_description(name, index):
        descs = A11Y_GALLERY.get(name, (name, []))[1]
        if 0 <= index < len(descs):
            return descs[index]
        return ""
