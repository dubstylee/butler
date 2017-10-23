import sys
from enum import Enum

class Status(Enum):
  STAND_UP = 0
  SIT_DOWN = 1
  HAS_LEFT = 2
  HAS_RIGTH = 3
  HAS_BOTH = 4
  EATING = 5

class Philosopher:
  state = Status.STAND_UP
  identifier = 0  

  def changeState(self):
    self.state = Status(self.state.value + 1)
    print "Philosopher %d %s" %(self.identifier,self.state.value)

p = Philosopher()

def main():
  if len(sys.argv) != 2:
    print "Invalid number of arguments"
  else:
    p.identifier = int(sys.argv[1])
    while p.state != Status.EATING:
      p.changeState()

if __name__ == "__main__": main()
