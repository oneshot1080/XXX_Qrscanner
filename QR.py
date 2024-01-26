import qrcode
from qrcode.constants import ERROR_CORRECT_L
def QR(ID: str):
    qr = qrcode.QRCode( # type: ignore
        version=None, 
        error_correction = ERROR_CORRECT_L, 
        box_size = 10,
        border = 1
    ) 

    qr.add_data(ID)
    qr.make(fit=True)
    img = qr.make_image(back_color='white', fill_color='black')
    return img