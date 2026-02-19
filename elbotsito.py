import telebot
import random
import json
import os

# ============================================
#  PEGA TU NUEVO TOKEN AQUÍ
# ============================================
TOKEN = "8401853349:AAHL7NPj0hkGqee6wopPQmIwEqZcXU42a3s"  

DB_FILE = "videos.json"

bot = telebot.TeleBot(TOKEN)

# --- Cargar videos ---
def load_videos():
    if not os.path.exists(DB_FILE):
        return []
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except:
        return []

# --- Guardar video ---
def save_video(file_id):
    videos = load_videos()
    if file_id not in videos:
        videos.append(file_id)
        with open(DB_FILE, "w") as f:
            json.dump(videos, f)
        print(f"Video guardado: {file_id}")

# --- Obtener video aleatorio ---
def get_random_video():
    videos = load_videos()
    if not videos:
        return None
    return random.choice(videos)

# --- Leer historial del grupo ---
def fetch_history(chat_id, limit=100):
    print(f"Buscando videos en el historial del grupo...")
    try:
        # Obtener historial (más reciente primero)
        messages = bot.get_chat_history(chat_id, limit=limit)
        
        videos_found = 0
        for msg in messages:
            if msg.video:
                save_video(msg.video.file_id)
                videos_found += 1
        
        print(f"Se encontraron {videos_found} videos en el historial.")
    except Exception as e:
        print(f"Error al leer historial: {e}")

# --- Detectar videos nuevos ---
@bot.message_handler(content_types=['video'])
def handle_video(message):
    if message.chat.type in ['group', 'supergroup']:
        try:
            save_video(message.video.file_id)
        except:
            pass

# --- Comando /video ---
@bot.message_handler(commands=['video'])
def send_random_video(message):
    video_id = get_random_video()
    if video_id:
        bot.send_video(message.chat.id, video_id)
    else:
        bot.reply_to(message, "❌ No encontré videos en este grupo.")

# --- Comando /start ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🎬 Bot de videos activo! Escribe /video para ver un video aleatorio del grupo.")

# --- Iniciar bot ---
print("Bot iniciado...")

# Intentamos cargar el historial al iniciar (opcional)
# Para activarlo, descomenta las siguientes líneas y reemplaza -100XXXXXXXXX por tu ID de grupo
# fetch_history(-100XXXXXXXXX)

bot.infinity_polling()