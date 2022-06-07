import ctypes
from ctypes import wintypes
import logging

logging.basicConfig(level=logging.DEBUG)


def displayGammaValues(lpRamp):
    """
    Displays the GammaArray of 256 values of R,G,B individually
    :param lpRamp: GammaArray
    :return: None
    """

    msgR = "R values:  "
    for j in range(256): msgR += str(lpRamp[0][j])+' '
    logging.debug(msgR)

    msgG = "G values:  "
    for j in range(256): msgG += str(lpRamp[1][j])+' '
    logging.debug(msgG)

    msgB = "B values:  "
    for j in range(256): msgB += str(lpRamp[2][j])+' '
    logging.debug(msgB+"\n")


def changeGammaValues(lpRamp, brightness):
    """
    Modifies the Gamma Values array according to specified 'wBrightness' value
    To reset the gamma values to default, call this method with 'wBrightness' as 128
    :param lpRamp: GammaArray
    :param brightness: Value of brightness between 0-255
    :return: Modified GammaValue Array
    """
    for i in range(256):
        iValue = i * (brightness + 128)
        if iValue > 65535: iValue = 65535
        lpRamp[0][i] = lpRamp[1][i] = lpRamp[2][i] = iValue
    return lpRamp


def changeGamma(brightness):
    GetDC = ctypes.windll.user32.GetDC
    ReleaseDC = ctypes.windll.user32.ReleaseDC
    SetDeviceGammaRamp = ctypes.windll.gdi32.SetDeviceGammaRamp
    GetDeviceGammaRamp = ctypes.windll.gdi32.GetDeviceGammaRamp

    hdc = wintypes.HDC(GetDC(None))

    if hdc:
        GammaArray = ((wintypes.WORD * 256) * 3)()
        if GetDeviceGammaRamp(hdc, ctypes.byref(GammaArray)):
            logging.debug("Current Gamma Ramp Values are:")
            displayGammaValues(GammaArray)

            GammaArray = changeGammaValues(GammaArray, brightness)

            logging.debug("New Current Gamma Ramp Values are:")
            displayGammaValues(GammaArray),

            if SetDeviceGammaRamp(hdc, ctypes.byref(GammaArray)):
                logging.info("Brightness set!!\n")
            else:
                logging.error("Unable to set brightness\n")
        
        try:
            if ReleaseDC(ctypes.POINTER(ctypes.c_int)(), hdc):  logging.info("HDC released\n")
            logging.debug("ReleaseDC Status:" + str(ReleaseDC(hdc)) + "\n")
        except Exception as error:
            logging.error(error)
    else:
        logging.error("HDC not found\n")


def apply_brightness(percent):
    """
    Converts percentages to actual brightness value between 0-128 and applies the brightness.
    :param: percent: Percentage in int
    """
    if percent<10: percent = 10
    if percent>100: percent = 100
    value = int((percent / 100) * 128)
    changeGamma(value)
    return percent


if __name__ == '__main__':
    apply_brightness(20)
    import time

    logging.info("Reverting in 2 second. DON'T EXIT!!")
    time.sleep(2)
    apply_brightness(100)




