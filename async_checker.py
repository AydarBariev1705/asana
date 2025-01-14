import asyncio
import logging
from typing import Optional
from concurrent.futures import ThreadPoolExecutor

from checker import checker


# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Асинхронная функция для проверки регистрации email
async def _checker(email: str, proxy: str, executor: ThreadPoolExecutor) -> Optional[bool]:
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        executor, checker, email, proxy,
        )
    return result

# Пример использования
async def main():
    emails = [
        "a_bariev@internet.ru", 
        "ivan@mail.ru",
        "qwer@qwewqwe.ru",
        ]
    proxy = "http://0iyLsMBhVIRtEBuqLoSS:RNW78Fm5@185.162.130.86:10000"

    with ThreadPoolExecutor(max_workers=10) as executor:
        tasks = [
            _checker(email, proxy, executor) for email in emails
            ]
        results = await asyncio.gather(*tasks)

    for email, result in zip(emails, results):
        if result is True:
            logger.info(f"{email} зарегистрирован")
        elif result is False:
            logger.info(f"{email} НЕ зарегистрирован")
        else:
            logger.warning(f"Не удалось выполнить проверку для {email}")

if __name__ == "__main__":
    asyncio.run(main())