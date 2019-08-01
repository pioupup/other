
import argparse

def cutMagicNumbers(archive):
	with open(archive, 'rb') as file:
		currentType = file.read(2).decode()
	return launcher(currentType)

def launcher(extension):
	return {'PK': prepareBruteZip,
			'Ra': prepareBruteRar,
			}.get(extension, 'Not Found')

def prepareBruteZip(archive, dictionary):
	import zipfile
	'''
	file == 2.0
	type(pwd) == byte
	'''
	zArchive = zipfile.ZipFile(archive)
	with open(dictionary, 'r') as wordlist:
		for word in wordlist.readlines():
			password = word.strip('\n').encode('ascii') # inicode -> byte
			brute(zArchive, password)

def prepareBruteRar(archive, dictionary):
	'''
	type(pwd) == str
	requirements installed unrar
	'''
	rArchive = rarfile.RarFile(archive)
	with open(dictionary, 'r') as wordlist:
		for word in wordlist.readlines():
			password = word.strip('\n')	#str
			brute(rArchive, password)

def brute(archive, password):
	try:
		archive.extracall(pwd=password)
		print('[+] Password is {}'.format(password))
	except:
		pass

if __name__ == "__main__":
	parser = argparse.ArgumentParser('--file' + '--dict')
	parser.add_argument('-f', '--file', dest='archive', required=True, type=str, help='Archive file')
	parser.add_argument('-d', '--dict', dest='dictionary', required=True, type=str, help='Dictionary file')
	args = parser.parse_args()

	cutMagicNumbers(args.archive)(args.archive, args.dictionary)