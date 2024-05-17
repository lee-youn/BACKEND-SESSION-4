from rest_framework import serializers
from .models import Poll

class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = '__all__'  # 모든 필드를 포함

class PollRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ['title', 'description']
