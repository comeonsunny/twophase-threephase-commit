from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from threephase.models import ThreePhaseParticipant, ThreePhaseValue

def get_context():
    context = {'participants': [], 'values': []}
    for p in ThreePhaseParticipant.objects.all():
        p.values=[]
        for v in ThreePhaseValue.objects.filter(participant=p):
            p.values.append(v)
        context['participants'].append(p)
    if len(context['participants']) != 0:
        context['values'] = context['participants'][0].values
    return context

def app_page(request):
    return render(request, 'index1.html', get_context())

def index(request):
    return app_page(request)

def add_participant(request, participant_name):
    response = HttpResponse()
    participants = ThreePhaseParticipant.objects.all()
    for p in participants:
        if p.state != 0:
            response.status_code = 500
            return response
        elif p.name == participant_name:
            response.status_code = 400
            return response

    p = ThreePhaseParticipant(name=participant_name, state=0)
    p.save()
    added_keys = []
    # add existed values
    for v in ThreePhaseValue.objects.all():
        if v.key not in added_keys:
            added_keys.append(v.key)
            new_value = ThreePhaseValue(participant=p, key=v.key, value=v.value, prepared_value=v.value)
            new_value.save()

    return app_page(request)

def add_value(request, key, value, prepared_value):
    response = HttpResponse()
    participants = ThreePhaseParticipant.objects.all()
    values = ThreePhaseValue.objects.all()
    for v in values:
        if v.key == key:
            response.status_code = 400
            return response

    for p in participants:
        new_value = ThreePhaseValue(participant=p, key=key, value=value, prepared_value= prepared_value)
        new_value.save()
    return app_page(request)
def delete_value(request):
    for num in range(9, 17):
        data = ThreePhaseValue.objects.get(id = num)
        data.delete()
    return app_page(request)

def update_name(request):
    participant = ThreePhaseParticipant.objects.filter(id=1).update(name = 'participant_1')
    participant = ThreePhaseParticipant.objects.filter(id=2).update(name = 'participant_2')
    participant = ThreePhaseParticipant.objects.filter(id=3).update(name = 'participant_3')
    participant = ThreePhaseParticipant.objects.filter(id=4).update(name = 'participant_4')
    for num in range(1, 5):
        value = ThreePhaseValue.objects.filter(id = num).update(key = 'height')
    for num in range(5, 9):
        value = ThreePhaseValue.objects.filter(id = num).update(key = 'weight')
    return app_page(request)
def prepare(request, key):
    response = HttpResponse()
    value = request.GET[key]
    participants = ThreePhaseParticipant.objects.all()
    values = ThreePhaseValue.objects.filter(key=key)
    if len(values) == 0:
        response.status_code = 400
        return response
    for p in participants:
        p.state = 1
        p.save()
    for v in values:
        if v.key == key:
            v.prepared_value = value
            v.save()
    return app_page(request)

def prepared(request, name):
    response = HttpResponse()
    flag = False
    for p in ThreePhaseParticipant.objects.filter(name=name):
        flag = True
        p.state = 2
        p.save()
    if flag is None:
        response.status_code = 400
        return response
    return app_page(request)

def pre_commit(request):
    context = get_context()
    response = HttpResponse()
    participants = ThreePhaseParticipant.objects.all()
    values = ThreePhaseValue.objects.all()
    for p in context['participants']:
        if (p.state == 5 or p.state == 6):
            for v in values:
                if v.key == p.name:
                    v.prepared_value = 'yes'
                    v.save()
        
           
    '''
    flag = True
    for p in context['participants']:
        if p.state != 2:
            flag = False
    for p in context['participants']:
        if flag:
            p.state = 3
        else:
            p.state = 0
            for v in p.values:
                v.prepared_value = v.value
                v.save()
        p.save() 
    '''
    return app_page(request)

def pre_committed(request, name):
    context = get_context()
    for p in context['participants']:
        if p.name == name:
            p.state = 4
            p.save()
    return app_page(request)

def Agree(request, name):
    context = get_context()
    for p in context['participants']:
        if p.name == name:
            p.state = 5
            p.save()
    for v in context['values']:
        if v.key == name:
            v.value = 'Agree'
            #v.prepared_value = 'yes'
            v.save()
    return app_page(request)

def Disagree(request, name):
    context = get_context()
    for p in context['participants']:
        if p.name == name:
            p.state = 6
            p.save()
    for v in context['values']:
        if v.key == name:
            v.value = 'Disagree'
            #v.prepared_value = 'yes'
            v.save()
    return app_page(request)

def commit(request):
    for num in range(109, 113):
        ThreePhaseValue.objects.filter(id=num).update(key = 'participant_1')
    for num in range(113, 117):
        ThreePhaseValue.objects.filter(id=num).update(key = 'participant_2')
    for num in range(117, 121):
        ThreePhaseValue.objects.filter(id=num).update(key = 'participant_3')
    for num in range(121, 125):
        ThreePhaseValue.objects.filter(id=num).update(key = 'participant_4')
    return app_page(request)
    '''
    context = get_context()
    flag = False
    for p in context['participants']:
        if p.state == 4:
            flag = True
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

    for num in range(69, 109):
        ThreePhaseValue.objects.filter(id = num).delete()
    return app_page(request)
    ''' 
