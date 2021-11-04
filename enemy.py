import pygame
from config import *

# class Enemy:

class First:
    def getClass(self):
        # super().getClass()
        print("Class Fist")
        super().getClass()

class Second:
    def getClass(self):
        
        print("Class Second")
        
        
class Third:
    def getClass(self):
        
        print("Class Second")
        

class Four(First, Second, Third):
    def getClass(self):
        super().getClass()

t = Four()
t.getClass()