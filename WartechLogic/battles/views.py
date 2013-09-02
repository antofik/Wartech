# coding=utf-8
from collections import defaultdict
import random
import json
from models import *
from ..main.views import is_authorized, JsonResponse


def test_fight(request):
    if not is_authorized(request):
        return JsonResponse(request, {"ok": False, "error_reason": "Not authorized"})

    user = User.objects.get(pk=request.session["user_id"])
    robots = user.robots.all()
    arena = Arena.objects.all()[0]
    fight(robots, robots, arena)
    return JsonResponse(request, {"ok": True})


class Battlefield(dict):
    def __init__(self, arena):
        super(Battlefield, self).__init__()
        self.arena = arena
        for i, kind in enumerate(json.loads(arena.terrain)):
            x, y = self.translate_point_to_hexagone(i)
            self[x, y] = kind

    def translate_point_to_hexagone(self, i):
        x, y = divmod(i, self.arena.width)
        y = -(y//2)
        return x, y

    def place_fighter_at_random_position(self, fighter):
        counter = 1000
        while counter:
            counter -= 1
            x, y = self.translate_point_to_hexagone(random.randint(0, len(self.arena) - 1))
            if self[x, y] == Arena.EMPTY:
                self[x, y] = fighter
                fighter.x, fighter.y = x, y
                break
        if not counter:
            raise Exception("cannot place fighter: not enough space")


class Fighter(object):
    def __init__(self, robot):
        self.robot = robot
        slots = defaultdict(list)
        for module in self.robot.hull.modules:
            slots[module.proto.slot].append(module)
        self.slots = slots
        self.sensors = slots['sensor']
        self.analyzers = slots['analyzer']
        self.decision = slots['decision']
        self.motion = slots['motion']
        self.weapon = slots['weapon']

    def process(self, battlefield):
        data = defaultdict(list)
        for module in self.sensors:
            sensor_data = module.process(battlefield, self)
            for result_type in sensor_data:
                data[result_type].append(sensor_data[result_type])
        for module in self.slots['logic']:
            data['sensor'].append(module.process(battlefield))


def fight(arena, *teams):
    battlefield = Battlefield(arena)
    fighters = []
    for robots in teams:
        for robot in robots:
            fighter = Fighter(robot)
            fighters.append(fighter)

    for fighter in fighters:
        battlefield.place_fighter_at_random_position(fighter)

    counter = 0
    while True:
        demage = False
        for fighter in fighters:
            fighter.process(battlefield)
        if not demage:
            counter += 1
        if counter > 100:
            break

