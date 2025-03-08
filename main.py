import rp2
import machine
import time
import neopixel
import math
from jtouch import Device

time.sleep_ms(1000)

machine.freq(125_000_000)

# NeoPixel setup
NUM_PIXELS = 12  # Number of LEDs in the NeoPixel ring
NEOPIXEL_PIN = 14  # GPIO pin connected to the NeoPixel data line
np = neopixel.NeoPixel(machine.Pin(NEOPIXEL_PIN), NUM_PIXELS)

hue_mode_pin=4
brightness_speed_pin=0
saturation_intensity_pin=8

# rate of change when button held
brightness_step=0.01
saturation_step=0.01
hue_step=0.002

effect_intensity_step=0.01
effect_speed_step=0.0001

max_speed=0.01
min_speed=0.0001
max_intensity=1.0
min_intensity=0.0

# starting colour
brightness = 0.0  # Range: 0.0 to 1.0
hue = 1.0  # Range: 0.0 to 1.0
saturation = 0.0  # Range: 0.0 to 1.0

brightness_direction = -1
saturation_direction = -1
effect_speed_direction = 1
effect_intensity_direction = 1
brightness_held = False
saturation_held = False
effect_speed_held = False
effect_intensity_held = False

effect_mode = False
current_effect = 0
effect_speed = 0.001
effect_intensity = [1.0] * 10
effect_timer = 0
effect_hue_offset = 0

min_double_tap_time=0.1
max_double_tap_time=0.8

tap_time = 0
last_tap = time.time()

threshold=20000
detection_level=0.5

def map_range(x, in_min, in_max, out_min, out_max):
    return (x - in_min) / (in_max - in_min) * (out_max - out_min) + out_min


def hsv_to_rgb(h, s, v):
    if s == 0.0:
        return int(v * 255), int(v * 255), int(v * 255)
    i = int(h * 6.0)
    f = (h * 6.0) - i
    p = v * (1.0 - s)
    q = v * (1.0 - s * f)
    t = v * (1.0 - s * (1.0 - f))
    i %= 6
    return [(int(v * 255), int(t * 255), int(p * 255)),
            (int(q * 255), int(v * 255), int(p * 255)),
            (int(p * 255), int(v * 255), int(t * 255)),
            (int(p * 255), int(q * 255), int(v * 255)),
            (int(t * 255), int(p * 255), int(v * 255)),
            (int(v * 255), int(p * 255), int(q * 255))][i]

import math
import random

import math
import random

def update_neopixels():
    global effect_hue_offset, effect_timer
    
    if not effect_mode:
        rgb = hsv_to_rgb(hue, saturation, brightness)
        for i in range(NUM_PIXELS):
            np[i] = rgb
    else:
        
        for i in range(NUM_PIXELS):
            if current_effect == 0:  # Rainbow Spin
                # Intensity controls saturation
                intensity=map_range(effect_intensity[current_effect],0,1,0.7,1.0)
                np[i] = hsv_to_rgb((effect_hue_offset + (i / NUM_PIXELS)) % 1.0, saturation * intensity, brightness)
                effect_hue_offset += effect_speed

            elif current_effect == 1:  # Rainbow Cycle
                # Intensity controls saturation
                intensity=map_range(effect_intensity[current_effect],0,1,0.7,1.0)
                np[i] = hsv_to_rgb((effect_hue_offset) % 1.0, saturation * intensity, brightness)
                effect_hue_offset += effect_speed/5

            elif current_effect == 2:  # Pulsing
                # Intensity controls the amplitude of the pulsing (how much it pulses)
                intensity=map_range(effect_intensity[current_effect],0,1,0.3,1.0)
                pulsing_brightness = 0.5 + 0.5 * math.sin(effect_timer * 50) * intensity
                np[i] = hsv_to_rgb(hue, saturation, pulsing_brightness)

            elif current_effect == 3:  # Wave Effect
                # Intensity controls the length of the wave (wider or narrower waves)
                intensity=map_range(effect_intensity[current_effect],0,1,0.2,6)
                wave_brightness = 0.5 + 0.8 * math.sin((i / NUM_PIXELS) * 2 * math.pi *intensity + effect_timer * 200)
                if wave_brightness<0:
                    wave_brightness=0
                elif wave_brightness>1:
                    wave_brightness=1
                np[i] = hsv_to_rgb(hue, saturation, wave_brightness)

            elif current_effect == 4:  # Wave Effect
                # Intensity controls the length of the wave (wider or narrower waves)
                
                intensity=map_range(effect_intensity[current_effect],0,1,0.2,6)
                wave_brightness = 0.5 + 0.8 * math.sin((i / NUM_PIXELS) * 2 * math.pi*intensity + effect_timer * 200)
                if wave_brightness<0:
                    wave_brightness=0
                elif wave_brightness>1:
                    wave_brightness=1
                np[i] = hsv_to_rgb((effect_hue_offset + (i / NUM_PIXELS)) % 1.0, saturation, wave_brightness)
                effect_hue_offset += effect_speed

            elif current_effect == 5:  # Random Blink
                intensity=map_range(effect_intensity[current_effect],0,1,0.3,0.01)
                if random.random() < intensity:  # Intensity adjusts blink frequency
                    np[i] = hsv_to_rgb(hue, saturation, brightness)
                else:
                    np[i] = hsv_to_rgb(hue, saturation, 0)  # Off


                
    np.write()
    effect_timer += effect_speed



