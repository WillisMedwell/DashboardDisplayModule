# Dashboard Display Module
The *Racecar DashBoard Display Module* is a unit to replace the car mirrors and displays the car performance to the driver. This module interfaces between a screen and multiple cameras using a raspberry pi. 
  This is for a semseter long "capstone" project for [Swinburne University](https://www.swinburne.edu.au/study/courses/units/Electrical-Integrated-Design-Project-EEE30005/international) 

## Requirements
- [X] Speedometer
- [X] Clock
- [ ] Side and Back mirror options
- [ ] Safety Information

### Current Known Issues
N/A

### Team Members
Willis Medwell [Personal Email](medwellwillis@gmail.com) ([Student Emaai](102567073@student.swin.edu.au))\
Daniel Failla [Personal Email](danielfailla4@gmail.com) ([Student Email](103191554@student.swin.edu.au))\
Giacomo Fantin [Personal Email](giacomofantin00@gmail.com) ([Student Email](103072015@student.swin.edu.au))\

### Versions
#### 1.04 OpenCV Camera
In progress...
#### 1.03 Pygame Demo
After poor performance on the Raspberry Pi, Willis changed the GUI from Tkinter to Pygame. This tripled the performance.
|           | Tkinter | Pygame |
|-----------|---------|--------|
| Time (ms) | 3.536   | 1.053  |
| Freq (Hz) | 282.8   | 949.7  |
<img src="/progress/103.gif" height="300">

#### 1.02 Tkinter in Realtime\
Willis improved Daniel's demo by making the mainloop dynamic instead of controlled by Tkinter. Also added gif and png shapes.\
<img src="/progress/102.png" height="300">

#### 1.01 Tkinter Demo\
Daniel created and implemented a working prototype that had a working speedometer, rpm, range and more.\
<img src="/progress/101.png" height="300">

#### 1.00 Requirements and Project Setup\
First commit laying out project brief and introducing members to the git/github process\