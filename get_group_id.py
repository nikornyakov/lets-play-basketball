import os
import requests
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

def get_group_id():
    """Получаем ID группы через Telegram API"""
    print("Отправьте любое сообщение в группе, куда добавлен бот...")
    print("Ожидание сообщений в течение 1 минуты...")
    
    # Получаем последние updates
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    
    # Ждем 1 минуту для получения сообщений
    for i in range(12):
        try:
            response = requests.get(url, timeout=10).json()
            
            if response["ok"] and response["result"]:
                for update in response["result"]:
                    if "message" in update and update["message"]["chat"]["type"] in ["group", "supergroup"]:
                        chat_id = update["message"]["chat"]["id"]
                        chat_title = update["message"]["chat"].get("title", "Без названия")
                        print(f"Найдена группа: {chat_title}")
                        print(f"ID группы: {chat_id}")
                        return chat_id
            
            print(f"Ожидание... ({i*5} секунд)")
            time.sleep(5)
        
        except Exception as e:
            print(f"Ошибка при получении данных: {e}")
            time.sleep(5)
    
    print("Не удалось найти группу. Убедитесь, что:")
    print("1. Бот добавлен в группу")
    print("2. В группе отправлено хотя бы одно сообщение")
    return None

if __name__ == "__main__":
    if not BOT_TOKEN:
        print("Ошибка: BOT_TOKEN не найден в .env файле")
    else:
        get_group_id()
