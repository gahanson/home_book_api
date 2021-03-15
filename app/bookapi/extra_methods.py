import json
import urllib
from urllib.request import pathname2url, urlretrieve

from django.apps import apps

from .models import Book, bookapiUserSettings, bookapiSourceFiles

class BookProcessing(object):

    def __GetBookFilesOnServer(self):
        """
        - retrieve list of book files on a remote file server
        - return json data consisting of a list of each file
        """
        info = bookapiUserSettings.load()

        with urllib.request.urlopen(info.source_ip+info.source_script_path) as url:
            booksRaw = json.loads(url.read().decode())

        return booksRaw

    def __NewBooks(self, current_files, previous_files):
        """
        - compare list of books on hard drive to a list saved from previous
        refresh
        - return list of new books on hard drive 
        """
        on_drive = current_files
        lastRun = previous_files
        returnValue = [i for i in on_drive if not i in lastRun ]

        return returnValue

    def __RemovedBooks(self, current_files, previous_files):
        """
        - compare list of books on hard drive to a list saved from previous
        refresh
        - return list of files that are no longer on the hard drive 
        """
        on_drive = current_files
        lastRun = previous_files
        returnValue = [i for i in lastRun if not i in on_drive ]

        return returnValue

    def __AddSingleBook(self, file_path):
        """
        - add a single book file to the database
        create a url to use for viewing the book in a web browser
        save book file name to database
        - return message if song has been saved to db or not
        """
        returnData = []

        info = bookapiUserSettings.load()
       
        book_url = info.source_ip+urllib.parse.quote(file_path[1:])

        if Book.objects.filter(remote_url=book_url).exists() == False:
            Book.objects.create(
                title = file_path[1:],
                remote_url = book_url,
            )
            returnData.append({"saved":file_path[1:]})
        else:
            returnData.append({"not saved":file_path[1:]})
                    
        return returnData
    
    def __DeleteSingleBook(self, file_path):
        """
        - remove a single book from the database
        """
        info = bookapiUserSettings.load()
        book_url = info.source_ip+urllib.parse.quote(file_path[1:])
        bookInstance = Book.objects.get(remote_url=book_url)
        bookInstance.delete()

        return {"deleted":file_path[1:]}

    def GetUserSettings(self):
        info = bookapiUserSettings.load()
        returnVal = {{"source_ip":info.source_ip},{"source_script_path":info.source_script_path}}
        return returnVal

    def SetUserSettings(self, sourceIP, sourceScriptPath):
        
        try:
            info = bookapiUserSettings.load()

            info.source_ip = sourceIP
            info.source_script_path = sourceScriptPath

            info.save()
            
            return {"result":"settings saved"}

        except:
            return {"result":"save settings error"}
        
    def RefreshBooks(self):
        """
        compare a list of current files on the file system to a saved list 
        add new files to DB
        remove old files from DB
        - return list of files added and removed
        """
        addReturnData = []
        delReturnData = []

        apiSettings = bookapiSourceFiles.load()

        filesOnServer = self.__GetBookFilesOnServer()
        filesPresentLastRefresh = []
        if apiSettings.source_json:
            filesPresentLastRefresh = json.loads(apiSettings.source_json)
                
        newBookFiles = self.__NewBooks(filesOnServer, filesPresentLastRefresh)
        deletedBooks = self.__RemovedBooks(filesOnServer, filesPresentLastRefresh)
        
        if newBookFiles:
            for book in newBookFiles:
                if ('.epub' in book) or ('.pdf' in book): 
                    addResult = self.__AddSingleBook(book)
                    addReturnData.append(addResult)
        
        if deletedBooks:
            for book in deletedBooks:
                if ('.epub' in book) or ('.pdf' in book):
                    delResult = self.__DeleteSingleBook(book)
                    delReturnData.append(delResult)

        
        apiSettings.source_json = json.dumps(filesOnServer)
        apiSettings.save()
        
        return {'added':addReturnData, 'deleted':delReturnData}
