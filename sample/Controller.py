import GuiView as V
import ArucoModel as A
from multiprocessing import Process, Queue
import tkinter as tk




if __name__ == "__main__":
    root = tk.Tk() # Create the toplevel parent window
    root.title('World Help Lab - Aruco Romper!')
    
    # A.startCV2()

    myapp = V.View(root)

    # update image viewer at 30Hz
    myapp.after(
        ms=1000,
        func=myapp.UpdateImageView
    )

    myapp.mainloop() 