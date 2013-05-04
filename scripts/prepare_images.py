import PIL
from PIL import Image, ImageDraw, ImageFont
import argparse
import create_fill_screenshot
import placeit
import os

from lxml import etree


thumbnail_basewidth = 640
full_basewidth = 1920


def update_xml_location(node, location_part, ratio):
    node.xpath(location_part)[0].text = str( int(float(node.xpath(location_part)[0].text) / ratio))

def prepare_images(current_location, new_location):
    # resize images for web, and update device placement coordinates in xml to reflect this
    try:
        os.makedirs( os.path.join(new_location,'thumbnails') )
    except:
        pass
    for i in os.listdir(current_location):
        if 'xml' in i:

            background, device_res, image_placement = placeit.load_background_xml( os.path.join(current_location, i) )
            image_name = i.replace('.xml', '.jpg')

            image = Image.open(current_location+image_name).convert("RGBA")
            #im = prepare_image(image, image_placement, device_res)
            im, resized = resize_image(image, 'full')
            
            if resized:
                ratio = float(image.size[0])/im.size[0]
                tree = etree.parse(os.path.join(current_location,i))
                placement_node = tree.xpath('/background/device/placement')[0]
                update_xml_location(placement_node, 'top_left_x', ratio )
                update_xml_location(placement_node, 'top_left_y', ratio )
                update_xml_location(placement_node, 'top_right_x', ratio )
                update_xml_location(placement_node, 'top_right_y', ratio )
                update_xml_location(placement_node, 'bottom_right_x', ratio )
                update_xml_location(placement_node, 'bottom_right_y', ratio )
                update_xml_location(placement_node, 'bottom_left_x', ratio )
                update_xml_location(placement_node, 'bottom_left_y', ratio )


                tree.write( os.path.join(new_location, i) )
            im.save(os.path.join(new_location,image_name))
            im,_ = resize_image(im, 'thumbnail')
            im.save(os.path.join(new_location,'thumbnails',image_name), "JPEG", optimize=True, progressive=True )

def prepare_image(image, image_placement, device_res):    
    width = device_res[0]
    height = device_res[1]
    PIL.ImageFile.MAXBLOCK = width * height
    screenshot = create_fill_screenshot.create_fill_screenshot(width, height)
    image = placeit.place_image2(screenshot, image, image_placement , device_res )

    return image

def resize_image(image, type="full"):
    if type == 'full':
        basewidth = full_basewidth
    else:
        basewidth = thumbnail_basewidth
    if basewidth > image.size[0]:
        return image, False

    wpercent = (basewidth / float(image.size[0]))
    hsize = int((float(image.size[1]) * float(wpercent)))
    return image.resize((basewidth, hsize), PIL.Image.ANTIALIAS), True



if __name__ == "__main__":
    parser = argparse.ArgumentParser("Script to prepare background images for web service")
    parser.add_argument("bg_location", help="location of background images to be prepared for the web service")
    parser.add_argument("web_background_location", help="location of where the web service expects background images")

    args = parser.parse_args()
    
    
    prepare_images(args.bg_location, args.web_background_location)
    #image.save(args.output)