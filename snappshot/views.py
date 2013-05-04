# Create your views here.
from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django.http import Http404
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

from scripts import placeit, create_fill_screenshot

import Image
import time
import os


#Check how many background images are available
def get_image_range():
    return range(1,len([f for f in os.listdir(settings.STATICFILES_DIRS[0] +"/images/backgrounds/")  if f.endswith('.jpg') and os.path.isfile(os.path.join(settings.STATICFILES_DIRS[0] +"/images/backgrounds/", f))]) +1)


def index(request):
    #return render_to_response('index.j2', {'image_range': get_image_range() }, context_instance=RequestContext(request))
    #Redirect to upload page of first image
    return redirect(reverse('upload', args=(1,)))

def faq(request):
    return render_to_response('faq.j2', {'image_range': get_image_range() }, context_instance=RequestContext(request))


def upload_screenshot(request, image_id):
    try:
        background, device_res, image_placement = placeit.load_background_xml(settings.STATICFILES_DIRS[0] +"/images/backgrounds/"+str(image_id)+".xml")
    except Exception as e:
        print e 
        raise Http404
    #print device_res
    return render_to_response('upload.j2', {'image_id': image_id, 'image_range': get_image_range(), 'width':device_res[0], 'height':device_res[1]}, context_instance=RequestContext(request))

def uploaded_screenshot(request, image_id):
    if request.method == 'POST':
        s_image = Image.open(request.FILES['file_input']).convert("RGBA")
        background, device_res, image_placement = placeit.load_background_xml(settings.STATICFILES_DIRS[0] +"/images/backgrounds/"+str(image_id)+".xml")
        b_image = Image.open(settings.STATICFILES_DIRS[0] +"/images/backgrounds/"+str(image_id)+".jpg").convert("RGBA")
        placed_image = placeit.place_image2(s_image, b_image, image_placement , device_res )

        image_id = int( time.time() )
        placed_image.save(settings.GENERATED_IMAGES_DIR + str(image_id) + ".jpg")
    else:
        #Screenshot not submitted - redirect to page for same background where user can upload screenshot
        return redirect(reverse('upload', args=(image_id,)))

    return render_to_response('finished_image.j2', {'image_id': image_id, 'image_range': get_image_range()}, context_instance=RequestContext(request))

#return "placed" image 
def get_image(request, image_id):
    try:
        image_data = open(settings.GENERATED_IMAGES_DIR + str(image_id) + ".jpg", "rb").read()
        return HttpResponse(image_data, mimetype="image/jpg")
    except:
        raise Http404

def get_screenshot(request,width, height):
    try:
        image_data = create_fill_screenshot.create_fill_screenshot(int(width),int(height))
        response = HttpResponse(mimetype="image/jpg")
        image_data.save(response, "JPEG", optimize=True, progressive=True)
        return response
    except Exception as e:
        print 'exception', e
        raise Http404    
