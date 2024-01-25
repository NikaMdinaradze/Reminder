import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
app = Celery("core")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self, message="Test"):
    result = f"{message} - Task ID: {self.request.id}"
    print(result)
    return result

app.autodiscover_tasks()
