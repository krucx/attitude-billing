import win32api
import win32print
import img2pdf
from PIL import Image
import os
from configuration import username
from html_2_jpg import conversion
 
def print_pdf(pdf_file_name):

    try:

        conversion(pdf_file_name)
        # storing image path
        img_path = f"C:\\Users\\{username}\\Desktop\\attitude\\bills\\"+pdf_file_name+".jpg"
        
        # storing pdf path
        pdf_path = f"C:\\Users\\{username}\\Desktop\\attitude\\bills\\bills_pdf\\"+pdf_file_name+".pdf"
        
        # opening image
        image = Image.open(img_path)
        
        # converting into chunks using img2pdf
        pdf_bytes = img2pdf.convert(image.filename)
        
        # opening or creating pdf file
        file = open(pdf_path, "wb")
        
        # writing pdf files with chunks
        file.write(pdf_bytes)
        
        # closing image file
        image.close()
        
        # closing pdf file
        file.close()
        win32api.ShellExecute(0,'print',"bills\\bills_pdf\\"+pdf_file_name+".pdf",None,".",0)
        return True
    except:
        return False

#print(print_pdf('1'))
