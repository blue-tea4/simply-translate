import pytesseract
import cv2
from googletrans import Translator

def text_recognition(image_path):
	#Proccesses the image and makes it the right size 
    # load the input image and grab the image dimensions
    image = cv2.imread(image_path)
    #makes the image pop up
    cv2.imshow( 'image' , image)
    
    image_height, image_width, image_channels = image.shape
    #Testing if it got the width and hight
    #print(str(image_width) + " " + str(image_height))
    orig = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
 
    # Performing OTSU threshold
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
	
	# Specify structure shape and kernel size. 
    # Kernel size increases or decreases the area 
    # of the rectangle to be detected.
    # A smaller value like (10, 10) will detect 
    # each word instead of a sentence.
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25))
      
    # Appplying dilation on the threshold image
    dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)
      
	# Finding contours
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, 
                                                     cv2.CHAIN_APPROX_NONE)
      
    # Creating a copy of image
    im2 = image.copy()

    #array for storing text 
    output_text = []  
    # Looping through the identified contours
    # Then rectangular part is cropped and passed on
    # to pytesseract for extracting text from it
    # Extracted text is then written into the text file
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
          
        # Drawing a rectangle on copied image
        rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
          
        # Cropping the text block for giving input to OCR
        cropped = im2[y:y + h, x:x + w]
          
        # Apply OCR on the cropped image
        text = pytesseract.image_to_string(cropped)
        #print(text)
        output_text.append(text)

    
    cv2.imshow( 'image' , im2)
    
          
    return output_text[::-1]

#Get rid of extra space around the text
def clean_string(image_text):
    clean = image_text.strip()
    return clean

def translate_text(image_text, starting_lang, ending_lang):
    translator = Translator()
    results = translator.translate(str(image_text), src=starting_lang, dest=ending_lang)
    #print(results)
    return results.text

        
        
def main():
    #image_path = "C:\\Users\\Natalie\\Desktop\\Coding_Project\\OCRtests\\First_test.png"
    image_path = input("Please input image path using two \ ")
    orig_lang = input("Original language: ")
    ending_lang = input("Language to translate into: ")
    string_from_image =text_recognition(image_path)
    #test for for loop
    #string_from_image = ["hello    ", "     yoooo", "\n yike \n"]
    
    #Runs through the list cleaning the extra white space
    striped_string = []
    final_text = ''
    for i in range(len(string_from_image)):
        x = clean_string(string_from_image[i])
        striped_string.append(x)
        trans_text = translate_text(x, orig_lang, ending_lang)
        
        print(trans_text)
        
#     x = striped_string[0]
#     print(type(x))
#     print(x)
        
    
    
     
    
# Using the special variable 
# __name__
if __name__=="__main__":
    main()