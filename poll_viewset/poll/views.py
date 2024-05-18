from django.shortcuts import render
from .models import Poll
from .serializers import PollRequestSerializer, PollSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from decimal import Decimal, InvalidOperation


class PollViewSet(viewsets.ViewSet):

        def list(self, request) :
            sort_by = request.GET.get('sort_by', 'latest')
                
            if sort_by == 'latest':
                queryset = Poll.objects.all().order_by('-createdAt')
            elif sort_by == 'oldest':
                queryset = Poll.objects.all().order_by('createdAt')
            elif sort_by == 'agree':
                queryset = Poll.objects.all().order_by('-agree')
            else: # sort_by == 'disagree'
                queryset = Poll.objects.all().order_by('-disagree')

            serializer = PollSerializer(queryset, many = True)
            return Response(serializer.data, status = status.HTTP_200_OK)
        
        def create(self, request) :
            serializer = PollRequestSerializer(data = request.data)
            if not serializer.is_valid():
                return Response(
                    serializer.errors, status = status.HTTP_400_BAD_REQUEST
                )
            
            # 저장 후 새로 저장된 poll 객체 가져오기
            poll = serializer.save()
            poll_serializer = PollSerializer(poll)
            return Response(poll_serializer.data, status = status.HTTP_201_CREATED)

        def retrieve(self, request, pk=None):
            poll = Poll.objects.get(pk=pk)
            serializer = PollSerializer(poll)
            return Response(serializer.data, status=status.HTTP_200_OK)

            
        def update(self, request, pk=None):
            poll = Poll.objects.get(pk=pk)
            serializer = PollRequestSerializer(poll, data = request.data)
            if not serializer.is_valid():
                return Response(
                    serializer.errors, status = status.HTTP_400_BAD_REQUEST
                )
            poll = serializer.save()
            poll_serializer = PollSerializer(poll)
            return Response(poll_serializer.data, status = status.HTTP_200_OK)
            
        def destory(self, request, pk = None):
            poll = Poll.objects.get(pk=pk)
            poll.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)
        


        @action(detail=True, methods=['post'], url_path='agree')
        def agree(self, request, pk=None):
            poll = Poll.objects.get(pk=pk)
            poll.agree += 1
            poll.save()
            # 찬성 표율 다시 계산
            total_votes = poll.agree + poll.disagree
            if total_votes > 0:
                try:
                    poll.agreeRate = (Decimal(poll.agree) / Decimal(total_votes))
                    poll.disagreeRate = (Decimal(poll.disagree) / Decimal(total_votes))
                except InvalidOperation:
                    poll.agreeRate = Decimal(0)
                    poll.disagreeRate = Decimal(0)
            else:
                poll.agreeRate = Decimal(0)
                poll.disagreeRate = Decimal(0)
            poll.save()
            serializer = PollSerializer(poll)
            return Response(serializer.data, status=status.HTTP_200_OK)

        @action(detail=True, methods=['post'], url_path='disagree')
        def disagree(self, request, pk=None):
            poll = Poll.objects.get(pk=pk)
            poll.disagree += 1
            poll.save()
            # 반대 표율 다시 계산
            total_votes = poll.agree + poll.disagree
            if total_votes > 0:
                try:
                    poll.disagreeRate = (Decimal(poll.disagree) / Decimal(total_votes))
                    poll.agreeRate = (Decimal(poll.agree) / Decimal(total_votes))
                except InvalidOperation:
                    poll.agreeRate = Decimal(0)
                    poll.disagreeRate = Decimal(0)
            else:
                poll.agreeRate = Decimal(0)
                poll.disagreeRate = Decimal(0)
            poll.save()
            serializer = PollSerializer(poll)
            return Response(serializer.data, status=status.HTTP_200_OK)