# coding=utf-8
import random
import string
from django.http import HttpResponse, Http404
import json
from django.template import RequestContext
from django.shortcuts import render_to_response
from models import *


def JsonResponse(request, data):
    mimetype = 'text/plain'
    if 'HTTP_ACCEPT_ENCODING' in request.META.keys():
        if "application/json" in request.META['HTTP_ACCEPT_ENCODING']:
            mimetype = 'application/json'
    response = HttpResponse(json.dumps(data), content_type=mimetype)
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "86400"
    response["x-test"] = "super secret header"
    if request.method == "OPTIONS":
        response["Access-Control-Allow-Headers"] = "origin, content-type, x-requested-with, accept, authorization"
    return response


def home(request):
    return render_to_response('home.html', {}, context_instance=RequestContext(request))


def dummy(request):
    data = {'Artem': 'Kurtem', 'session_key': request.session.session_id}
    return JsonResponse(request, data)


def is_authrized(request):
    if not "is_authorized" in request.session:
        return False
    return request.session["is_authorized"]


def get_all_users(request):
    user_id = request.session["user_id"] if "user_id" in request.session else None
    users = User.objects.filter(is_online=True).all()
    data = [{'name': user.name, 'available_for_fight': user.id != user_id} for user in users]
    return JsonResponse(request, data)


def request_fight(request):
    data = {
        'granted': True,
        'arena': {
            'width': 20,
            'height': 20,
            'cells': [
                1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            ],
        },
        'fight_replay': {},
    }
    return JsonResponse(request, data)


def get_all_modules(request):
    data = []
    for module in ModulePrototype.objects.all():
        item = {
            'slot': module.slot,
            'slug': module.slug,
            'name': module.name,
            'description': module.description,
            'parameters': module.parameters,
        }
        data.append(item)
    return JsonResponse(request, data)


def get_user_robot(request):
    if not is_authrized(request):
        return JsonResponse(request, {"ok": False, "error_message": "Not authorized"})

    user_id = request.session["user_id"]
    user = User.objects.get(pk=user_id)
    user.robot

    data = {
        'ok': True,
        'hull_name': 'monster',
        'hull_slots': [
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
                'slot': 'energy',
                'module': 'battery',
                'params': {
                    'energy': 87,
                    'capacity': 100
                },
            },
            {
                'id': 4,
                'slot': 'processor',
                'module': 'Pentium III',
                'params': {
                    'overheat': 12,
                },
            }
        ],
    }
    return JsonResponse(request, data)


def get_user_modules(request):
    data = [
        {
            'id': 1,
            'slot': 'sensor',
            'module': 'optic',
            'equipped': False,
        },
        {
            'id': 3,
            'slot': 'power',
            'module': 'Battery 10KJ',
            'equipped': True,
        },
        {
            'id': 4,
            'slot': 'power',
            'module': 'Battery 10KJ',
            'equipped': False,
        },
        {
            'id': 47,
            'slot': 'processor',
            'module': 'Pentium II',
            'equipped': False,
        }
    ]
    return JsonResponse(request, data)


def set_module_to_slot(request):
    data = {
        'ok': True,
        'unequipped_module': 4, # -1 if no module was unequipped
        'error_reason': '',
    }
    return JsonResponse(request, data)


def give_start_robot_to_user(user):
    hullProto = HullPrototype.objects.get(slug='start')
    hull = Hull()
    hull.proto = hullProto
    hull.parameters = hullProto.parameters
    hull.save()

    slots = json.load(hullProto.parameters)['slots']

    robot = Robot()
    robot.user = user
    robot.hull = hull
    robot.save()

    for moduleProto in ModulePrototype.objects.filter(category="start").all():
        module = UserModule()
        module.user = user
        module.proto = moduleProto
        module.hull = hull
        for slot in slots:
            if moduleProto.slot == slot.slot:
                module.hull_slot_id = slot.id
                slots.remove(slot)
                break
        module.save()


def login(request):
    for key in ["token", "provider"]:
        if key not in request.session:
            return JsonResponse(request, {"ok": False, "error_message": "key %s not found" % key})
    token = request.session["token"]
    provider = request.session["provider"]
    users = User.objects.filter(token=token).filter(provider=provider).all()
    if users:
        user = users[0]
    else:
        user = User()
        user.token = token
        user.provider = provider
        give_start_robot_to_user(user)
    user.is_online = True
    user.login_date = datetime.datetime.now()
    user.save()
    request.session["user_id"] = user.id
    request.session["is_authorized"] = True
    return JsonResponse(request, {'granted': True})


def logout(request):
    if not is_authrized(request):
        return JsonResponse(request, {"ok": False, "error_message": "Not authorized"})
    request.session["is_authorized"] = False
    return JsonResponse(request, {"ok": True})
