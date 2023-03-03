import tkinter as tk
import customtkinter as ctk
from PIL import Image,ImageTk,ImageGrab
import cv2
import numpy as np
import rbc_estimation
import colordetection as cd

class Gui:

    def __init__(self):
        ctk.set_default_color_theme("dark-blue")
        ctk.set_appearance_mode("dark")
        self.root = ctk.CTk()
        self.selectedFile = None
    
    def configure_root(self):
        self.root.title('Red Blood Cell analyzer')
        self.root.resizable(False, False)
        self.root.geometry('600x600')

        for i in range(3):
            self.root.columnconfigure(i, weight=1)
            self.root.rowconfigure(i, weight=1)
        ## geometry of the window
    
    def canvas(self):
        self.canvas = ctk.CTkCanvas(self.root, width = 400, height = 400)
        self.canvas.grid(row = 1, column = 1)
        self.canvas.config(highlightthickness = 0, borderwidth = 0)

    def update_canvas(self):
        self.img = Image.open(self.selectedFile)
        self.img = self.img.resize((400, 400), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(200, 200, image = self.img) 
        ## create_image arguments should be half of resize arguments
        ## 400/2 = 200

    def select_button(self):
        def select_file():
            filetypes = (
                ('jpeg files', '*.jpg'),
                ('All files', '*.*') )

            self.selectedFile = tk.filedialog.askopenfilename(
                title = 'Choose an image',
                initialdir = '/',
                filetypes  = filetypes )

            self.update_canvas()
            return
        
        open_button = ctk.CTkButton(
            self.root,
            text = 'Choose an image to analyze',
            command = select_file)

        open_button.grid(column = 1, row = 0)

    def proceed_button(self):
        def proceed():
            newWindow = chooseBackgroundGUI(self.root, self.selectedFile)
            newWindow.run()
            return
        
        run_button = ctk.CTkButton(
            self.root,
            text = 'Proceed with chosen image',
            command = proceed)
        
        run_button.grid(column = 1, row = 2)

    def run(self):
        self.canvas()
        self.configure_root()
        self.select_button()
        self.proceed_button()
        self.root.mainloop()


class chooseBackgroundGUI:

    def __init__(self,root,selectedFile):
        self.root = root
        self.nextWindow = ctk.CTkToplevel()
        self.selectedFile = selectedFile
        self.topx, self.topy, self.botx, self.boty = 0, 0, 0, 0
        self.rect_id = None

    def configure_root(self):
        self.nextWindow.title('Red Blood Cell analyzer')
        self.nextWindow.resizable(False, False)
        self.nextWindow.geometry('600x600')
        self.nextWindow.wm_attributes("-topmost", True) ## lift to front
        for i in range(3):
            self.nextWindow.columnconfigure(i, weight=1)
            self.nextWindow.rowconfigure(i, weight=1)
        
    def canvas(self):
        self.canvas = ctk.CTkCanvas(self.nextWindow, width = 400, height = 400)
        self.canvas.grid(row = 1, column = 1)
        self.canvas.config(highlightthickness = 0, borderwidth = 0)

        self.img = Image.open(self.selectedFile)
        self.img = self.img.resize((400, 400), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(200, 200, image = self.img)
        self.canvas.theimage = self.img # without this line, the canvas appears blank because of G-collector

        def get_mouse_posn(event):
            self.topx, self.topy = event.x, event.y

        def update_sel_rect(event): # Update selection rectangle
            self.botx, self.boty = event.x, event.y
            self.canvas.coords(self.rect_id, self.topx, self.topy, self.botx, self.boty)
        
        self.rect_id = self.canvas.create_rectangle(self.topx, self.topy, self.topx, self.topy,
            dash = (2,2), fill = '', outline = 'white')
        
        self.canvas.bind('<Button-1>', get_mouse_posn)
        self.canvas.bind('<B1-Motion>', update_sel_rect)
    
    def run_button(self):
   
        def button_logic():
            true_topx = min(self.topx,self.botx)
            true_botx = max(self.topx,self.botx)
            true_topy = min(self.topy,self.boty)
            true_boty = max(self.topy,self.boty)
            # rectangle can be drawn into 4 cardinal directions,
            # eg. from to topleft to botright or from botleft to topright
            # this makes sure that every direction works

            box = ( self.canvas.winfo_rootx() + true_topx,
                    self.canvas.winfo_rooty() + true_topy,
                    self.canvas.winfo_rootx() + true_botx,
                    self.canvas.winfo_rooty() + true_boty)
            ## rectangle coords created by user

            grabbedImage = ImageGrab.grab(bbox = box)
            ## get image bounded by coords

            grabbedImageToNpArray = np.array(grabbedImage)
            grabbedImageCV = cv2.cvtColor(grabbedImageToNpArray, cv2.COLOR_RGB2BGR)
            ## convert PIL image to openCV image

            backgroundAnalyzer = cd.BackgroundColorDetector(grabbedImageCV)
            background = backgroundAnalyzer.detect()
            ## background color by analyzing image

            lastGUI = analyzeGUI(self.selectedFile, background)
            lastGUI.run()
            self.nextWindow.destroy()
            ## create new window, get rid of current one
        
        run_button = ctk.CTkButton(
            self.nextWindow,
            text = 'Proceed with chosen background',
            command = button_logic )
        
        run_button.grid(row = 2, column = 1)

    def instructions_label(self):
        label = ctk.CTkLabel(self.nextWindow)
        label.configure(text = """Firstly click and then drag on the image
            to select background area (rectangle without any cells),
            then click the button to proceed""")
        
        label.grid(row = 0, column = 1)
                            
    def run(self):
        self.configure_root()
        self.run_button()
        self.canvas()
        self.instructions_label()






class analyzeGUI:

    def __init__(self,selectedFile,background):
        self.lastWindow = ctk.CTkToplevel()
        self.background = background
        self.selectedFile = selectedFile
        self.images = None
        self.img = None

        self.buttonVar = ctk.StringVar(value = "7")
        self.backgroundVar = tk.DoubleVar()
        self.iterationsVar = tk.IntVar()
        ## variables from sliders and segmented button

        self.RBC_count = 0
        self.RBC_string = ctk.StringVar()
    def configure_root(self):
        self.lastWindow.title('Red Blood Cell analyzer')
        self.lastWindow.resizable(False, False)
        self.lastWindow.geometry('900x900')
        for i in range(8):
            self.lastWindow.rowconfigure(i, weight=1)
        for i in range(5):
            self.lastWindow.columnconfigure(i, weight=1)

    def canvas(self):
        self.Canvas = ctk.CTkCanvas(self.lastWindow, width = 600, height = 600)
        self.Canvas.grid(row = 3, column = 2)
        self.Canvas.config(highlightthickness = 0, borderwidth = 0)

    def openCV_to_PIL(self,image): ## convert openCV image to PIL image
        openCV =  cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        temp = Image.fromarray(openCV)
        temp = temp.resize((600, 600), Image.ANTIALIAS)
        PIL_img = ImageTk.PhotoImage(temp)
        return PIL_img

    def get_images(self):
        self.analyzer = rbc_estimation.RBC_analyzer(
                imagePath = self.selectedFile,
                background = self.background,
                threshold  = self.backgroundVar.get(),
                erodeIterations = self.iterationsVar.get() )
        
        self.images , self.RBC_count  = self.analyzer.analyze_rbc()
        self.RBC_string.set(f"red blood cell count\n { round(self.RBC_count) }")
        
        self.images = [self.openCV_to_PIL(image) for image in self.images]
        ## convert images from analyzer to PIl format

        self.img = self.images[ int( self.buttonVar.get() ) ]
        self.Canvas.create_image(300, 300, image = self.img) 
        self.Canvas.theimage = self.img

    def run_button(self):
        Button = ctk.CTkButton( self.lastWindow,
            text    = 'Count Red Blood Cells!',
            command = self.get_images )
        
        Button.grid(row = 7, column = 2)

    def segmented_button(self):
        def segmented_button_callback(value):
            self.img = self.images[ int(value) ]
            self.Canvas.create_image(300, 300, image = self.img) 
            self.Canvas.theimage = self.img
            return

        Segmented_button = ctk.CTkSegmentedButton(
            master   = self.lastWindow,
            values   = [ f"{index}" for index in range(8) ],
            command  = segmented_button_callback,
            variable = self.buttonVar )
        
        Segmented_button.grid(column=2,row=4)

    def slider_background(self):
        slider_background = tk.Scale(self.lastWindow,
            from_= 0, to = 0.3,
            resolution = 0.01,
            variable = self.backgroundVar,
            orient = 'horizontal',
            label  = "Background devation",
            length = 200)
        
        slider_background.set(0.1)
        slider_background.grid(row = 5, column = 2)

    def slider_iteratins(self):
        slider_iterations = tk.Scale(self.lastWindow,
            from_ = 1, to = 10,
            resolution = 1,
            variable = self.iterationsVar,
            orient = 'horizontal',
            label  = "Erode iterations",
            length = 200)
        
        slider_iterations.set(1)
        slider_iterations.grid(row = 6, column = 2)

    def rbc_text_field(self):
        label = ctk.CTkLabel(master = self.lastWindow,
            textvariable = self.RBC_string,
            width  = 120,
            height = 50,
            font   = ("Cambria", 30),
            corner_radius = 8)
        
        label.grid(row = 1, column = 2)

    def run(self):
        self.configure_root()
        self.canvas()
        self.run_button()
        self.segmented_button()
        self.slider_background()
        self.slider_iteratins()
        self.get_images()
        self.rbc_text_field()
    
    
