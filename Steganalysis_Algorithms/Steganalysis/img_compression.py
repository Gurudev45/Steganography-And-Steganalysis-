import cv2 as ocv
imgpath = "/home/kali/Desktop/Steganalysis/Steganalysis_Algorithms/Steganalysis/images/edg2_img.png"
img = ocv.imread(imgpath)

img = ocv.cvtColor(img, ocv.COLOR_BGR2GRAY)

def save(path, image, jpg_quality=None, png_compression=None):
  if jpg_quality:
    ocv.imwrite(path, image, [int(ocv.IMWRITE_JPEG_QUALITY), jpg_quality])
  elif png_compression:
    ocv.imwrite(path, image, [int(ocv.IMWRITE_PNG_COMPRESSION), png_compression])
  else:
    ocv.imwrite(path, image)

# save the image in JPEG format with 85% quality
outpath_jpeg = "/home/kali/Desktop/Steganalysis/Steganalysis_Algorithms/Steganalysis/images/compressed_edg2_jpg.jpg"
save(outpath_jpeg,img,jpg_quality=40) #higher the no,better the quality
outpath_png = "./compressed_edg2_png.png"
# save the image in PNG format with 4 Compression
save(outpath_png, img,png_compression=9)#0-9, compression value
