# [Participating in Game Off 2021]
# Roctorio is game similar to Factorio which uses hexagonal field.
# You control the raccoon that tries to build his base on an unknown planet.
#
# (c) 2021, ProgramCrafter, dogIsuper, KarmaNT, 

from kivy.config import Config
Config.set('graphics', 'maxfps', 20)

from kivy.factory import Factory
from kivy.clock import Clock
from kivy.app import App

import os

from gameobject import GameObject

class RoctorioGameThread:
  def __init__(self, app):
    self.app = app
    
  def start(self):
    Clock.schedule_once(self.update, 0)
  
  def update(self, timer):
    self.app.game.step()
    self.app.root.ids.tps_meter.text = 'TPS: %.3f' % self.app.tps
    
    Clock.schedule_once(self.update, 0)

class RoctorioApp(App):
  def build(self):
    self.game = GameObject(self)
    self.root = Factory.Playground()
    
    hex_path = os.path.abspath(__file__ + '\\..\\hex-example.png')
    self.root.ids.playground_test_hex.export_to_png(hex_path)
    
    self.tps = 0.0
    
    self.game_thread = RoctorioGameThread(self)
    self.game_thread.start()

if __name__ == '__main__':
  try:
    RoctorioApp().run()
  except:
    __import__('traceback').print_exc()
    input('...')