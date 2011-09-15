# encoding: utf-8
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.core import serializers
from django.conf import settings

from lightwrite.texts.models import Text, TextForm

import json
import random
import string 

# Redirect to a random page
# If deploying, make sure you have a REDIR in your local_settings
# TODO: Don't redirect to already taken pads
def root(request):
    wash = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(9))
    return HttpResponseRedirect(settings.REDIR + '/' + wash) 

# The main event
def write(request, wash):
    if request.method == 'POST':
        t = Text.objects.filter(wash=wash)
        if (len(t)==0):
            t = Text(wash=wash)
            t.text = request.POST['writearea']
            t.save() 
            t = Text.objects.filter(wash=wash)
        else:
            t = t[0] 
            t.text = request.POST['writearea']
            t.save() 
            t = Text.objects.filter(wash=wash)
        if 'save' in request.POST:
            return render_to_response('light.html', {'wash': wash,}, context_instance=RequestContext(request))
        else:
            resp = HttpResponse(t[0].text.strip(), mimetype='text/plain')
            resp['Content-Disposition'] = 'attachment; filename=' + wash + '.txt'
            return resp

    return render_to_response('light.html', {'wash': wash,}, context_instance=RequestContext(request))

# Get the text result
def json_get_text(request, wash):
    t = Text.objects.filter(wash=wash)
    if (len(t)==0):
        t = Text(wash=wash)
        t.text = '\n\nWelcome to LightWrite!\nby Gun.io\n\nLightWrite is a web-based clone of WriteRoom - it\'s a place to write your thoughts without any distractions.\n\nTo use LightWrite, just start typing! You can move your mouse over the bottom of the page to save your text online or export to a file. \n\nTo enter fullscreen mode, just press F11, or ⇧⌘F if you\'re using OSX.\n\nEnjoy!\n\nLove,\nTeam Gun.io'
        t.save() 
        t = Text.objects.filter(wash=wash)
    data = serializers.serialize("json", t)
    return HttpResponse(data, mimetype='application/json')

def about(request):
    return render_to_response('about.html')
