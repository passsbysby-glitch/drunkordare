import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ===== GANTI TOKEN BOT DISINI =====
TOKEN = "8209259354:AAG3fSlq8bkfa-_Af318hGgzefaiQA6TBZw"

# ===== List supporter (isi manual ID Telegram) =====
supporters = []

# ===== Daftar tantangan per level =====
dare_levels = {
    1: [
        "(istri ke suami) Beri ciuman 5 detik",
        "(suami ke istri) Pijat bahu sebentar",
        "(partner ke istri) Bisikkan sesuatu yang nakal",
        "(istri ke partner) Tatap mata selama 10 detik",
        "(suami ke istri) Cium kening dengan lembut",
        "(istri ke suami) Duduk di pangkuan 1 menit",
        "(partner ke istri) Pegang tangan sebentar",
        "(istri ke suami) Beri pelukan hangat",
        "(suami ke istri) Cium pipi kiri & kanan",
        "(istri ke partner) Tanyakan fantasi nakal favorit",
        "(partner ke istri) Beri senyum genit",
        "(istri ke suami) Beri pujian nakal",
        "(istri ke semua) Lepaskan 1 pakaian",
        "(istri ke suami) Mainkan rambut suami sebentar",
        "(suami ke istri) Cium telinga pelan"
    ],
    2: [
        "(istri ke suami) Ciuman bibir 10 detik",
        "(suami ke istri) Cium leher",
        "(partner ke istri) Cium pipi",
        "(istri ke partner) Sentuh paha sebentar",
        "(suami ke istri) Rabaan lembut di pinggang",
        "(istri ke suami) Gigit manja bibir",
        "(partner ke istri) Pijat punggung sebentar",
        "(istri ke suami) Bisikkan fantasi liar",
        "(suami ke istri) Beri french kiss singkat",
        "(istri ke semua) Lepaskan 1 pakaian",
        "(partner ke istri) Pegang pinggul sebentar",
        "(istri ke suami) Sentuh dada lembut",
        "(suami ke istri) Sentuh paha pelan",
        "(istri ke partner) Dekatkan wajah 5cm",
        "(istri ke suami) Tatap mata nakal 10 detik"
    ],
    3: [
        "(istri ke suami) Cium bibir dalam 15 detik",
        "(partner ke istri) Cium leher lama",
        "(istri ke partner) Pegang dada sebentar",
        "(suami ke istri) Rabaan di paha dalam",
        "(istri ke semua) Lepaskan 1 pakaian",
        "(istri ke suami) Bisikkan hal nakal",
        "(partner ke istri) Rabaan di pinggang",
        "(istri ke partner) Sentuh rambut sambil senyum",
        "(suami ke istri) Cium pundak pelan",
        "(istri ke suami) Pegang bagian sensitif sebentar",
        "(partner ke istri) Beri ciuman di pipi lama",
        "(istri ke semua) Gunakan vibrator 1 menit",
        "(istri ke suami) Gigit lembut leher",
        "(istri ke partner) Rabaan tangan sebentar",
        "(suami ke istri) Rabaan pinggang lama"
    ],
    4: [
        "(istri ke semua) Lepaskan 1 pakaian",
        "(partner ke istri) Cium bibir lama",
        "(istri ke partner) Rabaan paha atas",
        "(suami ke istri) Rabaan dada pelan",
        "(istri ke suami) Bisikkan fantasi paling liar",
        "(partner ke istri) Rabaan pinggul lama",
        "(istri ke partner) Sentuh wajah perlahan",
        "(istri ke semua) Gunakan vibrator 2 menit",
        "(suami ke istri) Gigit lembut bibir",
        "(istri ke partner) Dekatkan tubuh erat",
        "(partner ke istri) Cium pundak lama",
        "(istri ke suami) Pegang bagian sensitif lebih lama",
        "(istri ke partner) Rabaan rambut & telinga",
        "(suami ke istri) Rabaan paha lama",
        "(istri ke semua) Lepaskan pakaian terakhir"
    ]
}

# ===== Logging =====
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# ===== Command /start =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎮 Main Game", callback_data="menu_play")],
        [InlineKeyboardButton("💖 Support tambkan tantangan di pesan", url="https://saweria.co/gameshappyhappy")]  # Ganti link support
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Selamat datang di *Truth or Dare Game*!\n\n"
        "👉 Semua level (1–4) gratis dimainkan.\n"
        "👉 Menambahkan tantangan baru hanya untuk supporter 💖\n\n"
        "Siap mulai? 👇",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# ===== Menu Play =====
async def menu_play(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("Level 1", callback_data="level_1")],
        [InlineKeyboardButton("Level 2", callback_data="level_2")],
        [InlineKeyboardButton("Level 3", callback_data="level_3")],
        [InlineKeyboardButton("Level 4", callback_data="level_4")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("🎮 Pilih level tantangan:", reply_markup=reply_markup)

# ===== Handler Level =====
async def level_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    level = int(query.data.split("_")[1])
    
    dare = random.choice(dare_levels[level])  # Pilih random
    keyboard = [
        [InlineKeyboardButton("✅ Dilakukan", callback_data="menu_play")],
        [InlineKeyboardButton("🥃 Minum 1 shot", callback_data="menu_play")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        f"🎯 Tantangan Level {level}:\n\n{dare}",
        reply_markup=reply_markup
    )

# ===== Tambah Dare =====
async def add_dare(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id not in supporters:
        await update.message.reply_text("⚠️ Fitur ini hanya untuk supporter 💖")
        return
    
    if len(context.args) < 2:
        await update.message.reply_text("Format: /add_dare <level> <isi tantangan>")
        return
    
    try:
        level = int(context.args[0])
        dare_text = " ".join(context.args[1:])
        dare_levels[level].append(dare_text)
        await update.message.reply_text(f"Tantangan baru ditambahkan ke Level {level} ✅")
    except:
        await update.message.reply_text("Format salah. Contoh: /add_dare 2 Cium pipi (istri ke suami)")

# ===== Command /menu =====
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎮 Main Game", callback_data="menu_play")],
        [InlineKeyboardButton("💖 Support tambkan tantangan di pesan", url="https://saweria.co/gameshappyhappy")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Kembali ke menu utama:", reply_markup=reply_markup)

# ===== Main =====
def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CommandHandler("add_dare", add_dare))
    app.add_handler(CallbackQueryHandler(menu_play, pattern="menu_play"))
    app.add_handler(CallbackQueryHandler(level_handler, pattern="level_"))
    
    app.run_polling()

if __name__ == "__main__":
    main()