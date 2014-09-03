import dropbox

import httplib2
import pprint

import sys
import os

from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from oauth2client.client import OAuth2WebServerFlow

class MyUser:
    def __init__(self, name):
        self.name = name
        self.clients = {}
        
    #returns client with least percentage of available memory used or None if all are full
    def getLeastUsedClient(self):
        lowestPercentage = 100 #100 percent is highest possible
        lowestClient = None
        for client in self.clients:
            percentage = client.getPercentageUsed()
            if(percentage < lowestPercentage):
                lowestPercentage = percentage
                lowestClient = client
        return lowestClient 

    #TO DO
    def upload_folder(path):
        file_name = path.split("/")[0]
        
    def upload_file(path):
        file_name = path.split("/")[0]

    def addDropboxAccount(self, account_name):
        if(account_name not in self.clients):
            dropbox_client = Dropbox(account_name)
            if(dropbox_client.authorize()):
                self.clients[account_name] = dropbox_client

    def addGoogleDriveAccount(self, account_name):
        if(account_name not in self.clients):
            google_drive_client = GoogleDrive(account_name)
            if(google_drive_client.authorize()):
                self.clients[account_name] = google_drive_client    
        

#WRITE getPercentageUsed

        


class Dropbox:
    def __init__(self, account_name):
        self.APP_KEY = 'rmo9qsubqjklumv'
        self.APP_SECRET = 'ngoaud74r2j9nmf'
        self.limit = None
        self.client = None
        self.access_token = None
        self.user_id = None
        self.used_data = 0
        self.name = account_name

    def authorize(self):
        try:
            flow = dropbox.client.DropboxOAuth2FlowNoRedirect(self.APP_KEY, self.APP_SECRET)
            authorize_url = flow.start()
            print '1. Go to: ' + authorize_url
            print '2. Click "Allow" (you might have to log in first)'
            print '3. Copy the authorization code.'
            code = raw_input("Enter the authorization code here: ").strip()
            self.access_token, self.user_id = flow.finish(code)
            self.client = dropbox.client.DropboxClient(self.access_token)
            print 'linked account: ', self.client.account_info()
            return True
        except Exception as e:
            print "Caught Exception"
            print e
            return False

    def upload(self, file_dir, title):
        f = open(file_dir, 'rb')
        response = client.put_file(title, f)
        print "uploaded:", response
        f.close()
        self.used_data += int(response['bytes'])

        
    def getPercentageUsed(self):
        return (float(self.used_data)/self.limit)*100

    def getTotalSpace(self):
        total_bytes = self.client.account_info()['quota_info']['quota']
        return bytesToGigabytes(total_bytes)

    def getAvailableSpace(self):
        return bytesToGigabytes(self.limit - self.used_data)

    def setLimit(self, limit):
        self.limit = limit


class GoogleDrive:
    def __init__(self, account_name):
        self.CLIENT_ID = "792583114708-6i87s1a76rre352jqjobtijci1rng6ah.apps.googleusercontent.com"
        self.CLIENT_SECRET = "stSFixZcDCZqVAl9pZzIWqRc"
        self.OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive'

        # Redirect URI for installed apps
        self.REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'
        self.limit = None
        self.google_credentials = None
        self.client = None
        self.name = account_name

    def authorize(self):
        try:
            flow = OAuth2WebServerFlow(self.CLIENT_ID, self.CLIENT_SECRET, self.OAUTH_SCOPE, self.REDIRECT_URI)
            authorize_url = flow.step1_get_authorize_url()
            print 'Go to the following link in your browser: ' + authorize_url
            code = raw_input('Enter verification code: ').strip()
            self.google_credentials = flow.step2_exchange(code)
            http = httplib2.Http()
            http = self.google_credentials.authorize(http)
            self.client = build('drive', 'v2', http=http)
            return True
        except Exception as e:
            print "Error encountered"
            print e
            return False

    def upload(self, filename, title,  mimeType):
        media_body = MediaFileUpload(filename, mimetype=mimeType, resumable=True)
        body = {
            'title':title,
            'description': description,
            'mimeType': mimetype
        }
        file = self.client.files().insert(body=body, media_body = media_body).execute()
        pprint.pprint(file)

    def getPercentageUsed(self):
        pass

    def getTotalSpace(self):
        pass

    def getTotalAvailableSpace(self):
        pass

    def setLimit(self, limit):
        self.limit = limit

def bytesToGigabytes(bytes):
    return float(bytes)/1073741824
