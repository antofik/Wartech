# coding=utf-8
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, Http404, redirect
from django.views.decorators.csrf import csrf_exempt


def default(request):
    return render_to_response('configurator.html', {}, context_instance=RequestContext(request))