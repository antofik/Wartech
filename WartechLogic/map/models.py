from django.db.models import *
import json


class MapTile(Model):
    id = AutoField( primary_key=True)
    ready_level = PositiveSmallIntegerField()
    type = PositiveSmallIntegerField()
    point = BigIntegerField()
    data = TextField()


class ChemicalElements(object):
    Ar = 0
    Fe = 1
    Lu = 2
    Rz = 3
    Es = 4
    Uq = 5
    Io = 7
    Bi = 8
    Ya = 9
    Ze = 10
    Xj = 11


class Material(object):
    Table = {}

    def __init__(self, name, state, substate, *elements):
        self.State = state
        self.Substate = substate
        self.Elements = elements
        self.Name = name
        self.ChemicalName = self.get_name()
        Material.Table[self.Name] = self

    def get_name(self):
        name = ''.join(['%s%s' for (el, n) in self.Elements])
        return '%s-%s-%s' % (name, self.State, self.Substate)

    def __str__(self):
        return self.Name

    @classmethod
    def register(cls, name, Material):
        print 'registering', name
        setattr(cls, name, Material)

    @staticmethod
    def get(name, chemicalName=None):
        if name in Material.Table:
            return Material.Table[name]
        #todo
        #state, substate, elements = Material.parse_chemical_name(chemicalName)
        #material = Material(name, )
        return Material.Table[Materials.Water]

    @staticmethod
    def parse_chemical_name(name):
        #todo
        return None, None, None


class MaterialState(object):
    Liquid = 0
    Dry = 1
    Solid = 2


class MaterialSubstate(object):
    Soft = 0
    Hard = 1


class Materials(object):
    Water = "Water"
    Rock = "Rock"
    Sand = "Sand"
    Soil = "Soil"

_ = ChemicalElements
Material.register(Materials.Water, Material(MaterialState.Liquid, MaterialSubstate.Soft, (_.Ar, 2), (_.Lu, 1)))
Material.register(Materials.Rock, Material(MaterialState.Solid, MaterialSubstate.Hard, (_.Fe, 5), (_.Lu, 1), (_.Es, 2)))
Material.register(Materials.Sand, Material(MaterialState.Dry, MaterialSubstate.Soft, (_.Ar, 1), (_.Es, 1), (_.Rz, 2)))
Material.register(Materials.Soil, Material(MaterialState.Dry, MaterialSubstate.Hard, (_.Ar, 1), (_.Lu, 2), (_.Fe, 2), (_.Rz, 1), (_.Es, 1)))


class MapCell(object):
    def __init__(self, x, y, height, material_name):
        self.X = x
        self.Y = y
        self.Height = height
        self.Material = Material.get(material_name)

    @staticmethod
    def parse(x, y, json_value):
        values = json.loads(json_value)
        cell = MapCell(x,y, values['height'], values['material_name'])
        return cell

    def json(self):
        return '{height:%s,material_name:%s}' % (self.X, self.Y, self.Height, self.Material.Name)

