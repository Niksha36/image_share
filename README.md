# Image Share

This project is a minimalistic desktop application designed to send and receive images via two modes: Sender and Catcher
=======
This project is a minimalistic desktop application designed to send and receive images & files via two modes: Sender and Catcher. You can open and check image or file by clicking on file icon and check it before sending it. In catcher mode you can see received image and you have opitons set this image as desctop background or go to the file in windows explorer. We have tryed to prevent any unexpected behavior like you can not set file as desctop background or send nothing. Each and every step was thought out and user will be notified about errors and problems.

# Features that were applyed in this project
1) GUI Framework: Tkinter

2) Networking: Sockets (for client-server communication)

3) Threading: Python's threading module

4) Image Processing: PIL (Pillow)

5) File Handling: Standard Python file operations

6) System Operations: ctypes for setting desktop background, os for file operations

7) IP Address Handling: psutil and ipaddress modules

8) Packaging: PyInstaller 

## User interface
**Main window**
</p>
        <img src="https://github.com/user-attachments/assets/bbc6093b-bac3-4656-a888-9bef4c9d11f9" alt="1" style="width: 50%; height: auto;"/>
</p>

**Sender mode**
</p>
        <img src="https://github.com/user-attachments/assets/89c41cee-f3a0-406e-88ad-3ed287f501c5" alt="2" style="width: 50%; height: auto; display: inline-block;"/>
        <img src="https://github.com/user-attachments/assets/e51e89a5-4368-4f2f-80f7-b46aedc92c61" alt="3" style="width: 50%; height: auto; display: inline-block;"/>
        <img src="https://github.com/user-attachments/assets/24bb0a0e-fa4d-46d7-aae5-5231bdb2b40c" alt="4" style="width: 50%; height: auto; display: inline-block;"/>
</p>

**Catcher mode**
</p>
        <img src="https://github.com/user-attachments/assets/a7a20960-4a5a-46e3-8cd5-08e34a9d235c" alt="5" style="width: 50%; height: auto;"/>
        <img src="https://github.com/user-attachments/assets/44657081-2c85-4b68-981b-65d314469be4" alt="6" style="width: 50%; height: auto;"/>
        <img src="https://github.com/user-attachments/assets/8d30e10c-058b-4ae2-aacb-bcae8bcc1a74" alt="7" style="width: 50%; height: auto;"/>
        <img src="https://github.com/user-attachments/assets/57bc19f3-311e-471d-9245-ea1d541ef6cf" alt="8" style="width: 50%; height: auto;"/>
</p>

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
2. use the command: `pyinstaller --onefile -w --add-data=".\drawables\*;." --add-data=".\fonts\*;."  ImageShareApp.py`


## Developers

[Ganzha Eduard](https://github.com/deep-learning-engineer) Б9123-01.03.02сп\
[Shurlo Nikita](https://github.com/Niksha36) Б9123-01.03.02сп 

=======


