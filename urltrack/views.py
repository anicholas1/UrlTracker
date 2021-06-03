from django.http import HttpResponseRedirect

from urltrack.models import UrlTracker
from urltrack.serializers import UrlTrackerSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, api_view, authentication_classes
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import status
from tasks.checkstatus import check_url_task
import json

from urltrack.utils.validate_email import validate_user_email


class UrlListViewSet(APIView):
    """
    List all urls associated with an account.
    Create new urls to monitor.
    """
    renderer_classes = [TemplateHTMLRenderer, ]
    template_name = 'dashboard.html'

    def get(self, request):
        # Fetch all urls for the user logged in
        queryset = UrlTracker.objects.all()
        return Response({'urls': queryset})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_url_tracker_view(request):
    data = request.data
    if data.get('user_emails'):
        # Hackish way to get around sqllite not having json field.
        # Need to have the request data in the right format
        emails = data.get('user_emails').split(',')
        email_data = json.dumps(emails)
        request.data.update({"user_emails": email_data})
    serializer = UrlTrackerSerializer(data=request.data)
    if serializer.is_valid():
        url_tracker = serializer.save()
        check_url_task(url_tracker.id, url_tracker.frequency)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailNotificationsViewset(APIView):
    """
    Update user_emails on Url Trackers.
    Currently only supports POST due to forms only supporting GET/POST.
    Normally I would have made this a patch
    """

    def post(self, request):
        """ Update only the user_emails field on UrlTracker"""
        url_tracker = UrlTracker.objects.get(pk=request.data.get('url_id'))
        if not url_tracker:
            return Response({"error": "invalid_data",
                             "error_description": "The id provided was invalid"
                             }
                            )
        # Hackish way again to make sure data is in a json format in the text field in sqllite
        user_email = request.data.get('user_emails')
        validate_user_email(user_email)
        emails = json.loads(url_tracker.user_emails)
        if emails:
            emails.append(user_email)
            email_data = json.dumps(emails)
        else:
            email_data = json.dumps([user_email])

        url_tracker.user_emails = email_data
        url_tracker.save()
        return HttpResponseRedirect(redirect_to='/')


class SearchUrlsViewSet(ViewSet):
    serializer_class = UrlTrackerSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = UrlTracker.objects.all()
        url_param = self.request.query_params.get('url')
        email_param = self.request.query_params.get('email')
        if url_param or email_param:
            if url_param:
                queryset = queryset.filter(url__contains=url_param)
            if email_param:
                queryset = queryset.filter(admin_email__icontains=email_param)
        else:
            return Response({"error": "invalid_params",
                             "error_description": "Missing either a url or email search param."
                             })
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
