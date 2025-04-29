import uuid
import qrcode

class Pix():
    def __init__(self):
        pass

    # base_dir created to use in unit tests   
    def create_payment(self, base_dir=""):
        # Create the payment at the bank
        bank_payment_id = str(uuid.uuid4())

        # Copie and paste pix
        hash_payment = f"hash_payment_{bank_payment_id}"

        # Qr Code
        img = qrcode.make(hash_payment)
        
        # Save qrcode image as png
        img.save(f"{base_dir}static/img/qr_code_payment_{bank_payment_id}.png")
        
        return {
                "bank_payment_id": bank_payment_id,
                "qr_code_path": f"qr_code_payment_{bank_payment_id}" 
                }