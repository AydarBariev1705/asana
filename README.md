# Asana Email Registration Checker

## Описание

Этот скрипт предназначен для проверки регистрации email на сайте [Asana](https://app.asana.com). Он использует Selenium и библиотеку `selenium-wire` для работы через прокси. Скрипт также поддерживает асинхронное выполнение задач для повышения производительности при работе с большим количеством email-адресов.

## Установка

### Требования

- Python 3.7+
- ChromeDriver (автоматически загружается с помощью `webdriver-manager`)
- Браузер Google Chrome

### Установка зависимостей

1. Создайте виртуальное окружение:
   
   ```
   python -m venv .venv
   ```

2. Активируйте виртуальное окружение:
   Windows:
   
   ```
   .venv\Scripts\activate 
   ```

   Linux/macOS:
   
   ```
   source .venv/bin/activate 
   ```
3. Установите необходимые зависимости:
   
   ```
   pip install -r requirements.txt 
   ```