# NeoLamp

NeoLamp is a customizable RGB LED ring lamp powered by an RP2040 Zero microcontroller, housed in a 3D-printed chassis. It features capacitive touch controls for adjusting brightness, saturation, and hue, along with a special effect mode for dynamic lighting patterns.

## Features
- **RGB NeoPixel Ring:** Uses a 12-LED addressable NeoPixel ring.
- **Capacitive Touch Controls:** Three buttons control:
  - Brightness
  - Saturation
  - Hue (loops continuously)
- **Effect Mode:**
  - Activated by pressing all three buttons simultaneously.
  - Brightness button adjusts effect speed.
  - Saturation button adjusts effect intensity.
  - Hue button cycles through various effects.
- **Effects Available:**
  1. Rainbow Spin
  2. Rainbow Cycle
  3. Pulsing
  4. Wave Effect (single hue)
  5. Wave Effect (color shift)
  6. Random Blink
- **Smooth Cycling:** Holding a button continuously cycles the parameter from min to max and vice versa.

## Hardware
- **MCU:** RP2040 Zero
- **LEDs:** WS2812B NeoPixel ring
- **Wiring** Logic level shifter to 5V
- **3D Printed Enclosure** with bolts used as the capacitive buttons

## Installation
1. **Flash Firmware:** Upload the provided MicroPython script to your RP2040 Zero.
2. **Connect Components:**
   - **NeoPixel Ring:** GPIO14 (Data)
   - **Capacitive Buttons:**
     - Brightness: GPIO0
     - Saturation: GPIO8
     - Hue: GPIO4
3. **Power On:** The NeoLamp should at zero brightness and zero saturation

## Usage
### Manual Mode
- **Brightness:** Tap to adjust, hold to continuously cycle.
- **Saturation:** Tap to adjust, hold to cycle.
- **Hue:** Tap to adjust (loops through colors).

### Effect Mode
- **Activate:** Press all three buttons simultaneously.
- **Controls:**
  - Brightness -> Adjusts effect speed.
  - Saturation -> Adjusts effect intensity.
  - Hue -> Cycles through different effects.
- **Exit Effect Mode:** Press all three buttons again.

## Potential Customization
- Modify or add effects in the `update_neopixels()` function.
- Adjust button sensitivity in `process_touch_inputs()`.
- Change pin mapping
- Adjust rate of change when holding buttons

## Acknowledgments
- **jtouch Library:** Modified version of [AncientJames's jtouch](https://github.com/AncientJames/jtouch/blob/main/jtouch.py)

## License
This project is open-source. Feel free to modify and improve!


