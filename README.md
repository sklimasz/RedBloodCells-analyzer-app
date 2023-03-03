# Red blood cell analyzer app in Python

Estimate number of red blood cells in given image using openCV. Quickly go through the process using GUI tkinter app. Easily change estimation parameters in the app.

# Requirements
- openCV
- numpy
- tkinter
- customtkinter
- PIL

# How to use
## First Window

<p align="center">
<img src="https://user-images.githubusercontent.com/80223720/222794970-6fe9cff8-c31a-4af8-bcc9-2aea103dd30c.png">  
<p align>

Click on the "choose an image to analyze" button
<p align="center">
<img src="https://user-images.githubusercontent.com/80223720/222795198-b0693643-d832-416f-a77f-fb9a057b96a3.png">  
<p align>
Then choose a file and open it
and click on the "Proceed with chosen image" button

## Second Window

<p align="center">
<img src="https://user-images.githubusercontent.com/80223720/222795568-7d76f37b-58de-4ef7-8ceb-2da27d118c90.png">  
<p align>

In the next window you have to click and drag on the image  
to create rectangle boxing background of the image  
There should not be any cells in the rectangle  
You should also try to create biggest rectangle possible   
  
Incorrect rectangle
<p align="center">
<img src="https://user-images.githubusercontent.com/80223720/222796200-838a5464-16b0-454b-b055-213dfa87f610.png"> 
<p align>

Correct rectangle
<p align="center">
<img src="https://user-images.githubusercontent.com/80223720/222796278-c79288b5-3790-467e-8201-e68560372301.png"> 
<p align>


## Final Window
<p align="center">
<img src="https://user-images.githubusercontent.com/80223720/222797857-c2628806-e741-4dbd-b511-048e2a908417.png"> 
<p align> 

Above the image you can see the estimation of the number of red blood cells  
<p align="center">
<img src="https://user-images.githubusercontent.com/80223720/222797921-4fbe3c0a-e5fe-42d6-8688-cc791612976f.png"> 
<p align> 
  
  
Sliders allow you to change the parameters of the estimation  
<p align="center">
<img src="https://user-images.githubusercontent.com/80223720/222798157-0513f084-2326-4fcb-8517-57835bfd287f.png"> 
<p align> 
        
  
Different contour colors indicate different number of cells in a cluster  
<p align="center">
<img src="https://user-images.githubusercontent.com/80223720/222798984-d2f5e79c-58ff-414f-96a3-8bed92231734.png"> 
<p align> 
  
You can see partial images by using buttons numbered 0-7  
Counting algorithm and partial images explained in rbc_estimation.py  
Partial image 1 ( white blood cells removed ) 
<p align="center">
<img src="https://user-images.githubusercontent.com/80223720/222804105-8060e695-4106-4188-b6b0-e64dcefce3e3.png"> 
<p align> 
  
To choose correct parameters look at image 6  
It is the last step and should give most insight  
  
Incorrect parameters  
<p align="center">
<img src="https://user-images.githubusercontent.com/80223720/222803592-886caf71-4c4c-4047-9971-d28404fece0d.png"> 
<p align> 

Correct parameters  
<p align="center">
<img src="https://user-images.githubusercontent.com/80223720/222803418-01debe5f-7064-45c7-a9d4-4e55d9cd70fe.png"> 
<p align> 

Area of one blood cell depends on the resolution of images  
Change self.AreaOfOneBlood cell if things dont work right  
You can also change the counting logic  
<p align="center">
<img src="https://user-images.githubusercontent.com/80223720/222804849-8d5d1cbd-2742-4b1f-852a-e9e21fc144d4.png"> 
<p align> 
  rbc_estimation.py







