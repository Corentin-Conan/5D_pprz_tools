#!/usr/bin/python3

from .user_profile.airmap_profile import AirmapUserProfile

class AirmapRequestManager(object):

	def __init__(self):
		super().__init__()
		self.airmap_user_profile = AirmapUserProfile