from __future__ import print_function

import json
import time
import csv

from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.utils.encoding import smart_str
from django.utils.crypto import get_random_string
from django.http import HttpResponse
from django.utils import timezone
from datetime import timedelta

from django.shortcuts import render

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.settings import api_settings
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination

from affairal_app.models import *
from affairal_app.permissions import *
from affairal_app.serializers import *


class AffairalUserList(generics.ListCreateAPIView):
    queryset = AffairalUser.objects.all()
    serializer_class = AffairalUserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminOrNewUser,)

    def list(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        stats = {"success": True}

        data = {"users": serializer.data}

        response = {"status": stats, "data": data}

        return Response(response)

    def post(self, request, *args, **kwargs):

        print(1)

        #document = request.file

        serializer = self.get_serializer(data=request.data)

        print (serializer.initial_data)

        print(2)
        serializer.is_valid(raise_exception=True)

        print(3)
        self.perform_create(serializer)
        print(4)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()


class AffairalUserDetail(generics.RetrieveUpdateDestroyAPIView):

    queryset = AffairalUser.objects.all()
    serializer_class = AffairalUserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsSelfOrAdmin,)

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_deleted is True:
            raise NotFound("Requested resource does not exists")

        serializer = self.get_serializer(instance)

        response_status = {"success": True}
        data = {"user": serializer.data}

        response = {"status": response_status, "data": data}

        return Response(response)


class EventList(generics.ListCreateAPIView):

    queryset = Event.objects.all()
    serializer_class = EventSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        stats = {"success": True}

        data = {"users": serializer.data}

        response = {"status": stats, "data": data}

        return Response(response)

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class EventDetail(generics.RetrieveUpdateDestroyAPIView):

    queryset = Event.objects.all()
    serializer_class = EventSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOwnerOrAdmin,)
