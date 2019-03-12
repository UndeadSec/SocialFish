import shutil

def cleanFake():
	try:
		shutil.rmtree('templates/fake')
	except:
		pass