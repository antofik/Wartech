import json
from django.db.models import *


class ModelWithParameters(object):
    def __init__(self):
        self.loaded = False

    def load_parameters(self):
        if not self.loaded:
            self.loaded = True
            if self.parameters:
                self._parameters = json.loads(self.parameters)
            else:
                self._parameters = {}
        for key in self._parameters:
            setattr(self, key, self._parameters[key])

    def save_parameters(self):
        if not self.loaded:
            return
        for key in self._parameters:
            self._parameters[key] = getattr(self, key)
        self.parameters = json.dumps(self._parameters)


class User(Model):
    id = AutoField(primary_key=True)
    name = CharField(max_length=64)
    provider = CharField(max_length=64)
    token = CharField(max_length=256)
    sig = CharField(max_length=256)
    is_online = BooleanField()
    login_date = DateField()


class Robot(Model):
    id = AutoField(primary_key=True)
    user = ForeignKey(User, related_name="robots")
    name = CharField(max_length=128)
    description = TextField()


class HullPrototype(Model, ModelWithParameters):
    id = AutoField(primary_key=True)
    slug = SlugField()
    name = CharField(max_length=50)
    description = TextField()
    parameters = TextField()
    slots = None


class ModulePrototype(Model, ModelWithParameters):
    id = AutoField(primary_key=True)
    slug = SlugField()
    name = CharField(max_length=50)
    slot = CharField(max_length=50)
    priority = IntegerField(default=0)
    category = CharField(max_length=50)
    description = TextField()
    parameters = TextField()


class Hull(Model, ModelWithParameters):
    id = AutoField(primary_key=True)
    proto = ForeignKey(HullPrototype, related_name="hull")
    robot = OneToOneField(Robot, related_name="hull")
    parameters = TextField()
    slots = None


class UserModule(Model, ModelWithParameters):
    id = AutoField(primary_key=True)
    user = ForeignKey(User, related_name="modules")
    proto = ForeignKey(ModulePrototype, related_name="proto")
    hull = ForeignKey(Hull, null=True, related_name="modules")
    hull_slot_id = IntegerField()
    parameters = TextField()
