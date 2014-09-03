from django.db import models
from django.contrib.auth.models import User
import dropbox

import pickle
import base64
from oauth2client.django_orm import FlowField
from oauth2client.django_orm import CredentialsField

#Google Drive imports
import httplib2
import pprint
from apiclient.discovery import build
#Google Drive credentials storage
from oauth2client.django_orm import Storage

import time


def bytesToGigabytes(bytes):
  return float(bytes)/1073741824

class CredentialsModel(models.Model):
  owner = models.TextField()
  credential = CredentialsField()

class DropboxModel(models.Model):
  owner = models.ForeignKey(User)
  access_token = models.TextField()
  user_id = models.TextField()
  account_name = models.TextField()

  @staticmethod
  def accountExists(user_id):
    if DropboxModel.objects.filter(user_id = user_id):
      return True
    else:
      return False

  @staticmethod
  def nameTaken(user, name):
    if DropboxModel.objects.filter(owner = user, account_name = name):
      return True
    else:
      return False

  @staticmethod
  def getAccountByName(user, name):
    accountQuerySet = DropboxModel.objects.filter(owner = user, account_name = name)
    if len(accountQuerySet) != 1:
      return None
    else:
      return accountQuerySet.get()

  @staticmethod
  def getAccountByUserId(user_id):
    accountQuerySet = DropboxModel.objects.filter(user_id = user_id)
    if len(accountQuerySet) != 1:
      return None
    else:
      return accountQuerySet.get()
  @staticmethod
  def getAllAccounts(user):
    return DropboxModel.objects.filter(owner=user)

  def getClient(self):
    return dropbox.client.DropboxClient(self.access_token)

  def getAccountInfo(self):
    client = self.getClient()
    return client.account_info()

  def getTotalSpace(self, client = None):
    if not client:
      client = self.getClient()
    total_bytes = client.account_info()['quota_info']['quota']
    return bytesToGigabytes(total_bytes)

  def createContext(self):
    client = self.getClient()
    account_info = client.account_info()
    context = {"username": account_info['display_name'], "account_name":self.account_name, "account_type":"Dropbox",
              'referral_link': account_info['referral_link'], "total_space": self.getTotalSpace(client)}
    return context




class GoogleDriveModel(models.Model):
  owner = models.ForeignKey(User)
  account_name = models.TextField()
  email_address = models.TextField()

  @staticmethod
  def accountExists(email_address):
    if GoogleDriveModel.objects.filter(email_address = email_address):
      return True
    else:
      return False
  @staticmethod
  def nameTaken(user, name):
    if GoogleDriveModel.objects.filter(owner = user, account_name = name):
      return True
    else:
      return False

  @staticmethod
  def getStorage(email_address):
    return Storage(CredentialsModel, 'owner', email_address, 'credential')

  @staticmethod
  def getAccountByName(user, name):
    accountQuerySet = GoogleDriveModel.objects.filter(owner = user, account_name = name)
    if len(accountQuerySet) != 1:
      return None
    else:
      return accountQuerySet.get()

  @staticmethod
  def getAllAccounts(user):
    return GoogleDriveModel.objects.filter(owner=user)

  @staticmethod
  def get_user_info(credentials):
    http = httplib2.Http()
    http = credentials.authorize(http)
    client = build('drive', 'v2', http=http)
    return client.about().get().execute()['user']['emailAddress']


  @classmethod
  def createModel(cls, user, credentials):
    email_address = cls.get_user_info(credentials)
    storage = cls.getStorage(email_address)
    storage.put(credentials)
    account_name = str(int(time.time()))
    return cls(owner = user, account_name = account_name, email_address = email_address)

  def getTotalSpace(self, client = None):
    if not client:
      client = self.getAPIClient(self.email_address)
    account_info = client.about().get().execute()
    total_space = bytesToGigabytes(int(account_info['quotaBytesTotal']))
    return total_space

  def getAPIClient(self, email_address):
    storage = self.getStorage(self.email_address)
    credentials = storage.get()
    http = httplib2.Http()
    http = credentials.authorize(http)
    client = build('drive', 'v2', http=http)
    return client

  def createContext(self):
    drive_client = self.getAPIClient(self.email_address)
    account_info = drive_client.about().get().execute()
    display_name = account_info['user']['displayName']
    email_address = account_info['user']['emailAddress']
    total_space = bytesToGigabytes(int(account_info['quotaBytesTotal']))
    context = {"username": display_name, "account_name":self.account_name, "account_type":"Google Drive",
              "total_space": total_space}
    return context

    


  



class MyUser(models.Model):
  user = models.OneToOneField(User, unique = True)
  