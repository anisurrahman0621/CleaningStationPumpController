# CleaningStationPumpController
## About
Application used to control pump in weather testing station. There are 3 different modes: timer, oscillating, and continuous.
Timer mode takes a time and power input from the user and outputs a corresponding signal to the arduino mapped from 0-100% to 0-5V. At any point during the operating time, the user can adjust the power by moving the scale at the bottom left of the application window or by entering a value in the entry field or shut the pump off immediately.
The continuous mode is similar to the timer mode except that it only takes a power input and runs until the user stops the pump using the "Shutoff" button.
Then oscillating mode takes 4 inputs from the user-- time on, time off, power level, and number of oscillations. 

## Future Plans
Additional functionality will be added. Currently, the stepper motors to position test samples are run using a different GUI. The goal is to have both GUIs combined so that everything can be controlled from one applicaiton.
