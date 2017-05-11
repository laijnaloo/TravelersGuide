__author__ = 'Lina Andersson'
from tkinter import*

class TravelStates():
    def __init__(self):
        self.bigImage = None
        self.mapIcon = None
        self.music = None
        self.left = None
        self.right = None
        self.placeImage = None
        self.cityText = None
        self.countryText = None
        self.infoText = None
        self.root = Tk()
        self.infoArray = None
        self.destinationNumber = 0
        self.pause = None
        self.artistRect = None
        self.rectInfo = None
        self.textArtist = None
        self.currentSound = None
        self.userClick = 0