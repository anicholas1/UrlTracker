from datetime import timedelta
from django.utils import timezone
from django_q.tasks import async_task, schedule
from django_q.models import Schedule
from urltrack.models import UrlTracker, UrlStatus
import requests


def check_url_task(url_id, frequency):
    """
        Task that creates a schedule using django-q. Will run based on what info
        is available in the url_tracker entry.
    """
    # TODO Create schedule using frequency and the url

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
    print(f"RESPONSE STATUS:{resp.status_code} for url_id {url_id}")
    if resp.status_code != url_entry.expected_status:
        UrlStatus.objects.create(url_tracker=url_entry, status_code=resp.status_code,
                                 time_checked=timezone.localtime(timezone.now()),
                                 state=0
                                 )
        # Increment failed status to keep track of consecutive failures
        url_entry.failed_status += 1
        url_entry.save()
        if url_entry.failed_status == 3:
            send_alert_email(url_entry, admin=True)
        else:
            send_alert_email(url_entry)
    else:
        UrlStatus.objects.create(url_tracker=url_entry, status_code=resp.status_code,
                                 time_checked=timezone.localtime(timezone.now()),
                                 state=0
                                 )
        # Set status to 0 again
        url_entry.failed_status = 0
        url_entry.save()


def send_alert_email(url_tracker: UrlTracker, admin=False):
    if admin:
        # TODO Send email only to admin?
        return
    else:
        # TODO send email to users in email list
        return
