#include <Arduino.h>
#include <Servo.h>

#include "defines.h"
#include "movements.h"

Servo tilt_servo;
Servo shoot_servo;

int tilt_angle = INITIAL_TILT_ANGLE;


void setup() {
    pinMode(TILT_SERVO_PIN, OUTPUT);
    pinMode(SHOOT_SERVO_PIN, OUTPUT);
    pinMode(ROTATION_D1, OUTPUT);
    pinMode(ROTATION_D2, OUTPUT);
    pinMode(IMPULSE_D1, OUTPUT);
    pinMode(IMPULSE_D2, OUTPUT);

    tilt_servo.attach(TILT_SERVO_PIN);
    shoot_servo.attach(SHOOT_SERVO_PIN);

    Serial.begin(9600);
    Serial.println("Turret ready!");

    tilt_servo.write(INITIAL_TILT_ANGLE);
    shoot_servo.write(0);

    digitalWrite(ROTATION_D1, LOW);
    digitalWrite(ROTATION_D2, LOW);
    digitalWrite(IMPULSE_D1, LOW);
    digitalWrite(IMPULSE_D2, LOW);

    
}

void loop() {
    if(Serial.available()){
        char movement = Serial.read();

        if(movement == 'c' || movement == 'b'){
            move_y_axis(tilt_servo, tilt_angle, movement);
        } else if(movement == 'e' || movement == 'd'){
            move_x_axis(movement);
        } else if(movement == 's'){
            shoot(shoot_servo);
        } else if(movement == 'o' || movement == 'O'){
            toggle_impulse(movement);
        }
        
        Serial.flush();
    }
}