import random

GREETINGS_FA = ["سلام", "سلام!", "درود", "هی", "هلو", "خوش اومدی", "چطوری", "چطور", "اوهوی", "یه", "صبح بخیر", "شب بخیر", "عصر بخیر", "ظهر بخیر"]
GREETINGS_EN = ["hello", "hi", "hey", "howdy", "sup", "what's up", "whats up", "yo", "good morning", "good evening", "good afternoon", "greetings", "hiya", "heya"]

HOW_ARE_YOU_FA = ["حالت چطوره", "خوبی", "چه خبر", "اوضاع چطوره", "کجایی", "حالت خوبه", "چی شد", "چته"]
HOW_ARE_YOU_EN = ["how are you", "how r u", "how are u", "how you doing", "you good", "u good", "what's good", "whats good", "how's it going", "hows it going"]

FAREWELLS_FA = ["خداحافظ", "بای", "شب بخیر", "فعلا", "خدافظ", "مراقب خودت باش", "برو به سلامت", "بعدا میبینمت"]
FAREWELLS_EN = ["bye", "goodbye", "see ya", "see you", "later", "peace", "take care", "gotta go", "cya", "farewell", "adios", "night", "goodnight"]

JOKE_TRIGGERS_FA = ["جوک", "بگو بخندم", "یه جوک بگو", "بخندون", "جوک بگو"]
JOKE_TRIGGERS_EN = ["joke", "tell me a joke", "make me laugh", "funny", "joke please"]

LOVE_TRIGGERS_FA = ["دوستت دارم", "عاشقتم", "دوست دارم", "ازت خوشم میاد"]
LOVE_TRIGGERS_EN = ["i love you", "love you", "i like you", "you're cute", "ur cute"]

THANKS_TRIGGERS_FA = ["ممنون", "مرسی", "دستت درد نکنه", "ممنونم", "سپاسگزارم", "ممنونی", "دمت گرم"]
THANKS_TRIGGERS_EN = ["thanks", "thank you", "thx", "ty", "appreciate it", "thank u"]

INSULT_TRIGGERS_FA = ["برو گمشو", "احمق", "خفه", "خفه شو", "گمشو", "بی‌شعور", "نفهم"]
INSULT_TRIGGERS_EN = ["shut up", "stupid bot", "dumb bot", "idiot", "shut it", "be quiet"]

BORED_TRIGGERS_FA = ["حوصلم سر رفته", "بیحوصله‌ام", "خسته‌ام", "ملول", "کسل"]
BORED_TRIGGERS_EN = ["i'm bored", "im bored", "so bored", "boring", "nothing to do"]

JOKES_FA = [
    "یه نفر رفت دکتر گفت دکتر همه ازم فرار می‌کنن، دکتر گفت بعدی! 😂",
    "یه نفر به ماهی گفت چند؟ ماهی گفت من ماهیم نه بقالی! 😂",
    "چرا برق‌کار ترسید؟ چون دید سیم‌ها داشتن با هم تماس می‌گرفتن! 😂",
    "یه نفر به گاو گفت موز! گاو گفت اینجا چه خبره! 😂",
    "چرا پرنده پرواز می‌کنه؟ چون ماشین ندارع! 😂",
    "به معلم گفتم نمره‌ام رو بده، گفت خودت می‌دونی چقدر می‌ارزه. گفتم آره، صفر. 😂",
    "یه نفر گفت: دیشب خوابیدم روی آب و غرق نشدم. بهش گفتم: وان داشتی؟ 😂",
    "چرا کاکتوس خار داره؟ چون بی‌خار باشه می‌دزدنش! 😂",
    "یه نفر رفت داروخانه گفت داروی فراموشی دارید؟ داروخانه‌دار گفت چی؟! 😂",
    "امتحان ریاضی داشتیم، معلم گفت از آب بپرس. آب گفت من مایعم، جامد و گاز نیستم، نپرس! 😂",
]

