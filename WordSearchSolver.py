from tkinter import *
import time
from PIL import Image
import pytesseract

root = Tk()
root.title('Word Search Solver')



class App():
    """THE INIT METHOD WILL USE OCR TO OBTAIN THE WORDSEARCH AND WORDBANK
    THESE WILL BE STORED AS LISTS. THE TKINTER WINDOW WILL BE SET UP WITH THE WORDEARCH,
    AN OPTION TO SOLVE THE ENTIRE PUZZLE AND A DROPDOWN TO SOLVE FOR A SINGLE WORD IN THE BANK"""
    def __init__(self,master):
        #convert worsearch to text file (a split list of each line) and convert wordbank
        self.wordsearch = self.convert_image_to_text('wordsearch1.png')
        self.word_bank = self.convert_image_to_text('wordbank1.png')
        #self.word_bank = ['BLUEBERRY']
        
        #welcomelabel
        self.welcome = Label(master, text = 'Select word from dropdrown or solve puzzle completely by selecting the button ! ', 
                             font = ("Helvetica", 15)).grid(row = 0, column = 1,pady = 20,columnspan = len(self.wordsearch[0]))
        #put the wordsearch in the tkinter window
        for i in range(0, len(self.wordsearch)):
            for j in range(0, len(self.wordsearch[i])):
                letter = Label(master,text = self.wordsearch[i][j],font = ("Helvetica", 10)).grid(row = i+1, 
                                                                                                       column = j+1,
                                                                                                       padx = 10, 
                                                                                                       pady = 10)
        
        #button to solve whole wordsearch
        self.button = Button(master,text = 'Complete Wordsearch',command = self.solve,  
                            borderwidth = 5,width = 20, font = ("Helvetica", 13)).grid(row = len(self.wordsearch)+2,
                                                                                      column = 0 , 
                                                                                      columnspan = int(len(self.wordsearch[0])/2),
                                                                                      padx = 5, pady = 20)
        
        
        #dropdown for wordbank so user can find an individual word
        self.var = StringVar()
        self.var.set(self.word_bank[0])
        #if the user changes the option on the dropdown, the program will find that variable in the puzzle
        self.var.trace("w",self.option_changed)

        #create dropdown menu
        self.drop = OptionMenu(master, self.var , *self.word_bank).grid(row = len(self.wordsearch)+2,
                                                                                      column = int(len(self.wordsearch[0])/2) , 
                                                                                      columnspan = int(len(self.wordsearch[0])/2),
                                                                                      padx = 5, pady = 20)
        #the program will find the word selected in the dropdown menu i.e first word in the bank
        self.word = self.var.get()
        self.find_word(self.word)
        
       
    def option_changed(self,*args):
        """THIS FUNCTION IS CALLED WHEN USER CHANGES VARIABLE IN DROPDOWN MENU,
        THE PROGRAM WILL FIND THIS VARIABLE IN THE PUZZLE"""
        self.word = self.var.get()
        self.find_word(self.word)
        
        
    def solve(self):
        """THIS SOLVES THE ENTIRE PUZZLE AND TIMES THE TIME TAKEN TO SOLVE"""
        #start timer
        start = time.time()
        for self.word in self.word_bank:
            print(self.word)
            self.find_word(self.word)
            #finish timer
            end = time.time()
            self.time_elapsed = "{:.2f}".format(end - start) + " s"
            
            #display time taken to solve
            label = Label(root,text = "Puzzle Solved in " + self.time_elapsed,
                          font = ("Helvetica", 15)).grid(row = len(self.wordsearch)+3,column = 0, 
                                                         columnspan = len(self.wordsearch[0]))
            
            
    def convert_image_to_text(self,path):
        """USING PYTESSERACT, THE WORDBANK AND WORDSEARCH IMAGES ARE CONVERTED TO TEXT
        THEY ARE SPLIT INTO LISTS I.E FOR THE WORDSEARCH ONE LARGE LIST AND WITHIN THIS LIST EACH ROW IS PRESENT
        EG - [
                [ASBASAD]
                [BASBASD]
                [ETC]
                ]"""
        pytesseract.pytesseract.tesseract_cmd = 'C:\\Users\\Kyle\\Documents\\Tesseract-OCR\\tesseract'

        im = Image.open(path)
        basewidth = 2200
        wpercent = (basewidth/float(im.size[0]))
        hsize = int((float(im.size[1])*float(wpercent)))
        im = im.resize((basewidth,hsize), Image.ANTIALIAS)
        text = pytesseract.image_to_string(im, lang = "eng")


        return text.split()
    
    def find_word(self,word):
        """USING THE INPUTED WORD,THIS CHECKS EACH CHARACTER IN THE WORDSEARCH AND SEES
        IF THE CHARACTER MATCHES THE FIRST CHARACTER OF THE WORD, IT THEN STORES THIS COORDINATE
        IN THE LIST START_POS"""
        self.start_pos = []
        #check each row
        for i in range(0,len(self.wordsearch)):
                #check each column
            for j in range(0, len(self.wordsearch[i])):
                #find all coordinates which have the first letter of the word and store them
                if self.wordsearch[i][j] == self.word[0]:
                    self.start_pos.append([i,j])
                
                   
        #print(count)
        for pos in self.start_pos:
            if self.check_start(self.word, pos):
                
                return
                
            
    def check_start(self,word,pos):
        self.directions = [
                    [0,1], #E
                    [0,-1], #W
                    [1,0], #N
                    [1,1], #NE
                    [1,-1], #NW
                    [-1,0], #S
                    [-1,1], #SE
                    [-1,-1] #SW
                     ]
        for d in self.directions:
            #run through all the posible directions a word can be found 
            if self.check_direction(self.word,pos,d):
                return True
    
    def check_direction(self,word,pos,d):
        """ USING THE INPUTED POSITION, THIS WILL CHECK EACH DIRECTION POSSIBLE THAT A WORD CAN BE SPELT IN,
        THE WHILE LOOP WILL STOP IF THE WORD FOUND NO LONGER MATHCES THE WORD YOU ARE LOOKING FOR AND YOU HAVE CHECKED ALL 
        POSSIBLE DIRECTIONS
        """
        self.word_found = [self.word[0]] #this is a list of the characters found in the word in the particular direction
        self.current_pos = pos #the position you start at - i.e the first character of the word
        self.pos_checked = [pos] #list containing all the positions we have checked so far
        
        
        while self.check_match(self.word_found,self.word):
            check = 0
            #check if length of word found is same is length of the word yoou are searching for
            if (len(self.word) == len(self.word_found)):
                
                #correct word has been found !
                #print('word found!')
                
                #change these characters to red to highlight the word
                #print(self.word_found)
                
                self.highlight_word(self.pos_checked)
                
                return True
                
                
            else:
                #word isnt correct length, move to next coordinate and try again
                self.current_pos = [self.current_pos[0] + d[0], self.current_pos[1] + d[1]] 
                #current_pos = [initial x pos + x indices of direction,
                self.pos_checked.append(self.current_pos) 
                #print(self.current_pos)                                                
                #  initial y pos + y indices of direction]
            
            if self.valid_coordinate(self.current_pos[0],self.current_pos[1]):
                self.word_found.append(self.wordsearch[self.current_pos[0]][self.current_pos[1]]) 
                #add new character to word found
            else:
                return #word not found - out of worsearch range
            
          
        
    def check_match(self, word_found,word):
        """this checks if the word found so far is the same as the word you are looking for""" 
        self.count = 0
        for char in self.word_found:
            if char != self.word[self.count]:
                return False
            self.count +=1
            #print(self.count)
    
        return True
    
    def valid_coordinate(self,row,column):
        """CHECKS IF COORDINATE YOU ARE SEARCHING IS WITHIN THE WORDSEARCH"""
        if row >= 0 and row < len(self.wordsearch):
            if column >= 0 and column < len(self.wordsearch[0]):
                return True
        return False
        
    def highlight_word(self,coordinates):
        """HIGHLIGHTS THE FOUND WORD IN RED"""
        for coordinate in coordinates:
            letter = Label(root,text = self.wordsearch[coordinate[0]][coordinate[1]],font = ("Helvetica", 10),fg = 'white',
                                                       bg = 'red').grid(row = coordinate[0]+1, column = coordinate[1]+1,
                                                                                                       padx = 10, 
                                                                                                       pady = 10)
                
        
run = App(root)

root.mainloop()