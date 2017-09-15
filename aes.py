import os, random, struct
from Crypto.Cipher import AES

def encrypt_file(key, in_filename,target_folder):
    chunksize=64*1024
    lastindex=in_filename.rfind("/")
    new_in_filename=in_filename[lastindex+1:] 
    out_filename =target_folder+"/"+ new_in_filename + '.enc'

    iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(in_filename)

    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += ' ' * (16 - len(chunk) % 16)
                outfile.write(encryptor.encrypt(chunk))
                os.remove(in_filename)


def decrypt_file(key, in_filename,target_folder):
    chunksize=64*1024
    full_name=os.path.splitext(in_filename)[0]
    lastindex=full_name.rfind("/")
    new_in_filename=full_name[lastindex+1:]
    out_filename =target_folder+"/"+new_in_filename
    print full_name
    with open(in_filename, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)

        with open(out_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))

            outfile.truncate(origsize)
            os.remove(in_filename)
