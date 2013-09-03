from django.db.models import *


class Arena(Model):
    EMPTY = 0
    UNPASSABLE = 1

    id = AutoField(primary_key=True)
    width = IntegerField()
    height = IntegerField()
    terrain = TextField()
    slug = CharField(max_length=50)
