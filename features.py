import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage.filters import sobel
from scipy.misc import imread, imsave
from sys import argv
import matplotlib.cm as cm
import IPython

def ToCharray(energy):
    height, width = np.shape(energy)
    out = np.zeros_like(energy).astype(str)
    for i in range(width):
        for j in range(height):
            e = energy[j,i]
            if e < 0.5:
                out[j,i] = ' '
            elif e < 1.0:
                out[j,i] = '.'
            elif e < 1.5:
                out[j,i] = '*'
            elif e < 2.0:
                out[j,i] = '%'
            else:
                out[j,i] = '@'
    return out



def Derivative(chunk):
    grey = np.average(chunk,axis=2)
    x_shift = np.roll(np.copy(grey),1,axis = 1)
    x_shift[0,:] = grey[0,:]
    y_shift = np.roll(np.copy(grey),1,axis = 0)
    y_shift[:,0] = grey[:,0]
    return np.dstack((grey - x_shift,grey - y_shift))

def GetCharray(img,nx,ny):
    """
    Converts an image to an array of Chars.
    ndarray<uint8> img: an image
    int nx: width of a character in pixels
    int ny: height of a character in pixels
    Returns ndarray<str[1]>
    """
    img = img / 255.0 #Convert to Float
    height, width, _ = np.shape(img)
    x = range(0,width,nx)
    y = range(0,height,ny)
    out_energy = np.zeros((len(y),len(x)))
    deriv = np.linalg.norm(Derivative(im/255.0), axis = 2)
    for i in range(len(x)):
        for j in range(len(y)):
            out_energy[j,i] = np.average(np.concatenate(deriv[y[j]:y[j]+ny,x[i]:x[i]+nx]),axis=0)
    out_energy = (out_energy - np.average(out_energy)) / np.std(out_energy)
    return ToCharray(out_energy)

def BlockPixels(img,nx,ny):
    """
    Converts an image to an array of colors averaged over blocks.
    ndarray<uint8> img: an image
    int nx: width of a character in pixels
    int ny: height of a character in pixels
    Returns ndarray<uint8>
    """
    img = img / 255.0 #Convert to Float
    height, width, _ = np.shape(img)
    x = range(0,width,nx)
    y = range(0,height,ny)
    out_rgb = np.zeros((len(y),len(x),3))
    for i in range(len(x)):
        for j in range(len(y)):
            chunk = img[y[j]:y[j]+ny,x[i]:x[i]+nx]
            out_rgb[j,i] = np.average(np.concatenate(chunk),axis=0)
    return (out_rgb*255).astype(np.uint8)


if __name__ == '__main__':
    im = imread(argv[1])
    chars = GetCharray(im, 10, 20)
    for i in range(len(chars)):
        s=''
        for j in range(len(chars[i])):
            s+=chars[i][j]
        print s
    rgb = BlockPixels(im, 10, 20)
    plt.imshow(rgb, interpolation='none')
    plt.show()
