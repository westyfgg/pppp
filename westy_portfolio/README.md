# WESTY Portfolio — Django

Адаптивне портфоліо українською мовою: проєкти та звернення зберігаються у базі даних, а керувати ними можна через Django Admin. Рожевий дизайн, CSS 3D-ефекти та поява блоків під час прокручування реалізовані локальними CSS і JavaScript без зовнішніх бібліотек.

## Структура

```text
westy_portfolio/
├── manage.py
├── requirements.txt
├── portfolio/                 # моделі, форми, views, admin і CSP middleware
├── westy_portfolio/           # settings, URLs, ASGI та WSGI
├── templates/                 # base, головна сторінка та форма контакту
├── static/portfolio/          # CSS і JavaScript
└── media/projects/            # зображення проєктів, завантажені через адмінку
```

## Локальний запуск Windows

У PowerShell перейдіть до папки проєкту:

```powershell
cd "C:\Users\Admin\Desktop\сайт\westy_portfolio"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:DJANGO_SECRET_KEY = python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
$env:DJANGO_DEBUG = "True"
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Сайт: <http://127.0.0.1:8000/>  
Адмін-панель: <http://127.0.0.1:8000/admin/>

`.env.example` — зразок назв змінних; Django не завантажує `.env` автоматично. Команди вище встановлюють ключ у поточному вікні PowerShell.

## Керування контентом

- **Проєкти:** в адмінці відкрийте «Проєкти», додайте назву, опис, зображення, адресу, стек технологій і позначку публікації.
- **Звернення:** записи з форми «Контакт» автоматично з'являються в «Повідомленнях».
- Форма вимагає ім'я, повідомлення та принаймні один контакт — email або Telegram.

## Безпека

- Django CSRF middleware увімкнений; форма містить `{% csrf_token %}`.
- Django-шаблони автоматично екранують змінні; введений користувачем текст не позначається як безпечний HTML.
- Дані форми перевіряються через `ModelForm`; ORM використовує параметризовані запити.
- CSP забороняє зовнішні скрипти, об'єкти та вбудовування сайту. Для стандартного Django Admin окремо дозволені inline-скрипти/стилі, потрібні його інтерфейсу.
- Налаштовані `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, безпечна referrer policy та cookies лише через HTTPS у production.
- Секретний ключ і debug-режим налаштовуються через `DJANGO_SECRET_KEY` і `DJANGO_DEBUG`. Не використовуйте debug-ключ і `DJANGO_DEBUG=True` на публічному сервері.

Для production обов'язково задайте `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=False`, `DJANGO_ALLOWED_HOSTS` (список хостів через кому) та налаштуйте HTTPS. SSL-перенаправлення й HSTS на один рік увімкнені за замовчуванням поза режимом DEBUG; вмикайте production-режим лише після налаштування HTTPS. Якщо всі піддомени також використовують HTTPS, можна встановити `DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS=True`; не вмикайте цей параметр або HSTS preload, доки не перевірите вимоги для свого домену. Якщо HTTPS завершується на reverse proxy, налаштуйте його для передавання HTTPS-запитів Django належним чином. За потреби PostgreSQL встановіть `DATABASE_URL`, наприклад `postgresql://user:password@host:5432/database`; без нього використовується SQLite. Перед публікацією виконайте `python manage.py migrate` і `python manage.py collectstatic`. Завантажені зображення (`media/`) у production треба зберігати на диску з постійним сховищем або налаштувати для них окреме медіа-сховище.
