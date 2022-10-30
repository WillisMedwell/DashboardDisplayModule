# Dashboard Display Module
The *Racecar DashBoard Display Module* is a unit to replace the car mirrors and displays the car performance to the driver. This module interfaces between a screen and multiple cameras using a raspberry pi. 
  This is for a semseter long "capstone" project for [Swinburne University](https://www.swinburne.edu.au/study/courses/units/Electrical-Integrated-Design-Project-EEE30005/international) 

## Requirements
- [X] Speedometer
- [X] Clock
- [ ] Side and Back mirror options
- [ ] Safety Information

### Requirements
#### The project needs the following software installed...
1. update Rpi system
  > sudo apt update
2.python & pip
  >sudo apt install python<br>
  >sudo apt install python-pip
3. numpy 
  >pip install numpy
4. pygame 
  >pip install python-pygame
5. openCV 
  >pip install python-opencv
#### The project needs the following hardware avaliable...
1. RPi4 (unsure of previous versions are compatible)
2. 3 USB cameras connected
3. Display output (the target device was 1280 x 400)

### Team Members
Willis Medwell [Personal Email](medwellwillis@gmail.com) ([Student Email](102567073@student.swin.edu.au))\
Daniel Failla [Personal Email](danielfailla4@gmail.com) ([Student Email](103191554@student.swin.edu.au))\
Giacomo Fantin [Personal Email](giacomofantin00@gmail.com) ([Student Email](103072015@student.swin.edu.au))

### Versions
#### 1.07 Design Updates
Final result on RPi4
<br><img src="/progress/107.jpg" height="480" width = "640">

#### 1.06 Design Updates
Daniel Revamped the design to look slick.
<br><img src="/progress/106.png" height="200" width = "640">

#### 1.05 Image Detection
Due to the OpenCV library, we were able to integrate machine vision using a trained model (XML).
<br><img src="/progress/105.gif" height="200" width = "640">

#### 1.04 OpenCV Camera
Camera Support! Each camera runs on their own thread and each image is read from alternating buffers for thread safety.
This works out perfectly as we need support for 3 cameras and the RPi4 has 4 cores... (3 camera threads and 1 main thread).
<br><img src="/progress/104.gif" height="200" width = "640">
#### 1.03 Pygame Demo
After poor performance on the Raspberry Pi, Willis changed the GUI from Tkinter to Pygame. This tripled the performance.
|  Desktop  | Tkinter | Pygame |
|-----------|---------|--------|
| Time (ms) | 3.536   | 1.053  |
| Freq (Hz) | 282.8   | 949.7  |

|  RPi4     | Tkinter | Pygame |
|-----------|---------|--------|
| Time (ms) | 24.44   | 40.92  |
| Freq (Hz) | 4.711   | 212.6  |
* From 40 fps to 200 fps (on the target device) was a major and neccessary improvement.
<img src="/progress/103.gif" height="200" width = "600">

#### 1.02 Tkinter in Realtime
Willis improved Daniel's demo by making the mainloop dynamic instead of controlled by Tkinter. Also added gif and png shapes.
<br><img src="/progress/102.png" height="200" width = "600">

#### 1.01 Tkinter Demo
Daniel created and implemented a working prototype that had a working speedometer, rpm, range and more.
<br><img src="/progress/101.png" height="200" width = "600">

#### 1.00 Requirements and Project Setup
First commit laying out project brief and introducing members to the git/github process\