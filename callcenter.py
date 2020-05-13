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

    def lineReceived(self, line):
        command = line.split()
        if command[0] == 'call':
            self.sendLine('Call ' + command[1] + ' received')
            if self.A.state == 'available':
                self.sendLine('Call ' + command[1] + ' ringing for operator A')
                self.A.state = 'ringing'
                self.A.call = command[1]
            elif self.B.state == 'available':
                self.sendLine('Call ' + command[1] + ' ringing for operator B')
                self.B.state = 'ringing'
                self.B.call = command[1]
            else:
                self.sendLine('Call ' + command[1] + ' wating in queue')
                self.queue.append(int(command[1]))

        elif command[0] == 'answer':
            print ''

        elif command[0] == 'rejected':
            print ''

        elif command[0] == 'hangup':
            print ''


class CallCenterFactory(Factory):
    def buildProtocol(self, addr):
        return CallCenter()


class Operator():
    def __init__(self):
        self.state = 'available'
        self.call = 0

    def reset(self):
        self.state = 'available'
        self.call = 0


reactor.listenTCP(5678, CallCenterFactory())
reactor.run()
