# coding=utf-8
from django.db import transaction
from django.http import HttpResponse
import json
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import Q
from models import *
from random import randint
from PIL import Image


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
    if request.method == "OPTIONS":
        response["Access-Control-Allow-Headers"] = "origin, content-type, x-requested-with, accept, authorization"
    return response


def create_roughness(heights):
    for i in xrange(len(heights)):
        r = randint(0, 20)
        if r > 19:
            heights[i] += 3
        elif r > 18:
            heights[i] -= 3
        elif r > 16:
            heights[i] += 2
        elif r > 14:
            heights[i] -= 2
        elif r > 11:
            heights[i] += 1
        elif r > 8:
            heights[i] -= 1
        heights[i] = max(0, min(7, heights[i]))
    for x in xrange(1,99):
        for y in xrange(1,99):
            heights[y*100+x] = (heights[y*100+x] + heights[y*100+x+1] + heights[y*100+x-1] + heights[y*100+x+100] + heights[y*100+x-100])/5


def create_mountains(heights):
    def coordinates(width=0):
        return randint(width, 99-width), randint(width, 99-width)

    for i in xrange(randint(0, 100)):
        x, y = coordinates()


def create_ravines(heights):
    pass


def generate_map(sx, sy):
    """
    sx,sy=0..999
    """
    sx, sy = int(sx), int(sy)
    im = Image.open("media/images/map.png")
    pixels = im.load()
    pixel = pixels[sx, sy]

    material = Materials.Water
    height = 0
    if pixel == 75:
        material = Materials.Water
        height = 0
    elif pixel == 2:
        material = Materials.Soil
        height = 2
    elif pixel == 3:
        material = Materials.Soil
        height = 4
    elif pixel == 5:
        material = Materials.Soil
        height = 6
    elif pixel == 6:
        material = Materials.Soil
        height = 7

    m = [material] * 10000

    for x in xrange(10):
        for y in xrange(10):
            point = (sx*10 + x) * 1000000 + (sy*10 + y)
            heights = [height] * 10000
            if material == Materials.Soil:
                create_roughness(heights)
                create_mountains(heights)
                create_ravines(heights)
            elif material == Materials.Rock:
                create_roughness(heights)
                create_mountains(heights)
            elif material == Materials.Sand:
                create_roughness(heights)

            m = ''.join(m)
            heights = ''.join(map(str, heights))
            MapTile(point=point, type=4, data=m, heights=heights).save()


def get_map(sx, sy):
    """
    x=0..9999, y=0.9999
    result contain 100x100 cells
    """
    point = sx * 1000000 + sy
    try:
        m = MapTile.objects.get(Q(point=point), Q(type=4))
    except MapTile.DoesNotExist:
        generate_map(sx//10, sy//10)
        m = MapTile.objects.get(Q(point=point), Q(type=4))
    return m


def get(request):
    sx = int(request.GET.get('x', 0))
    sy = int(request.GET.get('y', 0))

    map = get_map(sx, sy)

    jsonData = {'map': map.data, 'heights': map.heights}
    return JsonResponse(request, jsonData) #3, 2, 75, 5, 6
