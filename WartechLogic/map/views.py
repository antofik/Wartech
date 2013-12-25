# coding=utf-8
from django.db import transaction
from django.http import HttpResponse
import json
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import Q
from models import *
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


def generate_map(sx, sy):
    """
    sx,sy=0..999
    """
    print sx, sy
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
        height = 8

    heights = str(height) * 10000
    map = material * 10000

    for x in xrange(10):
        for y in xrange(10):
            point = (sx*10 + x) * 1000000 + (sy*10 + y)
            MapTile(point=point, type=4, data=map, heights=heights).save()


def get_map(sx, sy):
    """
    x=0..9999, y=0.9999
    result contain 100x100 cells
    """
    point = sx * 1000000 + sy
    m = MapTile.objects.get(Q(point=point), Q(type=4))
    if not m:
        generate_map(sx//10, sy//10)
        m = MapTile.objects.get(Q(point=point), Q(type=4))
    return m.data


def get(request):
    sx = int(request.GET.get('x', 0)) * 100
    sy = int(request.GET.get('y', 0)) * 100

    im = Image.open("media/images/map.png")
    pixels = im.load()
    data = []
    width, height = 100, 100
    for x in xrange(width):
        l = []
        for y in xrange(height):
            l.append(pixels[sx+x,sy+y])
        data.append(l)
    jsonData = {'map': data}
    return JsonResponse(request, jsonData) #3, 2, 75, 5, 6