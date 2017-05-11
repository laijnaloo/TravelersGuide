__author__ = 'Lina Andersson'
#Lina Andersson
#Labb 4
#Multimediaprogrammering i Python
#Version 3

from tkinter import*
from PIL import ImageTk, Image
import os
import pygame
from Labb4Utilis import TravelStates

def main():
    #import objects from Labb4Utilis
    state = TravelStates()

    readFile(state)
    state.root.resizable(width=False, height=False)
    state.root.geometry("750x495+30+30")
    state.root.configure(bg="white")
    state.root.iconbitmap(os.path.abspath("travelIcon.ico"))
    state.root.title("Travelers Guide")
    mapIconGUI(state)
    travelGUI(state, state.destinationNumber)
    buttonsGUI(state)
    mainloop()

def mapIconGUI(state):
    map = Image.open('mapIcon.png')
    state.mapIcon = ImageTk.PhotoImage(map)

    placeMapIcon = Label(state.root, image=state.mapIcon, bg="white")
    placeMapIcon.place(x=148, y=397)

#Presents different data depending on the destination
def travelGUI(state, destinationNumber):

    image = Image.open(state.infoArray[destinationNumber][2])
    state.bigImage = ImageTk.PhotoImage(image)

    placeImage = Label(state.root, image=state.bigImage, width= 750, height=377)
    placeImage.place(x= 0, y= 0)

    state.cityText = Label(state.root, text =state.infoArray[state.destinationNumber][0], bg = "white", font = ("Myriad Pro", 20))
    state.cityText.place(x = 10, y = 385)

    state.countryText = Label(state.root, text =state.infoArray[state.destinationNumber][1], fg = "#96affe", bg = "white", font = ("Myriad Pro", 10))
    state.countryText.place(x = 160, y = 397)

    state.infoText = Label(state.root, wraplength= 500, justify = "left" , text =state.infoArray[state.destinationNumber][4], bg = "white", font = ("Myriad Pro", 10))
    state.infoText.place(x = 10, y = 418)

#Buttons used to go back and forward between the different destinations
def buttonsGUI(state):
    if state.destinationNumber == 0:
        #If the user is on the first destination in the list they should not be able to go to
        # a previous one - thereby an unactive button which is not clickable
        arrowL = 'leftDeactive.png'

        leftButton = Image.open(arrowL)
        state.left = ImageTk.PhotoImage(leftButton)

        buttonLeft = Label(state.root, image=state.left, bg="white")
        buttonLeft.place(x=580, y=390)
    else:
        arrowL = 'leftArrow.png'

        leftButton = Image.open(arrowL)
        state.left = ImageTk.PhotoImage(leftButton)

        buttonLeft = Label(state.root, image=state.left, bg="white")
        buttonLeft.bind("<Button-1>", lambda x: previousDestination(state))
        buttonLeft.place(x=580, y=390)

    if state.destinationNumber == len(state.infoArray)-1:
        arrowR = 'rightDeactive.png'

        rightButton = Image.open(arrowR)
        state.right = ImageTk.PhotoImage(rightButton)

        buttonRight = Label(state.root, image=state.right, bg="white")
        buttonRight.place(x=635, y=390)
    else:
        arrowR = 'rightArrow.png'

        rightButton = Image.open(arrowR)
        state.right = ImageTk.PhotoImage(rightButton)

        buttonRight = Label(state.root, image=state.right, bg="white")
        buttonRight.bind("<Button-1>", lambda x: nextDestination(state))
        buttonRight.place(x=635, y=390)

    musicIcon = Image.open('musicIcon.png')
    state.music = ImageTk.PhotoImage(musicIcon)

    musicButton = Label(state.root, image=state.music, bg="white")

    #Play music on click
    musicButton.bind("<Button-1>", lambda x: playMusic(state))

    #make artist info visible on hover
    musicButton.bind("<Enter>", lambda x: showArtistInfo(state))
    musicButton.bind("<Leave>", lambda x: hideArtistInfo(state))
    musicButton.place(x=690, y=390)

def showArtistInfo(state):
    artistInfo = Image.open('rectangel.png')
    state.artistRect = ImageTk.PhotoImage(artistInfo)

    state.rectInfo = Label(state.root, bg="white", image=state.artistRect)
    state.rectInfo.place(x=580, y=440)

    state.textArtist = Label(state.root, fg="white", bg= "#96affe", wraplength= 135, justify = CENTER, text = state.infoArray[state.destinationNumber][5], font = ("Myriad Pro", 8))
    state.textArtist.place(x=590, y=445)

def hideArtistInfo(state):
    if state.rectInfo:
        state.rectInfo.destroy()
        state.textArtist.destroy()

def playMusic(state):
    state.userClick += 1
    if state.userClick == 1:
        #Play music when music button is pushed
        pygame.init()
        pygame.mixer.init()
        musicPlay = pygame.mixer.Sound(state.infoArray[state.destinationNumber][3])
        state.currentSound = musicPlay.play()

        pauseIcon = Image.open('pauseButton.png')
        state.pause = ImageTk.PhotoImage(pauseIcon)

        pauseButton = Label(state.root, image=state.pause, bg="white")
        pauseButton.bind("<Button-1>", lambda x: pauseMusic(state))

        #SHow artist info when sound is playing
        pauseButton.bind("<Enter>", lambda x: showArtistInfo(state))
        pauseButton.bind("<Leave>", lambda x: hideArtistInfo(state))
        pauseButton.place(x=690, y=390)
        state.root.after(100, lambda: checkIfMusicEnded(state))
    else:
        pauseMusic(state)

def checkIfMusicEnded(state):
    if not state.currentSound.get_busy():
        pauseMusic(state)
    else:
        state.root.after(100, lambda: checkIfMusicEnded(state))

def pauseMusic(state):
    state.userClick = 0
    pygame.mixer.stop()
    buttonsGUI(state)

def previousDestination(state):
    #Delete information about previous destination
    if state.destinationNumber > 0:
        if state.currentSound:
            pauseMusic(state)
        state.destinationNumber -= 1
        state.cityText.destroy()
        state.countryText.destroy()
        state.infoText.destroy()
        buttonsGUI(state)
        travelGUI(state, state.destinationNumber)

def nextDestination(state):
    #Delete information about previous destination
    if state.destinationNumber < len(state.infoArray)-1:
        if state.currentSound:
            pauseMusic(state)
        state.destinationNumber += 1
        state.cityText.destroy()
        state.countryText.destroy()
        state.infoText.destroy()
        buttonsGUI(state)
        travelGUI(state, state.destinationNumber)

def readFile(state):
    file = open("travelInfo.txt", "r")
    lines = file.readlines()

    state.infoArray = []
    for line in lines:
        state.infoArray.append(line.split("\t"))

if __name__ == "__main__":
    main()
