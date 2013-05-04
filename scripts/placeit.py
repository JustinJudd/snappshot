import Image
import numpy
import argparse
from lxml import etree
import tarfile


def find_coeffs(pa, pb):
    matrix = []
    for p1, p2 in zip(pa, pb):
        matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
        matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])

    A = numpy.matrix(matrix, dtype=numpy.float)
    B = numpy.array(pb).reshape(8)

    res = numpy.dot(numpy.linalg.inv(A.T * A) * A.T, B)
    return numpy.array(res).reshape(8)


def place_image(screenshot_location, background_location, image_placement, device_res):
    return place_image2( Image.open(screenshot_location).convert("RGBA"), Image.open(background_location).convert("RGBA"), image_placement, device_res )


def place_image2(screenshot, background, image_placement, device_res):
    device_points = [(0, 0), (device_res[0], 0), (device_res[0], device_res[1]), (0, device_res[1])]
    coeffs = find_coeffs( image_placement, device_points)
    #print coeffs

    transformed = screenshot.transform( background.size, Image.PERSPECTIVE, coeffs )
    #transformed = transformed.convert('RGBA')

    new_image= Image.composite(transformed, background, transformed)
    return new_image
    


def run():
    placed_image = place_image(screenshot_location, background_location, image_placement, device_res)
    placed_image.save(final_img_location)


def get_string_from_xml_element(element):
    return element.text.split()[0]

def get_int_from_xml_element(element):
    return int( get_string_from_xml_element(element) )

def load_background_xml(background_xml):
    tree = etree.parse(background_xml)
    bg_node = tree.xpath('/background')[0]

    background_location = get_string_from_xml_element(bg_node.xpath('location')[0])
    device_node = bg_node.xpath('device')[0]

    device_res = ( get_int_from_xml_element(device_node.xpath('resolution/width')[0]), get_int_from_xml_element(device_node.xpath('resolution/height')[0]) )
    placement_node = device_node.xpath('placement')[0]
    image_placement = [
                        ( get_int_from_xml_element(placement_node.xpath('top_left_x')[0]), get_int_from_xml_element(placement_node.xpath('top_left_y')[0]) ), 
                        ( get_int_from_xml_element(placement_node.xpath('top_right_x')[0]), get_int_from_xml_element(placement_node.xpath('top_right_y')[0]) ), 
                        ( get_int_from_xml_element(placement_node.xpath('bottom_right_x')[0]), get_int_from_xml_element(placement_node.xpath('bottom_right_y')[0]) ),
                        ( get_int_from_xml_element(placement_node.xpath('bottom_left_x')[0]), get_int_from_xml_element(placement_node.xpath('bottom_left_y')[0]) )
                        ]
    return background_location, device_res, image_placement

def load_background(background_file):
    t = tarfile.open(background_file, 'r:bz2')
    background_location, device_res, image_placement = load_background_xml( t.extractfile('background.xml') )
    
    background = t.extractfile(background_location)
    return background, device_res, image_placement


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Script to place screenshots into an image")
    parser.add_argument("screenshot", help="location of screenshot image to place")

    be_group = parser.add_mutually_exclusive_group()

    #b_group = be_group.add_argument_group('-b','background', nargs=2    )
    be_group.add_argument("-b", "--background",nargs=2, help="location of image to use as background and xml file containing background data")
    #b_group.add_argument("background_xml", help="location of xml file defining background information")

    be_group.add_argument("-t", "--tar_file", action='store', help="location of tar bz2 file containing backgroung data")
    

    parser.add_argument("final", help="location of final created image")

    args = parser.parse_args()
    
    if args.tar_file:
        background, device_res, image_placement = load_background(args.tar_file)
    else:
        background, device_res, image_placement = load_background_xml(args.background[1])
        background = args.background[0]
    
    placed_image = place_image(args.screenshot, background, image_placement , device_res )
    placed_image.save(args.final)


