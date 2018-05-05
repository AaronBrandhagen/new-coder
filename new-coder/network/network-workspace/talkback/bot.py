from twisted.internet import protocol
from twisted.python import log
from twisted.words.protocols import irc

class TalkBackFactory(protocol.ClientFactory):
	
	def __init__(self,channel, nickname, realname, quotes, triggers):
		protocol = TalkBackBot
		self.channel = channel
		self.nickname = nickname
		self.realname = realname
		self.quotes = quotes
		self.triggers = triggers


class TalkBackBot(irc.IRCClient):
	
	def connectionMade(self):
		self.nickname = self.factory.nickname
		self.realname = self.factory.nickname
		irc.IRCClient.connectionMade(self)
		log.msg('connectionMade')
		
	def connectionLost(self, reason):
		irc.IRCClient.connectionLost(self, reason)
		log.msg('connectionLost {!r}'.format(reason))
	def signedOn(self):
		log.msg('signed on')
		if self.nickname != self.factory.nickname:
			log.msg('Your nickname was already occupied, actual nickname is {}'.format(self.nickname))
		self.join(self.factory.channel)
	
	def signedOff(self):
		pass
	def joined(self, channel):
		log.msg('[{nick} has joined {channel}]'.format(nick=self.nickname, channel = self.factory.channel,))
	def privmsg(self, user, channel, msg):
		sendTo = None
		prefix = ''
		senderNick = user.split('!', 2)[0]
		if channel == self.nickname:
			sendTo = senderNick
		elif msg.startswith(self.nickname):
			sendTo = channel
			prefix = senderNick
		else:
			msg = msg.lower()
			for trigger in self.factory.triggers:
				if msg in trigger:
					sendTo = channel
					prefix = senderNick + ': '
					break
		if sendTo:
			quote = self.factory.quotes.pick()
			self.msg(sendTo, prefix + quote)
			log.msg('sent message to {receiver}, triggered by {sender}:\n\t{quote}'.format(receiver=sendTo, sender=senderNick, quote=quote))
			



