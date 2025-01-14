import logging
from typing import Optional
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchWindowException


# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def checker(email: str, proxy: str) -> Optional[bool]:
    """
    Проверяет, зарегистрирован ли email на сайте Asana.
    :param email: Email для проверки.
    :param proxy: Прокси в формате "user:password@ip:port".
    :return: True, если email зарегистрирован; False, если нет; None в случае ошибки.
    """
    # Настройка Selenium Wire
    options = {
        "proxy": {
            "http": proxy,
            "no_proxy": "localhost,127.0.0.1"  # Исключения для прокси
        }
    }

    # Настройка Chrome
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    try:
        # Инициализация драйвера с selenium-wire
        driver = webdriver.Chrome(
            service=Service(), seleniumwire_options=options, options=chrome_options,
            )
        driver.set_page_load_timeout(30)  # Таймаут загрузки страницы

        # Переход на страницу входа Asana
        driver.get("https://app.asana.com/-/login")
        logger.info(f"Текущий адрес: {driver.current_url}")

        # Ожидание появления поля для ввода email
        wait = WebDriverWait(driver, 30)  # Ожидание до 30 секунд
        try:
            accept_cookies_button = wait.until(
                EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")),
                )
            accept_cookies_button.click()
            logger.info("Куки приняты.")
        except TimeoutException:
            logger.info("Кнопка принятия куки не найдена или уже приняты.")

        email_input = wait.until(
            EC.presence_of_element_located((By.NAME, "e")),
            )
        email_input.send_keys(email)

        # Нажимаем кнопку "Продолжить"
        continue_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'LoginEmailForm-continueButton')]")),
            )
        continue_button.click()

        # Ожидание появления сообщения
        try:
            # Проверяем наличие сообщения "Добро пожаловать в Asana"
            welcome_message = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'LoginPasswordForm-loginButton') and text()='Войти']")),
                )
            if welcome_message:
                logger.info(f"Зарегистрирован: {email}")
                return True  # Email зарегистрирован
        except TimeoutException:
            pass

        # Проверяем наличие сообщения "To get started, please sign up"
        short_wait = WebDriverWait(driver, 5)
        try:
            signup_message = short_wait.until(
                EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'To get started, please sign up')]"))
            )
            if signup_message:
                return False  # Email не зарегистрирован
        except TimeoutException:
            pass

        # Если ни одно из сообщений не найдено, возвращаем None
        return None
    except TimeoutException:
        logger.error("Таймаут при загрузке страницы.")
        return None
    except WebDriverException as e:
        logger.error(f"Ошибка WebDriver: {e}")
        return None
    finally:
        try:
            # Проверяем, существует ли текущее окно
            if driver.current_window_handle:
                driver.quit()  # Закрываем браузер
                logger.info("Браузер успешно закрыт.")
        except NoSuchWindowException:
            logger.info("Окно уже закрыто.")
        except Exception as e:
            logger.error(f"Ошибка при закрытии браузера: {e}")

if __name__ == "__main__":
    # Пример использования
    result = checker("a_bariev@internet.ru", "http://0iyLsMBhVIRtEBuqLoSS:RNW78Fm5@185.162.130.86:10000")
    print(result)  # Вернет True
    result = checker("ivan@mail.ru", "http://0iyLsMBhVIRtEBuqLoSS:RNW78Fm5@185.162.130.86:10000")
    print(result)  # Вернет False