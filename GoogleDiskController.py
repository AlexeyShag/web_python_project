from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload,MediaFileUpload
from googleapiclient.discovery import build
import pprint
import io

pp = pprint.PrettyPrinter(indent=4)

# see, edit, create and delete all of your google drive files


class GoogleDiskController:
    def __init__(self):
        self.__SCOPES = ['https://www.googleapis.com/auth/drive']

        self.__SERVICE_ACCOUNT_FILE = 'web-python-42-f734891ba1d0.json'

        self.__credentials = service_account.Credentials.from_service_account_file(
        self.__SERVICE_ACCOUNT_FILE, scopes=self.__SCOPES)

        self.__service = build(
            'drive', 
            'v3', 
            credentials=self.__credentials
            )

    def connect(self):
        pass

    def get(self):
        print(1)
        results = self.__service.files().list(pageSize=10,
                               fields="nextPageToken, files(id, name, mimeType, parents, createdTime)").execute()
        #pp.pprint(results)

        return results.get('files')
    
    def createFolder(self, parent, name):
        file_metadata = {
            'name': name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parent]
        }


        file = self.__service.files().create(body=file_metadata,
                                    fields='id').execute()



        
    def download(self, fileName: str, fileId: str):

        file_id = fileId

        request = self.__service.files().get_media(fileId=file_id)



        filename = 'Saves/' + fileName

        f = open(filename, "w+")
        f.write("1")
        f.close()

        fh = io.FileIO(filename, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print ("Download %d%%." % int(status.progress() * 100))
