
from curses import KEY_MAX
import math

from PIL import Image as Image

# NO ADDITIONAL IMPORTS ALLOWED!

def set_pixel(image, c):
    image['pixels'].append(c)


def apply_per_pixel(image, func):
    result = {
        'height': image['height'],
        'width': image['width'],
        'pixels': [],
    }
    for y in range(image['height']):
        for x in range(image['width']):
            color = image['pixels'][y*image['width'] + x]
            newcolor = func(color)
            set_pixel(result, newcolor)
    return result


def inverted(image):
    return apply_per_pixel(image, lambda c: 255-c)


# HELPER FUNCTIONS

def get_pixel(image, x, y, boundary_behavior):
    if 0 <= x < (image['height']) and 0 <= y < (image['width']):
        return image['pixels'][x*image['width'] + y]
    else:
        if boundary_behavior == 'zero':
            return 0
        if boundary_behavior == 'extend':
            if x < 0:
                x = 0
            elif x >= image['height']:
                x = image['height'] - 1
            if y < 0:
                y = 0
            elif y >= image['width']:
                y = image['width'] - 1
            return image['pixels'][x*image['width'] + y]
        if boundary_behavior == 'wrap':
            if x < 0:
                if abs(x) <= image['height']:
                    x += image['height']
                else:
                    x += (x % image['height']) + image['height']
            elif x >= image['height']:
                if x - image['height'] >= 0:
                    x -= image['height']
                else:
                    x -= (x % image['height']) + image['height']
            if y < 0:
                if abs(y) <= image['width']:
                    y += image['width']
                else:
                    y += (y % image['width']) + image['width']
            elif y >= image['width']:
                if y - image['width'] <= image['width']:
                    y -= image['width']
                else:
                    y -= (y % image['width']) + image['width']
            return image['pixels'][x*image['width'] + y]        
             
