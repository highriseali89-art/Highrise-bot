import asyncio
import random
import re
from datetime import datetime
from highrise import BaseBot
from highrise.models import (
    User, Position, AnchorPosition, SessionMetadata, CurrencyItem,
)
from dances import DANCES, get_dance, persian_to_int, total_dances
from responses import get_response, detect_lang
from config import (
    load_admins, save_admins,
    load_teleport, save_teleport, delete_teleport,
    load_zones, save_zones, delete_all_zones,
    load_vips, save_vips,
)

TIP_AMOUNT = CurrencyItem(amount=1, type="gold_bar_1")

# ─────────────────────────────────────────────────────────────────
# Static data
# ─────────────────────────────────────────────────────────────────

DJ_NAMES = [
    "🎧 DJ Fire", "🎵 DJ Blaze", "🎶 DJ Storm", "🔥 DJ Wave",
    "💫 DJ Star", "🌊 DJ Ocean", "⚡ DJ Thunder", "🎸 DJ Rock",
    "🌙 DJ Night", "☀️ DJ Sunny", "🦋 DJ Butterfly", "🌈 DJ Rainbow",
]

BATTLE_OUTCOMES = [
    "با یه حرکت خفن همه رو متوقف کرد! 🔥",
    "فلور رو گرفت و هیچکس نتونست جواب بده! 👑",
    "با انرژی فوق‌العاده‌ای همه رو شگفت‌زده کرد! 💥",
    "ریتم رو کاملاً در دست گرفت! 🎵",
    "حرکاتش بی‌نظیر بود — قهرمان بی‌چون و چرا! 🏆",
]

VIP_WELCOME = [
    "✨ یه ستاره وارد شد! خوش اومدی VIP عزیز!",
    "👑 سلطان/سلطانه وارد شد! همه احترام بذارید!",
    "💎 یه الماس وارد روم شد! خوش اومدی!",
    "🌟 ستاره ویژه ما وارد شد! روم نورانی شد!",
    "🔥 VIP آمد! بهترین‌ها فقط بهترین جاها میان!",
]

COMPLIMENTS = [
    "چقدر باحالی! 🌟", "تو بهترین عضو روم هستی! 👑",
    "انرژیت بی‌نظیره! ⚡", "خیلی باکلاسی! 💎",
    "دنستت حرف نداره! 💃", "روم بدون تو کامل نیست! 🌸",
    "تو یه هنرمند واقعی هستی! 🎨", "شخصیتت خیلی جذابه! ✨",
    "همیشه مثبت و پرانرژی هستی! 🔥", "خوش‌تیپ‌ترین آدم روم! 😎",
]

TRIVIA_QUESTIONS = [
    ("پایتخت ایران کجاست؟", ["تهران", "tehran"]),
    ("بزرگترین کشور جهان کدامه؟", ["روسیه", "russia"]),
    ("نویسنده شاهنامه کیه؟", ["فردوسی", "فردوسي", "ferdowsi"]),
    ("رنگ آسمان در روز چیه؟", ["آبی", "ابی", "blue"]),
    ("عدد ۵ ضربدر ۵ چند میشه؟", ["۲۵", "25"]),
    ("پرجمعیت‌ترین کشور جهان کدامه؟", ["چین", "china"]),
    ("کدام حیوان بزرگترین پستاندار دریایی‌ه؟", ["نهنگ", "نهنگ آبی", "whale"]),
    ("عدد پی (π) با چه عددی شروع میشه؟", ["۳", "3"]),
    ("هواپیما رو چه کسی اختراع کرد؟", ["برادران رایت", "رایت", "wright"]),
    ("خورشید از کجا طلوع میکنه؟", ["شرق", "مشرق", "east"]),
    ("کدام فصل گرم‌ترین فصله؟", ["تابستان", "summer"]),
    ("زبان رسمی برزیل چیه؟", ["پرتغالی", "portuguese"]),
    ("عدد ۱۰ ضربدر ۱۰ چند میشه؟", ["۱۰۰", "100"]),
    ("مرتفع‌ترین کوه جهان کدامه؟", ["اورست", "اورست", "everest"]),
    ("کدام سیاره به خورشید نزدیک‌تره؟", ["عطارد", "mercury"]),
]

# mood messages
MOOD_DATA = {
    "energetic": {
        "emoji": "🔥",
        "label": "Energetic",
        "welcome": [
            "🔥 YO! {u} وارد شد! بریم باهاش بریزیم! 💪",
            "⚡ {u} اینجاست! آماده دنس هستیم! 🔥",
        ],
        "chat_prefix": "🔥 ",
    },
    "chill": {
        "emoji": "😌",
        "label": "Chill",
        "welcome": [
            "😌 {u} عزیز، خوش اومدی. راحت باش! 🌿",
            "🌊 {u} سلام. امیدوارم وقت خوبی داشته باشی! ☁️",
        ],
        "chat_prefix": "😌 ",
    },
    "funny": {
        "emoji": "😂",
        "label": "Funny",
        "welcome": [
            "😂 بپا {u} اومد! الان دردسر شروع میشه 😆",
            "🤪 {u} وارد ساختمون شد! اورژانس آماده باشه! 😂",
        ],
        "chat_prefix": "🤣 ",
    },
}

