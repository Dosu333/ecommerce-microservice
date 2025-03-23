from decouple import config
import requests

PAYMENT_SERVICE_URL = config('PAYMENT_SERVICE_URL')

def initialize_payment(headers, order_id, amount, vendor_id):
    headers = {"Authorization": headers.get("Authorization")}
    payment_response = requests.post(
            f"{PAYMENT_SERVICE_URL}/payment/initialize/",
            json={
                "orderId": order_id,
                "vendorId": vendor_id,
                "amount": amount
            },
            headers=headers
        )

    if payment_response.status_code == 201:
        payment_data = payment_response.json()
        payment_link = payment_data.get("data", {}).get('paymentUrl')
        return {'success': True, 'payment_link': payment_link}
    else:
        try:
            payment_data = payment_response.json()
            message = payment_data.get("message")
            return {'success': False, "message": message}
        except: 
            return {'success': False, "message": None}