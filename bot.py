from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, ConversationHandler, filters

TOKEN = "TON_TOKEN_TELEGRAM"

# Étapes de la conversation
IDEA, INSTRUMENTS, LYRICS, ARTIST = range(4)

user_data = {}

# Démarrage
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salut ! Dis-moi d'abord l’idée de ta musique (ex : chanson romantique, afrobeats, gospel...)")
    return IDEA

# Récupère l'idée de la chanson
async def get_idea(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data["idea"] = update.message.text
    await update.message.reply_text("Quels instruments veux-tu qu’on utilise ? (ex : piano, guitare, batterie...)")
    return INSTRUMENTS

# Récupère les instruments
async def get_instruments(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data["instruments"] = update.message.text
    await update.message.reply_text("Tu peux me donner les paroles maintenant (ou dis 'génère' si tu veux que je les écrive).")
    return LYRICS

# Récupère les paroles
async def get_lyrics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data["lyrics"] = update.message.text
    await update.message.reply_text("Un artiste à qui tu veux que la chanson ressemble ? (ex : Burna Boy, Dadju, etc.) Ou dis 'aucun'")
    return ARTIST

# Récupère l'inspiration artistique
async def get_artist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data["artist"] = update.message.text

    # Résumé de la demande
    summary = (
        f"Super ! Voici ta commande :\n\n"
        f"Idée : {user_data['idea']}\n"
        f"Instruments : {user_data['instruments']}\n"
        f"Paroles : {user_data['lyrics']}\n"
        f"Inspiration : {user_data['artist']}\n\n"
        f"Je prépare ta musique IA..."
    )
    await update.message.reply_text(summary)
    
    # (Plus tard ici : appel API IA musicale comme Suno ou autre)

    return ConversationHandler.END

# Annulation
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Création annulée.")
    return ConversationHandler.END

# Lancement de l'application
app = ApplicationBuilder().token(TOKEN).build()

conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        IDEA: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_idea)],
        INSTRUMENTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_instruments)],
        LYRICS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_lyrics)],
        ARTIST: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_artist)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

app.add_handler(conv_handler)

print("Bot actif...")
app.run_polling()
