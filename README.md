# Image Share
This project is a minimalistic desktop application designed to send and receive images via two modes: Sender and Catcher

## Installation Guide

**The first way**
1. Clone the repository to your local device: `https://github.com/Niksha36/image_share.git`
2. Create a new virtual environment
3. Install dependencies with the command: `pip install -r requirements.txt`
4. Run the script `ImageShareApp.py` on the devices you want to exchange images with

**The second way**\
Install the files `ImageShareApp.exe` on both devices and run them


## Assembly .exe file

To build the project yourself:
1. install the .exe file library `pyinstaller`
2. use the command: `pyinstaller --onefile ImageShareApp.py`

**If icons or fonts are not displayed correctly, replace the field `datas` in the relevant `.spec` file to the following lines:**

`datas=[
        ('drawables/app_icon.png', 'drawables'),
        ('drawables/icon_back.png', 'drawables'), 
        ('fonts/Roboto-Regular.ttf', 'fonts')
    ],`


## Developers

[Ganzha Eduard](https://github.com/deep-learning-engineer) Б9123-01.03.02сп\
[Shurlo Nikita](https://github.com/Niksha36) Б9123-01.03.02сп 
