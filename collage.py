#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Collage

Creates a collage from a collection of images

"""
from PIL import Image


MARGIN_SIZE = 2


def exif_transpose(image):
    """ Transpose Image

    """
    EXIF_ORIENTATION_TAG = 274

    # Check for EXIF data (only present on some files)
    if (
        hasattr(image, "_getexif")
        and isinstance(image._getexif(), dict)
        and EXIF_ORIENTATION_TAG in image._getexif()
    ):
        exif_data = image._getexif()
        orientation = exif_data[EXIF_ORIENTATION_TAG]

        # Handle EXIF Orientation
        if orientation == 1:
            # Normal image - Do nothing
            image_t = image
        elif orientation == 2:
            # Mirror left to right
            image_t = image.transpose(Image.FLIP_LEFT_RIGHT)
        elif orientation == 3:
            # Rotate 180 degrees
            image_t = image.rotate(180)
        elif orientation == 4:
            # Mirror top to bottom
            image_t = image.rotate(180).transpose(Image.FLIP_LEFT_RIGHT)
        elif orientation == 5:
            # Mirror along top-left diagonal
            image_t = image.rotate(-90, expand=True).transpose(
                Image.FLIP_LEFT_RIGHT
            )
        elif orientation == 6:
            # Rotate 90 degrees
            image_t = image.rotate(-90, expand=True)
        elif orientation == 7:
            # Mirror along top-right diagonal
            image_t = image.rotate(90, expand=True).transpose(
                Image.FLIP_LEFT_RIGHT
            )
        elif orientation == 8:
            # Rotate 270 degrees
            image_t = image.rotate(90, expand=True)

    else:
        # EXIF data not present, just use the original image
        image_t = image

    return image_t


def make_collage(images, width, init_height):
    """ Make collage
        
    """
    if not images:
        print('No images for collage found!')
        return False

    # run until a suitable arrangement of images is found
    while True:
        x = 0

        # copy images to images_list
        images_list = images[:]
        coefs_lines = []
        images_line = []

        while images_list:
            # get first image 
            img_path = images_list.pop(0)

            # open image 
            try:
                img = Image.open(img_path)
            except:
                print("[ERROR] {}".format(img_path))
                continue

            # rotate image if needed
            img = exif_transpose(img)

            # resize to `init_height`
            img.thumbnail((width, init_height))
            
            # when `x` will go beyond the `width`, start the next line
            if x > width:
                coefs_lines.append((float(x) / width, images_line))
                images_line = []
                x = 0
            x += img.size[0] + MARGIN_SIZE
            images_line.append(img_path)
            

        # finally add the last line with images
        coefs_lines.append((float(x) / width, images_line))

        # compact the lines, by reducing the `init_height`, if any with one or less images
        if len(coefs_lines) <= 1:
            break

        if any(map(lambda c: len(c[1]) <= 1, coefs_lines)):
            # reduce `init_height`
            init_height -= 10
        else:
            break

    # get output height
    out_height = 0
    for coef, imgs_line in coefs_lines:
        if imgs_line:
            out_height += int(init_height / coef) + MARGIN_SIZE
    
    if not out_height:
        print('Height of collage could not be 0!')
        return False

    collage_image = Image.new('RGB', (width, int(out_height)), (35, 35, 35))
    
    # add images to the collage
    y = 0
    cnt = 0
    for coef, imgs_line in coefs_lines:
        if imgs_line:
            x = 0
            for img_path in imgs_line:
                img = Image.open(img_path)
                img = exif_transpose(img)

                # if need to enlarge an image, use `resize`
                # otherwise use `thumbnail` because it's faster
                k = (init_height / coef) / img.size[1]
                if k > 1:
                    img = img.resize((int(img.size[0] * k), int(img.size[1] * k)), Image.LANCZOS)
                else:
                    img.thumbnail((int(width / coef), int(init_height / coef)), Image.LANCZOS)
    
                if collage_image:
                    collage_image.paste(img, (int(x), int(y)))

                x += img.size[0] + MARGIN_SIZE
                cnt += 1

            y += int(init_height / coef) + MARGIN_SIZE
    
    print("{} photos used".format(cnt))

    return collage_image
    

if __name__ == "__main__":
    import argparse
    import os
    import random

    # prepare argument parser
    parse = argparse.ArgumentParser(description='Photo collage maker')
    parse.add_argument('-f', '--folder', dest='image_folder', help='folder with images (*.jpg, *.jpeg, *.png)', default='.')
    parse.add_argument('-o', '--output', dest='output', help='output collage image filename', default='collage.jpg')
    parse.add_argument('-w', '--collage_width', dest='collage_width', type=int, help='collage image width (px)')
    parse.add_argument('-i', '--image_height', dest='image_height', type=int, help='individual image height (px)')
    parse.add_argument('-s', '--shuffle', action='store_true', dest='shuffle', help='shuffle images')
    parse.add_argument('-g', '--greyscale', action='store_true', dest='greyscale', help='greyscale')

    args = parse.parse_args()
    if not args.collage_width or not args.image_height:
        parse.print_help()
        exit(1)

    # get images
    files = [os.path.join(args.image_folder, fn) for fn in os.listdir(args.image_folder)]
    img_list = [fn for fn in files if os.path.splitext(fn)[1].lower() in ('.jpg', '.jpeg', '.png')]
    if not img_list:
        print('No images for making collage! Please select another folder with images!')
        exit(1)

    # shuffle images if needed
    if args.shuffle:
        random.shuffle(img_list)

    # make collage
    print('Making collage...')
    collage = make_collage(img_list, args.collage_width, args.image_height)
    if not collage:
        print('Failed to create collage!')
        exit(1)

    # convert to grayscale
    if args.greyscale:
        collage = collage.convert('L')
    
    # save collage
    collage.save(args.output)
    print('Collage complete!')
