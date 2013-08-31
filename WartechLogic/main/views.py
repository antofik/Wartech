# coding=utf-8
from django.http import HttpResponse
import json
from django.template import RequestContext
from django.shortcuts import render_to_response
from models import *


def JsonResponse(request, data):
    mimetype = 'text/plain'
    if 'HTTP_ACCEPT_ENCODING' in request.META.keys():
        if "application/json" in request.META['HTTP_ACCEPT_ENCODING']:
            mimetype = 'application/json'
    if 'ok' not in data:
        data['ok'] = True
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


def get_request_values(request, *keys):
    d = request.POST if request.method == "POST" else request.GET
    for key in keys:
        if key not in d:
            return False, ()
    return True, [d[key] for key in keys]


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
    data = []
    for robot in user.robots:
        item = {
            'id': robot.id,
            'name': robot.name,
            'description': robot.description,
            'hull': {
                'name': robot.hull.proto.name,
                'slug': robot.hull.proto.slug,
                'description': robot.hull.proto.description,
                'parameters': robot.hull.parameters,
                'modules': [{
                    'id': module.id,
                    'name': module.name,
                    'slot_id': module.hull_slot_id,
                    'parameters': module.parameters,
                    'slug': module.proto.slug,
                    'category': module.proty.category,
                    'description': module.proty.description,
                } for module in robot.hull.modules]
            }
        }
        data.append(item)
    return JsonResponse(request, data)


def get_user_modules(request):
    if not is_authrized(request):
        return JsonResponse(request, {"ok": False, "error_message": "Not authorized"})

    user_id = request.session["user_id"]
    user = User.objects.get(pk=user_id)
    data = [{
        'id': module.id,
        'slot': module.slot,
        'equipped': module.hull_id is not None,
        'slug': module.proto.slug,
        'parameters': module.parameters,
    } for module in user.modules]
    return JsonResponse(request, data)


def set_module_to_slot(request):
    if not is_authrized(request):
        return JsonResponse(request, {"ok": False, "error_message": "Not authorized"})

    ok, values = get_request_values(request, "slot_id", "module_id", "robot_id")
    if not ok:
        return JsonResponse(request, {"ok": False,
                                      "error_message": "Request should contain all 'slot_id', "
                                                       "'module_id', and 'robot_id' parameters"})
    slot_id, module_id, robot_id = values

    user_id = request.session["user_id"]
    user = User.objects.get(pk=user_id)

    robot = None
    for r in user.robots:
        if r.id == robot_id:
            robot = r
    if not robot:
        return JsonResponse(request, {"ok": False, "error_message": "Robot not found"})

    module = None
    for m in user.modules:
        if m.id == module_id:
            module = m
    if not module:
        return JsonResponse(request, {"ok": False, "error_message": "Module not found"})

    hull = robot.hull
    slots = json.loads(hull.parameters)['slots']
    old_module_id = -1
    for slot in slots:
        if slot['id'] == slot_id:
            if slot['slot'] == module.slot:
                if 'module_id' in slot:
                    old_module_id = slot['module_id']
                slot['module_id'] = module.id
                module.hull = hull
                module.hull_slot_id = slot_id
                hull.parameters = json.dumps(slots)
                module.save()
                hull.save()
                break
            else:
                return JsonResponse(request, {"ok": False, "error_message": "You are trying mount <%s> "
                                                                            "module in <%s> slot" %
                                                                            (module.slot, slot['slot'])})
    else:
        return JsonResponse(request, {"ok": False, "error_message": "Slot not found"})

    return JsonResponse(request, {'ok': True, 'unequipped_module': old_module_id})


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
