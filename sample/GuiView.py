import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import ImageTk, Image
import ArucoModel as am

from multiprocessing import Process, Queue


class View(tk.Frame):
    """ View Module Class """

    def __init__(self, parent):
        # Create and initialize widgets and frames
        
        tk.Frame.__init__(self,parent)
        self.parent = parent # Parent Frame Object pass when constructor is used -> the ttk.root is expected
        self.frame_padding = 3
        self.DataBlockMinedCounter = 0 # count blocks pressed

        #========= Img Path Defintions =========#
        self.img0 = ImageTk.PhotoImage(Image.open(am.img_0_path).resize((100,100)))
        self.img1 = ImageTk.PhotoImage(Image.open(am.img_1_path).resize((100,100)))
        self.img2 = ImageTk.PhotoImage(Image.open(am.img_2_path).resize((100,100)))
        self.img3 = ImageTk.PhotoImage(Image.open(am.img_3_path).resize((100,100)))
        self.img4 = ImageTk.PhotoImage(Image.open(am.img_4_path).resize((100,100)))
        self.img5 = ImageTk.PhotoImage(Image.open(am.img_5_path).resize((100,100)))
        self.img6 = ImageTk.PhotoImage(Image.open(am.img_6_path).resize((100,100)))
        self.img7 = ImageTk.PhotoImage(Image.open(am.img_7_path).resize((100,100)))
        self.img8 = ImageTk.PhotoImage(Image.open(am.img_8_path).resize((100,100)))
        self.img9 = ImageTk.PhotoImage(Image.open(am.img_9_path).resize((1280,720)))
        self.img10 = ImageTk.PhotoImage(Image.open("sample\images\mc_cobblestone.png").resize((100,100)))

        #========== Frame Definitions ==========#
        self.OpenCVFrame = ttk.Frame(
            master=self.parent,
            padding=self.frame_padding,
            relief="raised"
            )
        self.OpenCVFrame.grid(
            row=0,
            column=1,
            rowspan=3,
            sticky=NSEW,
        )


        # Top level Menu Frame
        self.TopLevelMenuFrame = ttk.Frame(
            master=self.parent,
            padding=self.frame_padding,
            relief="raised"
        ).grid(
            row=0,
            column=0,
            sticky=NSEW
        )
        

        self.MenuTop = ttk.Frame(master=self.TopLevelMenuFrame, padding=self.frame_padding, relief="raised")
        self.MenuTop.grid(
            row=0,
            column=0,
            sticky=NSEW
        )

        self.MenuMiddle = ttk.Frame(master=self.TopLevelMenuFrame, padding=self.frame_padding, relief="raised")
        self.MenuMiddle.grid(
            row=1,
            column=0,
            sticky=NSEW
        )

        self.MenuBottom  = ttk.Frame(master=self.TopLevelMenuFrame, padding=self.frame_padding, relief="raised")
        self.MenuBottom.grid(
            row=2,
            column=0,
            sticky=NSEW
        )

        #============ Widget Definitions =========#
        # Top Menu Widgets
        self.MenuTopText = ttk.Label(
            master=self.MenuTop,
            text=r"Select the block that you would like to data mine!"
        )
        self.MenuTopText.grid(
            row=0,
            column=0,
            sticky=NSEW
        )
        
        # Middle Menu Widgets
        self.DataBlock0 = ttk.Button(
            master=self.MenuMiddle,
            command=self.ButtonPress0,
            image=self.img0
        )
        self.DataBlock0.grid(
            row=0,
            column=0,
            sticky=NSEW
        )


        self.DataBlock1 = ttk.Button(
            master=self.MenuMiddle,
            command=self.ButtonPress1,
            image=self.img1
        )
        self.DataBlock1.grid(
            row=0,
            column=1,
            sticky=NSEW
        )

        self.DataBlock2 = ttk.Button(
            master=self.MenuMiddle,
            command=self.ButtonPress2,
            image=self.img2
        )
        self.DataBlock2.grid(
            row=1,
            column=0,
            sticky=NSEW
        )

        self.DataBlock3 = ttk.Button(
            master=self.MenuMiddle,
            command=self.ButtonPress3,
            image=self.img3
        )
        self.DataBlock3.grid(
            row=1,
            column=1,
            sticky=NSEW
        )
        
        self.DataBlock4 = ttk.Button(
            master=self.MenuMiddle,
            command=self.ButtonPress4,
            image=self.img4
        )
        self.DataBlock4.grid(
            row=2,
            column=0,
            sticky=NSEW
        )

        self.DataBlock5 = ttk.Button(
            master=self.MenuMiddle,
            command=self.ButtonPress5,
            image=self.img5
        )
        self.DataBlock5.grid(
            row=2,
            column=1,
            sticky=NSEW
        )

        self.DataBlock6 = ttk.Button(
            master=self.MenuMiddle,
            command=self.ButtonPress6,
            image=self.img6
        )
        self.DataBlock6.grid(
            row=3,
            column=0,
            sticky=NSEW
        )

        self.DataBlock7 = ttk.Button(
            master=self.MenuMiddle,
            command=self.ButtonPress7,
            image=self.img7
        )
        self.DataBlock7.grid(
            row=3,
            column=1,
            sticky=NSEW
        )

        self.DataBlock8 = ttk.Button(
            master=self.MenuMiddle,
            command=self.ButtonPress8,
            image=self.img8
        )
        self.DataBlock8.grid(
            row=4,
            column=0,
            sticky=NSEW
        )

        # Bottom Menu Widgets
        self.MenuResetbtn = ttk.Button(
            master=self.MenuBottom,
            command=self.ButtonReset,
            text="Reset Data Blocks"
        )
        self.MenuResetbtn.grid(
            row=0,
            column=0,
            sticky=NSEW
        )

        self.MenuBar = ttk.Progressbar(
            master=self.MenuBottom
        )
        self.MenuBar.grid(
            row=0,
            column=1,
            sticky=NSEW
        )

        # Open CV Image Viewer
        self.OpenCvImage = ttk.Label(
            master=self.OpenCVFrame,
            image=self.img9
        )
        self.OpenCvImage.grid(
            row=0,
            column=0,
            sticky=NSEW
        )
        
    def ButtonPress0(self):
        # change the btn image to white
        self.DataBlock0.configure(
            image=self.img10
        )

        # increment counter
        if am.G_IMG_0_ENABLE_FLAG is True: self.DataBlockMinedCounter += 1

        # change the enable flag
        am.G_IMG_0_ENABLE_FLAG = False
        
        # update progress bar
        self.UpdateProgressBar()

        pass
    def ButtonPress1(self):
        # change the btn image to white
        self.DataBlock1.configure(
            image=self.img10
        )

        # increment counter
        if am.G_IMG_1_ENABLE_FLAG is True: self.DataBlockMinedCounter += 1

        # change the enable flag
        am.G_IMG_1_ENABLE_FLAG = False

        # update progress bar
        self.UpdateProgressBar()

        pass
    def ButtonPress2(self):
        # change the btn image to white
        self.DataBlock2.configure(
            image=self.img10
        )

        # increment counter
        if am.G_IMG_2_ENABLE_FLAG is True: self.DataBlockMinedCounter += 1

        # change the enable flag
        am.G_IMG_2_ENABLE_FLAG = False

        # update progress bar
        self.UpdateProgressBar()
        pass

    def ButtonPress3(self):
        # change the btn image to white
        self.DataBlock3.configure(
            image=self.img10
        )

        # increment counter
        if am.G_IMG_3_ENABLE_FLAG is True: self.DataBlockMinedCounter += 1

        # change the enable flag
        am.G_IMG_3_ENABLE_FLAG = False
        # update progress bar
        self.UpdateProgressBar()
        pass

    def ButtonPress4(self):
        # change the btn image to white
        self.DataBlock4.configure(
            image=self.img10
        )

        # increment counter
        if am.G_IMG_4_ENABLE_FLAG is True: self.DataBlockMinedCounter += 1

        # change the enable flag
        am.G_IMG_4_ENABLE_FLAG = False
        # update progress bar
        self.UpdateProgressBar()
        pass

    def ButtonPress5(self):
        # change the btn image to white
        self.DataBlock5.configure(
            image=self.img10
        )

        # increment counter
        if am.G_IMG_5_ENABLE_FLAG is True: self.DataBlockMinedCounter += 1

        # change the enable flag
        am.G_IMG_5_ENABLE_FLAG = False
        # update progress bar
        self.UpdateProgressBar()
        pass
    
    def ButtonPress6(self):
        # change the btn image to white
        self.DataBlock6.configure(
            image=self.img10
        )

        # increment counter
        if am.G_IMG_6_ENABLE_FLAG is True: self.DataBlockMinedCounter += 1

        # change the enable flag
        am.G_IMG_6_ENABLE_FLAG = False
        # update progress bar
        self.UpdateProgressBar()
        pass

    def ButtonPress7(self):
        # change the btn image to white
        self.DataBlock7.configure(
            image=self.img10
        )

        # increment counter
        if am.G_IMG_7_ENABLE_FLAG is True: self.DataBlockMinedCounter += 1

        # change the enable flag
        am.G_IMG_7_ENABLE_FLAG = False
        # update progress bar
        self.UpdateProgressBar()
        pass

    def ButtonPress8(self):
        # change the btn image to white
        self.DataBlock8.configure(
            image=self.img10
        )

        # increment counter
        if am.G_IMG_8_ENABLE_FLAG is True: self.DataBlockMinedCounter += 1

        # change the enable flag
        am.G_IMG_8_ENABLE_FLAG = False
        # update progress bar
        self.UpdateProgressBar()
        pass

    # Function to handle bar updating
    def UpdateProgressBar(self):
        
        # change the bar level
        self.MenuBar.configure(
            maximum=9,
            value=self.DataBlockMinedCounter,
            mode="determinate",
            orient="horizontal"
        )
        pass

    def ButtonReset(self):
        self.DataBlock0.configure(
            image=self.img0
        )

        self.DataBlock1.configure(
            image=self.img1
        )

        self.DataBlock2.configure(
            image=self.img2
        )

        self.DataBlock3.configure(
            image=self.img3
        )

        self.DataBlock4.configure(
            image=self.img4
        )

        self.DataBlock5.configure(
            image=self.img5
        )

        self.DataBlock6.configure(
            image=self.img6
        )

        self.DataBlock7.configure(
            image=self.img7
        )

        self.DataBlock8.configure(
            image=self.img8
        )

        # Reset all enable flags
        am.G_IMG_0_ENABLE_FLAG = True
        am.G_IMG_1_ENABLE_FLAG = True
        am.G_IMG_2_ENABLE_FLAG = True
        am.G_IMG_3_ENABLE_FLAG = True
        am.G_IMG_4_ENABLE_FLAG = True
        am.G_IMG_5_ENABLE_FLAG = True
        am.G_IMG_6_ENABLE_FLAG = True
        am.G_IMG_7_ENABLE_FLAG = True
        am.G_IMG_8_ENABLE_FLAG = True
        
        # Rest progress bar
        self.DataBlockMinedCounter = 0
        self.UpdateProgressBar()

        pass

    def UpdateImageView(self, OpenCVImage):
        
        #update the image widger
        self.OpenCvImage.configure(
            image=ImageTk.PhotoImage(image=OpenCVImage)
        )

        pass


if __name__ == "__main__":
    root = tk.Tk() # Create the toplevel parent window
    root.title('GUI Test')
    
    am.startCV2()

    myapp = View(root)

    # update image viewer at 30Hz
    myapp.after(
        ms=30,
        func=myapp.UpdateImageView
    )

    myapp.mainloop() 