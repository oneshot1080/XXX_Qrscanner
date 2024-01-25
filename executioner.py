from process_data import add_many
from online_tickets import extract_ID_and_create_QRCODE

path = "members.xlsx"
add_many(path)
extract_ID_and_create_QRCODE()