HELP_FA = """╔════════════════════════════╗
║       🤖 راهنمای ربات       ║
╠════════════════════════════╣
║ 💃 عدد ۱ تا {total} → دنس  ║
║   stop — توقف               ║
╠════════════════════════════╣
║ 🎲 roll — دنس تصادفی        ║
║ ⚔️  battle @user — مبارزه   ║
║ 📢 shout @user [پیام]       ║
║ 💬 compliment @user         ║
╠════════════════════════════╣
║ 🎧 dj on / dj off           ║
║ 🎊 party on / party off     ║
║ ❓ trivia — سوال جایزه‌دار  ║
╠════════════════════════════╣
║ 🏆 top — برترین دنسرها      ║
║ 🎭 mood energetic/chill/    ║
║       funny (ادمین)         ║
╠════════════════════════════╣
║ 💰 تیپ (ادمین):             ║
║   tip all / tip @user      ║
║   lucky — تیپ تصادفی       ║
║   timer 60 — شمارش معکوس   ║
║   say پیام — اعلام بات      ║
║   announce پیام — اعلام رسمی║
╠════════════════════════════╣
║ 🚫 kick/mute/ban @user      ║
║ 📍 set tel / unset tele     ║
║   ویپر tp — تله‌پورت        ║
║ 🎯 set zone [عدد] / unset   ║
╠════════════════════════════╣
║ 👑 صاحب روم:                ║
║   admin add/remove @user   ║
║   vip add/remove @user     ║
║   «بیا بات»                ║
╚════════════════════════════╝"""

HELP_EN = """╔════════════════════════════╗
║      🤖 Bot Help Guide      ║
╠════════════════════════════╣
║ 💃 Number 1-{total} → dance ║
║   stop — stop dance        ║
╠════════════════════════════╣
║ 🎲 roll — random dance      ║
║ ⚔️  battle @user — battle   ║
║ 📢 shout @user [message]    ║
║ 💬 compliment @user         ║
╠════════════════════════════╣
║ 🎧 dj on / dj off           ║
║ 🎊 party on / party off     ║
║ ❓ trivia — win a tip!      ║
╠════════════════════════════╣
║ 🏆 top — dance leaderboard  ║
║ 🎭 mood energetic/chill/    ║
║       funny (admin)         ║
╠════════════════════════════╣
║ 💰 Tip (admin):             ║
║   tip all / tip @user      ║
║   lucky — random tip       ║
║   timer 60 — countdown     ║
║   say text — bot speaks    ║
║   announce text — big msg  ║
╠════════════════════════════╣
║ 🚫 kick/mute/ban @user      ║
║ 📍 set tel / unset tele     ║
║   whisper tp — teleport    ║
║ 🎯 set zone [num] / unset   ║
╠════════════════════════════╣
║ 👑 Owner only:              ║
║   admin add/remove @user   ║
║   vip add/remove @user     ║
║   "come here bot"          ║
╚════════════════════════════╝"""


# ─────────────────────────────────────────────────────────────────
# Bot class
# ─────────────────────────────────────────────────────────────────

