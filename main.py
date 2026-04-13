import rp2
import machine
import time
import neopixel
import math
from jtouch import Device

time.sleep_ms(1000)

machine.freq(125_000_000)

# print("Hi")

# NeoPixel setup
np = neopixel.NeoPixel(machine.Pin(29), 3)
np27 = neopixel.NeoPixel(machine.Pin(27), 12)  # Second LED ring

# np[0]=[255,255,255]
# time.sleep_ms(1000)

hue_mode_pin=3
brightness_speed_pin=4
saturation_intensity_pin=5

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

# Control mode: 0 = both lamps, 1 = np only (pin 29), 2 = np27 only (pin 27)
control_mode = 0
long_press_threshold = 0.5  # seconds
all_pressed_start_time = -1

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
    
    # Update main lamp (pin 29)
    if control_mode in [0, 1]:  # control both or control pin 29
        if not effect_mode:
            rgb = hsv_to_rgb(hue, saturation, brightness)
            for i in range(NUM_PIXELS):
                np[i] = rgb
        else:
            for i in range(NUM_PIXELS):
                np[i] = hsv_to_rgb(hue, saturation, brightness)
    
    # Update second lamp (pin 27) - only applies effects
    if control_mode in [0, 2]:  # control both or control pin 27
        if not effect_mode:
            rgb = hsv_to_rgb(hue, saturation, brightness)
            for i in range(NUM_PIXELS):
                np27[i] = rgb
        else:
            for i in range(NUM_PIXELS):
                if current_effect == 0:  # Rainbow Spin
                    intensity=map_range(effect_intensity[current_effect],0,1,0.7,1.0)
                    np27[i] = hsv_to_rgb((effect_hue_offset + (i / NUM_PIXELS)) % 1.0, saturation * intensity, brightness)
                    effect_hue_offset += effect_speed

                elif current_effect == 1:  # Rainbow Cycle
                    intensity=map_range(effect_intensity[current_effect],0,1,0.7,1.0)
                    np27[i] = hsv_to_rgb((effect_hue_offset) % 1.0, saturation * intensity, brightness)
                    effect_hue_offset += effect_speed/5

                elif current_effect == 2:  # Pulsing
                    intensity=map_range(effect_intensity[current_effect],0,1,0.3,1.0)
                    pulsing_brightness = 0.5 + 0.5 * math.sin(effect_timer * 50) * intensity
                    np27[i] = hsv_to_rgb(hue, saturation, pulsing_brightness)

                elif current_effect == 3:  # Wave Effect
                    intensity=map_range(effect_intensity[current_effect],0,1,0.2,6)
                    wave_brightness = 0.5 + 0.8 * math.sin((i / NUM_PIXELS) * 2 * math.pi *intensity + effect_timer * 200)
                    if wave_brightness<0:
                        wave_brightness=0
                    elif wave_brightness>1:
                        wave_brightness=1
                    np27[i] = hsv_to_rgb(hue, saturation, wave_brightness)

                elif current_effect == 4:  # Wave Effect
                    intensity=map_range(effect_intensity[current_effect],0,1,0.2,6)
                    wave_brightness = 0.5 + 0.8 * math.sin((i / NUM_PIXELS) * 2 * math.pi*intensity + effect_timer * 200)
                    if wave_brightness<0:
                        wave_brightness=0
                    elif wave_brightness>1:
                        wave_brightness=1
                    np27[i] = hsv_to_rgb((effect_hue_offset + (i / NUM_PIXELS)) % 1.0, saturation, wave_brightness)
                    effect_hue_offset += effect_speed

                elif current_effect == 5:  # Random Blink
                    intensity=map_range(effect_intensity[current_effect],0,1,0.3,0.01)
                    if random.random() < intensity:
                        np27[i] = hsv_to_rgb(hue, saturation, brightness)
                    else:
                        np27[i] = hsv_to_rgb(hue, saturation, 0)
                
    np.write()
    np27.write()
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
    global control_mode, all_pressed_start_time

    device.update()
    current_time = time.time()

    hue_mode_button=device.level(1)
    brightness_speed_button=device.level(0)
    saturation_intensity_button=device.level(2)

    all_pressed = all(x > detection_level for x in (hue_mode_button, brightness_speed_button, saturation_intensity_button))
    
    if all_pressed:
        # Track when all buttons are pressed
        if all_pressed_start_time < 0:
            all_pressed_start_time = current_time
        
        # Long press: toggle effect mode (0.5 seconds)
        if current_time - all_pressed_start_time > long_press_threshold:
            if last_tap < all_pressed_start_time:  # Ensure we only toggle once per press
                effect_mode = not effect_mode
                print("effect mode: " + str(effect_mode))
                last_tap = current_time
    else:
        # All buttons released
        if all_pressed_start_time >= 0:
            press_duration = current_time - all_pressed_start_time
            # Short tap (less than long_press_threshold): cycle control mode
            if press_duration < long_press_threshold:
                control_mode = (control_mode + 1) % 3
                modes = ["both", "pin 29", "pin 27"]
                print("control mode: " + modes[control_mode])
            all_pressed_start_time = -1
    
    if not all_pressed:
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
                if current_time - last_tap > 0.3:  # Tap to cycle effects
                    current_effect = (current_effect + 1) % 6
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
