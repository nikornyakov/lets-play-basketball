"""
Configuration module for Basketball Bot.
Contains all configuration dataclasses and settings.
"""
import os
from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class BotConfig:
    """Configuration for Telegram bot connection."""
    token: str
    group_id: int

    def __post_init__(self):
        """Validate configuration after initialization."""
        if not self.token:
            raise ValueError("BOT_TOKEN is required")
        if not self.group_id or not isinstance(self.group_id, int):
            raise ValueError("GROUP_ID must be a valid integer")


@dataclass
class ScheduleConfig:
    """Configuration for training schedule."""
    training_days: List[int]  # 0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri, 5=Sat, 6=Sun
    poll_days: List[int]      # Days when to send polls
    reminder_days: List[int]  # Days when to send reminders
    training_time: str        # e.g., "19:00-20:30"
    venue: str                # Training venue address


@dataclass
class MessagesConfig:
    """Configuration for bot messages."""
    welcome_message: str
    poll_options: List[str]
    reminder_template: str
    location_info: str


@dataclass
class AppConfig:
    """Main application configuration."""
    bot: BotConfig
    schedule: ScheduleConfig
    messages: MessagesConfig


def load_config() -> AppConfig:
    """Load configuration from environment variables."""
    # Load bot configuration
    token = os.getenv("BOT_TOKEN")
    group_id_str = os.getenv("GROUP_ID")

    if not group_id_str:
        raise ValueError("GROUP_ID environment variable is required")

    try:
        group_id = int(group_id_str)
    except ValueError:
        raise ValueError("GROUP_ID must be a valid integer")

    bot_config = BotConfig(token=token, group_id=group_id)

    # Schedule configuration
    schedule_config = ScheduleConfig(
        training_days=[1, 3],  # Tuesday, Thursday
        poll_days=[0, 2],      # Monday, Wednesday
        reminder_days=[1, 3],  # Tuesday, Thursday
        training_time="19:00-20:30",
        venue="Basket Hall, ул. Салова, 57 корпус 5"
    )

    # Messages configuration
    messages_config = MessagesConfig(
        welcome_message="""
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
        """,
        poll_options=["✅ Буду", "❌ Не смогу", "🤔 Еще не знаю", "⏰ Планирую опоздать"],
        reminder_template="""
⏰ Напоминание
Тренировка {training_day} в {training_time}!

Не забудьте:
• Спортивную форму
• Кроссовки
• Воду
• Хорошее настроение!

По прибытию на ресепшене узнайте номер зала и раздевалки.
        """,
        location_info="""
💡 Место проведения: Basket Hall
по адресу ул. Салова, 57 корпус 5.
        """
    )

    return AppConfig(
        bot=bot_config,
        schedule=schedule_config,
        messages=messages_config
    )


# Global configuration instance
config = load_config()
