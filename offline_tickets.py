import uuid
from PIL import Image
import qrcode
ticket = Image.open('420171276_218935001215342_6328032920352527963_n.jpg')

for index in range(1, 1200):
    ID = uuid.uuid5(uuid.NAMESPACE_DNS, str(index))
    qr = qrcode.make(index).save('temp.png')
    qr = Image.open('temp.png')
    qr = qr.resize((77, 77))
    ticket.paste(qr, (352, 90))
    ticket.save(f'QRCODES/offline/{index}.png')

