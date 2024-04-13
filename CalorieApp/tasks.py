from celery import shared_task


@shared_task
def add(x, y):
    print("tasks has run")
    return x + y