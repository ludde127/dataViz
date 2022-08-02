from pprint import pprint

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from data.models import DataStorage
# Create your views here.


@api_view(["GET", "POST", "PUT", "DELETE"])
def access_data(request, key):
    try:
        data = DataStorage.get_by_key(key)
    except DataStorage.DoesNotExist:
        data = None
    if data is not None:
        if request.method == "POST":
            data.add_data(request.data)
            data.save()
            return Response("SUCCESS", status=status.HTTP_200_OK)
        elif request.method == "GET":
            return HttpResponse(data.get_all_data().strip()) # Strip as trailing \n existed
        elif request.method == "PUT":
            data.put_data(request.data)
            data.save()
            return Response("SUCCESS", status=status.HTTP_200_OK)
        elif request.method == "DELETE":
            data.delete_data()
            data.save()
            return Response("SUCCESS", status=status.HTTP_200_OK)
        else:
            return Response("REQUEST METHOD " + request.method + " Not yet implemented.",
                            status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response("FORBIDDEN", status=status.HTTP_403_FORBIDDEN)
