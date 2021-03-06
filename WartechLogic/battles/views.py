# coding=utf-8
from collections import defaultdict
import random
import json
from datetime import datetime
from django.http import HttpResponse
from logic_modules.eye import *
from main.models import User
from main.views import is_authorized, JsonResponse, get_request_values


def get_value(request, key, default_value):
    ok, values = get_request_values(request, key)
    if ok:
        return values[0]
    return default_value


def test_fight(request):
    if not is_authorized(request):
        return JsonResponse(request, {"ok": False, "error_reason": "Not authorized"})

    user = User.objects.get(pk=request.session["user_id"])
    robots = list(user.robots.all()) * int(get_value(request, 'count', 1))
    arena = Arena.objects.get(slug=get_value(request, 'arena', 'small'))
    fight_result = fight(arena, *([robots] * int(get_value(request, "team_count", 2))))
    journal = fight_result['journal']
    final = fight_result['final_message']

    ok, _ = get_request_values(request, "journal")
    if ok:
        return JsonResponse(request, fight_result['fight_journal'])

    ok, _ = get_request_values(request, 'human')
    if ok:
        return HttpResponse(
            ("<!DOCTYPE html><html><body><div style='color: blue;'>%s</div><br/><pre>%s</pre></body</html>" %
             (final, json.dumps(journal)))
            .replace("{", "\r\n{")
            .replace("}],", "}],\r\n\r\n")
            .replace('\n{"', '\n    {"')
        )
    return JsonResponse(request, {
        "ok": True,
        "journal": journal,
        "final_message": final,
        "time_elapsed": fight_result["time_elapsed"],
        "arena": {
            'width': arena.width,
            'height': arena.height,
            'terrain': json.loads(arena.terrain),
        }
    })


class Battlefield(dict):
    def __init__(self, arena, fight_journal):
        super(Battlefield, self).__init__()
        self.arena = arena
        self.fight_journal = fight_journal
        for i, kind in enumerate(json.loads(arena.terrain)):
            x, y = self.translate_point_to_hexagone(i)
            self[x, y] = kind

    def translate_point_to_hexagone(self, i):
        y, x = divmod(i, self.arena.width)
        x -= y // 2
        return x, y

    def place_fighter_at_random_position(self, fighter):
        counter = 1000
        while counter:
            counter -= 1
            x, y = self.translate_point_to_hexagone(random.randint(0, self.arena.width * self.arena.height - 1))
            if self[x, y] == Arena.EMPTY:
                self[x, y] = fighter
                fighter.set_position(x, y, start=True)
                fighter.set_direction(random.randint(0, 5), start=True)
                self.fight_journal.append("%s placed at (%s, %s)" % (fighter.name, x, y))
                break
        if not counter:
            raise Exception("cannot place fighter: not enough space")

    def get_visual_object_at(self, x, y):
        type = 'error'
        object = None
        if (x, y) in self:
            item = self[x, y]
            object = item
            if isinstance(item, Fighter):
                type = 'fighter'
            elif isinstance(item, int):
                type = 'nature'
        return {'type': type, 'object': object}

    def move_fighter(self, fighter):
        if not fighter.goto:
            return
        dx, dy = fighter.goto['vector']
        direction = fighter.goto['direction']
        fighter.set_direction(direction)
        if dx == dy == 0:
            self.fight_journal.append("%s stays" % fighter.name)
        else:
            x, y = fighter.x + dx, fighter.y + dy
            if (x, y) in self and self[x, y] == Arena.EMPTY:
                self.fight_journal.append("%s moving (%s, %s) at (%s, %s)" % (fighter.name, dx, dy, x, y))
                self[fighter.x, fighter.y] = Arena.EMPTY
                self[x, y] = fighter
                fighter.set_position(x, y)
            else:
                self.fight_journal.append("%s fails to move (%s, %s)" % (fighter.name, dx, dy))

    def remove_fighter(self, fighter):
        self[fighter.x, fighter.y] = Arena.EMPTY
        fighter.remove()


