from django.db.models import *


class Session(Model):
    id = AutoField(primary_key=True)
    session_id = CharField(max_length=256)


class User(Model):
    id = AutoField(primary_key=True)
    name = CharField(max_length=64)
    provider = CharField(max_length=64)
    token = CharField(max_length=256)
    sig = CharField(max_length=256)
    session = ForeignKey(Session, related_name="user")
    is_online = BooleanField()
    login_date = DateField()


class Robot(Model):
    id = AutoField(primary_key=True)
    user = ForeignKey(User, related_name="robots")
    hull = OneToOneField(Hull)


class HullPrototype(Model):
    id = AutoField(primary_key=True)
    slug = SlugField()
    name = CharField(max_length=50)
    description = TextField()
    parameters = TextField()


class ModulePrototype(Model):
    id = AutoField(primary_key=True)
    slug = SlugField()
    name = CharField(max_length=50)
    slot = CharField(max_length=50)
    category = CharField(max_length=50)
    description = TextField()
    parameters = TextField()


class Hull(Model):
    id = AutoField(primary_key=True)
    proto = OneToOneField(HullPrototype, related_name="proto")
    parameters = TextField()


class UserModule(Model):
    id = AutoField(primary_key=True)
    user = ForeignKey(User, related_name="modules")
    proto = OneToOneField(ModulePrototype, related_name="proto")
    hull = ForeignKey(Hull, related_name="equipped_modules")
    hull_slot_id = IntegerField()
    parameters = TextField()