def applykernel(image, x, y, boundary_behavior, kernel):
    pixel = 0
    h = int(len(kernel) ** (1/2))
    w = int(len(kernel) ** (1/2))
    for i in range(x-(h//2), x + (h//2) + 1):
        for j in range(y - (w//2), y + (w//2) + 1):
            kx = i - x+(h//2)
            ky = j - y +(w//2)
            pixel += get_pixel(image, i, j, boundary_behavior) * kernel[kx*w + ky]
    return pixel

def correlate(image, kernel, boundary_behavior):
    """
    Compute the result of correlating the given image with the given kernel.
    `boundary_behavior` will one of the strings 'zero', 'extend', or 'wrap',
    and this function will treat out-of-bounds pixels as having the value zero,
    the value of the nearest edge, or the value wrapped around the other edge
    of the image, respectively.

    if boundary_behavior is not one of 'zero', 'extend', or 'wrap', return
    None.

    Otherwise, the output of this function should have the same form as a 6.101
    image (a dictionary with 'height', 'width', and 'pixels' keys), but its
    pixel values do not necessarily need to be in the range [0,255], nor do
    they need to be integers (they should not be clipped or rounded at all).

    This process should not mutate the input image; rather, it should create a
    separate structure to represent the output.

    Kernels are represented by 2D lists, with sub-list in the list representing a row.
    """
    if boundary_behavior == 'zero' or boundary_behavior == 'extend' or boundary_behavior == 'wrap':
        new_pixels = []
        for x in range(image['height']):
            for y in range(image['width']):
                new_pixels.append(applykernel(image, x, y, boundary_behavior, kernel))
        return {'height': image['height'], 'width': image['width'], 'pixels': new_pixels}
    else:
        return None


def round_and_clip_image(image):
    """
    Given a dictionary, ensure that the values in the 'pixels' list are all
    integers in the range [0, 255].

    All values should be converted to integers using Python's `round` function.

    Any locations with values higher than 255 in the input should have value
    255 in the output; and any locations with values lower than 0 in the input
    should have value 0 in the output.
    """
    for i in range(len(image['pixels'])):
        if image['pixels'][i] < 0:
            image['pixels'][i] = 0
        elif image['pixels'][i] > 255:
            image['pixels'][i] = 255
        else:
            image['pixels'][i] = round(image['pixels'][i])
    return image


# FILTERS
def get_blur_kern(n):
    value = 1/(n*n)
    kernel = []
    for i in range(n*n):
        kernel.append(value)
    return kernel

def blurred(image, n):
    """
    Return a new image representing the result of applying a box blur (with
    kernel size n) to the given input image.

    This process should not mutate the input image; rather, it should create a
    separate structure to represent the output.
    """
    # first, create a representation for the appropriate n-by-n kernel (you may
    # wish to define another helper function for this)
    kernel = get_blur_kern(n)

    # then compute the correlation of the input image with that kernel
    new_image = correlate(image, kernel, 'extend')

    # and, finally, make sure that the output is a valid image (using the
    # helper function from above) before returning it.
    return round_and_clip_image(new_image)

def sharpened(image, n):
    blurred_image = blurred(image, n)
    sharpened_pixels = []
    for i in range(len(image['pixels'])):
        sharpened_pixels.append((image['pixels'][i]*2) - blurred_image['pixels'][i])
    sharpened_image = {'height': image['height'], 'width': image['width'], 'pixels': sharpened_pixels}
    return round_and_clip_image(sharpened_image)


def edges(image):
    kernel_x = [-1, 0, 1, -2, 0, 2, -1, 0, 1]
    kernel_y = [-1, -2, -1, 0, 0, 0, 1, 2, 1]
    image_x = correlate(image, kernel_x, 'extend')
    image_y = correlate(image, kernel_y, 'extend')
    edges_pixels = []
    for i in range(len(image['pixels'])):
        a = image_x['pixels'][i] ** 2
        b = image_y['pixels'][i] ** 2
        pixel = round((a + b)** (1/2))
        edges_pixels.append(pixel)
    new_image = {'height': image['height'], 'width': image['width'], 'pixels': edges_pixels}
    return round_and_clip_image(new_image)


# HELPER FUNCTIONS FOR LOADING AND SAVING IMAGES

def load_greyscale_image(filename):
    """
    Loads an image from the given file and returns a dictionary
    representing that image.  This also performs conversion to greyscale.

    Invoked as, for example:
       i = load_image('test_images/cat.png')
    """
    with open(filename, 'rb') as img_handle:
        img = Image.open(img_handle)
        img_data = img.getdata()
        if img.mode.startswith('RGB'):
            pixels = [round(.299 * p[0] + .587 * p[1] + .114 * p[2])
                      for p in img_data]
        elif img.mode == 'LA':
            pixels = [p[0] for p in img_data]
        elif img.mode == 'L':
            pixels = list(img_data)
        else:
            raise ValueError('Unsupported image mode: %r' % img.mode)
        w, h = img.size
        return {'height': h, 'width': w, 'pixels': pixels}


def save_greyscale_image(image, filename, mode='PNG'):
    """
    Saves the given image to disk or to a file-like object.  If filename is
    given as a string, the file type will be inferred from the given name.  If
    filename is given as a file-like object, the file type will be determined
    by the 'mode' parameter.
    """
    out = Image.new(mode='L', size=(image['width'], image['height']))
    out.putdata(image['pixels'])
    if isinstance(filename, str):
        out.save(filename)
    else:
        out.save(filename, mode)
    out.close()

if __name__ == '__main__':
    # code in this block will only be run when you explicitly run your script,
    # and not when the tests are being run.  this is a good place for
    # generating images, etc.
    python = load_greyscale_image('/Users/natalietang/Downloads/image_processing/test_images/python.png')
    save_greyscale_image(round_and_clip_image(sharpened(python, 11)), 'sharpened_python.png', mode='PNG')
