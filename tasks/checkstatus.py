import json
from datetime import timedelta
from django.utils import timezone
from django_q.tasks import async_task, schedule
from django_q.models import Schedule
from urltrack.models import UrlTracker, UrlStatus
from django.core.mail import send_mail
import requests


def check_url_task(url_id, frequency):
    """
        Task that creates a schedule using django-q. Will run based on what info
        is available in the url_tracker entry.
    """
    schedule('tasks.checkstatus.check_url_status',
             str(url_id),
             schedule_type=Schedule.MINUTES,
             minutes=frequency,
             repeats=-1,
             kwargs=None  # optional kwargs to pass to check_url_status function
             )


def check_url_status(url_id: str, **kwargs):
    """
        Function called by scheduler that actually checks the url status, as well
        as save status updates.
    """
    url_entry = UrlTracker.objects.get(id=int(url_id))
    resp = requests.get(url_entry.url)
    time_checked = timezone.localtime(timezone.now())
    # print(f"RESPONSE STATUS:{resp.status_code} for url_id {url_id}")
    if resp.status_code != url_entry.expected_status:
        UrlStatus.objects.create(url_tracker=url_entry, status_code=resp.status_code,
                                 time_checked=time_checked,
                                 state=0
                                 )
        # Increment failed status to keep track of consecutive failures
        url_entry.failed_status += 1
        url_entry.last_checked = time_checked
        url_entry.save()
        if url_entry.failed_status == 3:
            # Admin email due to consecutive failures
            send_alert_email(url_entry, admin=True)
        else:
            send_alert_email(url_entry)
    else:
        UrlStatus.objects.create(url_tracker=url_entry, status_code=resp.status_code,
                                 time_checked=timezone.localtime(timezone.now()),
                                 state=1
                                 )
        # Set status to 0 again
        url_entry.failed_status = 0
        url_entry.last_checked = time_checked
        url_entry.save()


def send_alert_email(url_tracker: UrlTracker, admin=False):
    """
        Dummy email function. I don't have an smtp server set up so this
        won't actually work, but I think you get the gist
        of what I would do with a real server such as Twilio set up

    """
    if admin:
        send_mail(f"High Priority Alert for {url_tracker.url}",
                  f"{url_tracker.url} has been down 3 times consecutively "
                  f"and needs your attention!", 'from@example.com',
                  ['to@example.com'], fail_silently=True)
    else:
        if url_tracker.user_emails:
            # Load list of emails from text field and pass to TO kwarg
            emails = json.loads(url_tracker.user_emails)
            send_mail(f"Alert regarding {url_tracker.url}",
                      f"{url_tracker.url} status is currently down",
                      'from@example.com',
                      emails, fail_silently=True)
