#include <Arduino.h>
#include <HID-Project.h>

#define IN_AXIS_PIN					A0
#define EX_AXIS_PIN					A1
#define BUTTON_PIN					A2
#define LED_PIN						2

#define SERIAL_BAUDRATE				115200
#define AXIS_MIN_VALUE				1023
#define AXIS_MAX_VALUE				0

#define JOYSTICK_INTERVAL_MS		20
#define JOYSTICK_BUTTON_ID			1
#define JOYSTICK_MAX_AXIS_VALUE		0x7FFF

uint32_t next_joystick_ms = 0;


uint16_t get_axis_value(uint8_t pin)
{
	return map(analogRead(pin), AXIS_MIN_VALUE, AXIS_MAX_VALUE, 0, JOYSTICK_MAX_AXIS_VALUE);
}

void setup()
{
	// Serial.begin(SERIAL_BAUDRATE);

	pinMode(BUTTON_PIN, INPUT_PULLUP);
	pinMode(LED_PIN, OUTPUT);

	Gamepad.begin();
}

void loop()
{
	uint32_t cur_ms = millis();

	if (next_joystick_ms <= cur_ms) {
		next_joystick_ms = cur_ms + JOYSTICK_INTERVAL_MS;
		digitalWrite(LED_PIN, !digitalRead(LED_PIN));
		Gamepad.releaseAll();
		if (!digitalRead(BUTTON_PIN))
			Gamepad.press(JOYSTICK_BUTTON_ID);
		// Serial.print("analog: ");
		// Serial.println(analogRead(EX_AXIS_PIN));
		Gamepad.xAxis(get_axis_value(EX_AXIS_PIN));
		Gamepad.yAxis(get_axis_value(IN_AXIS_PIN));
		Gamepad.write();
	}
}
