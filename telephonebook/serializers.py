from rest_framework import serializers
from .models import Person, Info
from drf_writable_nested import WritableNestedModelSerializer

class InfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Info
        fields = ['number', 'email']

class PersonSerializer(WritableNestedModelSerializer):
    info = InfoSerializer(required=False)
    class Meta:
        model = Person
        fields = '__all__'

    def create(self, validated_data):
        #info_item = validated_data.pop('info')
        person = Person.objects.create(name=validated_data['name'], lastname=validated_data['lastname'])

        for item in validated_data['info']:
            #for item in info_item:
            detail = Info(number=item['number'], email=item['email'], person=person)
            detail.save()
        return person

    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.save()

        numbers = [item['number'] for item in validated_data['number']]
        for num in instance.number:
            if num.number not in numbers:
                num.delete()
        emails = [item['email'] for item in validated_data['email']]
        for ema in instance.email:
            if ema.email not in emails:
                ema.delete()

        for item in validated_data['info']:
            detail = Info(number=item['number'], email=item['email'], person=instance)
            detail.save()

        return instance
