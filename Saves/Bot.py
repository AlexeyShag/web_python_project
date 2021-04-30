from GoogleDiskController import GoogleDiskController

class Bot:
	def __init__(self):
		print(1)
		self.__controller = GoogleDiskController()

		a = self.__controller.get()

		self.__controller.download(a['name'], a['id'])
		pass

