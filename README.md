# Payments System — Django Backend

# 🏦 Bank Webhook Handler

Backend-сервис на Django для приёма и обработки webhook-ов от банка. Начисляет сумму на баланс организации по ИНН, логирует изменения и обеспечивает защиту от повторной обработки.

---

## 🚀 Возможности

* Принимает входящие POST-запросы от банка
* Начисляет сумму на баланс организации по `payer_inn`
* Создаёт запись `Payment` (одна операция = один `operation_id`)
* Логирует изменение баланса (`BalanceLog`)
* Идемпотентность: повторный webhook с тем же `operation_id` не изменяет данные
* Получение текущего баланса организации по ИНН

---

## 📦 Технологии

* Python 3.9
* Django 4.2.17
* MySQL
* Poetry (Python dependencies)
* Ruff (линтер)
* Docker + Docker Compose

---

### 🐍 Poetry

   Обновите pip:
   ```bash
   pip install --upgrade pip
   ```
   Установите pipx:
   ```bash
   pip install pipx
   ```
   Установите Poetry (если не установлен):
   ```bash
   pipx install poetry
   ```

---

### 🐳 Docker
- Запуск проекта:

    ```bash
    docker-compose up --build
    ```
- Применение миграций:

    ```bash
    docker-compose exec web python manage.py migrate
    ```
---


## ✅ Защита от дублей

При получении webhook проверяется `operation_id`. Если Payment уже существует — webhook не обрабатывается.

---

