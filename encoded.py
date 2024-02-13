import base64

# Read the image file as binary data
with open("logo.png", "rb") as image_file:
    # Encode the binary data as Base64
    base64_encoded = base64.b64encode(image_file.read()).decode("utf-8")

# Save the Base64-encoded string to a variable in another file
with open("logo_base64.py", "w") as output_file:
    output_file.write(f"logo_base64 = '''\n{base64_encoded}\n'''")
