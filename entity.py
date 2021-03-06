from kivy.factory import Factory

from utils import DisallowInterfaceInstantiation, DivideFrequency
from invariants import NoExcept
from inventory import Inventory
from utils import directions

import random

class IEntity(DisallowInterfaceInstantiation):
  tx_source = ''

  def init(self, world, px, py): pass
  def draw(self):                pass
  def undraw(self):              pass
  def step(self):                pass
  def local_controlled(self):    pass
  def attack(self, amount):      pass

class Entity(IEntity):
  tx_source = 'assets/entities/entity-256.png'

  @NoExcept
  def __init__(self, world, px, py):
    self.pos = px, py
    self.world = world
    self.canvas = world.canvas
    
    self.widget = None
    self.hp_bar = EntityHP(world, px, py)
    
    if not self.local_controlled():
      self.inventory = Inventory(world, self, 9)

  @NoExcept
  def draw(self):
    if not self.widget:
      self.widget = Factory.Entity()
      self.widget.tx_source = self.tx_source
      self.canvas.add_widget(self.widget)
    
    self.widget.px, self.widget.py = self.pos
    self.hp_bar.pos = self.pos
    self.hp_bar.draw()
  
  @NoExcept
  def undraw(self):
    if self.widget:
      self.canvas.remove_widget(self.widget)
      self.widget = None
    
    self.hp_bar.undraw()

  @NoExcept
  @DivideFrequency(40)
  def step(self):
    px, py = self.pos
    dx, dy = directions[random.randrange(0, 6)]
    nx, ny = px + dx, py + dy
    
    if self.world.has_block(nx, ny) and not self.world.has_entity(nx, ny):
      self.pos = nx, ny
  
  @NoExcept
  def local_controlled(self):
    return False
  
  @NoExcept
  def attack(self, amount):
    self.hp_bar.hp -= amount
    
    if self.hp_bar.hp <= 0:
      self.world.remove_entity(self)

class EntityPlayer(Entity):
  tx_source = 'assets/entities/entity-256.png'
  
  @NoExcept
  def __init__(self, world, px, py):
    super(EntityPlayer, self).__init__(world, px, py)
    
    self.inventory = Inventory(world, world.canvas, 9)
  
  @NoExcept
  def step(self):
    pass
  
  @NoExcept
  def draw(self):
    super(EntityPlayer, self).draw()
    
    self.inventory.draw(debug=False) # TODO: remove debug prints

  @NoExcept
  def local_controlled(self):
    return True

class IEntityHP(DisallowInterfaceInstantiation):
  def init(self, world, px, py): pass
  def draw(self):                pass
  def undraw(self):              pass
  
class EntityHP(IEntityHP):
  @NoExcept
  def __init__(self, world, px, py):
    self.pos = px, py
    self.canvas = world.canvas
    self.widget = None
    self.hp = 10
    
  @NoExcept
  def draw(self):
    if not self.widget:
      self.widget = Factory.EntHP()
      self.canvas.add_widget(self.widget)
    
    self.widget.px, self.widget.py = self.pos
    self.widget.health = self.hp
    
  @NoExcept
  def undraw(self):
    if self.widget:
      self.canvas.remove_widget(self.widget)
      self.widget = None
