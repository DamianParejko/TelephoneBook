from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.http import  HttpResponseRedirect

from rest_framework import generics
from rest_framework import mixins
from rest_framework import viewsets

from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Person, Info
from .forms import PersonForm, InfoForm
from .serializers import PersonSerializer, InfoSerializer

# Create your views here.

class PersonViewSet(viewsets.ModelViewSet):
    serializer_class = PersonSerializer
    queryset = Person.objects.all()
    lookup_field = 'id'

    @action(methods=["GET"], detail=True)
    def choices(self, request, id=None):
        number = self.get_object()
        choices = Info.objects.filter(number=number)
        serializer = InfoSerializer(choices, many=True)
        return Response(serializer.data, status=200)

class PersonListView(
    generics.GenericAPIView,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin):

    serializer_class = PersonSerializer
    queryset = Person.objects.all()
    lookup_field = 'id'

    def get_queryset(self, *args, **kwargs):
        queryset_list = Person.objects.all()
        query = self.request.GET.get('q')
        if query:
            queryset_list = queryset_list.filter(
                Q(name__icontains=query) |
                Q(lastname__icontains=query)
            )
        return queryset_list

    def get(self, request, id=None):
        if id:
            return self.retrieve(request, id)
        else:
            return self.list(request)

    def post(self, request, id=None):
        return self.create(request, id)

    def put(self, request, id=None):
        return self.update(request, id)

    def delete(self, request, id=None):
        return self.destroy(request, id)


def index(request):
    querysetPerson = Person.objects.all()
    querysetInfo = Info.objects.all()
    query = request.GET.get('q')
    if query:
        querysetPerson = querysetPerson.filter(
            Q(name__icontains=query) |
            Q(lastname__icontains=query))
    elif query:
        querysetInfo = querysetInfo.filter(
            Q(number__icontains=query) |
            Q(email__icontains=query))
    context = {
        'P' : querysetPerson,
        'I' : querysetInfo
    }
    return render(request, 'index.html', context)

def details(request, id=None):
    setting = get_object_or_404(Person, id=id)
    info = Info.objects.all()
    context = {

        'question' : setting,
        'info' : info
    }
    return render(request, 'details.html', context)

def editInfo(request, id=None):
    instance = get_object_or_404(Person, id=id)
    form = InfoForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form": form,
    }
    return render(request, "form_info.html", context)

def editPerson(request, id=None):
    instance = get_object_or_404(Person, id=id)
    form = PersonForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {

        "form":form,
    }
    return render(request, "form_person.html", context)

def create(request):
    person_form = PersonForm(request.POST or None, instance=Person())
    info_form = [InfoForm(request.POST or None, prefix=str(x), instance=Info()) for x in range(1)]
    if person_form.is_valid() and all([inf.is_valid() for inf in info_form]):
        instance = person_form.save(commit=False)
        instance.save()
        for inf in info_form:
            instance_info = inf.save(commit=False)
            instance_info.number = instance
            instance_info.save()
        return HttpResponseRedirect('/index/')
    context = {
        "form_person" : person_form,
        "form_info" : info_form
        }
    return render(request, 'create.html', context)

def delete(request, id=None):
    queryset = get_object_or_404(Person, id=id)
    number = Info.objects.values('number')
    email = Info.objects.values('email')
    if number is not True or email is not True:
        queryset.delete()
    return redirect('/')
