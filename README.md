## Студент

**Ладинский Александр Владимирович**


## Установка и запуск

### Вариант 1 (как в задании)

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Linux / macOS:

```bash
source .venv/bin/activate
```

Установка зависимостей:

```bash
pip install -r requirements.txt
```

Запуск:

```bash
uvicorn main:app --reload
```

### Вариант 2 (показывает, что переменная приложения переименована)

```bash
uvicorn app:api --reload
```

## Что открыть в браузере

- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/docs`

## Быстрая проверка без ручного тестирования

```bash
python check_app.py
```

Если всё в порядке, скрипт выведет:

```bash
Все проверки пройдены.
```


