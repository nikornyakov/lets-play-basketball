import os
import logging
import asyncio
from datetime import datetime, timedelta
from telegram import Bot
from telegram.error import TelegramError

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("simple_bot.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

async def send_welcome_message(bot, group_id):
    """Функция отправки приветственного сообщения"""
    try:
        welcome_text = """
Привет всем! Ваш бот с баскетбольными пожеланиями! 🏀

*📅 РАСПИСАНИЕ ТРЕНИРОВОК НА СЛЕДУЮЩУЮ НЕДЕЛЮ:*

ВТОРНИК : 🏀 *19:00-20:30*

ЧЕТВЕРГ : 🏀 *19:00-20:30*

*📅 БУДЬТЕ В КУРСЕ:*
Команда Авито играет в турнире Шестового дивизиона НБЛ
🏀 СУББОТА: 29.11 16:10 *Авито vs Балтика*
Смотрите трансляцию https://vk.com/nevabasket

*📍 АДРЕС ЗАЛА:* "Basket Hall" 
ул. Салова, 57 корпус 5

Продуктивных выходных!❄️🏀
        """
        
        await bot.send_message(
            chat_id=group_id,
            text=welcome_text,
            parse_mode='Markdown'
        )
        
        logger.info("Приветственное сообщение отправлено")
        return True
        
    except Exception as e:
        logger.error(f"Ошибка при отправке приветственного сообщения: {e}")
        return False

async def send_simple_poll():
    """Упрощенная функция отправки опроса"""
    try:
        # Получаем токен из переменных окружения
        token = os.getenv("BOT_TOKEN")
        group_id = os.getenv("GROUP_ID")
        
        logger.info(f"Получены переменные: BOT_TOKEN={token[:10]}..., GROUP_ID={group_id}")
        
        if not token or not group_id:
            logger.error("Не установлены BOT_TOKEN или GROUP_ID")
            return False
        
        # Преобразуем group_id в целое число
        try:
            group_id = int(group_id)
        except ValueError:
            logger.error(f"GROUP_ID должен быть числом, получено: {group_id}")
            return False
        
        # Определяем текущий день недели
        now = datetime.now()
        day_of_week = now.weekday()  # 0-пн, 1-вт, 2-ср, 3-чт, 4-пт, 5-сб, 6-вс
        
        # Форматируем дату для отображения
        date_str = now.strftime("%d.%m.%Y")
        
        # Определяем текст опроса в зависимости от дня недели
        if day_of_week == 0:  # Понедельник
            training_date = (now + timedelta(days=1)).strftime("%d.%m.%Y")
            question = f"Баскетбол во вторник ({training_date}) 🏀"
            options = ["✅ Буду", "❌ Не смогу", "🤔 Еще не знаю", "⏰ Планирую опоздать"]
            poll_message = f"Тренировка во вторник ({training_date}) с 19:00 до 20:30. Кто будет?"
            
        elif day_of_week == 2:  # Среда
            training_date = (now + timedelta(days=1)).strftime("%d.%m.%Y")
            question = f"Баскетбол в четверг ({training_date}) 🏀"
            options = ["✅ Буду", "❌ Не смогу", "🤔 Еще не знаю", "⏰ Планирую опоздать"]
            poll_message = f"Тренировка в четверг ({training_date}) с 19:00 до 20:30. Кто будет?"
            
        else:
            logger.info(f"Сегодня не понедельник и не среда, опрос не требуется")
            return False
        
        # Создаем экземпляр бота
        bot = Bot(token=token)
        logger.info("Бот успешно инициализирован")
        
        # Отправляем НЕанонимный опрос
        logger.info(f"Отправляем опрос в группу: {question}")
        await bot.send_poll(
            chat_id=group_id,
            question=question,
            options=options,
            is_anonymous=False,
            allows_multiple_answers=False
        )
        
        # Отправляем сообщение с инструкцией
        reminder = """
        💡 Место проведения: Basket Hall 
        по адресу ул. Салова, 57 корпус 5.
        """
        
        await bot.send_message(chat_id=group_id, text=poll_message + reminder)
        
        logger.info("Опрос успешно отправлен")
        return True
        
    except TelegramError as e:
        logger.error(f"Ошибка Telegram API при отправке опроса: {e}")
        return False
    except Exception as e:
        logger.error(f"Неожиданная ошибка при отправке опроса: {e}")
        return False

async def send_training_reminder():
    """Функция отправки напоминания о тренировке"""
    try:
        # Получаем токен из переменных окружения
        token = os.getenv("BOT_TOKEN")
        group_id = os.getenv("GROUP_ID")
        
        if not token or not group_id:
            logger.error("Не установлены BOT_TOKEN или GROUP_ID")
            return False
        
        group_id = int(group_id)
        
        # Определяем текущий день недели
        now = datetime.now()
        day_of_week = now.weekday()
        
        # Отправляем напоминание только по вторникам и четвергам
        if day_of_week == 1:  # Вторник
            training_day = "сегодня"
        elif day_of_week == 3:  # Четверг
            training_day = "сегодня"
        else:
            logger.info(f"Сегодня не вторник и не четверг, напоминание не требуется")
            return False
        
        # Создаем экземпляр бота
        bot = Bot(token=token)
        
        reminder = f"""
⏰ Напоминание
Тренировка {training_day} в 19:00-20:30! 

Не забудьте:
• Спортивную форму
• Кроссовки
• Воду
• Хорошее настроение!

По прибытию на ресепшене узнайте номер зала и раздевалки.
        """
        
        # Отправляем напоминание
        await bot.send_message(chat_id=group_id, text=reminder)
        
        logger.info("Напоминание о тренировке отправлено")
        return True
        
    except Exception as e:
        logger.error(f"Ошибка при отправке напоминания: {e}")
        return False

async def send_manual_welcome():
    """Функция для ручной отправки приветственного сообщения"""
    try:
        token = os.getenv("BOT_TOKEN")
        group_id = os.getenv("GROUP_ID")
        
        if not token or not group_id:
            logger.error("Не установлены BOT_TOKEN или GROUP_ID")
            return False
        
        group_id = int(group_id)
        bot = Bot(token=token)
        
        await send_welcome_message(bot, group_id)
        return True
        
    except Exception as e:
        logger.error(f"Ошибка при отправке приветственного сообщения: {e}")
        return False

async def main():
    """Основная асинхронная функция"""
    logger.info("=" * 50)
    logger.info("Запуск упрощенной версии бота")
    logger.info("=" * 50)
    
    # Определяем, что нужно делать в зависимости от дня недели
    now = datetime.now()
    day_of_week = now.weekday()
    
    # Проверяем, есть ли аргумент командной строки для приветствия
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "welcome":
        success = await send_manual_welcome()
        if success:
            logger.info("Приветственное сообщение отправлено успешно!")
        else:
            logger.info("Приветственное сообщение не было отправлено")
    
    elif day_of_week in [0, 2]:  # Понедельник или среда
        success = await send_simple_poll()
        if success:
            logger.info("Опрос отправлен успешно!")
        else:
            logger.info("Опрос не был отправлен")
    
    elif day_of_week in [1, 3]:  # Вторник или четверг
        success = await send_training_reminder()
        if success:
            logger.info("Напоминание отправлено успешно!")
        else:
            logger.info("Напоминание не было отправлено")
    
    else:
        logger.info("Сегодня не день для опросов или напоминаний")
    
    logger.info("Завершение работы")
    logger.info("=" * 50)

if __name__ == "__main__":
    asyncio.run(main())
