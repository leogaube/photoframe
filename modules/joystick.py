import pygame
import ddc_control

import time
import logging
from threading import Thread

class Joystick(Thread):
	def __init__(self, createEventFunc):
		Thread.__init__(self)
		self.daemon = True

		self.createSlideshowEvent = createEventFunc

		self.increaseBrightness = ddc_control.increaseBrightness
		self.decreaseBrightness = ddc_control.decreaseBrightness
		self.increaseContrast = ddc_control.increaseContrast
		self.decreaseContrast = ddc_control.decreaseContrast

		# joystick reconnect required after 10 min without any input
		self.joystickReconnectTimeout = 600

		self.start()

	def connect(self):
		pygame.display.init()
		pygame.joystick.init()
		while pygame.joystick.get_count() == 0:
			pygame.quit()
			time.sleep(10)
			pygame.display.init()
			pygame.joystick.init()

		for i in range(pygame.joystick.get_count()):
			pygame.joystick.Joystick(i).init()
			logging.info("Joystick connected!")

		self.lastEvent = time.time()

	def run(self):
		self.connect()
		while True:
			for event in pygame.event.get():
				# Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
				if event.type == pygame.JOYBUTTONDOWN:
					if event.button == 4:
						self.createSlideshowEvent("prevImage")
					elif event.button == 5:
						self.createSlideshowEvent("nextImage")
					elif event.button == 6:
						self.createSlideshowEvent("prevAlbum")
					elif event.button == 7:
						self.createSlideshowEvent("nextAlbum")

					elif event.button == 13:
						self.increaseBrightness()
					elif event.button == 14:
						self.decreaseBrightness()
					elif event.button == 15:
						self.decreaseContrast()
					elif event.button == 16:
						self.increaseContrast()

					self.lastEvent = time.time()
					logging.debug("%d Button pressed!"%event.button)
				if event.type == pygame.JOYBUTTONUP:
					pass

			if time.time()-self.lastEvent > self.joystickReconnectTimeout:
				logging.info("joystick reconnect required!")
				pygame.quit()
				self.connect()

			time.sleep(0.1)
