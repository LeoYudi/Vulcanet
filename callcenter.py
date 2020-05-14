from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import Factory
from twisted.internet import reactor


class CallCenter(LineReceiver):
  def __init__(self):
    self.queue = []
    self.A = Operator()
    self.B = Operator()

  def connectionMade(self):
    self.sendLine('Connection Made')

  def verifyQueue(self, operatorId):
    if operatorId == 'A':
      if len(self.queue) > 0:
        callId = self.queue.pop(0)
        self.sendLine('Call ' + str(callId) + ' ringing for operator A')
        self.A.state = 'ringing'
        self.A.call = callId
    else:
      if len(self.queue) > 0:
        callId = self.queue.pop(0)
        self.sendLine('Call ' + str(callId) + ' ringing for operator B')
        self.B.state = 'ringing'
        self.B.call = callId

  def lineReceived(self, line):
    command = line.split()
    if len(command) != 2:
      self.sendLine('Command Invalid')
    elif command[0] == 'call':
      self.sendLine('Call ' + command[1] + ' received')
      if self.A.state == 'available':
        self.sendLine('Call ' + command[1] + ' ringing for operator A')
        self.A.state = 'ringing'
        self.A.call = int(command[1])
      elif self.B.state == 'available':
        self.sendLine('Call ' + command[1] + ' ringing for operator B')
        self.B.state = 'ringing'
        self.B.call = int(command[1])
      else:
        self.sendLine('Call ' + command[1] + ' wating in queue')
        self.queue.append(int(command[1]))

    elif command[0] == 'answer':
      if command[1] == 'A':
        if self.A.state == 'ringing':
          self.sendLine('Call ' + str(self.A.call) + ' answered by operator A')
          self.A.state = 'busy'
        else:
          self.sendLine('That is not possible')
      elif command[1] == 'B':
        if self.B.state == 'ringing':
          self.sendLine('Call ' + str(self.B.call) + ' answered by operator B')
          self.B.state = 'busy'
        else:
          self.sendLine('That is not possible')
      else:
        self.sendLine('Operator ' + command[1] + ' does not exist')

    elif command[0] == 'reject':
      if command[1] == 'A':
        if self.A.state == 'ringing':
          self.sendLine('Call ' + str(self.A.call) + ' rejected by operator A')
          self.queue.append(self.A.call)
          self.A.reset()
          self.verifyQueue('A')
        else:
          self.sendLine('That is not possible')
      elif command[1] == 'B':
        if self.B.state == 'ringing':
          self.sendLine('Call ' + str(self.B.call) + ' rejected by operator B')
          self.queue.append(self.B.call)
          self.B.reset()
          self.verifyQueue('B')
        else:
          self.sendLine('That is not possible')
      else:
        self.sendLine('Operator ' + command[1] + ' does not exist')

    elif command[0] == 'hangup':
      if self.A.state == 'busy' and self.A.call == int(command[1]):
        self.sendLine('Call ' + command[1] + ' finished and operator A is available')
        self.A.reset()
        self.verifyQueue('A')

      elif self.B.state == 'busy' and self.B.call == int(command[1]):
        self.sendLine('Call ' + command[1] + ' finished and operator B is available')
        self.B.reset()
        self.verifyQueue('B')

      elif self.A.state == 'ringing' and self.A.call == int(command[1]):
        self.sendLine('Call ' + command[1] + ' missed')
        self.A.reset()
        self.verifyQueue('A')

      elif self.B.state == 'ringing' and self.B.call == int(command[1]):
        self.sendLine('Call ' + command[1] + ' missed')
        self.B.reset()
        self.verifyQueue('B')

      else:
        ok = False
        for callId in self.queue:
          if callId == int(command[1]):
            ok = True
            break
        if ok:
          self.queue.remove(int(command[1]))
          self.sendLine('Call ' + command[1] + ' missed')

    elif command[0] == 'exit':
      reactor.stop()

    else:
      self.sendLine('Command ' + command[0] + ' does not exist')


class CallCenterFactory(Factory):
  def buildProtocol(self, addr):
    return CallCenter()


class Operator:
  def __init__(self):
    self.state = 'available'
    self.call = 0

  def reset(self):
    self.state = 'available'
    self.call = 0


reactor.listenTCP(5678, CallCenterFactory())
reactor.run()
