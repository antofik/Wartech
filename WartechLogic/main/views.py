# coding=utf-8
import string
from django.http import HttpResponse
from django.utils import simplejson
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, Http404, redirect
from django.views.decorators.csrf import csrf_exempt


def JsonResponse(data):
    response = HttpResponse(simplejson.dumps(data), content_type="application/json")
    response["Access-Control-Allow-Origin"] = "*"  
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"  
    response["Access-Control-Max-Age"] = "1000"  
    response["Access-Control-Allow-Headers"] = "Origin, Content-Type"
    return response


def home(request):
    return render_to_response('home.html', {}, context_instance=RequestContext(request))
    
def dummy(request):    
    data = {
        'Artem': 'Kurtem'
    }
    return JsonResponse(data) 
    
def init(request):    
    data = {
        'session_id': 'dummy_session_key'
    }
    return HttpResponse(simplejson.dumps(data), content_type="application/json")
    
def get_all_users(request):    
    data = [
        {'name':'antofik', 'available_for_fight': True},
        {'name':'ents', 'available_for_fight': True},
        {'name':'BaDkInG', 'available_for_fight': False}
    ]
    return JsonResponse(data)
    
def request_fight(request):    
    data = {
        'granted': true,
        'arena': {
            'width': 20,
            'height': 20,
            'cells': [
                1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
                1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
            ],
        },
        'fight_replay': {},
    }
    return JsonResponse(data)
    
def get_all_modules(request):    
    data = [
        {
           'slot':'sensor',
           'modules':[
                'optic',
                'sound',
                'wifi'
           ]
        },
        {
           'slot':'processor',
           'modules':[
                'Pentium I',
                'Pentium II',
                'Pentium III',
                'Pentium IV'
           ]
        }
    ]
    return JsonResponse(data)
    
def get_user_robot(request):    
    data = {
        'hull_name': 'monster',
        'hull_slots':[
            {
                'id': 1,
                'slot': 'sensor',
                'module': 'eye',
            },
            {
                'id': 32,
                'slot': 'sensor',
                'module': 'eye',
            },
            {
                'id': 2,
                'slot': 'motion',
                'module': 'legs',
                'params': {
                     'count': 3,
                },
            },
            {
                'id': 3,
                'slot':'energy',
                'module':'battery',
                'params':{
                     'energy': 87,
                     'capacity': 100
                },
            },
            {
                'id': 4,
                'slot':'processor',
                'module':'Pentium III',
                'params':{
                     'overheat': 12,
                },
            }
        ],
    }
    return JsonResponse(data)
    
def get_user_modules(request):    
    data = [
            {
               'id': 1,
               'slot':'sensor',
               'module': 'optic',
               'equipped': false,
            },
            {
               'id': 3,
               'slot':'power',
               'module': 'Battery 10KJ',
               'equipped': true,
            },
            {
               'id': 4,
               'slot':'power',
               'module': 'Battery 10KJ',
               'equipped': false,
            },
            {
               'id': 47,
               'slot':'processor',
               'module': 'Pentium II',
               'equipped': false,
            }
        ]    
    return JsonResponse(data)
    
def set_module_to_slot(request):    
    data = {
        'ok': true,
        'unequipped_module': 4, # -1 if no module was unequipped
        'error_reason': '',    
    }
    return JsonResponse(data)
    
def create_new_user(request):    
    data = {
        'id': 11023,
        'session_id': '$fFDf32sd$@$@#$sdf3424fsd3==43223%@@!d', #must be added to cookies
        'user_name': 'RJ122302',
        'serial_number': '00203-22-108', #unique text id, which cannot be changed by user
    }
    return JsonResponse(data)
        
def login(request):    
    data = {
        'granted': false,
        'error_message': 3, # e.g., "3" is localization key, which corresponds to 'invalid password'
    }
    return JsonResponse(data)
        
def logout(request):    
    data = {}
    return JsonResponse(data)
