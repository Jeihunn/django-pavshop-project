from celery import shared_task
import time
from django.template.loader import render_to_string
from django.conf import settings
from core.models import Newsletter
from product.models import ProductVersion
from account.models import User
from django.db.models import Count
from django.core.mail import EmailMultiAlternatives
from datetime import timedelta
from django.utils import timezone
SERVER_BASE_URL = "https://technest-pav.shop"

@shared_task  # background task testing
def export_data():
    print("export data Starts")
    time.sleep(1)
    print("export data Ends")


@shared_task        # periodik task testing
def send_email_to_subscribers():
    one_week_ago = timezone.now() - timedelta(days=7)
    email_list = Newsletter.objects.filter(
        subscription_status=True).values_list('email', flat=True)
    products = ProductVersion.objects.filter(is_active=True, created_at__gte=one_week_ago).annotate(
        reviews_count=Count('reviews')).order_by('-reviews_count')[:3]
    subject = 'Most popular products of this week'
    mail = EmailMultiAlternatives(
        subject=subject, from_email=settings.EMAIL_HOST_USER, to=email_list)

    product_data_list = []

    for product in products:
        product_data = {
            'title': product.title,
            'price': product.price,
            'description': product.description,
            'designer': product.designer,
            'url': f'{SERVER_BASE_URL}/product/{product.slug}',
            'cover_image_cid': f'{SERVER_BASE_URL}{product.cover_image.url}',
        }

        product_data_list.append(product_data)
        mail.attach_alternative(
            f'<img src="cid:{product_data["cover_image_cid"]}" alt="Product Image">', "text/html")

        # image_path = product.cover_image.path
        # mail.attach_file(image_path, mimetype='image/jpeg')
        mail.attach_alternative(
            f'<img src="cid:{product_data["cover_image_cid"]}" alt="Product Image">', "text/html")

    message = render_to_string(
        'core/email-subscribers.html', {'products': product_data_list})

    mail.content_subtype = 'html'
    mail.from_email = "Pavshop Project"

    mail.attach_alternative(message, "text/html")
    mail.send()
    print("* ", "Emails successfully sent!")


@shared_task        # periodik task testing
def send_email_to_subscribers_last_popular_products():
    one_month_ago = timezone.now() - timedelta(days=30)
    # inactive_users = User.objects.filter(
    #     last_login__lte=F('date_joined') + timedelta(days=30))
    # inactive_users = inactive_users.filter(last_login__lte=one_month_ago)
    inactive_users = User.objects.filter(last_login=one_month_ago)
    inactive_user_emails = list(inactive_users.values_list('email', flat=True))
    products = ProductVersion.objects.filter(is_active=True,
                                             created_at__gte=one_month_ago).annotate(
        reviews_count=Count('reviews')).order_by('-reviews_count')[:3]
    subject = 'Most popular products of last month'
    mail = EmailMultiAlternatives(
        subject=subject, from_email=settings.EMAIL_HOST_USER, to=inactive_user_emails)

    product_data_list = []

    for product in products:
        product_data = {
            'title': product.title,
            'price': product.price,
            'description': product.description,
            'designer': product.designer,
            'url': f'{SERVER_BASE_URL}/product/{product.slug}',
            'cover_image_cid': f'{SERVER_BASE_URL}{product.cover_image.url}',
        }

        product_data_list.append(product_data)
        mail.attach_alternative(
            f'<img src="cid:{product_data["cover_image_cid"]}" alt="Product Image">', "text/html")

        # image_path = product.cover_image.path
        # mail.attach_file(image_path, mimetype='image/jpeg')
        mail.attach_alternative(
            f'<img src="cid:{product_data["cover_image_cid"]}" alt="Product Image">', "text/html")

    message = render_to_string(
        'core/email-subscribers.html', {'products': product_data_list})

    mail.content_subtype = 'html'
    mail.from_email = "Pavshop Project"

    mail.attach_alternative(message, "text/html")
    mail.send()
