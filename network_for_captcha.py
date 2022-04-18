#!/usr/bin/python
# For the Faster r-cnn model and the tests on downloaded images
import tensorflow as tf
import tensorflow_hub as hub

# For drawing onto the image.
import numpy as np
from PIL import Image
from PIL import ImageColor
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageOps

# For closing the application.
import os


# Print Tensorflow version
# print(tf.__version__)

# Check available GPU devices.
# __print("The following GPU devices are available: %s" % tf.test.gpu_device_name())


def resize_image(filename, new_width=256, new_height=256):
    pil_image = Image.open(filename)
    pil_image = ImageOps.fit(pil_image, (new_width, new_height), Image.ANTIALIAS)
    pil_image_rgb = pil_image.convert("RGB")
    pil_image_rgb.save(filename, format="JPEG", quality=100)
    print("Image Saved to %s." % filename)

    return filename


def load_img(path):
    img = tf.io.read_file(path)
    img = tf.image.decode_jpeg(img, channels=3)
    return img


def run_detector(filename):
    
    module_handle = "https://tfhub.dev/google/openimages_v4/ssd/mobilenet_v2/1"
    detector = hub.load(module_handle).signatures['default']
    
    resize_image(filename)
    
    img = load_img(filename)

    converted_img = tf.image.convert_image_dtype(img, tf.float32)[tf.newaxis, ...]
    result = detector(converted_img)

    result = {key: value.numpy() for key, value in result.items()}


    classes_detected = [x.decode('ascii') for x in result["detection_class_entities"]]
    classes_detected = list(dict.fromkeys(classes_detected))


    os.remove(filename)

    return classes_detected


