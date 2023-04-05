# Collage

Creates a collage from a collection of images. Automatically rotates images based on EXIF data.

## Setup
Create [virtual environment](https://realpython.com/python-virtual-environments-a-primer/) and install requirements:
```shell
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage:
```shell
./collage.py
usage: collage.py [-h] [-f IMAGE_FOLDER] [-o OUTPUT] [-w COLLAGE_WIDTH] [-i IMAGE_HEIGHT] [-s] [-g]

Photo collage maker

options:
  -h, --help            show this help message and exit
  -f IMAGE_FOLDER, --folder IMAGE_FOLDER
                        folder with images (*.jpg, *.jpeg, *.png)
  -o OUTPUT, --output OUTPUT
                        output collage image filename
  -w COLLAGE_WIDTH, --collage_width COLLAGE_WIDTH
                        collage image width (px)
  -i IMAGE_HEIGHT, --image_height IMAGE_HEIGHT
                        individual image height (px)
  -s, --shuffle         shuffle images
  -g, --greyscale       greyscale
```

Quickstart:
```shell
./collage.py -f images/ -w 2478 -i 80 -s
```