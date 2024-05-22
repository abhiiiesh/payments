# from flask import Flask, render_template, request, redirect, url_for, jsonify
# import qrcode
# from io import BytesIO
# import base64
# import urllib.parse

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/generate_qr', methods=['POST'])
# def generate_qr():
#     contact_number = request.form['contact_number']
#     vyaparify_link = request.form['vyaparify_link']

#     # Encode contact number and Vyaparify link in URL
#     encoded_contact_number = urllib.parse.quote(contact_number)
#     encoded_vyaparify_link = urllib.parse.quote(vyaparify_link)
#     display_url = f"http://{request.host}/display_links?contact_number={encoded_contact_number}&vyaparify_link={encoded_vyaparify_link}"

#     # Generate QR code
#     qr = qrcode.QRCode(
#         version=1,
#         error_correction=qrcode.constants.ERROR_CORRECT_L,
#         box_size=10,
#         border=4,
#     )
#     qr.add_data(display_url)
#     qr.make(fit=True)
    
#     img = qr.make_image(fill='black', back_color='white')
#     buffered = BytesIO()
#     img.save(buffered, format="PNG")
#     img_str = base64.b64encode(buffered.getvalue()).decode()

#     return render_template('qrcode.html', qr_code=img_str)

# @app.route('/display_links')
# def display_links():
#     contact_number = request.args.get('contact_number')
#     vyaparify_link = request.args.get('vyaparify_link')
#     payment_link = f"upi://pay?pa={contact_number}"  # Example UPI payment link format

#     return render_template('display_links.html', payment_link=payment_link, vyaparify_link=vyaparify_link)

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for
import qrcode
from io import BytesIO
import base64
import urllib.parse

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    contact_number = request.form['contact_number']
    vyaparify_link = request.form['vyaparify_link']

    if not contact_number or not vyaparify_link:
        return "Contact number and Vyaparify link are required.", 400

    # Encode contact number and Vyaparify link in URL
    encoded_contact_number = urllib.parse.quote(contact_number)
    encoded_vyaparify_link = urllib.parse.quote(vyaparify_link)
    display_url = f"http://{request.host}/display_links?contact_number={encoded_contact_number}&vyaparify_link={encoded_vyaparify_link}"

    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(display_url)
    qr.make(fit=True)
    
    img = qr.make_image(fill='black', back_color='white')
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    return render_template('qrcode.html', qr_code=img_str)

@app.route('/display_links')
def display_links():
    contact_number = request.args.get('contact_number')
    vyaparify_link = request.args.get('vyaparify_link')

    if not contact_number or not vyaparify_link:
        return "Contact number and Vyaparify link are required.", 400

    # Decode the URLs to ensure they are properly formatted
    decoded_contact_number = urllib.parse.unquote(contact_number)
    decoded_vyaparify_link = urllib.parse.unquote(vyaparify_link)
    
    payment_link = f"upi://pay?pa={decoded_contact_number}"  # Example UPI payment link format

    return render_template('display_links.html', payment_link=payment_link, vyaparify_link=decoded_vyaparify_link)

if __name__ == '__main__':
    app.run(debug=True)
