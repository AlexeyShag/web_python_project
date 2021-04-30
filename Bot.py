from GoogleDiskController import GoogleDiskController
import telebot


class Bot:

    def __init__(self):
        self.__controller = GoogleDiskController()

        a = self.__controller.connect()

        self.__nowFolderId = '1Ygaq2cVyIbhp-LfH7ST1zfttPRHGkqKt'
        self.__rootId = '1Ygaq2cVyIbhp-LfH7ST1zfttPRHGkqKt'
        self.__nowFolderPath = '~/'

        #self.__controller.download(a[0]['name'], a[0]['id'])


        self.__bot = telebot.TeleBot('1664214879:AAEtSQdM25d1CbFTzUpliUP6tghSI-S3hvM');
        
        @self.__bot.message_handler(content_types=['text'])
        def get_text_messages(message):

            answer = ""

            if message.text == "ls":
                answer += self._Bot__nowFolderPath
                answer += '\n' + '\n'

                files = self._Bot__controller.get()

                for file in files:
                    if file['id'] != self._Bot__rootId and file['parents'][0] == self._Bot__nowFolderId:
                        answer += file['name']
                        answer += '\n'

                self._Bot__bot.send_message(
                    message.from_user.id,
                    answer
                    )
                return

            if message.text[:2] == "cd":
                _, path = message.text.split(' ')
                path = path.split('/')

                files = self._Bot__controller.get()

                if path[0] == '.':
                    return

                if path[0] == '..':
                    if self._Bot__nowFolderId == self._Bot__rootId:
                        self._Bot__bot.send_message(
                            message.from_user.id,
                            "cannot clime up from root folder"
                        )
                        return


                    for file in files:
                        if file['id'] == self._Bot__nowFolderId:



                            self._Bot__nowFolderId = file['parents'][0]
                            #print(self._Bot__nowFolderId)
                            p = self._Bot__nowFolderPath.split('/')
                            p.pop()
                            p.pop()
                            self._Bot__nowFolderPath = ""
                            for f in p:
                                self._Bot__nowFolderPath += f + '/'
                            self._Bot__bot.send_message(
                                message.from_user.id,
                                self._Bot__nowFolderPath
                            )
                            return




                for nextFolder in path:
                    goodStep = False
                    for file in files:
                        if file['id'] != self._Bot__rootId and file['parents'][0] == self._Bot__nowFolderId:

                            if file['name'] == nextFolder:
                                goodStep = True

                                self._Bot__nowFolderId = file['id']
                                self._Bot__nowFolderPath += nextFolder + '/'
                            if goodStep:
                                break


                        if goodStep:
                            break
                    if not goodStep:
                        self._Bot__bot.send_message(
                            message.from_user.id,
                            self._Bot__nowFolderPath + '\n\n' + "incorrect path"
                        )
                        return

                self._Bot__bot.send_message(
                    message.from_user.id,
                    self._Bot__nowFolderPath
                    )


            if message.text[:5] == "mkdir":
                _, folderName = message.text.split(' ')
                self._Bot__controller.createFolder(self.__nowFolderId, folderName)
                self._Bot__bot.send_message(
                    message.from_user.id,
                    self._Bot__nowFolderPath
                )

        self.__bot.polling(none_stop=True, interval=0)

