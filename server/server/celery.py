from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Đặt biến môi trường cho Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')

# Tạo đối tượng Celery
app = Celery('server')

# Đọc cấu hình từ Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Tự động nạp các tasks từ tất cả các ứng dụng trong INSTALLED_APPS
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
