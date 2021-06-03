from urltrack.models import UrlTracker
from urltrack.serializers import UrlTrackerSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, api_view, authentication_classes

from tasks.checkstatus import check_url_task


class UrlListViewSet(APIView):
    """
    List all urls associated with an account.
    Create new urls to monitor.
    """
    queryset = UrlTracker.objects.all()

    def get(self, request):
        # Fetch all urls for the user logged in
        # TODO Add admin account with
        urls = UrlTracker.objects.all()
        serializer = UrlTrackerSerializer(urls, many=True)
        return Response(serializer.data)

    # def post(self, request):
    #     # TODO USE JWT TOken to get the account to set admin
    #     serializer = UrlTrackerSerializer(data=request.data)
    #     if serializer.is_valid():
    #         url_tracker = serializer.save()
    #         print(serializer.data)
    #         check_url_task(url_tracker.id, url_tracker.frequency)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_url_tracker_view(request):
    serializer = UrlTrackerSerializer(data=request.data)
    if serializer.is_valid():
        url_tracker = serializer.save()
        print(serializer.data)
        check_url_task(url_tracker.id, url_tracker.frequency)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SearchUrls(APIView):

    def get(self, request):
        pass