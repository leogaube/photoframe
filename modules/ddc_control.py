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

def isDDCinstalled():
  pass
  #TODO test for ddcutil

def getBrightness():
  output = subprocess.check_output(["ddcutil", "getvcp", "10"])
  try:
    brightness = int(output.split("current value =")[1].split(",")[0].strip())
    return brightness
  except:
    logging.debug("unable to retrieve monitor brightness")
    return None

def getContrast():
  output = subprocess.check_output(["ddcutil", "getvcp", "12"])
  try:
    contrast = int(output.split("current value =")[1].split(",")[0].strip())
    return contrast
  except:
    logging.debug("unable to retrieve monitor contrast")
    return None
      
def increaseBrightness(step=10):
  current_value = getBrightness()
  if current_value is None:
    return
  new_value = max(0, min(current_value + step, 100))
  rc = subprocess.call(["ddcutil", "setvcp", "10", str(new_value)])
  logging.debug("new brightness value: %d"%new_value)

def decreaseBrightness(step=10):
  assert(step > 0)
  increaseBrightness(-step)


def increaseContrast(step=10):
  current_value = getContrast()
  if current_value is None:
    return
  new_value = max(0, min(current_value + step, 100))
  rc = subprocess.call(["ddcutil", "setvcp", "12", str(new_value)])
  logging.debug("new contrast value: %d"%new_value)

def decreaseContrast(step=10):
  assert(step > 0)
  increaseContrast(-step)



