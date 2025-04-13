import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ConversationHandler, ContextTypes, filters
)
from musicgen import generate_music
import os

# Configuration du journal
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# États de la conversation
IDEA, INSTRUMENTS, LYRICS, ARTIST = range(4)

# Stockage temporaire des données utilisateur
user_data = {}

# Commande /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salut ! Donne-moi d’abord une idée pour ta musique :")
    return IDEA

# Réception de l'idée
async def get_idea(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data['idea'] = update.message.text
    await update.message.reply_text("Super ! Quels instruments veux-tu entendre dans ta musique ?")
    return INSTRUMENTS

# Réception des instruments
async def get_instruments(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data['instruments'] = update.message.text
    await update.message.reply_text("Parfait ! Maintenant, envoie-moi les paroles (lyrics) de ta musique.")
    return LYRICS

# Réception des paroles
async def get_lyrics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data['lyrics'] = update.message.text
    await update.message.reply_text("Génial ! Un artiste t’inspire ? Si oui, donne son nom. Sinon, tape 'non'.")
    return ARTIST

# Réception de l’artiste et génération de la musique
async def get_artist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data['artist'] = update.message.text

    summary = (
        f"Super ! Voici ta commande :\n\n"
        f"Idée : {user_data['idea']}\n"
        f"Instruments : {user_data['instruments']}\n"
        f"Paroles : {user_data['lyrics']}\n"
        f"Inspiration : {user_data['artist']}\n\n"
        f"Je génère la musique pour toi, ça peut prendre quelques secondes..."
    )
    await update.message.reply_text(summary)

    # Génération IA
    prompt = f"{user_data['idea']} song using {user_data['instruments']}, inspired by {user_data['artist']}. Lyrics: {user_data['lyrics']}"
    huggingface_token = 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  # <-- remplace ici par ton nouveau token

    music_path = generate_music(prompt, huggingface_token)

    if music_path:
        with open(music_path, "rb") as audio:
            await update.message.reply_audio(audio, filename="generated_music.wav", title="Ta musique IA")
        os.remove(music_path)
    else:
        await update.message.reply_text("Désolé, une erreur est survenue pendant la création de la musique.")

    return ConversationHandler.END

# Annulation de la conversation
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Création de musique annulée. Reviens quand tu veux !")
    return ConversationHandler.END

# Fonction principale
def main():
    app = ApplicationBuilder().token(7589790981:AAH1PqG1E6P1if_MLkuMWRw6tNTWvGJ85y0).build()

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
    app.run_polling()

if __name__ == "__main__":
    main()
