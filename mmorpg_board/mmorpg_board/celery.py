# mmorpg_board/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Устанавливаем значение переменной окружения для Django настроек
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mmorpg_board.settings')

# Создаем экземпляр Celery
app = Celery('mmorpg_board')

# Используем настройки Celery из Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически ищем задачи в зарегистрированных приложениях Django
app.autodiscover_tasks()

# Для отладки можно также использовать
@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
