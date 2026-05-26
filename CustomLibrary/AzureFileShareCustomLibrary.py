
from azure.storage.fileshare import ShareDirectoryClient
from datetime import datetime

class AzureFileShareCustomLibrary(object):

    ROBOT_LIBRARY_VERSION = '__version__'
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    global currentMonth, currentYear, getMonthYear, stbconn, fileUploadStatus

    fileUploadStatus = False
    currentMonth = str(datetime.now().month)
    currentYear = str(datetime.now().year)

    getMonthYear = currentMonth+"-"+currentYear
    stbconn = ""

    def __init__(self, connStr, shareName, directoryPath):
        self.stbconn = ShareDirectoryClient.from_connection_string(conn_str=connStr, share_name=shareName, directory_path=directoryPath + "/" + getMonthYear)

    #def connect_to_afs(self, connStr, shareName, directoryPath):
    #    stbconn = ShareDirectoryClient.from_connection_string(conn_str=connStr, share_name=shareName, directory_path=directoryPath+"/"+getMonthYear)
    #    return stbconn

    def verify_if_file_is_available(self, fileName):
        file_list = list(self.stbconn.list_directories_and_files())
        #file_list = list(stbconn.list_directories_and_files())
        print(file_list)
        for file in file_list:
            getFileDetails = str(file)
            for getFileName in fileName:
                if getFileName in getFileDetails:
                    print(file)
                    fileUploadStatus = True
                    return fileUploadStatus
                else:
                    fileUploadStatus = False
                    continue
        return fileUploadStatus