# THRUST RIG
The Thrust Rig is used to test the thrust from different motor propeller combinations.

## Hardware Required
i)   HX711 Weight Sensor Module

ii)  5Kg Load Cell

iii) Raspberry Pi

iv)  Brushless DC Motor

v)   Propellers

vi)  Electronic Speed Controllers

vii) Push Button

## Assembling the hardware
### Connecting the HX711 Weight Sensor Module to Raspberry Pi
i)    VCC to Raspberry Pi Pin 2 (5V)
 
ii)   GND to Raspberry Pi Pin 6 (GND)

iii)  DT to Raspberry Pi Pin 29 (GPIO 5)

iv)   SCK to Raspberry Pi Pin 31 (GPIO 6)

### Connecting the ESC to the Raspberry Pi
Note: Do not connect the 5v pin to the Raspberry PI
i) Black pin to GND

ii) Yellow Pin to Pi Pin 7 (GPIO 4)

### Connecting the ESC to the Motor

## Running the files
Clone the repository using the command below
```bash
$git clone https://github.com/RogeK/Thrust_Rig.git
```

Navigate to the src directory

The mass of the motor and the propeller may affect the accuracy of your reading. To prevent this, run the example.py file and press the push button. The value of the readings will be set to 0.

To run the example.py file, run the command below
```bash
python3 example.py
```
Once the value of the readings have been set to 0, exit the program by pressing ctrl + c keys. You can now start testing the thrust of the motor by running the command below

```bash
python3 start3.py
```
The thrust values are written to the Thrust_Values.csv file in the src directory


## License
[MIT](https://choosealicense.com/licenses/mit/)
