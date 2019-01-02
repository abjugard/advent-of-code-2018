from santas_little_helpers import day, get_data, timed
from importlib import import_module
from operator import attrgetter as attr

today = day(2018, 10)

class Particle(object):
  def __init__(self, line):
    self.x = int(line[10:16])
    self.y = int(line[18:24])
    self.vx = int(line[-8:-6])
    self.vy = int(line[-5:-2])

  def travel(self):
    self.y += self.vy
    self.x += self.vx

  def __lt__(self, other):
    return self.y < other.y

  def __eq__(self, other):
    return (self.y, self.x) == (other[1], other[0])

  def ellipse(self, ymin, xmin, pixel_size):
    yp = (self.y-ymin+2) * pixel_size
    xp = (self.x-xmin+2) * pixel_size
    return (xp, yp), (xp + pixel_size + 7, yp + pixel_size + 7)

def calculate_sky_message(particles):
  height = abs(max(particles).y - min(particles).y)
  time = 0
  while height > 10:
    for particle in particles:
      particle.travel()
    height = abs(max(particles).y - min(particles).y)
    time += 1

  ymax, ymin = max(particles).y, min(particles).y
  xmax = max(particles, key=attr('x')).x
  xmin = min(particles, key=attr('x')).x

  try:
    return time, tesseract_parse(particles, ymax, ymin, xmax, xmin)
  except ImportError:
    for y in range(ymin, ymax+1):
      l = ''
      for x in range(xmin, xmax+1):
        l += '█' if (x, y) in particles else ' '
      print(l)
    print()
    return time, None

def tesseract_parse(particles, ymax, ymin, xmax, xmin):
  Image = import_module('PIL.Image')
  ImageDraw = import_module('PIL.ImageDraw')
  pytesseract = import_module('pytesseract')

  pixel_size = 10
  dimensions = ((xmax - xmin+5) * pixel_size, (ymax - ymin+5) * pixel_size)
  img = Image.new('RGBA', dimensions, (255, 255, 255, 0))
  draw = ImageDraw.Draw(img)
  for particle in particles:
    draw.ellipse(particle.ellipse(ymin, xmin, pixel_size), fill='black')
  result = pytesseract.image_to_string(img, config='--psm 6')
  return result

def main() -> None:
  particles = list(get_data(today, [('func', Particle)]))

  time, result = calculate_sky_message(particles)
  if result is None:
    print('for cooler results, please install Pillow and pytesseract\n' \
        + '(along with a tesseract-ocr distribution)\n')
    print(f'{today} star 1 printed in block letters')
  else:
    print(f'{today} star 1 = {result}')
  print(f'{today} star 2 = {time}')

if __name__ == '__main__':
  timed(main)
