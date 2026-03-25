# https://youtube.com/shorts/lqeTFISx8pE

import random
import shutil
import time
import sys

CONFIG = {
  "speed": 0.07,    
  "density": 0.9, 
  "charset": "0123456789ABCDEF", 
  "min_trail": 30,
  "max_trail": 40
}


class Column:
  def __init__(self, rows, config):
    self.rows = rows
    self.config = config
    self.reset()

  def reset(self):
    self.y = random.randint(0, self.rows)
    self.trail = random.randint(
      self.config["min_trail"],
      self.config["max_trail"]
    )
    self.active = random.random() < self.config["density"]

  def step(self):
    if not self.active:
      if random.random() < self.config["density"]:
        self.reset()
      return

    self.y += 1

    if self.y > self.rows + self.trail:
      if random.random() > 0.97:
        self.reset()


class MatrixRain:
  def __init__(self, config):
    self.config = config
    self.cols, self.rows = shutil.get_terminal_size()

    self.columns = [
      Column(self.rows, config)
      for _ in range(self.cols)
    ]

    print("\033[?25l", end="") 

  def move_cursor(self, x, y):
    return f"\033[{y};{x}H"

  def draw_column(self, x, col):
    y = col.y
    trail = col.trail
    chars = self.config["charset"]

    if 0 < y < self.rows:
      print(self.move_cursor(x + 1, y) + "\033[97m" + random.choice(chars), end="")

    for t in range(1, trail):
      ty = y - t
      if 0 < ty < self.rows:
        color = "\033[32m" if t < trail // 2 else "\033[2;32m"
        print(self.move_cursor(x + 1, ty) + color + random.choice(chars), end="")

    tail_end = y - trail
    if 0 < tail_end < self.rows:
      print(self.move_cursor(x + 1, tail_end) + " ", end="")

  def run(self):
    try:
      while True:
        for x, col in enumerate(self.columns):
          if col.active:
            self.draw_column(x, col)
          col.step()

        print("\033[0m", end="")
        sys.stdout.flush()
        time.sleep(self.config["speed"])

    except KeyboardInterrupt:
      print("\033[?25h") 
      sys.exit()


if __name__ == "__main__":
  app = MatrixRain(CONFIG)
  app.run()
