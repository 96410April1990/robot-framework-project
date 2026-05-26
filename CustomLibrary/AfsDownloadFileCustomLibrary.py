from azure.storage.fileshare import ShareFileClient
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import os
import time

class AfsDownloadFileCustomLibrary(object):

    ROBOT_LIBRARY_VERSION = '__version__'
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    global file_client_download
    global blob_client_download

    def download_file_from_afs(self, connStr, shareName, remoteFilePath, fileName):
        self.file_client_download = ShareFileClient.from_connection_string(conn_str=connStr, share_name=shareName, file_path=remoteFilePath + "/" + fileName)

        print("Downloading the file from the AFS to the Downloads folder")

        with open("Downloads/"+fileName, "wb") as file_handle:
            data = self.file_client_download.download_file()
            file_handle.write(data.readall())

    def upload_file_to_afs(self, connStr, shareName, remoteFilePath, fileName):
        self.file_client_upload = ShareFileClient.from_connection_string(conn_str=connStr, share_name=shareName, file_path=remoteFilePath + "/" + fileName)

        print("Uploading the file from the Downloads folder to the AFS")

        with open("Downloads/"+fileName, "rb") as file_handle:
            os.system("chmod 777 Downloads/"+fileName)
            data = self.file_client_upload.upload(file_handle)

    def download_file_from_blob(self, connStr, containerName, fileName):
        self.blob_client_download = BlobServiceClient.from_connection_string(connStr)

        container_name = containerName
        blob_name = fileName
        blob_client = self.blob_client_download.get_blob_client(container_name, blob_name)
        
        print("Downloading the file from the Azure Blob to the Downloads folder")
        
        with open("Downloads/"+fileName, "wb") as file_handle:
            os.system("chmod 777 Downloads/"+fileName)
            file_handle.write(blob_client.download_blob().readall())

    def delete_file_inside_blob(self, connStr, fromContainerName, file_name):
        self.blob_service_client = BlobServiceClient.from_connection_string(connStr)

        source_blob = fromContainerName
        blob_name = file_name
        source_blob_client = self.blob_service_client.get_blob_client(source_blob, blob_name)
        source_blob_client.delete_blob()

    def upload_file_to_blob(self, connStr, toContainerName, fileName):
        self.blob_client_download = BlobServiceClient.from_connection_string(connStr)

        container_name = toContainerName
        blob_name = fileName
        blob_client = self.blob_client_download.get_blob_client(container_name, blob_name)

        print("Uploading the file to the"+" "+toContainerName+" "+"blob folder from the Downloads folder")

        with open("Downloads/"+fileName, "rb") as data:
            os.system("chmod 777 Downloads/"+fileName)
            blob_client.upload_blob(data)

    def move_file_from_blob_to_blob(self, connStr, fromContainerName, toContainerName, fileName):
        self.blob_client_move_file = BlobServiceClient.from_connection_string(connStr)

        source_blob_client = self.blob_client_move_file.get_blob_client(fromContainerName, fileName)
        destination_blob_client = self.blob_client_move_file.get_blob_client(toContainerName, fileName)
        copy_file = destination_blob_client.start_copy_from_url(source_blob_client.url)

        while destination_blob_client.get_blob_properties().copy.status != 'success':
            time.sleep(1)

        source_blob_client.delete_blob()
