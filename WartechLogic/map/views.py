# coding=utf-8
from django.db import transaction
from django.http import HttpResponse
import json
from django.template import RequestContext
from django.shortcuts import render_to_response
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

def get(request, sx, sy):
    sx = int(sx)
    sy = int(sy)
    if sx > 9: sx = 9
    if sy > 9: sy = 9
    sx *= 100
    sy *= 100
    print sx, sy

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
