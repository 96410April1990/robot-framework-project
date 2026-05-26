#  Customize Azure Module

# import os
# import azure
from azure.cosmos.cosmos_client import CosmosClient
from azure.cosmos.database import DatabaseProxy
from azure.cosmos.container import ContainerProxy

#import azure.cosmos.cosmos_client as CosmosClient
#import azure.cosmos.database as  DatabaseProxy
#import azure.cosmos.container as ContainerProxy

class CosmosLibrary(CosmosClient,DatabaseProxy,ContainerProxy):
    """
    Loading all cosmos files
    """
    #get_database_link= CosmosClient._get_database_link(DATABASE_ID)
    #ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    def __init__(self, url, credential , database_id, container_id):
        self.url = url
        self.credential = credential
        self.database_id = database_id
        self.container_id = container_id
        super().__init__(self.url, self.credential)
        super(CosmosClient, self).__init__(self.client_connection,self.database_id)
    #  super(DatabaseProxy, self).__init__(self.client_connection,self.database_link,container_id)
    def set_container(self,container_id):
        self.container_id = container_id
        super(DatabaseProxy, self).__init__(self.client_connection,self.database_link,container_id)
#    def get_database_link(self,database_id):
#        self.get_database_link= CosmosClient._get_database_link(database_id)
#        return  self.get_database_link
#    def get_container_link(self,container_id):
#        self.get_container_link= DatabaseProxy._get_container_link(self,container_or_id=container_id)
#        return  self.get_container_link
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'