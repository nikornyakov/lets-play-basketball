# get_group_id.py
import logging
import os
from telegram.ext import Updater, MessageHandler, Filters
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Токен вашего бота из переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")

def get_chat_id(update, context):
    """Функция для получения ID чата/группы"""
    chat_id = update.message.chat_id
    chat_type = update.message.chat.type
    chat_title = update.message.chat.title if update.message.chat.title else "Личный чат"
    
    # Формируем информационное сообщение
    message = (
        f"📋 Информация о чате:\n"
        f"• Название: {chat_title}\n"
        f"• Тип: {chat_type}\n"
        f"• ID: {chat_id}\n\n"
        f"💡 Скопируйте этот ID и используйте его в настройках бота"
    )
    
    # Отправляем информацию в чат
    update.message.reply_text(message)
    
    # Также выводим в консоль для удобства
    print(f"ID группы '{chat_title}': {chat_id}")

def main():
    """Основная функция"""
    if not BOT_TOKEN:
        print("Ошибка: Не найден BOT_TOKEN в переменных окружения")
        print("Убедитесь, что у вас есть файл .env с BOT_TOKEN=ваш_токен")
        return
    
    print("Запуск бота для получения ID группы...")
    print("1. Добавьте этого бота в вашу группу")
    print("2. Напишите любое сообщение в группе")
    print("3. Бот ответит с ID группы")
    print("=" * 50)
    
    # Создаем updater и dispatcher
    updater = Updater(BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    
    # Добавляем обработчик для всех текстовых сообщений
    dispatcher.add_handler(MessageHandler(Filters.text, get_chat_id))
    
    # Запускаем бота
    updater.start_polling()
    print("Бот запущен и ожидает сообщения...")
    print("Для остановки нажмите Ctrl+C")
    
    # Бесконечный цикл для работы бота
    updater.idle()

if __name__ == "__main__":
    main()
