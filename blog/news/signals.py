from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import mail_managers, send_mail
from .models import Author, Post, User


# создаём функцию обработчик с параметрами под регистрацию сигнала
@receiver(post_save, sender=Post)
def notify_post(sender, instance, created, **kwargs): 
    if created:
        # subject = f'{instance.post_title} {instance.date_create.strftime("%d %m %Y")}'
        subject = f'{instance.title}! Опубликована новая запись.'
    else:
        # subject = f'Appointment changed for {instance.post_title} {instance.date_create.strftime("%d %m %Y")}'
        # subject = f'{instance.title} - статья была изменена.'
        pass
 
    mail_managers(
        subject=subject,
        message=instance.text,
    )
    