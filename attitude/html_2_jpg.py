import imgkit

def conversion(filename):
    options = {
        'crop-w':'380'
    }
    try:
        imgkit.from_file(f'bills//{filename}.html', f'bills//{filename}.jpg',options=options)
        return True
    except:
        return False
#print(conversion('6'))
