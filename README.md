# Snappshot

Merge app screenshots with a background image.

Snappshot takes your screenshots and generates photos showcasing your app in action. It is designed as an open source alternative to [Placeit.](http://placeit.breezi.com/) I thought the concept was great, but was dissapointed by the selection and that some of the images were incorrect or placed the screenshots incorrectly. I created Snappshot so that the community can add background images and correct the placement of screenshots on the backgrounds if needed.


## Modes
Snappshot has two modes that it can be used in. Both modes require Python and PIL.

### Standalone
I have created standalone scripts that can be run to place a screenshot into an image.

	python scripts/placeit.py --background \[background_image_location\] \[background_image_xml\] \[output_image\]

### Website
I have created a django app for Snappshot. The following steps are needed to prepare and run the django app.
1. Prepare the available background images for the site

	python scripts/prepare_images.py photos/ snappshot/static/images/backgrounds_test/
2. Update the django app settings
3. Run the django app

	python manage.py runserver 0.0.0.0:\[port\]