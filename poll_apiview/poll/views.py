from django.shortcuts import render
from .models import Poll
from .serializers import PollRequestSerializer, PollSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from decimal import Decimal, DivisionByZero

# Create your views here.

@api_view(['GET','POST'])
def poll_list(request):
    if request.method == 'GET':
        sort_by = request.GET.get('sort_by', 'latest')
            
        if sort_by == 'latest':
            polls = Poll.objects.all().order_by('-createdAt')
        elif sort_by == 'oldest':
            polls = Poll.objects.all().order_by('createdAt')
        elif sort_by == 'agree':
            polls = Poll.objects.all().order_by('-agree')
        else: # sort_by == 'disagree'
            polls = Poll.objects.all().order_by('-disagree')

        serializer = PollSerializer(polls, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    if request.method == 'POST':
        serializer = PollRequestSerializer(data = request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status = status.HTTP_400_BAD_REQUEST
            )
        
        # 저장 후 새로 저장된 poll 객체 가져오기
        poll = serializer.save()
        poll_serializer = PollSerializer(poll)
        return Response(poll_serializer.data, status = status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def poll_detail(request, id):
    if request.method == 'GET':
        poll = Poll.objects.get(id=id)
        serializer = PollSerializer(poll)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    if request.method == 'PUT':
        poll = Poll.objects.get(id=id)
        serializer = PollRequestSerializer(poll, data = request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status = status.HTTP_400_BAD_REQUEST
            )
        poll = serializer.save()
        poll_serializer = PollSerializer(poll)
        return Response(poll_serializer.data, status = status.HTTP_200_OK)
    
    if request.method == 'DELETE':
        poll = Poll.objects.get(id=id)
        poll.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def poll_agree(request, id):
    poll = Poll.objects.get(id=id)
    poll.agree += 1
    poll.save()

    # 찬성 표율 다시 계산
    total_votes = poll.agree + poll.disagree
    
    try:
        if total_votes > 0:
            poll.agreeRate = (Decimal(poll.agree) / Decimal(total_votes))
            poll.disagreeRate = (Decimal(poll.disagree) / Decimal(total_votes))
        else:
            poll.agreeRate = Decimal(0)
            poll.disagreeRate = Decimal(0)
    except DivisionByZero:
        poll.agreeRate = Decimal(0)
        poll.disagreeRate = Decimal(0)
    poll.save()
    
    serializer = PollSerializer(poll)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def poll_disagree(request, id):
    poll = Poll.objects.get(id=id)
    poll.disagree += 1
    poll.save()

    # 반대 표율 다시 계산
    total_votes = poll.agree + poll.disagree
    
    try:
        if total_votes > 0:
            poll.agreeRate = (Decimal(poll.agree) / Decimal(total_votes))
            poll.disagreeRate = (Decimal(poll.disagree) / Decimal(total_votes))
        else:
            poll.agreeRate = Decimal(0)
            poll.disagreeRate = Decimal(0)
    except DivisionByZero:
        poll.agreeRate = Decimal(0)
        poll.disagreeRate = Decimal(0)
    poll.save()
    
    serializer = PollSerializer(poll)
    return Response(serializer.data, status=status.HTTP_200_OK)
