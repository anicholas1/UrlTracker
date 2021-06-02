from datetime import timedelta
from django.utils import timezone
from django_q.tasks import async_task, schedule
from django_q.models import Schedule
from urltrack.models import UrlTracker
import requests
import logging
import arrow
from math import copysign

logger = logging.getLogger(__name__)


def url_status_logger(resp):
    logger.debug(resp.status_code)


def check_url_task(url_id, frequency):
    # TODO Create schedule using frequency and the url

    schedule('tasks.checkstatus.check_url_status',
                 str(url_id),
                 schedule_type=Schedule.MINUTES,
                 minutes=frequency,
                 repeats=-1,
                 kwargs=None  # optional kwargs to pass to check_url_status function
                 )


def check_url_status(url_id: str, **kwargs):
    print(f"Checking Status for {url_id}")
    url_entry = UrlTracker.objects.get(id=int(url_id))
    resp = requests.get(url_entry.url)
    print(f"RESPONSE STATUS:{resp.status_code} for url_id {url_id}")

    # TODO Create entry in db for pass or fail
    if resp.status_code != url_entry.expected_status:

        pass
        # TODO Send email if failed


def send_alert_email(email):
    # TODO send email to all users for account except admin
    # TODO add functionality to send email to admin only
    pass
