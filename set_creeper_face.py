from common.return_pattern_list import PatternList
from sense_hat import SenseHat

creeper_image = PatternList("creeper_head.json").create_pattern_list()
sense = SenseHat()
# send the 'image' to the hat
sense.set_pixels(creeper_image)