# def update_neopixels():
#     global effect_hue_offset, effect_timer
    
#     if not effect_mode:
#         rgb = hsv_to_rgb(hue, saturation, brightness)
#         for i in range(NUM_PIXELS):
#             np[i] = rgb
#     else:
        
#         for i in range(NUM_PIXELS):
#             if current_effect == 1:  # Rainbow Spin
#                 np[i] = hsv_to_rgb((effect_hue_offset + (i / NUM_PIXELS)) % 1.0, 1.0, brightness)
#                 effect_hue_offset += effect_speed
#             elif current_effect == 2:  # Rainbow Cycle
#                 np[i] = hsv_to_rgb((effect_hue_offset) % 1.0, 1.0, brightness)
#                 effect_hue_offset += effect_speed
#             elif current_effect == 3:  # Pulsing
#                 pulsing_brightness = 0.5 + 0.5 * math.sin(effect_timer * 100)
#                 np[i] = hsv_to_rgb(hue, saturation, pulsing_brightness)
#             elif current_effect == 4:  # Wave Effect
#                 wave_brightness = 0.5 + 0.5 * math.sin((i / NUM_PIXELS) * 2 * math.pi + effect_timer *50)
#                 np[i] = hsv_to_rgb(hue, saturation, wave_brightness)
#             elif current_effect == 5:  # Travelling Pulse
#                 wave_brightness = 1 - 0.5 * math.sin((i / NUM_PIXELS) * 2 * math.pi + effect_timer *10)
#                 np[i] = hsv_to_rgb(hue, saturation, wave_brightness)
                
#     np.write()
#     effect_timer += effect_speed

def process_touch_inputs(device):
    global brightness, hue, saturation, brightness_direction, saturation_direction, brightness_held, saturation_held
    global effect_mode, current_effect, effect_speed, effect_intensity, tap_time, last_tap
    global effect_speed_held,effect_intensity_held,effect_intensity_direction,effect_speed_direction

    device.update()
    current_time = time.time()

    hue_mode_button=device.level(1)
    brightness_speed_button=device.level(0)
    saturation_intensity_button=device.level(2)

    if all(x > detection_level for x in (hue_mode_button, brightness_speed_button, saturation_intensity_button)):  # Hue Button
        if current_time - last_tap > 1:  # Double tap detected
            effect_mode = not effect_mode
            # if effect_mode:
            #     current_effect=1
            print("switch mode")
        last_tap = current_time
    else:
        if not effect_mode:
            # set brightness
            if brightness_speed_button > detection_level:  # Brightness Button
                if not brightness_held:
                    brightness_direction *= -1 if brightness in [0.0, 1.0] else 1
                    brightness_held = True
                brightness = max(0.0, min(1.0, brightness + brightness_step * brightness_direction))
            else:
                brightness_held = False

            # set hue
            if hue_mode_button > detection_level:
                hue += hue_step
                if hue > 1.0:
                    hue -= 1.0
            
            # set saturation
            if saturation_intensity_button > detection_level:  # Saturation Button
                if not saturation_held:
                    saturation_direction *= -1 if saturation in [0.0, 1.0] else 1
                    saturation_held = True
                saturation = max(0.0, min(1.0, saturation + saturation_step * saturation_direction))
            else:
                saturation_held = False
        else:
            if hue_mode_button > detection_level:
                if current_time - last_tap > 0.3:  # Double tap detected
                    current_effect =current_effect+1
                    if current_effect>5:
                        current_effect=0
                    print("effect "+str(current_effect))
                last_tap = current_time
                

            # effect intensity
            if saturation_intensity_button > detection_level:  # Intensity Button
                if not effect_intensity_held:
                    effect_intensity_direction *= -1 if effect_intensity[current_effect] in [min_intensity, max_intensity] else 1
                    effect_intensity_held = True
                effect_intensity[current_effect] = max(min_intensity, min(max_intensity, effect_intensity[current_effect] + effect_intensity_step * effect_intensity_direction))
            else:
                effect_intensity_held = False

            # effect speed
            if brightness_speed_button > detection_level:  # speed Button
                if not effect_speed_held:
                    effect_speed_direction *= -1 if effect_speed in [min_speed, max_speed] else 1
                    effect_speed_held = True
                effect_speed = max(min_speed, min(max_speed, effect_speed + effect_speed_step * effect_speed_direction))
            else:
                effect_speed_held = False

def main():
    touch_pins = (brightness_speed_pin, hue_mode_pin, saturation_intensity_pin)
    with Device(touch_pins, threshold) as touch_device:
        while True:
            process_touch_inputs(touch_device)
            update_neopixels()
            time.sleep(0.01)

if __name__ == "__main__":
    main()
