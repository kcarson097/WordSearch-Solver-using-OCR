# WordSearch-Solver-using-OCR
This is a word search puzzle solver which takes in an image of a wordsearch and using the pytesseract library, converts it into a text file and uses this data to create a tkinter window of the wordsearch. The program can then solve the wordsearch using a depth first alogoithm (DFS). It finds all the characters in the wordsearch that match the beginning of the word it is searching for and then checks every possible direction to see if the word is present from that position. (more explanation in code notes). The user can also solve for a single word by selecting a word from the word bank using the dropdown menu in the tkinter window.

When using, I reccomend you use the provided wordsearches in this repositry - you will have to change the preprocessing of the image to get an accurate OCR for new images - this current code is refinded for the attached wordsearches but the pre processing can be easily altered using the openCV library and pytesseract. OCR accuracy is normally imporved by increasing the resolution of the image, ensuring there is small spacing between each character in the wordsearch and changing the image to grey.

Images of the example window that will be shown is attached.