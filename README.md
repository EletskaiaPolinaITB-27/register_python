## Запуск проекта

### 1 создание текстового файла с библиотеками
 - authx==1.5.2
 - fastapi==0.115.11
 - pydantic==2.10.6
 - sqlalchemy==2.0.39
 - uvicorn==0.34.0

### 2 установка библиотек
> pip install -r requirements.txt

### 3 запуск проекта
> uvicorn main:app --reload

*** при условии что у вас app в main.py ***

### 4 открыть сваггер
> 127.0.0.1:8000/docs# register_python
