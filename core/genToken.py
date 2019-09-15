import secrets
import qrcode.image.svg
import qrcode
import os

from flask import current_app

def genToken():
    return ''.join(secrets.token_urlsafe(16))

def genQRCode(revoked=False):
	root_path = current_app.root_path
	qr = os.path.join(root_path, "static/token/qrcode.svg")
	if revoked:
		os.remove(qr)
	if not os.path.exists(qr):
		factory = qrcode.image.svg.SvgImage
		img = qrcode.make(token, image_factory=factory)
		img.save(qr)
	else:
		os.remove(qr)