class HighriseBot(BaseBot):

    def __init__(self):
        super().__init__()
        self.owner_id: str | None = None
        self.admins: list[str] = load_admins()
        self.vips: list[str] = load_vips()
        # dance tasks per user
        self.user_dance_tasks: dict[str, asyncio.Task] = {}
        # zones
        self.zones: list[dict] = load_zones()
        self.user_zone: dict[str, str] = {}
        # auto DJ
        self.dj_task: asyncio.Task | None = None
        self.dj_on: bool = False
        # party mode
        self.party_task: asyncio.Task | None = None
        self.party_on: bool = False
        # trivia
        self.trivia_active: bool = False
        self.trivia_answer: list[str] = []
        # timer
        self.timer_task: asyncio.Task | None = None
        # dance stats (in memory)
        self.dance_counts: dict[str, int] = {}   # user_id → count
        self.user_names: dict[str, str] = {}      # user_id → username
        # mood
        self.mood: str = "energetic"
        # room users cache
        self.room_users: dict[str, User] = {}

    # ── Lifecycle ─────────────────────────────────────────────────

    async def on_start(self, session_metadata: SessionMetadata) -> None:
        self.owner_id = session_metadata.room_info.owner_id
        print(f"[BOT] Online | owner={self.owner_id}")
        await self.highrise.chat("🤖 ربات آنلاین شد! برای راهنما: help یا راهنما 🎉")
        await self._sync_room_users()

    async def on_user_join(self, user: User, position: Position | AnchorPosition) -> None:
        self.room_users[user.id] = user
        self.user_names[user.id] = user.username

        # VIP welcome
        if user.id in self.vips:
            msg = random.choice(VIP_WELCOME)
            await self.highrise.chat(f"{msg} 🌟 @{user.username}")
            try:
                await self.highrise.send_emote(random.choice(DANCES[:20]))
            except Exception:
                pass
            return

        # time-based + mood-based welcome whisper
        hour = datetime.now().hour
        if 6 <= hour < 12:
            time_greet = "صبح بخیر ☀️"
        elif 12 <= hour < 18:
            time_greet = "ظهر بخیر 🌤️"
        elif 18 <= hour < 22:
            time_greet = "عصر بخیر 🌇"
        else:
            time_greet = "شب بخیر 🌙"

        mood_info = MOOD_DATA.get(self.mood, MOOD_DATA["energetic"])
        mood_welcome = random.choice(mood_info["welcome"]).format(u=user.username)

        # public mood welcome
        await self.highrise.chat(mood_welcome)

        # private full welcome
        await self.highrise.send_whisper(
            user.id,
            f"👋 {time_greet} {user.username} عزیز!\n"
            f"💃 عدد ۱ تا {total_dances()} برای دنس\n"
            f"🎲 roll — دنس تصادفی\n"
            f"⚔️ battle @user — مبارزه\n"
            f"❓ trivia — تیپ جایزه\n"
            f"📖 help برای همه دستورها"
        )
        try:
            await self.highrise.send_emote(random.choice(DANCES[:30]))
        except Exception:
            pass

    async def on_user_leave(self, user: User) -> None:
        self.room_users.pop(user.id, None)
        self._cancel_dance(user.id)
        self.user_zone.pop(user.id, None)
        # farewell based on mood
        mood_info = MOOD_DATA.get(self.mood, MOOD_DATA["energetic"])
        farewells = {
            "energetic": f"💨 @{user.username} رفت! انرژیش باهامون موند! 🔥",
            "chill": f"🌿 @{user.username} خداحافظ! برو به سلامت! 😌",
            "funny": f"😂 @{user.username} فرار کرد! دنبالش نگیرید! 🤣",
        }
        await self.highrise.chat(farewells.get(self.mood, f"👋 خداحافظ @{user.username}!"))

    async def on_user_move(self, user: User, destination: Position | AnchorPosition) -> None:
        self.room_users[user.id] = user
        if not isinstance(destination, Position) or not self.zones:
            return
        zone = self._find_zone_at(destination.x, destination.y, destination.z)
        if zone:
            if self.user_zone.get(user.id) == zone["label"]:
                return
            self.user_zone[user.id] = zone["label"]
            dance_id = get_dance(zone["dance"]) if zone.get("dance") else random.choice(DANCES[:50])
            await self.highrise.chat(f"🎯 @{user.username} وارد زون دنس شد! 🕺💃🎵")
            self._cancel_dance(user.id)
            self.user_dance_tasks[user.id] = asyncio.create_task(
                self._dance_loop(dance_id, user.id)
            )
        else:
            if user.id in self.user_zone:
                self.user_zone.pop(user.id)
                self._cancel_dance(user.id)
                try:
                    await self.highrise.send_emote(random.choice(DANCES[:30]))
                except Exception:
                    pass

    # ── Main chat handler ─────────────────────────────────────────

    async def on_chat(self, user: User, message: str) -> None:
        self.room_users[user.id] = user
        self.user_names[user.id] = user.username
        msg = message.strip()
        msg_lower = msg.lower()

        # ── Trivia answer check (always first) ──
        if self.trivia_active and self.trivia_answer:
            if msg_lower.strip() in self.trivia_answer:
                await self._trivia_correct(user)
                return

        # ── Help ──
        if msg_lower in ("help", "راهنما", "/help", "!help"):
            lang = detect_lang(msg)
            text = HELP_FA if lang == "fa" else HELP_EN
            await self.highrise.send_whisper(user.id, text.format(total=total_dances()))
            return

        # ── Stop dance ──
        if msg_lower in ("stop", "استاپ", "وایسا", "بس", "بس کن", "i stop"):
            await self._stop_dance(user)
            return

        # ── Roll ──
        if msg_lower in ("roll", "رول", "تصادفی", "رندوم"):
            await self._handle_roll(user)
            return

        # ── Top leaderboard ──
        if msg_lower in ("top", "لیدربورد", "برترین", "top dancers"):
            await self._handle_top(user)
            return

        # ── Trivia start ──
        if msg_lower in ("trivia", "سوال", "quiz"):
            await self._start_trivia()
            return

        # ── Battle ──
        m = re.match(r"battle\s+@?(\S+)", msg_lower)
        if m:
            await self._handle_battle(user, m.group(1))
            return

        # ── Shoutout ──
        m = re.match(r"shout\s+@?(\S+)(?:\s+(.+))?", msg, re.IGNORECASE)
        if m and msg_lower.startswith("shout"):
            await self._handle_shoutout(user, m.group(1), m.group(2))
            return

        # ── Compliment ──
        m = re.match(r"compliment\s+@?(\S+)", msg_lower)
        if m:
            await self._handle_compliment(user, m.group(1))
            return

        # ── DJ ──
        if msg_lower in ("dj on", "dj روشن"):
            await self._dj_start(user)
            return
        if msg_lower in ("dj off", "dj خاموش"):
            await self._dj_stop(user)
            return

        # ── Party ──
        if msg_lower in ("party on", "پارتی"):
            await self._party_start(user)
            return
        if msg_lower in ("party off", "پارتی آف"):
            await self._party_stop(user)
            return

        # ── Number → dance ──
        num = persian_to_int(msg)
        if num is not None:
            await self._start_dance(user, num)
            return

        # ── Admin commands ──
        if self._is_admin(user.id):
            if await self._handle_admin_commands(user, msg, msg_lower):
                return

        # ── Owner commands ──
        if self._is_owner(user.id):
            if await self._handle_owner_commands(user, msg, msg_lower):
                return

        # ── Moderation ──
        if await self._handle_moderation(user, msg, msg_lower):
            return

        # ── Come here ──
        if await self._handle_come_here(user, msg, msg_lower):
            return

        # ── Natural language ──
        reply = get_response(msg, total_dances())
        if reply:
            mood_info = MOOD_DATA.get(self.mood, MOOD_DATA["energetic"])
            await self.highrise.chat(mood_info["chat_prefix"] + reply)

    async def on_emote(self, user: User, emote_id: str, receiver: User | None) -> None:
        print(f"[EMOTE] user={user.username} emote={emote_id} receiver={receiver.username if receiver else None}")

    async def on_whisper(self, user: User, message: str) -> None:
        msg_lower = message.lower().strip()
        if msg_lower in ("tp", "tele", "teleport", "تله‌پورت", "تلپورت"):
            await self._do_teleport(user)

    # ─────────────────────────────────────────────────────────────
    # 💃 Dance system
    # ─────────────────────────────────────────────────────────────

    async def _start_dance(self, user: User, num: int) -> None:
        dance_id = get_dance(num)
        if not dance_id:
            await self.highrise.send_whisper(
                user.id, f"❌ عدد اشتباه! بین ۱ تا {total_dances()} بفرست."
            )
            return
        self._cancel_dance(user.id)
        # track dance stat
        self.dance_counts[user.id] = self.dance_counts.get(user.id, 0) + 1
        self.user_names[user.id] = user.username
        await self.highrise.send_whisper(
            user.id, f"💃 دنس #{num} شروع شد! برای توقف: stop"
        )
        self.user_dance_tasks[user.id] = asyncio.create_task(
            self._dance_loop(dance_id, user.id)
        )

    async def _dance_loop(self, dance_id: str, user_id: str) -> None:
        try:
            while True:
                await self.highrise.send_emote(dance_id, user_id)
                await asyncio.sleep(8)
        except asyncio.CancelledError:
            pass
        except Exception as e:
            print(f"[BOT] dance_loop error dance={dance_id} uid={user_id}: {e}")

    async def _stop_dance(self, user: User) -> None:
        if user.id in self.user_dance_tasks:
            self._cancel_dance(user.id)
            await self.highrise.send_whisper(user.id, "⏹️ دنس متوقف شد!")
        else:
            await self.highrise.send_whisper(user.id, "🤔 دنس فعالی نداری!")

    def _cancel_dance(self, user_id: str) -> None:
        task = self.user_dance_tasks.pop(user_id, None)
        if task and not task.done():
            task.cancel()

    # ─────────────────────────────────────────────────────────────
    # 🎲 Roll
    # ─────────────────────────────────────────────────────────────

    async def _handle_roll(self, user: User) -> None:
        num = random.randint(1, min(50, total_dances()))
        dance_id = get_dance(num)
        self.dance_counts[user.id] = self.dance_counts.get(user.id, 0) + 1
        self.user_names[user.id] = user.username
        await self.highrise.chat(f"🎲 @{user.username} تاس انداخت → دنس #{num}! 💃")
        self._cancel_dance(user.id)
        if dance_id:
            self.user_dance_tasks[user.id] = asyncio.create_task(
                self._dance_loop(dance_id, user.id)
            )

    # ─────────────────────────────────────────────────────────────
    # 🏆 Dance Leaderboard
    # ─────────────────────────────────────────────────────────────

    async def _handle_top(self, user: User) -> None:
        if not self.dance_counts:
            await self.highrise.chat("📊 هنوز کسی دنس نزده!")
            return
        sorted_dancers = sorted(self.dance_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]
        lines = ["🏆 برترین دنسرهای روم:"]
        for i, (uid, count) in enumerate(sorted_dancers):
            name = self.user_names.get(uid, uid[:8])
            lines.append(f"{medals[i]} @{name} — {count} دنس")
        await self.highrise.chat("\n".join(lines))

    # ─────────────────────────────────────────────────────────────
    # ❓ Trivia
    # ─────────────────────────────────────────────────────────────

    async def _start_trivia(self) -> None:
        if self.trivia_active:
            await self.highrise.chat("❓ سوال قبلی هنوز جواب داده نشده!")
            return
        q, answers = random.choice(TRIVIA_QUESTIONS)
        self.trivia_active = True
        self.trivia_answer = answers
        await self.highrise.chat(
            f"❓ سوال: {q}\n"
            f"💰 اول جواب بده، یه تیپ بگیر! ⏱️ ۳۰ ثانیه فرصت!"
        )
        asyncio.create_task(self._trivia_timeout())

    async def _trivia_correct(self, user: User) -> None:
        self.trivia_active = False
        self.trivia_answer = []
        await self.highrise.chat(
            f"🎉 آفرین @{user.username}! جواب درست بود! 🏆"
        )
        try:
            await self.highrise.tip_user(user.id, TIP_AMOUNT)
            await self.highrise.chat(f"💰 جایزه به @{user.username} رسید!")
        except Exception:
            pass

    async def _trivia_timeout(self) -> None:
        await asyncio.sleep(30)
        if self.trivia_active:
            self.trivia_active = False
            self.trivia_answer = []
            await self.highrise.chat("⏰ وقت تموم شد! کسی جواب نداد 😅")

    # ─────────────────────────────────────────────────────────────
    # ⚔️ Dance Battle
    # ─────────────────────────────────────────────────────────────

    async def _handle_battle(self, challenger: User, target_name: str) -> None:
        target = self._find_user_by_name(target_name)
        if not target:
            await self.highrise.chat(f"❌ کاربر @{target_name} پیدا نشد.")
            return
        if target.id == challenger.id:
            await self.highrise.chat("😂 نمیشه با خودت مبارزه کنی!")
            return
        await self.highrise.chat(
            f"⚔️ @{challenger.username} به @{target.username} چالش دنس داد! 🔥"
        )
        await asyncio.sleep(1)
        num1 = random.randint(1, 20)
        num2 = random.randint(1, 20)
        d1 = get_dance(num1)
        d2 = get_dance(num2)
        await self.highrise.chat(
            f"🎵 @{challenger.username} → #{num1}  VS  @{target.username} → #{num2}"
        )
        self._cancel_dance(challenger.id)
        self._cancel_dance(target.id)
        if d1:
            self.user_dance_tasks[challenger.id] = asyncio.create_task(
                self._dance_loop(d1, challenger.id)
            )
        if d2:
            self.user_dance_tasks[target.id] = asyncio.create_task(
                self._dance_loop(d2, target.id)
            )
        await asyncio.sleep(10)
        winner = random.choice([challenger, target])
        loser = target if winner.id == challenger.id else challenger
        outcome = random.choice(BATTLE_OUTCOMES)
        self._cancel_dance(challenger.id)
        self._cancel_dance(target.id)
        await self.highrise.chat(
            f"🏆 برنده: @{winner.username}\n{outcome}\n😅 @{loser.username} بهتره تمرین کنه!"
        )
        try:
            await self.highrise.tip_user(winner.id, TIP_AMOUNT)
            await self.highrise.chat(f"💰 جایزه به @{winner.username}! 🎊")
        except Exception:
            pass

    # ─────────────────────────────────────────────────────────────
    # 📢 Shoutout
    # ─────────────────────────────────────────────────────────────

    async def _handle_shoutout(self, sender: User, target_name: str, custom_msg: str | None) -> None:
        target = self._find_user_by_name(target_name)
        name = f"@{target.username}" if target else f"@{target_name}"
        if custom_msg:
            text = f"📢 شاوت‌اوت از @{sender.username} به {name}:\n💬 «{custom_msg.strip()}»"
        else:
            text = f"📢 شاوت‌اوت از @{sender.username} به {name}: {random.choice(COMPLIMENTS)}"
        await self.highrise.chat(text)
        try:
            await self.highrise.send_emote(random.choice(DANCES[:15]))
        except Exception:
            pass

    # ─────────────────────────────────────────────────────────────
    # 💬 Compliment
    # ─────────────────────────────────────────────────────────────

    async def _handle_compliment(self, sender: User, target_name: str) -> None:
        target = self._find_user_by_name(target_name)
        name = f"@{target.username}" if target else f"@{target_name}"
        compliment = random.choice(COMPLIMENTS)
        await self.highrise.chat(f"💬 @{sender.username} به {name} میگه: {compliment} 🌸")

    # ─────────────────────────────────────────────────────────────
    # 🎧 Auto DJ
    # ─────────────────────────────────────────────────────────────

    async def _dj_start(self, user: User) -> None:
        if not self._is_admin(user.id):
            await self.highrise.send_whisper(user.id, "⚠️ فقط ادمین می‌تونه DJ رو روشن کنه!")
            return
        if self.dj_on:
            await self.highrise.chat("🎧 DJ از قبل روشنه!")
            return
        self.dj_on = True
        self.dj_task = asyncio.create_task(self._dj_loop())
        await self.highrise.chat(
            f"🎧 {random.choice(DJ_NAMES)} وارد شد! بریم! 🔥🎵"
        )

    async def _dj_stop(self, user: User) -> None:
        if not self._is_admin(user.id):
            await self.highrise.send_whisper(user.id, "⚠️ فقط ادمین!")
            return
        if not self.dj_on:
            await self.highrise.chat("🎧 DJ الان خاموشه!")
            return
        self.dj_on = False
        if self.dj_task and not self.dj_task.done():
            self.dj_task.cancel()
        await self.highrise.chat("🎧 DJ سشن تموم شد! ممنون! 🙏🎵")

    async def _dj_loop(self) -> None:
        track = 0
        try:
            while self.dj_on:
                track += 1
                num = random.randint(1, min(50, total_dances()))
                dance_id = get_dance(num)
                dj = random.choice(DJ_NAMES)
                await self.highrise.chat(f"🎵 Track #{track} — {dj} playing #{num}! 🕺")
                if dance_id:
                    try:
                        await self.highrise.send_emote(dance_id)
                    except Exception:
                        pass
                await asyncio.sleep(30)
        except asyncio.CancelledError:
            pass

    # ─────────────────────────────────────────────────────────────
    # 🎊 Party Mode
    # ─────────────────────────────────────────────────────────────

    async def _party_start(self, user: User) -> None:
        if not self._is_admin(user.id):
            await self.highrise.send_whisper(user.id, "⚠️ فقط ادمین!")
            return
        if self.party_on:
            await self.highrise.chat("🎊 پارتی از قبل روشنه!")
            return
        self.party_on = True
        if not self.dj_on:
            self.dj_on = True
            self.dj_task = asyncio.create_task(self._dj_loop())
        self.party_task = asyncio.create_task(self._party_loop())
        await self.highrise.chat(
            "🎊🎉🎈 پارتی شروع شد! 🎈🎉🎊\n"
            "💃 DJ روشنه | 💰 تیپ‌های شانسی | 📢 شاوت‌اوت‌های خودکار!"
        )

    async def _party_stop(self, user: User) -> None:
        if not self._is_admin(user.id):
            await self.highrise.send_whisper(user.id, "⚠️ فقط ادمین!")
            return
        self.party_on = False
        if self.party_task and not self.party_task.done():
            self.party_task.cancel()
        await self._dj_stop(user)
        await self.highrise.chat("🎊 پارتی تموم شد! ممنون از همه! 🙏✨")

    async def _party_loop(self) -> None:
        round_num = 0
        try:
            while self.party_on:
                round_num += 1
                await asyncio.sleep(60)
                if not self.party_on:
                    break
                # auto shoutout random user
                if self.room_users:
                    lucky = random.choice(list(self.room_users.values()))
                    compliment = random.choice(COMPLIMENTS)
                    await self.highrise.chat(
                        f"🎊 پارتی شاوت‌اوت #{round_num}: @{lucky.username} — {compliment}"
                    )
                    await asyncio.sleep(5)
                    # lucky tip every other round
                    if round_num % 2 == 0:
                        candidates = list(self.room_users.values())
                        if candidates:
                            winner = random.choice(candidates)
                            await self.highrise.chat(f"🍀 تیپ شانسی پارتی به @{winner.username}! 💰")
                            try:
                                await self.highrise.tip_user(winner.id, TIP_AMOUNT)
                            except Exception:
                                pass
        except asyncio.CancelledError:
            pass

    # ─────────────────────────────────────────────────────────────
    # 🍀 Lucky Tip
    # ─────────────────────────────────────────────────────────────

    async def _handle_lucky_tip(self, sender: User) -> None:
        await self._sync_room_users()
        candidates = [u for uid, u in self.room_users.items() if uid != sender.id]
        if not candidates:
            await self.highrise.chat("❌ هیچ‌کسی تو روم نیست!")
            return
        winner = random.choice(candidates)
        await self.highrise.chat(f"🍀 قرعه‌کشی! برنده: @{winner.username}! 🎉")
        await asyncio.sleep(1)
        try:
            await self.highrise.tip_user(winner.id, TIP_AMOUNT)
            await self.highrise.chat(f"💰 تیپ به @{winner.username} رسید! تبریک! 🎊")
        except Exception as e:
            await self.highrise.chat(f"❌ {e}")

    # ─────────────────────────────────────────────────────────────
    # ⏰ Timer / Countdown
    # ─────────────────────────────────────────────────────────────

    async def _handle_timer(self, user: User, seconds: int) -> None:
        if seconds <= 0 or seconds > 300:
            await self.highrise.chat("❌ تایمر باید بین ۱ تا ۳۰۰ ثانیه باشه.")
            return
        if self.timer_task and not self.timer_task.done():
            self.timer_task.cancel()
        self.timer_task = asyncio.create_task(self._timer_loop(seconds))
        await self.highrise.chat(f"⏰ تایمر {seconds} ثانیه‌ای شروع شد!")

    async def _timer_loop(self, total: int) -> None:
        try:
            checkpoints = [c for c in [total, total // 2, 10, 5, 3, 2, 1] if 0 < c < total]
            checkpoints = sorted(set(checkpoints), reverse=True)
            elapsed = 0
            for checkpoint in checkpoints:
                wait = total - elapsed - (total - checkpoint)
                if wait > 0:
                    await asyncio.sleep(wait)
                    elapsed = total - checkpoint
                remaining = total - elapsed
                if remaining > 0:
                    await self.highrise.chat(f"⏰ {remaining} ثانیه مونده!")
            remaining_wait = total - elapsed
            if remaining_wait > 0:
                await asyncio.sleep(remaining_wait)
            await self.highrise.chat("🔔 تایمر تموم شد! ⏰✅")
        except asyncio.CancelledError:
            pass

    # ─────────────────────────────────────────────────────────────
    # 🎭 Mood
    # ─────────────────────────────────────────────────────────────

    async def _handle_mood(self, user: User, mood: str) -> None:
        if not self._is_admin(user.id):
            await self.highrise.send_whisper(user.id, "⚠️ فقط ادمین می‌تونه حالت رو عوض کنه!")
            return
        mood = mood.lower().strip()
        mood_map = {
            "energetic": "energetic", "انرژیک": "energetic", "پرانرژی": "energetic",
            "chill": "chill", "آروم": "chill", "آرام": "chill",
            "funny": "funny", "خنده": "funny", "بامزه": "funny",
        }
        target = mood_map.get(mood)
        if not target:
            await self.highrise.chat(
                "🎭 حالت‌های موجود: energetic | chill | funny"
            )
            return
        self.mood = target
        info = MOOD_DATA[target]
        await self.highrise.chat(
            f"🎭 حالت ربات تغییر کرد به: {info['emoji']} {info['label']}!"
        )

    # ─────────────────────────────────────────────────────────────
    # Admin commands
    # ─────────────────────────────────────────────────────────────

    async def _handle_admin_commands(self, user: User, msg: str, msg_lower: str) -> bool:

        # mood
        m = re.match(r"mood\s+(\S+)", msg_lower)
        if m:
            await self._handle_mood(user, m.group(1))
            return True

        # timer
        m = re.match(r"timer\s+(\d+)", msg_lower)
        if m:
            await self._handle_timer(user, int(m.group(1)))
            return True

        # say
        m = re.match(r"say\s+(.+)", msg, re.IGNORECASE)
        if m and msg_lower.startswith("say "):
            await self.highrise.chat(f"🤖 {m.group(1).strip()}")
            return True

        # announce
        m = re.match(r"announce\s+(.+)", msg, re.IGNORECASE)
        if m and msg_lower.startswith("announce "):
            text = m.group(1).strip()
            border = "═" * min(len(text) + 4, 28)
            await self.highrise.chat(
                f"╔{border}╗\n"
                f"║  📣 {text}  ║\n"
                f"╚{border}╝"
            )
            return True

        # tip all
        if msg_lower.startswith("tip all"):
            await self._tip_all(user)
            return True

        # tip @user
        m = re.match(r"tip\s+@?(\S+)", msg_lower)
        if m and msg_lower.startswith("tip"):
            await self._tip_user_by_name(user, m.group(1))
            return True

        # lucky
        if msg_lower in ("lucky", "لاکی", "قرعه"):
            await self._handle_lucky_tip(user)
            return True

        # set teleport
        if msg_lower.startswith("set tel"):
            await self._save_teleport(user)
            return True

        # unset teleport
        if msg_lower.startswith("unset tele"):
            delete_teleport()
            await self.highrise.chat("📍 تله‌پورت حذف شد.")
            return True

        # set zone
        m = re.match(r"set zone(?:\s+(\S+))?$", msg_lower)
        if m and msg_lower.startswith("set zone"):
            dance_num = persian_to_int(m.group(1)) if m.group(1) else None
            await self._save_zone(user, dance_num)
            return True

        # unset zone
        if msg_lower == "unset zone":
            self.zones.clear()
            delete_all_zones()
            await self.highrise.chat("🎯 تمام زون‌های دنس حذف شدن.")
            return True

        return False

    # ─────────────────────────────────────────────────────────────
    # Owner-only commands
    # ─────────────────────────────────────────────────────────────

    async def _handle_owner_commands(self, user: User, msg: str, msg_lower: str) -> bool:
        # admin add
        m = re.match(r"admin\s+add\s+@?(\S+)", msg_lower)
        if m:
            target = self._find_user_by_name(m.group(1))
            if target:
                if target.id not in self.admins:
                    self.admins.append(target.id)
                    save_admins(self.admins)
                    await self.highrise.chat(f"✅ @{target.username} ادمین بات شد!")
                else:
                    await self.highrise.chat(f"⚠️ @{target.username} از قبل ادمینه!")
            else:
                await self.highrise.chat(f"❌ @{m.group(1)} پیدا نشد.")
            return True

        # admin remove
        m = re.match(r"admin\s+remove\s+@?(\S+)", msg_lower)
        if m:
            target = self._find_user_by_name(m.group(1))
            if target and target.id in self.admins:
                self.admins.remove(target.id)
                save_admins(self.admins)
                await self.highrise.chat(f"✅ @{target.username} از ادمین‌ها حذف شد!")
            elif target:
                await self.highrise.chat(f"⚠️ @{target.username} ادمین نیست!")
            else:
                await self.highrise.chat(f"❌ @{m.group(1)} پیدا نشد.")
            return True

        # admin list
        if msg_lower in ("admin list", "لیست ادمین"):
            if not self.admins:
                await self.highrise.chat("📋 هیچ ادمینی ثبت نشده.")
            else:
                names = [
                    f"@{self.room_users[aid].username}" if aid in self.room_users else f"[{aid[:8]}]"
                    for aid in self.admins
                ]
                await self.highrise.chat(f"📋 ادمین‌ها: {', '.join(names)}")
            return True

        # vip add
        m = re.match(r"vip\s+add\s+@?(\S+)", msg_lower)
        if m:
            target = self._find_user_by_name(m.group(1))
            if target:
                if target.id not in self.vips:
                    self.vips.append(target.id)
                    save_vips(self.vips)
                    await self.highrise.chat(f"💎 @{target.username} به VIP‌ها اضافه شد! 👑")
                else:
                    await self.highrise.chat(f"⚠️ @{target.username} از قبل VIPه!")
            else:
                await self.highrise.chat(f"❌ @{m.group(1)} پیدا نشد.")
            return True

        # vip remove
        m = re.match(r"vip\s+remove\s+@?(\S+)", msg_lower)
        if m:
            target = self._find_user_by_name(m.group(1))
            if target and target.id in self.vips:
                self.vips.remove(target.id)
                save_vips(self.vips)
                await self.highrise.chat(f"✅ @{target.username} از VIP‌ها حذف شد.")
            elif target:
                await self.highrise.chat(f"⚠️ @{target.username} VIP نیست!")
            else:
                await self.highrise.chat(f"❌ @{m.group(1)} پیدا نشد.")
            return True

        # vip list
        if msg_lower in ("vip list", "لیست vip"):
            if not self.vips:
                await self.highrise.chat("💎 هیچ VIPی ثبت نشده.")
            else:
                names = [
                    f"@{self.room_users[vid].username}" if vid in self.room_users else f"[{vid[:8]}]"
                    for vid in self.vips
                ]
                await self.highrise.chat(f"💎 VIP‌ها: {', '.join(names)}")
            return True

        return False

    # ─────────────────────────────────────────────────────────────
    # Moderation
    # ─────────────────────────────────────────────────────────────

    async def _handle_moderation(self, user: User, msg: str, msg_lower: str) -> bool:
        if not self._is_admin(user.id):
            return False

        m = re.match(r"kick\s*@?(\S+)", msg_lower)
        if m and msg_lower.startswith("kick"):
            target = self._find_user_by_name(m.group(1))
            if target:
                try:
                    await self.highrise.moderate_room(target.id, "kick")
                    await self.highrise.chat(f"🚪 @{target.username} از روم اخراج شد!")
                except Exception as e:
                    await self.highrise.chat(f"❌ {e}")
            else:
                await self.highrise.chat(f"❌ @{m.group(1)} پیدا نشد.")
            return True

        m = re.match(r"mute\s*@?(\S+)(?:\s+(\d+))?", msg_lower)
        if m and msg_lower.startswith("mute"):
            target = self._find_user_by_name(m.group(1))
            secs = int(m.group(2)) if m.group(2) else 300
            if target:
                try:
                    await self.highrise.moderate_room(target.id, "mute", secs)
                    await self.highrise.chat(f"🔇 @{target.username} برای {secs}ث میوت شد!")
                except Exception as e:
                    await self.highrise.chat(f"❌ {e}")
            else:
                await self.highrise.chat(f"❌ @{m.group(1)} پیدا نشد.")
            return True

        m = re.match(r"ban\s*@?(\S+)", msg_lower)
        if m and msg_lower.startswith("ban"):
            target = self._find_user_by_name(m.group(1))
            if target:
                try:
                    await self.highrise.moderate_room(target.id, "ban")
                    await self.highrise.chat(f"⛔ @{target.username} بن شد!")
                except Exception as e:
                    await self.highrise.chat(f"❌ {e}")
            else:
                await self.highrise.chat(f"❌ @{m.group(1)} پیدا نشد.")
            return True

        m = re.match(r"unban\s*@?(\S+)", msg_lower)
        if m and msg_lower.startswith("unban"):
            target = self._find_user_by_name(m.group(1))
            if target:
                try:
                    await self.highrise.moderate_room(target.id, "unban")
                    await self.highrise.chat(f"✅ @{target.username} آن‌بن شد!")
                except Exception as e:
                    await self.highrise.chat(f"❌ {e}")
            else:
                await self.highrise.chat(f"❌ @{m.group(1)} پیدا نشد.")
            return True

        return False

    # ─────────────────────────────────────────────────────────────
    # Come here (owner)
    # ─────────────────────────────────────────────────────────────

    async def _handle_come_here(self, user: User, msg: str, msg_lower: str) -> bool:
        triggers = ["بیا بات", "بیا ربات", "بیا پیشم", "بیا اینجا",
                    "come here bot", "come bot", "come here rb"]
        if not any(t in msg_lower for t in triggers):
            return False
        if not self._is_owner(user.id):
            await self.highrise.send_whisper(user.id, "⚠️ فقط صاحب روم!")
            return True
        try:
            resp = await self.highrise.get_room_users()
            for u, pos in resp.content:
                if u.id == user.id and isinstance(pos, Position):
                    await self.highrise.teleport(
                        await self._bot_id(),
                        Position(pos.x + 1, pos.y, pos.z, "FrontRight"),
                    )
                    break
        except Exception as e:
            print(f"[BOT] come here error: {e}")
        await self.highrise.send_whisper(user.id, "جانم ارباب! 🤖👑")
        return True

    # ─────────────────────────────────────────────────────────────
    # Tip helpers
    # ─────────────────────────────────────────────────────────────

    async def _tip_all(self, sender: User) -> None:
        await self._sync_room_users()
        count = 0
        for uid, u in list(self.room_users.items()):
            if uid == sender.id:
                continue
            try:
                await self.highrise.tip_user(uid, TIP_AMOUNT)
                count += 1
                await asyncio.sleep(0.5)
            except Exception as e:
                print(f"[BOT] tip error uid={uid}: {e}")
        await self.highrise.chat(f"💰 {count} نفر تیپ گرفتن!")

    async def _tip_user_by_name(self, sender: User, username: str) -> None:
        target = self._find_user_by_name(username)
        if not target:
            await self.highrise.chat(f"❌ @{username} پیدا نشد.")
            return
        try:
            await self.highrise.tip_user(target.id, TIP_AMOUNT)
            await self.highrise.chat(f"💰 @{target.username} تیپ گرفت!")
        except Exception as e:
            await self.highrise.chat(f"❌ {e}")

    # ─────────────────────────────────────────────────────────────
    # Teleport & Zone helpers
    # ─────────────────────────────────────────────────────────────

    async def _save_teleport(self, user: User) -> None:
        try:
            resp = await self.highrise.get_room_users()
            for u, pos in resp.content:
                if u.id == user.id and isinstance(pos, Position):
                    save_teleport({"x": pos.x, "y": pos.y, "z": pos.z, "facing": pos.facing})
                    await self.highrise.chat(
                        f"📍 تله‌پورت ست شد: ({pos.x:.1f}, {pos.y:.1f}, {pos.z:.1f})"
                    )
                    return
            await self.highrise.chat("❌ موقعیت پیدا نشد.")
        except Exception as e:
            await self.highrise.chat(f"❌ {e}")

    async def _do_teleport(self, user: User) -> None:
        tele = load_teleport()
        if tele:
            try:
                pos = Position(tele["x"], tele["y"], tele["z"], tele.get("facing", "FrontRight"))
                await self.highrise.teleport(user.id, pos)
            except Exception as e:
                await self.highrise.send_whisper(user.id, f"❌ {e}")
        else:
            await self.highrise.send_whisper(user.id, "❌ تله‌پورتی ست نشده.")

    async def _save_zone(self, user: User, dance_num: int | None) -> None:
        try:
            resp = await self.highrise.get_room_users()
            for u, pos in resp.content:
                if u.id == user.id and isinstance(pos, Position):
                    label = f"zone_{len(self.zones) + 1}"
                    zone = {"label": label, "x": pos.x, "y": pos.y,
                            "z": pos.z, "radius": 1.2, "dance": dance_num}
                    self.zones.append(zone)
                    save_zones(self.zones)
                    info = f"دنس #{dance_num}" if dance_num else "تصادفی"
                    await self.highrise.chat(
                        f"🎯 [{label}] ست شد ({pos.x:.1f},{pos.z:.1f}) — {info}"
                    )
                    return
            await self.highrise.chat("❌ موقعیت پیدا نشد.")
        except Exception as e:
            await self.highrise.chat(f"❌ {e}")

    def _find_zone_at(self, x: float, y: float, z: float) -> dict | None:
        for zone in self.zones:
            dist = ((x - zone["x"]) ** 2 + (z - zone["z"]) ** 2) ** 0.5
            if dist <= zone.get("radius", 1.2):
                return zone
        return None

    # ─────────────────────────────────────────────────────────────
    # Utilities
    # ─────────────────────────────────────────────────────────────

    def _is_owner(self, user_id: str) -> bool:
        return user_id == self.owner_id

    def _is_admin(self, user_id: str) -> bool:
        return user_id == self.owner_id or user_id in self.admins

    def _find_user_by_name(self, username: str) -> User | None:
        name = username.lower().lstrip("@")
        for u in self.room_users.values():
            if u.username.lower() == name:
                return u
        return None

    async def _sync_room_users(self) -> None:
        try:
            resp = await self.highrise.get_room_users()
            self.room_users = {u.id: u for u, _ in resp.content}
        except Exception as e:
            print(f"[BOT] sync error: {e}")

    async def _bot_id(self) -> str:
        try:
            resp = await self.highrise.get_room_users()
            for u, _ in resp.content:
                if getattr(self.highrise, "_bot_id", None) == u.id:
                    return u.id
        except Exception:
            pass
        return ""
