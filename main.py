# -*- coding: utf-8 -*-

class Controller:
    
    def __init__(self, io):
        self.io = io
    
    def app(self):
        pass
    
class InputOutput:
    def get_gpx(self):
        input()

def main():
   con = Controller()
   io = InputOutput()
   con.app(io)
    
if __name__ == "__main__":
    main()  

