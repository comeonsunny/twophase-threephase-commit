from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from twophase.models import TwoPhaseParticipant, TwoPhaseValue

def get_context():
    context = {'participants': [], 'values': []}
    for p in TwoPhaseParticipant.objects.all():
        p.values=[]
        for v in TwoPhaseValue.objects.filter(participant=p):
            p.values.append(v)
        context['participants'].append(p)
    if len(context['participants']) != 0:
        context['values'] = context['participants'][0].values
    return context

def app_page(request):
    return render(request, 'index0.html', get_context())

def index(request):
    return app_page(request)

def add_participant(request, participant_name):
    response = HttpResponse()
    participants = TwoPhaseParticipant.objects.all()
    for p in participants:
        if p.state != 0:
            response.status_code = 500
            return response
        elif p.name == participant_name:
            response.status_code = 400
            return response

    p = TwoPhaseParticipant(name=participant_name, state=0)
    p.save()
    added_keys = []
    # add existed values
    for v in TwoPhaseValue.objects.all():
        if v.key not in added_keys:
            added_keys.append(v.key)
            new_value = TwoPhaseValue(participant=p, key=v.key, value=v.value, previous_value=v.prepare_value)
            new_value.save()

    return app_page(request)

def add_value(request, key, value):
    response = HttpResponse()
    participants = TwoPhaseParticipant.objects.all()
    values = TwoPhaseValue.objects.all()
    for v in values:
        if v.key == key:
            response.status_code = 400
            return response

    for p in participants:
        new_value = TwoPhaseValue(participant=p, key=key, value=value, previous_value=value)
        new_value.save()
    return app_page(request)

def update_value(request):
    for num in range(1, 5):
        values = TwoPhaseValue.objects.filter(id = num).update(key = 'height')
    for num in range(5, 9):
        values = TwoPhaseValue.objects.filter(id = num).update(key = 'weight')
    TwoPhaseParticipant.objects.filter(id = 1).update(name = 'participant_1')
    TwoPhaseParticipant.objects.filter(id = 2).update(name = 'participant_2')
    TwoPhaseParticipant.objects.filter(id = 3).update(name = 'participant_3')
    TwoPhaseParticipant.objects.filter(id = 4).update(name = 'participant_4')

    return app_page(request)

def prepare(request, key):
    response = HttpResponse()
    value = request.GET[key]
    participants = TwoPhaseParticipant.objects.all()
    values = TwoPhaseValue.objects.filter(key=key)
    if len(values) == 0:
        response.status_code = 400
        return response
    for p in participants:
        p.state = 1
        p.save()
    for v in values:
        v.prepared_value = value
        v.save()
    return app_page(request)

def prepared(request, name):
    response = HttpResponse()
    flag = False
    for p in TwoPhaseParticipant.objects.filter(name=name):
        flag = True
        p.state = 2
        p.save()
    if flag is None:
        response.status_code = 400
        return response
    return app_page(request)

def commit(request):
    context = get_context()
    flag = True
    for p in context['participants']:
        if p.state != 2:
            flag = False
    if flag:
        for p in context['participants']:
            p.state = 0
            p.save()
            for v in p.values:
                v.value = v.prepared_value
                v.save()
    else:
        for p in context['participants']:
            p.state = 0
            p.save()
            for v in p.values:
                v.prepared_value = v.value
                v.save()

    return app_page(request)
