from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from caloriecounter.voice.models import VoiceSession, VoiceSessionItem


class VoiceSessionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoiceSessionItem
        fields = ['created_on', 'user_created', 'session', 'type', 'text', 'data', ]
        read_only_fields = ['created_on', 'user_created', 'session', 'type', 'data']

    def validate(self, attrs):
        if 'text' not in attrs or attrs.get('text', None) == '':
            raise serializers.ValidationError({'text' : _('This field is required')})

        return attrs


class VoiceSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoiceSession
        fields = ['pk', 'user_date', 'user_time', 'items']
        read_only_fields = ['pk']

    items = VoiceSessionItemSerializer(many=True)

    def create(self, validated_data):
        item = VoiceSessionItem.objects.create(type='user_input', **validated_data)

    def validate_items(self, value):
        """
        Check that there is one item in the session
        """
        if len(value) != 1:
            raise serializers.ValidationError(_('A new Voice Session should contain 1 item'))

        item = value[0]

        VoiceSessionItemSerializer().validate(item)

        return value

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        session = VoiceSession.objects.create(**validated_data)

        for item_data in items_data:
            VoiceSessionItem.objects.create(session=session, type='user_input', **item_data)
        return session

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items')
        instance = super().update(instance, validated_data)

        for item_data in items_data:
            VoiceSessionItem.objects.create(session=instance, type='user_input', **item_data)

        return instance