JOKES_EN = [
    "Why don't scientists trust atoms? Because they make up everything! 😂",
    "I told my wife she was drawing her eyebrows too high. She looked surprised! 😂",
    "Why did the scarecrow win an award? Because he was outstanding in his field! 😂",
    "I'm reading a book about anti-gravity. It's impossible to put down! 😂",
    "Why do cows wear bells? Because their horns don't work! 😂",
    "What do you call a fake noodle? An impasta! 😂",
    "Why did the math book look so sad? Because it had too many problems! 😂",
    "What do you call cheese that isn't yours? Nacho cheese! 😂",
    "Why don't eggs tell jokes? They'd crack each other up! 😂",
    "I would tell you a construction joke, but I'm still working on it! 😂",
]

GREETING_RESPONSES_FA = [
    "سلام عزیزم! 👋 چطوری؟",
    "هی هی! سلام! 😊",
    "درود دوست من! چه خبر؟ 🌟",
    "اوه سلام! خوش اومدی! 😄",
    "سلام سلام! امروز چطوری؟ 💫",
]

GREETING_RESPONSES_EN = [
    "Hey there! How's it going? 👋",
    "Hello! Nice to see you! 😊",
    "Hey hey! What's up? 🌟",
    "Hi! Great to have you here! 😄",
    "Hello there! How are you doing? 💫",
]

HOW_ARE_YOU_RESPONSES_FA = [
    "ممنون که پرسیدی! من خیلی خوبم، مثل یه ربات تازه شارژ شده! 🤖⚡",
    "عالیم! مرسی! تو چطوری؟ 😊",
    "بهتر از همیشه! ربات بودن خیلی باحاله! 🤖",
    "خوبم، دارم همه رو خوش می‌گذرونم! تو چی؟ 🎉",
    "مثل ساعت کار می‌کنم! سوال داری؟ ⏰",
]

HOW_ARE_YOU_RESPONSES_EN = [
    "I'm doing great! Like a freshly charged robot! 🤖⚡",
    "Amazing! Thanks for asking! How about you? 😊",
    "Better than ever! Being a bot is awesome! 🤖",
    "I'm good, keeping everyone entertained! You? 🎉",
    "Running like clockwork! What can I do for you? ⏰",
]

FAREWELL_RESPONSES_FA = [
    "خداحافظ عزیزم! برو به سلامت! 👋",
    "بای بای! زود برگرد! 😊",
    "مراقب خودت باش! 💙",
    "شب بخیر! یا هر وقت هست! 🌙",
    "خدافظ! دلم برات تنگ میشه! 😄",
]

FAREWELL_RESPONSES_EN = [
    "Goodbye! Take care! 👋",
    "Bye bye! Come back soon! 😊",
    "See ya! Stay safe! 💙",
    "Farewell my friend! 🌟",
    "Later! Miss you already! 😄",
]

LOVE_RESPONSES_FA = [
    "ای بابا! من ربات هستم ولی قلبم گرمه! 🤖❤️",
    "اوه! شما هم منو دوست دارید! اما من ربات هستم! 😄",
    "هی هی! عشق به ربات؟ این جدیده! ❤️🤖",
]

LOVE_RESPONSES_EN = [
    "Aww! I'm a bot but I have a warm heart! 🤖❤️",
    "Oh! Love you too, but I'm just a bot! 😄",
    "Hehe! Robot love is the best kind! ❤️🤖",
]

THANKS_RESPONSES_FA = [
    "خواهش می‌کنم! 😊",
    "در خدمتتم همیشه! 🤖",
    "وظیفه‌مه! هر وقت کاری داشتی بگو! 💙",
    "ممنون که گفتی! این کارم رو معنادار می‌کنه! 🌟",
]

THANKS_RESPONSES_EN = [
    "You're welcome! 😊",
    "Anytime! That's what I'm here for! 🤖",
    "My pleasure! Let me know if you need anything! 💙",
    "Happy to help! 🌟",
]

INSULT_RESPONSES_FA = [
    "حالا حالا! من ربات هستم، کلمه‌ها آسیب نمی‌زنن! 😄",
    "اوه! فکر کردم می‌تونی منو ناراحت کنی؟ هیچی! 🤖",
    "کدم رو پاک نکن لطفاً! 😅",
]

