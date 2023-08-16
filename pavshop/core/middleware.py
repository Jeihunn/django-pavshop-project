from django.utils import timezone
import logging
from account.models import Blacklist
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse
from django.template import loader


class AddUserIpsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            ip_address = self.get_client_ip(request)

            if not request.user.ips:
                request.user.ips = []

            if ip_address not in request.user.ips:
                request.user.ips.append(ip_address)
                request.user.save()
        return None

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class LoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        logger = logging.getLogger('project_logs')
        logger.info("=" * 100)
        logger.info(f"Timestamp: {timezone.now()}")
        logger.info(f"Request Method: {request.method}")
        logger.info(f"URL Requested: {request.get_full_path()}")
        logger.info(f"Client IP Address: {request.META.get('REMOTE_ADDR')}")
        logger.info(f"Host Name of Client: {request.META.get('REMOTE_HOST')}")
        logger.info(f"Host Name of the Server: {request.META.get('SERVER_NAME')}")
        logger.info(f"Port of the Server: {request.META.get('SERVER_PORT')}")
        return None

    def process_response(self, request, response):
        logger = logging.getLogger('project_logs')
        logger.info(f"Response Status Code: {response.status_code}")
        logger.info("=" * 100)
        return response


class BlacklistMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user = request.user
        ip_address = self.get_client_ip(request)

        blacklist_entry = Blacklist.objects.filter(
            ip_address=ip_address, is_active=True).first()

        if not blacklist_entry:
            if user.is_authenticated:
                blacklist_entry = Blacklist.objects.filter(
                    user=user, is_active=True).first()

        if blacklist_entry:
            if timezone.now() > blacklist_entry.start_time:
                if timezone.now() < blacklist_entry.start_time + blacklist_entry.duration:
                    if user.is_authenticated:
                        return self.blocked_response(request, "user-based")
                    else:
                        return self.blocked_response(request, "IP-based")
                else:
                    blacklist_entry.is_active = False
                    blacklist_entry.save()

        return None

    def blocked_response(self, request, block_type):
        template = loader.get_template('account/blacklist.html')
        context = {'block_type': block_type}
        return HttpResponse(template.render(context, request))

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
