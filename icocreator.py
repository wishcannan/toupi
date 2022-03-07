#生成一个ico文件 用来作为网站图标

from PIL import Image
# from matplotlib import image

IMAGE_SIZE = 32 #规定图标大小

pri_image = Image.open(r'F:\py\image\villpix\笹木咲\88904389.jpg')
pri_image.resize((IMAGE_SIZE,IMAGE_SIZE),Image.ANTIALIAS ).save("./static/img/favicon.ico")