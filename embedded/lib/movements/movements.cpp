#include <Arduino.h>

#include "defines.h"
#include "movements.h"

void move_y_axis(Servo &tilt_servo, int &tilt_angle, char movement){
    switch (movement){
        case 'b':
            // Serial.println("Move down");
            if(tilt_angle + 1 <= 60){
                tilt_angle += 1;
                tilt_servo.write(tilt_angle);
            }
            break;
        case 'c':
            // Serial.println("Move up");
            if(tilt_angle - 1 >= 0){
                tilt_angle -= 1;
                tilt_servo.write(tilt_angle);
            }
            break;
    }
}

void move_x_axis(char movement){

    switch(movement){
        case 'd':
            // Serial.println("Rotate clockwise");
            digitalWrite(ROTATION_D1, HIGH);
            digitalWrite(ROTATION_D2, LOW);
            delay(2);
            digitalWrite(ROTATION_D1, LOW);
            digitalWrite(ROTATION_D2, LOW);
            break;
        case 'e':
            // Serial.println("Rotate counter-clockwise");
            digitalWrite(ROTATION_D1, LOW);
            digitalWrite(ROTATION_D2, HIGH);
            delay(2);
            digitalWrite(ROTATION_D1, LOW);
            digitalWrite(ROTATION_D2, LOW);
            break;
    }
}

void shoot(Servo &shoot_servo){
    // Serial.println("Shoot!");
    shoot_servo.write(90);
    delay(200);
    shoot_servo.write(0);
}

void toggle_impulse(char impulse_on){
    if(impulse_on == 'o'){
        // Serial.println("Impulse off");
        digitalWrite(IMPULSE_D1, LOW);
        digitalWrite(IMPULSE_D2, LOW);
        // impulse_on = false;
    } else if(impulse_on == 'O'){
        digitalWrite(IMPULSE_D1, LOW);
        analogWrite(IMPULSE_D2, 200);
        // digitalWrite(IMPULSE_D2, HIGH);
        // impulse_on = true;
    }
}