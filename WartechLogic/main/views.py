# coding=utf-8
from django.db import transaction
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
    response = HttpResponse(json.dumps(data), content_type=mimetype)
    response["Access-Control-Allow-Credentials"] = "true"
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "86400"
    response["x-test"] = "super secret header"
    if request.method == "OPTIONS":
        response["Access-Control-Allow-Headers"] = "origin, content-type, x-requested-with, accept, authorization"
    return response



def home(request):
    text = open(r'../.git/refs/heads/master').read()
    return render_to_response('home.html', {'git_version': text}, context_instance=RequestContext(request))


def dummy(request):
    data = {'Artem': 'Kurtem', 'session_key': request.session.session_id}
    return JsonResponse(request, data)


def get_request_values(request, *keys):
    d = request.POST if request.method == "POST" else request.GET
    for key in keys:
        if key not in d:
            return False, ()
    return True, [d[key] for key in keys]


def get_is_authorized(request):
    return JsonResponse(request, is_authorized(request))


def is_authorized(request):
    if not request.session or not "is_authorized" in request.session:
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
    if not is_authorized(request):
        return JsonResponse(request, {"ok": False, "error_message": "Not authorized"})

    user_id = request.session["user_id"]
    user = User.objects.get(pk=user_id)
    data = []
    for robot in user.robots.select_related("hull__proto").all():
        print 'proto=%s' % robot.hull.proto
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
                    'name': module.proto.name,
                    'slot_id': module.hull_slot_id,
                    'parameters': module.parameters,
                    'slug': module.proto.slug,
                    'category': module.proto.category,
                    'description': module.proto.description,
                } for module in robot.hull.modules.all().prefetch_related("proto", "hull")]
            }
        }
        data.append(item)
    return JsonResponse(request, data)


def get_user_modules(request):
    if not is_authorized(request):
        return JsonResponse(request, {"ok": False, "error_message": "Not authorized"})

    user_id = request.session["user_id"]
    user = User.objects.get(pk=user_id)
    data = [{
        'id': module.id,
        'slot': module.proto.slot,
        'equipped': module.hull_id is not None,
        'slug': module.proto.slug,
        'parameters': module.parameters,
    } for module in user.modules.all()]
    return JsonResponse(request, data)


@transaction.commit_on_success
def set_module_to_slot(request):
    if not is_authorized(request):
        return JsonResponse(request, {"ok": False, "error_message": "Not authorized"})

    ok, values = get_request_values(request, "slot_id", "module_id", "robot_id")
    if not ok:
        return JsonResponse(request, {"ok": False,
                                      "error_message": "Request should contain all 'slot_id', "
                                                       "'module_id', and 'robot_id' parameters"})
    try:
        slot_id, module_id, robot_id = map(int, values)
    except TypeError:
        return JsonResponse(request, {"ok": False, "error_message": "Invalid parameters"})

    user_id = request.session["user_id"]
    user = User.objects.get(pk=user_id)

    try:
        robot = user.robots.get(pk=robot_id)
    except Robot.DoesNotExist:
        return JsonResponse(request, {"ok": False, "error_message": "Robot not found"})

    if module_id != -1:
        try:
            module = user.modules.get(pk=module_id)
        except UserModule.DoesNotExist:
            return JsonResponse(request, {"ok": False, "error_message": "Module not found"})
    else:
        module = None

    old_module_id = -1
    hull = robot.hull
    hull.load_parameters()

    for slot in hull.slots:
        if slot['id'] == slot_id:
            if not module or slot['slot'] == module.proto.slot:
                if 'module_id' in slot:
                    old_module_id = slot['module_id']
                    if old_module_id != '-1':
                        old_module = user.modules.get(pk=old_module_id)
                        old_module.hull = None
                        old_module.hull_slot_id = -1
                        old_module.save()
                slot['module_id'] = module_id
                if module:
                    module.hull = hull
                    module.hull_slot_id = slot_id
                    module.save()
                hull.save_parameters()
                hull.save()
                break
            else:
                return JsonResponse(request, {"ok": False, "error_message": "You are trying mount <%s> "
                                                                            "module in <%s> slot" %
                                                                            (module.proto.slot, slot['slot'])})
    else:
        return JsonResponse(request, {"ok": False, "error_message": "Slot not found"})

    return JsonResponse(request, {'ok': True, 'unequipped_module': old_module_id})


@transaction.commit_on_success
def give_start_robot_to_user(user):
    hullProto = HullPrototype.objects.get(slug='start')
    hull = Hull()
    hull.proto = hullProto
    hull.parameters = hullProto.parameters

    robot = Robot()
    robot.user = user
    robot.save()

    hull.robot = robot
    hull.save()

    hull.load_parameters()
    for moduleProto in ModulePrototype.objects.filter(category="start").all():
        module = UserModule()
        module.user = user
        module.proto = moduleProto
        module.hull = hull
        slot = None
        for slot in hull.slots:
            if moduleProto.slot == slot['slot'] and 'module_id' not in slot:
                module.hull_slot_id = slot['id']
                break
        module.save()
        if slot:
            slot['module_id'] = module.id
    hull.save_parameters()
    hull.save()


@transaction.commit_on_success
def login(request):
    ok, values = get_request_values(request, "token", "provider")
    if not ok:
        return JsonResponse(request, {"ok": False, "error_message": "Request should contain `token` and "
                                                                    "`provider` fields"})

    token, provider = values

    users = User.objects.filter(token=token).filter(provider=provider).all()
    create_new_robot = False
    if users:
        user = users[0]
    else:
        user = User()
        user.token = token
        user.provider = provider
        create_new_robot = True
    user.is_online = True
    user.login_date = datetime.datetime.now()
    user.save()
    if create_new_robot:
        give_start_robot_to_user(user)
    request.session["user_id"] = user.id
    request.session["is_authorized"] = True
    return JsonResponse(request, {'granted': True})


def logout(request):
    if not is_authorized(request):
        return JsonResponse(request, {"ok": False, "error_message": "Not authorized"})
    request.session["is_authorized"] = False
    return JsonResponse(request, {"ok": True})
