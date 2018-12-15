from santas_little_helpers import day, get_data, timed, alphabet
from itertools import product
from importlib import import_module

today = day(2018, 10)

def calculate_sky_message(data):
  points, velocities = [p[0] for p in data], [p[1] for p in data]
  ydiff = first = abs(max(p[1] for p in points)-min(p[1] for p in points))
  time = 0
  while ydiff > 10:
    for index in range(len(points)):
      points[index] = points[index][0] + velocities[index][0], points[index][1] + velocities[index][1]
    ydiff = abs(max(p[1] for p in points)-min(p[1] for p in points))
    time += 1
  ymax, ymin = max(p[1] for p in points), min(p[1] for p in points)
  xmax, xmin = max(p[0] for p in points), min(p[0] for p in points)

  try:
    return time, tesseract_parse(points)
  except ImportError:
    for y in range(ymin, ymax+1):
      l = ''
      for x in range(xmin, xmax+1):
        l += '█' if (x, y) in points else ' '
      print(l)
    print()
    return time, None

def tesseract_parse(points):
  Image = import_module('PIL.Image')
  ImageDraw = import_module('PIL.ImageDraw')
  pytesseract = import_module('pytesseract')

  ymax, ymin = max(p[1] for p in points), min(p[1] for p in points)
  xmax, xmin = max(p[0] for p in points), min(p[0] for p in points)

  pixel_size = 10
  dimensions = ((xmax-xmin+3) * pixel_size, (ymax-ymin+3) * pixel_size)
  img = Image.new('RGBA', dimensions, (255, 255, 255, 0))
  draw = ImageDraw.Draw(img)
  for x, y in product(range(xmin, xmax+1), range(ymin, ymax+1)):
    yp = (y-ymin+1) * pixel_size
    xp = (x-xmin+1) * pixel_size
    if (x, y) in points:
      draw.rectangle(((xp, yp), (xp + pixel_size, yp + pixel_size)), fill='black')
  result = pytesseract.image_to_string(img, config=f'--psm 6 -c tessedit_char_whitelist={alphabet.upper()}')
  return result.replace('“', 'Z') # for some reason tesseract sees my Z as a “ character.

def fmt(line):
  return (int(line[10:16]), int(line[18:24])), (int(line[-8:-6]), int(line[-5:-2]))

def main() -> None:
  points = list(get_data(today, [('func', fmt)]))

  time, result = calculate_sky_message(points)
  if result is None:
    print('for cooler results, please install Pillow and pytesseract\n'\
        +'(along with a tesseract-ocr distribution)\n')
    print(f'{today} star 1 printed in block letters')
  else:
    print(f'{today} star 1 = {result}')
  print(f'{today} star 2 = {time}')

if __name__ == '__main__':
  timed(main)
