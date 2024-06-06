from PIL import Image
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import binascii

def image_to_hex(image_path):
    with Image.open(image_path) as img:
        img = img.convert('RGB')
        width, height = img.size
        pixel_data = list(img.getdata())
        hex_data = ''.join([f'{r:02x}{g:02x}{b:02x}' for r, g, b in pixel_data])
    return hex_data, width, height

def hex_to_image(hex_data, width, height, output_path):
    pixel_data = [tuple(int(hex_data[i:i+2], 16) for i in range(j, j+6, 2)) for j in range(0, len(hex_data), 6)]
    img = Image.new('RGB', (width, height))
    img.putdata(pixel_data)
    img.save(output_path)

def des_encrypt(hex_data, key):
    backend = default_backend()
    cipher = Cipher(algorithms.DES(key), modes.ECB(), backend=backend)
    encryptor = cipher.encryptor()
    # Ensure the hex data is padded to a multiple of 16 characters
    padded_hex_data = hex_data + ('0' * (16 - len(hex_data) % 16))
    encrypted_data = encryptor.update(binascii.unhexlify(padded_hex_data)) + encryptor.finalize()
    return binascii.hexlify(encrypted_data).decode()

def des_decrypt(encrypted_hex_data, key):
    backend = default_backend()
    cipher = Cipher(algorithms.DES(key), modes.ECB(), backend=backend)
    decryptor = cipher.decryptor()
    encrypted_data = binascii.unhexlify(encrypted_hex_data)
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
    return binascii.hexlify(decrypted_data).decode()

def main(input_image_path, output_image_path, key):
    # Ensure the key is 8 bytes
    if len(key) != 8:
        raise ValueError("Key must be 8 bytes long")

    # Convert image to hex string
    hex_data, width, height = image_to_hex(input_image_path)

    # Encrypt the hex string
    encrypted_hex_data = des_encrypt(hex_data, key)

    # Convert encrypted hex string back to image
    hex_to_image(encrypted_hex_data[:len(hex_data)], width, height, output_image_path)
    print(f"Encrypted image saved to {output_image_path}")

if __name__ == '__main__':
    input_image_path = 'cardinal.png'
    output_image_path = 'output.bmp'
    key = b'8bytekey'  # 8-byte key for DES

    main(input_image_path, output_image_path, key)
