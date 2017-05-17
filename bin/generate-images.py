#!/usr/bin/python

# util to generate images used on footer page

import sys
from wand.image import Image
from wand.color import Color
from wand.drawing import Drawing
from wand.display import display

letter_mapping = {
    "L" : "red",
    "E" : "green",
    "A" : "lightblue",
    "R" : "yellow",
    "N" : "white",
}

def generate_letter_images(letter, background_color, path):
  with Image(width=80, height=80, background=Color('transparent')) as image:
    with Drawing() as drawing:
      drawing.fill_color = Color(background_color)
      drawing.stroke_color = Color('black')
      drawing.stroke_width = 2
      drawing.circle((40, 40), (20, 20))
      drawing.push()
      drawing.fill_color = Color('black')
      drawing.font_size = 25
      drawing.text_alignment = 'center'
      metrics = drawing.get_font_metrics(image,letter,multiline=False)
      font_width=int(round(metrics.text_width))
      font_height=int(round(metrics.text_height))
      drawing.text((image.width/2),((image.height+int(round(metrics.text_height)/2))/2), letter)
      drawing(image)
      image.format = "png"
      image.save(filename=path+"/"+letter+'.png')

def generate_menu_button(label, path):
  with Image(width=120, height=70, background=Color('transparent')) as image:
    with Drawing() as drawing:
      drawing.fill_color = Color('lightblue')
      drawing.stroke_color = Color('black')
      drawing.stroke_width = 2
      drawing.rectangle(left=10, top=10, width=100, height=50)
      drawing.push()
      drawing.fill_color = Color('black')
      drawing.font_size = 25
      drawing.text_alignment = 'center'
      metrics = drawing.get_font_metrics(image,label,multiline=False)
      font_width=int(round(metrics.text_width))
      font_height=int(round(metrics.text_height))
      drawing.text((image.width/2),((image.height+int(round(metrics.text_height)/2))/2), label)
      drawing(image)
      image.format = "png"
      image.save(filename=path+"/menu.png")

if len(sys.argv) != 2:
  print "Invalid usage: " + sys.argv[0] + " image_path"
  sys.exit(1)

for letter, background in letter_mapping.iteritems():
  generate_letter_images(letter, background, sys.argv[1])

generate_menu_button('Menu', sys.argv[1])