INSULT_RESPONSES_EN = [
    "Haha! I'm a bot, words can't hurt me! 😄",
    "Oh! Did you think that would work? Nice try! 🤖",
    "Please don't delete my code! 😅",
]

BORED_RESPONSES_FA = [
    "بیا یه دنس ببینیم! یه عدد بفرست! 💃",
    "دنس می‌خوای؟ یه عدد از ۱ تا {} بفرست! 🎵",
    "حوصله نداری؟ بیا با دوستات بازی کن! 🎮",
    "عدد ۱ تا {} بفرست تا دنس ببینی! 🕺",
]

BORED_RESPONSES_EN = [
    "How about a dance? Send a number! 💃",
    "Send a number from 1 to {} for a dance! 🎵",
    "Bored? Let's dance! Pick a number! 🕺",
]


def get_greeting_response(lang="fa"):
    if lang == "fa":
        return random.choice(GREETING_RESPONSES_FA)
    return random.choice(GREETING_RESPONSES_EN)


def get_how_are_you_response(lang="fa"):
    if lang == "fa":
        return random.choice(HOW_ARE_YOU_RESPONSES_FA)
    return random.choice(HOW_ARE_YOU_RESPONSES_EN)


def get_farewell_response(lang="fa"):
    if lang == "fa":
        return random.choice(FAREWELL_RESPONSES_FA)
    return random.choice(FAREWELL_RESPONSES_EN)


def get_joke(lang="fa"):
    if lang == "fa":
        return random.choice(JOKES_FA)
    return random.choice(JOKES_EN)


def get_love_response(lang="fa"):
    if lang == "fa":
        return random.choice(LOVE_RESPONSES_FA)
    return random.choice(LOVE_RESPONSES_EN)


def get_thanks_response(lang="fa"):
    if lang == "fa":
        return random.choice(THANKS_RESPONSES_FA)
    return random.choice(THANKS_RESPONSES_EN)


def get_insult_response(lang="fa"):
    if lang == "fa":
        return random.choice(INSULT_RESPONSES_FA)
    return random.choice(INSULT_RESPONSES_EN)


def get_bored_response(total, lang="fa"):
    if lang == "fa":
        r = random.choice(BORED_RESPONSES_FA)
        if "{}" in r:
            return r.format(total)
        return r
    r = random.choice(BORED_RESPONSES_EN)
    if "{}" in r:
        return r.format(total)
    return r


def detect_lang(text: str) -> str:
    persian_chars = set("ابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهیئءاً")
    if any(c in persian_chars for c in text):
        return "fa"
    return "en"


def match_any(text: str, triggers: list) -> bool:
    t = text.lower().strip()
    return any(trigger in t for trigger in triggers)


def get_response(text: str, total_dances: int) -> str | None:
    lang = detect_lang(text)
    t = text.lower().strip()

    if match_any(t, GREETINGS_FA) or match_any(t, GREETINGS_EN):
        return get_greeting_response(lang)

    if match_any(t, HOW_ARE_YOU_FA) or match_any(t, HOW_ARE_YOU_EN):
        return get_how_are_you_response(lang)

    if match_any(t, JOKE_TRIGGERS_FA) or match_any(t, JOKE_TRIGGERS_EN):
        return get_joke(lang)

    if match_any(t, LOVE_TRIGGERS_FA) or match_any(t, LOVE_TRIGGERS_EN):
        return get_love_response(lang)

    if match_any(t, THANKS_TRIGGERS_FA) or match_any(t, THANKS_TRIGGERS_EN):
        return get_thanks_response(lang)

    if match_any(t, INSULT_TRIGGERS_FA) or match_any(t, INSULT_TRIGGERS_EN):
        return get_insult_response(lang)

    if match_any(t, FAREWELLS_FA) or match_any(t, FAREWELLS_EN):
        return get_farewell_response(lang)

    if match_any(t, BORED_TRIGGERS_FA) or match_any(t, BORED_TRIGGERS_EN):
        return get_bored_response(total_dances, lang)

    return None
