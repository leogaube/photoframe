# This file is part of photoframe (https://github.com/mrworf/photoframe).
#
# photoframe is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# photoframe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with photoframe.  If not, see <http://www.gnu.org/licenses/>.
#

import logging
import subprocess

from math import sqrt

class MonitorControl:
  BUS = None

  BRIGHTNESS = None
  CONTRAST = None

  SENSITIVITY = 6.

  @staticmethod
  def isDDCinstalled():
    pass
    #TODO test for ddcutil

  @staticmethod
  def detectBus():
    if MonitorControl.BUS is None:
      output = subprocess.check_output(["ddcutil", "detect"])
      try:
        MonitorControl.BUS = int(output.split("/dev/i2c-")[1].split("\n")[0].strip())
      except:
        logging.debug("unable to retrieve display bus")
      
    return MonitorControl.BUS

  @staticmethod
  def increaseSensitivity():
    if MonitorControl.SENSITIVITY < 10:
      MonitorControl.SENSITIVITY += 0.5
    return MonitorControl.SENSITIVITY

  @staticmethod
  def decreaseSensitivity():
    if MonitorControl.SENSITIVITY > 2.5:
      MonitorControl.SENSITIVITY -= 0.5
    return MonitorControl.SENSITIVITY
    
  @staticmethod
  def getBrightness():
    if MonitorControl.BRIGHTNESS is None:
      output = subprocess.check_output(["ddcutil", "getvcp", "10"])
      try:
        MonitorControl.BRIGHTNESS = int(output.split("current value =")[1].split(",")[0].strip())
      except:
        logging.debug("unable to retrieve monitor brightness")

    return MonitorControl.BRIGHTNESS

  @staticmethod
  def getContrast():
    if MonitorControl.CONTRAST is None:
      output = subprocess.check_output(["ddcutil", "getvcp", "12"])
      try:
        MonitorControl.CONTRAST = int(output.split("current value =")[1].split(",")[0].strip())
      except:
        logging.debug("unable to retrieve monitor contrast")

    return MonitorControl.CONTRAST

  @staticmethod     
  def increaseBrightness(step=10):
    currentValue = MonitorControl.getBrightness()
    newValue = max(0, min(currentValue + step, 100))
    MonitorControl.setBrightness(newValue)

  @staticmethod
  def decreaseBrightness(step=10):
    assert(step > 0)
    MonitorControl.increaseBrightness(-step)

  @staticmethod
  def increaseContrast(step=10):
    currentValue = MonitorControl.getContrast()
    newValue = max(0, min(currentValue + step, 100))
    MonitorControl.setContrast(newValue)

  @staticmethod
  def decreaseContrast(step=10):
    assert(step > 0)
    MonitorControl.increaseContrast(-step)

  @staticmethod
  def setBrightness(value):
    MonitorControl.detectBus()
    subprocess.call(["ddcutil", "setvcp", "10", str(value), "--noverify", "--force", "--force-slave-address", "--nodetect", "--bus", str(MonitorControl.BUS)])
    MonitorControl.BRIGHTNESS = value
    logging.debug("new brightness value: %d"%value)

  @staticmethod
  def setContrast(value):
    MonitorControl.detectBus()
    subprocess.call(["ddcutil", "setvcp", "12", str(value), "--noverify", "--force", "--force-slave-address", "--nodetect", "--bus", str(MonitorControl.BUS)])
    MonitorControl.CONTRAST = value
    logging.debug("new contrast value: %d"%value)

  @staticmethod
  def adjust(temperature, lux):
    # y = 10*sqrt(int(lux))
    # lux = 10  --> brightness = 0; contrast = 30;
    # lux = 25  --> brightness = 0; contrast = 50;
    # lux = 100 --> brightness = 0; contrast = 100;
    # lux = 400 --> brightness = 100; contrast = 100;
    y = MonitorControl.SENSITIVITY*sqrt(int(lux)) 

    contrast = min(int(y), 100)
    brightness = min(max(0, int(y-100)), 100)

    if MonitorControl.BRIGHTNESS is None:
      MonitorControl.setBrightness(brightness)
    else:
      brightnessChange = brightness-MonitorControl.BRIGHTNESS
      if abs(brightnessChange) > 15:
        MonitorControl.setBrightness(brightness)
      elif brightnessChange > 0:
        MonitorControl.increaseBrightness(1)
      elif brightnessChange < 0:
        MonitorControl.decreaseBrightness(1)

    if MonitorControl.CONTRAST is None:
      MonitorControl.setContrast(contrast)
    else:
      contrastChange = contrast-MonitorControl.CONTRAST
      if abs(contrastChange) > 15:
        MonitorControl.setContrast(contrast)
      elif contrastChange > 0:
        MonitorControl.increaseContrast(1)
      elif contrastChange < 0:
        MonitorControl.decreaseContrast(1)



