from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import Factory
from twisted.internet import reactor

class CallCenter(LineReceiver):
	def __init__(self):
		self.operator = {
			'A': {
				'state': 'available',
				'call': 0
			},
			'B': {
				'state': 'available',
				'call': 0
			}
		}

	def connectionMade(self):
		self.sendLine('Connection Made')

	def lineReceived(self, line):
		command = line.split()
		if command[0] == 'call':
			self.sendLine('Call ' + command[1] + ' received')
			if self.operator['A']['state'] == 'available':
				self.sendLine('Call ' + command[1] + ' ringing for operator A')
				self.operator['A'] == 'ringing'

class CallCenterFactory(Factory):
	def buildProtocol(self, addr):
		return CallCenter()

class Operator():
	def __init__(self):
		self.A = {
			
		}

reactor.listenTCP(5678, CallCenterFactory())
reactor.run()