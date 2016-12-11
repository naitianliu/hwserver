from celery import task
from api.notification.apns_helper import APNSHelper


@task
def send_apns_notification(user_id, message):
    APNSHelper(user_id).send_simple_notification(message)