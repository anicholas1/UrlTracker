from urltrack.models import UrlTracker
from urltrack.serializers import UrlTrackerSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from tasks.checkstatus import check_url_task

# TODO What views do I need
# 1. GET Search
# 2. POST Add url!
# 3. POST JWT Access Token Request
# 4. GET urls associated with account


class UrlListViewSet(APIView):
    """
    List all urls associated with an account.
    Create new urls to monitor.
    """
    queryset = UrlTracker.objects.all()

    def get(self, request):
        # Fetch all urls for the user logged in
        # TODO add account lookup here. How do we know if they are logged in
        urls = UrlTracker.objects.all()
        serializer = UrlTrackerSerializer(urls, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Create url tracker
        # TODO this should require only api auth
        serializer = UrlTrackerSerializer(data=request.data)
        if serializer.is_valid():
            url_tracker = serializer.save()
            check_url_task(url_tracker.id, url_tracker.frequency)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SearchUrls(APIView):

    def get(self, request):
        pass