from celery import shared_task
import time

@shared_task
def notify_create_post():
    print("Hello, world!")


