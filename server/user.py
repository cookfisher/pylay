from common.hostmask import *

class User(object):
	"""
	Manages the state of a user, starting from the time of connection.
	"""

	def __init__(self, host):
		"""
		Create a new user that has connected from the given hostname.
		The user starts in an unregistered state.

		@param host The hostname of the user.
		@return None
		"""

		self._registered = False
		self._hostmask   = Hostmask(None, None, host)

	def update(self, nickname = None, username = None):
		"""
		Update the username/nickname of a user after a USER or NICK command.
		Any argument that is not None will be updated with the given value.
		Note that the username can only be updated before the user registers.

		@param nickname The nickname to update to.
		@param username The username to update to.
		@return None
		"""

		if username is not None:
			if self._registered:
				raise RuntimeError('username has already been solidified')
			else:
				newh = Hostmask.update(self._hostmask, username = username)
				self._hostmask = newh

		if nickname is not None:
			self._hostmask.nickname = nickname

	def is_registered(self):
		"""
		Check if a user has been registered.

		@return None
		"""

		return self._registered

	def can_register(self):
		"""
		Check if a user can register in its current state.

		@return True if the user can register, False otherwise.
		"""

		if self._hostmask.nickname is None:
			return False
		if self._hostmask.username is None:
			return False

		return True

	def register(self):
		"""
		Set a user as registered.
		A user must have a nickname and a username at this point.

		@return None
		"""

		if self._registered:
			raise RuntimeError('user has already been registered')
		if not self.can_register():
			raise RuntimeError('user cannot be registered')

		self._registered = True
