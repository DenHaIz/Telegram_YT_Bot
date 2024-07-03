import os
import telebot
from pytube import YouTube
from moviepy.editor import *

API_TOKEN = '6133358289:AAHyE_9XfiK9uIVczmWbTcRY9_ye1ffU3AE'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Отправь мне ссылку на видео с YouTube, и я конвертирую его в MP3 для тебя.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text
    if 'youtube.com' in url or 'youtu.be' in url:
        bot.reply_to(message, "Скачиваю видео, подождите немного...")

        try:
            yt = YouTube(url)
            video = yt.streams.filter(only_audio=True).first()
            downloaded_file = video.download()
            
            # Конвертация видео в MP3
            mp3_file = downloaded_file.split('.')[0] + '.mp3'
            video_clip = AudioFileClip(downloaded_file)
            video_clip.write_audiofile(mp3_file)
            video_clip.close()

            with open(mp3_file, 'rb') as audio:
                bot.send_audio(message.chat.id, audio)

            os.remove(downloaded_file)
            os.remove(mp3_file)

        except Exception as e:
            bot.reply_to(message, f"Произошла ошибка: {e}")
    else:
        bot.reply_to(message, "Пожалуйста, отправьте действительную ссылку на видео с YouTube.")

bot.polling()