import imgkit

def conversion(filename):
    options = {
        'crop-w':'380'
    }
    try:
        con = imgkit.config(wkhtmltoimage='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltoimage.exe')
        imgkit.from_file(f'bills//{filename}.html', f'bills//{filename}.jpg',options=options,config=con)
        return True
    except:
        return False

#print(conversion('12'))
