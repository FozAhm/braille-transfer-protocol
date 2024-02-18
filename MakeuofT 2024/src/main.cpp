#include "Arduino.h"
#include <ESP32Servo.h>

Servo gantry, puncher, wheel;
int forward = 60;
int backward = 140;
int stop = 90;

void setup()
{
  Serial.begin(115200);
  // Allow allocation of all timers
  ESP32PWM::allocateTimer(0);
  ESP32PWM::allocateTimer(1);
  ESP32PWM::allocateTimer(2);
  ESP32PWM::allocateTimer(3);
}

void loop()
{
  if (!gantry.attached())
  {
    gantry.setPeriodHertz(50);  // standard 50 hz servo
    gantry.attach(33, 0, 2500); // Attach the servo after it has been detatched
    // gantry slows from 60. stops at 100. reverses direction and max speed at 140
  }

  if (!wheel.attached())
  {
    wheel.setPeriodHertz(50);    // standard 50 hz servo
    wheel.attach(32, 500, 2500); // Attach the servo after it has been detatched
  }

  if (!puncher.attached())
  {
    puncher.setPeriodHertz(400);   // standard 50 hz servo
    puncher.attach(25, 500, 2500); // Attach the servo after it has been detatched
    // 500 to 2500 sets the angle
  }

  // take picture
  gantry.write(forward);
  delay(2000);
  gantry.write(stop);
  delay(3000);

  // puncture
  gantry.write(forward);
  delay(2500);
  gantry.write(stop);
  delay(3000);

  // return
  gantry.write(backward);
  delay(4500);
  gantry.write(stop);
  delay(3000);

  // puncher.write(1600); // 2400 low, 1500 high

  // delay(1000);

  // puncher.write(1980); // 2400 low, 1500 high. dont go higher than 1900

  // delay(1000);
}