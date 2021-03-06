from tkinter import *
from mutagen import File
from pygame import mixer
from PIL import Image, ImageTk
import os, time

class myProg_tk(Tk):
    def __init__(self, parent):
        Tk.__init__(self, parent)
        self.parent = parent
        self.exists = True
        self.initialize()

    def initialize(self):
        self.root = self
        self.pause = False

        self.root.bind('<Escape>', lambda e: self.root.iconify())
        self.root.protocol("WM_DELETE_WINDOW", self.root.iconify())
        
        self.grid()
        self.label = Label(self, text = 'Queue Song (Hit Enter)')
        self.label.grid(column = 0, row = 0, sticky = 'E')

        self.entryVar = StringVar()
        self.entry = Entry(self, textvariable = self.entryVar)
        self.entry.grid(column = 1, row = 0, sticky = 'E')
        self.entry.bind("<Return>", self.QueueSong)

        self.volLevel = DoubleVar()
        self.volume = Scale(self, orient = 'vertical',
                            from_ = 1.0, to = 0.0,
                            resolution = 0.05,
                            variable = self.volLevel, command = self.checkVol)
        self.volume.set(1)
        self.volume.grid(column = 2, row = 0)
        self.pause = Button(self, text = 'Pause', command = self.pauseSong)
        self.pause.grid(column = 3, row = 2, sticky = 'E')

        self.grid_columnconfigure(0, weight = 1)
        self.resizable(False, False)
        self.artwork = []
        self.artworkNo = 0
        self.currentImage = Image.open('albumArt.jpg')
        self.currentImage = self.currentImage.resize((150, 150), Image.ANTIALIAS)
        self.currentImage = ImageTk.PhotoImage(self.currentImage)
        self.imageDisplayed = Label(self, image=self.currentImage)
        self.imageDisplayed.grid(column = 3, row = 0, sticky = 'NE')

    def getArtwork(self, location):
        file = File(location)
        try:
            artwork = file.tags['APIC:'].data
            self.artwork.append(artwork)
        except KeyError:
            artwork = 'albumArt.jpg'
            self.artwork.append(artwork)

    def updateAlbum(self):
        self.artworkNo += 1
        self.currentImage = Image.open(self.artwork[self.artworkNo])
        self.currentImage = ImageTk.PhotoImage(self.currentImage)

    def QueueSong (self, event):
        songName = self.entryVar.get()
        self.entryVar.set('')
        dirLoc = os.path.dirname(os.path.abspath(__file__))
        path = dirLoc + "/songs/" + songName + ".mp3"
        self.getArtwork(path)
        if (mixer.music.get_busy() == False):
            mixer.music.load(path)
            mixer.music.play()
        else:
            mixer.music.queue(path)

    def checkVol (self, event):
        mixer.music.set_volume(self.volume.get())

    def pauseSong (self):
        if (self.pause == True):
            mixer.music.unpause()
        else:
            mixer.music.pause()
            self.pause = True

    def closeSafely(self):
        mixer.music.stop()
        Tk.destroy(self)
        self.exists = False

def onClose(whileLooping):
    whileLooping = False

mixer.init()
app = myProg_tk(None)
app.title('Music Box')
playedOnce = False
while (app.exists):
    Tk.update_idletasks(app)
    Tk.update(app)
    if mixer.music.get_busy() == True:
        playedOnce = True
    if playedOnce == True:
        if mixer.music.get_busy() == False:
            app.updateAlbum()
            time.sleep(0.1)


mixer.music.stop()
mixer.quit()