class Fighter(object):
    def __init__(self, robot, teamid, journal=None):
        self.tick = 0
        self.robot = robot
        self.teamid = teamid
        self.journal = journal
        slots = defaultdict(list)
        for module in self.robot.hull.modules.all():
            slots[module.proto.slot].append(module)
        self.slots = slots
        self.sensors = [m for m in [SensorWrapper.create(self, module) for module in slots['sensor']] if m]
        self.sensors.sort(key=lambda item: item.priority)
        self.analyzers = [m for m in [AnalyzerWrapper.create(self, module) for module in slots['analyzer']] if m]
        self.analyzers.sort(key=lambda item: item.priority)
        self.weapon_analyzers = [m for m in
                                 [AnalyzerWrapper.create(self, module) for module in slots['weapon_analyzer']] if m]
        self.weapon_analyzers.sort(key=lambda item: item.priority)
        self.decision = DecisionMaker(self, slots['decision'])
        self.motion = MotionWrapper(slots['motion'])
        self.weapon = [m for m in [WeaponModuleWrapper.create(module) for module in slots['weapon']] if m]
        self.health = 100
        self.id = random.randint(100, 999)

        self.log("slots: %s" % self.slots)
        self.log("found sensors: %s" % self.sensors)
        self.log("found analyzers: %s" % self.analyzers)
        self.log("found weapon analyzers: %s" % self.weapon_analyzers)
        self.log("found weapon: %s" % self.weapon)

        self.actions = {
            'name': self.name,
            'teamid': self.teamid,
            'general': [],
            'health': [],
            'movements': [],
            'shoots': [],
        }
        self.tick_actions = defaultdict(list)
        self.action(action='start', team=self.teamid)
        self.action('health', value=self.health)

        for module in slots['sensor']:
            if module.proto.slug == 'eye':
                self.action(action='eye', configuration=json.loads(module.proto.parameters))


    def log(self, message):
        if self.journal:
            self.journal.append("----%s> %s" % (self.name, message))

    def process(self, tick, battlefield):
        self.tick = tick
        data = defaultdict(list)
        for module in self.sensors:
            if module:
                self.log("processing module %s" % module)
                data.update(module.process(battlefield))
        for module in self.analyzers:
            if module:
                self.log("processing analyzer %s" % module)
                data.update(module.process(data))
        for weapon in self.weapon:
            for module in self.weapon_analyzers:
                if module:
                    self.log("processing weapon module %s for weapon %s" % (module, weapon))
                    data.update(module.process(data, weapon, self.log))
        self.log("result visual = %s" % data['visual'])
        self.log("result objects = %s" % data['objects'])
        commands = self.decision.process(data, self.weapon, self.motion, self.log)
        self.goto = commands['goto'] if 'goto' in commands else None

        for shoot in commands['shoot']:
            self.action('shoots', bullet='TODO', target_position=shoot['target_position'])
        return commands['shoot']

    def set_position(self, x, y, start=False):
        self.x, self.y = x, y
        self.action('movements', type='move' if not start else 'start_position', x=self.x, y=self.y)

    def set_direction(self, direction, start=False):
        self.direction = direction
        self.action('movements', type='turn' if not start else 'start_direction', direction=self.direction)

    def remove(self):
        self.action(action='removed')

    def action(self, journal='general', **args):
        d = {'tick': self.tick}
        d.update(args)
        self.actions[journal].append(d)

        d = {'type': journal, 'name': self.name}
        d.update(args)
        self.tick_actions[self.tick].append(d)

    def bullet_hit(self, bullet):
        self.health -= 10
        self.action('health', value=self.health)
        if not self.alive:
            self.action(action='dead')
        return -10

    @property
    def alive(self):
        return self.health > 0

    @property
    def name(self):
        return "R%s.%s" % (self.teamid, self.id)

    @property
    def action_journal(self):
        return self.actions

    @property
    def tick_action_journal(self):
        return self.tick_actions


def aggregate_action_journals(journals):
    journal = {}
    tick = 0
    while True:
        actions = []
        for action_journal in journals:
            name = action_journal['name']
            teamid = action_journal['teamid']
            pass

        if actions:
            journal[tick] = actions
            tick += 1
        else:
            break


def fight(arena, *teams):
    final = ""
    fight_journal = []
    fight_start = datetime.now()
    fight_journal.append("Fight started at %s" % fight_start)

    battlefield = Battlefield(arena, fight_journal)
    fighters = []
    for robots in teams:
        teamid = random.randint(10, 99)
        for robot in robots:
            fighter = Fighter(robot, teamid, fight_journal)
            fighters.append(fighter)

    for fighter in fighters:
        battlefield.place_fighter_at_random_position(fighter)

    all_fighters = list(fighters)

    tick = 0
    idle_counter = 0
    while True:
        tick += 1

        if not fighters:
            fight_journal.append("Fight finished: no more alive fighters found")
            break

        idle = True
        shoots = []
        for fighter in fighters:
            if fighter.alive:
                bullets = fighter.process(tick, battlefield)
                for bullet in bullets:
                    target = bullet['target']
                    fight_journal.append("%s fires at %s" % (fighter.name, target.name))
                shoots.extend(bullets)
        fight_journal.append("Shooting at %s" % shoots)
        for shoot in shoots:
            target_position = shoot['target_position']
            if target_position not in battlefield:
                continue
            target = battlefield[shoot['target_position']]
            if isinstance(target, Fighter):
                idle = False
                idle_counter = 0
                bullet = shoot['bullet']
                hit = target.bullet_hit(bullet)
                fight_journal.append("%s received %s damage" % (target.name, hit))

        alive_teams = set()
        for fighter in list(fighters):
            fight_journal.append("%s has %s health. Alive=%s" % (fighter.name, fighter.health, fighter.alive))
            if fighter.alive:
                alive_teams.add(fighter.teamid)
                battlefield.move_fighter(fighter)
            else:
                fight_journal.append("%s is dead" % fighter.name)
                fighters.remove(fighter)
                battlefield.remove_fighter(fighter)

        if len(alive_teams) == 0:
            final = "Fight finished: all are dead"
            fight_journal.append(final)
            break
        elif len(alive_teams) == 1:
            final = "Fight finished: team %s is winner. Alive: %s. Dead: %s" % \
                    (
                        alive_teams.pop(),
                        ",".join([f.name for f in all_fighters if f.alive]),
                        ",".join([f.name for f in all_fighters if not f.alive]),
                    )
            fight_journal.append(final)
            break

        if idle:
            idle_counter += 1
        if idle_counter > 100:
            final = "Fight finished: 100 cycles without shooting&hitting. It's really boring"
            fight_journal.append(final)
            break

        if (datetime.now() - fight_start).total_seconds() > 3:
            final = "Fight finished: exceeded time limit"
            fight_journal.append(final)
            break

    max_tick = tick
    journals = [fighter.tick_action_journal for fighter in all_fighters]
    result = {}
    for tick in xrange(max_tick + 1):
        result[tick] = []
        for journal in journals:
            if tick in journal:
                for item in journal[tick]:
                    result[tick].append(item)
    return {
        'final_message': final,
        'journal': result,
        'time_elapsed': (datetime.now() - fight_start).total_seconds(),
        'fight_journal': {fighter.name:fighter.action_journal for fighter in all_fighters},
    }

