from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Poll
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from decimal import Decimal, DivisionByZero
import json

# Create your views here.

@csrf_exempt
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

        poll_list = list(polls.values())
        return JsonResponse(poll_list, safe=False, status=200)
    
    if request.method == 'POST':
        data = json.loads(request.body)
        title = data.get('title')
        description = data.get('description')
        if not title or not description:
            return JsonResponse({'error': 'Title and description are required.'}, status=400)
        
        # 저장 후 새로 저장된 poll 객체 가져오기
        poll = Poll.objects.create(title=title, description=description)
        return JsonResponse({
            'id': poll.id,
            'title': poll.title,
            'description': poll.description,
            'agree': poll.agree,
            'disagree': poll.disagree,
            'agreeRate': float(poll.agreeRate),
            'disagreeRate': float(poll.disagreeRate),
            'createdAt': poll.createdAt,
        }, status=201)


@csrf_exempt
def poll_detail(request, id):
    poll = get_object_or_404(Poll, id=id)
    if request.method == 'GET':
        return JsonResponse({
            'id': poll.id,
            'title': poll.title,
            'description': poll.description,
            'agree': poll.agree,
            'disagree': poll.disagree,
            'agreeRate': float(poll.agreeRate),
            'disagreeRate': float(poll.disagreeRate),
            'createdAt': poll.createdAt,
        }, status=200)
    
    if request.method == 'PUT':
        data = json.loads(request.body)
        title = data.get('title')
        description = data.get('description')
        
        if not title or not description:
            return JsonResponse({'error': 'Title and description are required.'}, status=400)
        
        poll.title = title
        poll.description = description
        poll.save()
        return JsonResponse({
            'id': poll.id,
            'title': poll.title,
            'description': poll.description,
            'agree': poll.agree,
            'disagree': poll.disagree,
            'agreeRate': float(poll.agreeRate),
            'disagreeRate': float(poll.disagreeRate),
            'createdAt': poll.createdAt,
        }, status=200)
    
    if request.method == 'DELETE':
        poll.delete()
        return JsonResponse({}, status=204)


@csrf_exempt
def poll_agree(request, id):
    poll = get_object_or_404(Poll, id=id)
    poll.agree += 1

    poll.save()

    total_votes = poll.agree + poll.disagree
    
    try:
        if total_votes > 0:
            poll.agreeRate = (Decimal(poll.agree) / Decimal(total_votes)) * Decimal(100)
            poll.disagreeRate = (Decimal(poll.disagree) / Decimal(total_votes)) * Decimal(100)
        else:
            poll.agreeRate = Decimal(0)
            poll.disagreeRate = Decimal(0)
    except DivisionByZero:
        poll.agreeRate = Decimal(0)
        poll.disagreeRate = Decimal(0)
    
    poll.save()
    return JsonResponse({
        'id': poll.id,
        'title': poll.title,
        'description': poll.description,
        'agree': poll.agree,
        'disagree': poll.disagree,
        'agreeRate': float(poll.agreeRate),
        'disagreeRate': float(poll.disagreeRate),
        'createdAt': poll.createdAt,
    }, status=200)


@csrf_exempt
def poll_disagree(request, id):
    poll = get_object_or_404(Poll, id=id)
    poll.disagree += 1

    poll.save()
    
    total_votes = poll.agree + poll.disagree
    
    try:
        if total_votes > 0:
            poll.agreeRate = (Decimal(poll.agree) / Decimal(total_votes)) * Decimal(100)
            poll.disagreeRate = (Decimal(poll.disagree) / Decimal(total_votes)) * Decimal(100)
        else:
            poll.agreeRate = Decimal(0)
            poll.disagreeRate = Decimal(0)
    except DivisionByZero:
        poll.agreeRate = Decimal(0)
        poll.disagreeRate = Decimal(0)

    poll.save()
    return JsonResponse({
        'id': poll.id,
        'title': poll.title,
        'description': poll.description,
        'agree': poll.agree,
        'disagree': poll.disagree,
        'agreeRate': float(poll.agreeRate),
        'disagreeRate': float(poll.disagreeRate),
        'createdAt': poll.createdAt,
    }, status=200)
