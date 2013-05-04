from PIL import Image, ImageDraw, ImageFont
import argparse


def create_fill_screenshot(width, height, fontfile="/usr/share/fonts/truetype/ubuntu-font-family/Ubuntu-R.ttf" ):

	im = Image.new('RGBA', (width, height), (0, 0, 0, 0)) 
	draw = ImageDraw.Draw(im) 


	draw.rectangle((0, 0, width, height), fill="darkgray")
	font = ImageFont.truetype(fontfile, width/10)
	message = str(width)+'x'+str(height)
	w, h = draw.textsize(message)
	draw.text(((width-w)/4,(height-h)/2), message, font=font)
	return im

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Script to prepare screenshot image for device resolution")
    parser.add_argument("width", type=int,  help="width of device")
    parser.add_argument("height", type=int, help="height of device")
    #parser.add_argument("-f", "--fontfile",  help="increase output verbosity")
    parser.add_argument("output", help="location of created screnshot fill image")

    args = parser.parse_args()
    
    
    image = create_fill_screenshot(args.width, args.height)
    image.save(args.output)