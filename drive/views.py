from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import transaction
from django.core.urlresolvers import reverse

# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

# Create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

# Manually create HttpResponses or raise an Http404 exception
from django.http import HttpResponse, Http404

from models import *
from forms import *
from mimetypes import guess_type
import time

import dropbox

#Google Drive imports
from apiclient.http import MediaFileUpload
from oauth2client.client import OAuth2WebServerFlow

#Global Constants
DROPBOX_CLIENT_KEY = 'rmo9qsubqjklumv'
DROPBOX_CLIENT_SECRET = 'ngoaud74r2j9nmf'

GOOGLE_CLIENT_KEY = "792583114708-8cmffai4gdv6gha87ri1ee74ati9sio8.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "vZZgRwYyuyQtCfIHFArhq-DT"
GOOGLE_OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive'

model_dict = {
  "Dropbox" : DropboxModel,
  "Google Drive" : GoogleDriveModel,
}

@login_required
def home(request):
  accounts_dict = {}
  total = 0
  for key in model_dict.keys():
    model_classname = model_dict[key]
    all_accounts = list(model_classname.getAllAccounts(request.user))
    #all_accounts = [x.account_name for x in all_accounts]
    print "all_accounts: ", all_accounts
    for account in all_accounts:
      total+=account.getTotalSpace()
    if(len(all_accounts)>0):
      accounts_dict[key]=all_accounts


  context = {'accounts_dict':accounts_dict, 'total_space':total}
  return render(request, 'home.html', context)



@login_required
def addGoogleDrive(request):
  OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive'
  redirect_url = 'http://%s%s' % (request.get_host(), reverse('googleCallback'))
  flow = OAuth2WebServerFlow(GOOGLE_CLIENT_KEY, GOOGLE_CLIENT_SECRET, OAUTH_SCOPE, redirect_url)
  authorize_url = flow.step1_get_authorize_url()
  print authorize_url
  return redirect(authorize_url)

@login_required
def googleCallback(request):
  OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive'
  redirect_url = 'http://%s%s' % (request.get_host(), reverse('googleCallback'))
  flow = OAuth2WebServerFlow(GOOGLE_CLIENT_KEY, GOOGLE_CLIENT_SECRET, OAUTH_SCOPE, redirect_url)
  code = request.GET['code']
  credentials = flow.step2_exchange(code)
  if credentials.refresh_token is not None:
    google_drive_account = GoogleDriveModel.createModel(request.user,credentials)
    google_drive_account.save()
    context = google_drive_account.createContext()
    return render(request, 'rename.html', context)
  else:
    print "token", credentials.refresh_token
    print "no refresh_token"
    return redirect(reverse('home'))
    



@login_required
def addDropbox(request):
  redirect_url = 'http://%s%s' % (request.get_host(), reverse('dropboxCallback'))
  oauth_client = dropbox.client.DropboxOAuth2Flow(DROPBOX_CLIENT_KEY, DROPBOX_CLIENT_SECRET, redirect_url, request.session, "dropbox-auth-csrf-token")
  authorize_url = oauth_client.start()
  return redirect(authorize_url)

@login_required
def dropboxCallback(request):
  redirect_url = 'http://%s%s' % (request.get_host(), reverse('dropboxCallback'))
  oauth_client = dropbox.client.DropboxOAuth2Flow(DROPBOX_CLIENT_KEY, DROPBOX_CLIENT_SECRET, redirect_url, request.session, "dropbox-auth-csrf-token")
  try:
    access_token, user_id, url_state = oauth_client.finish(request.GET)
    if(DropboxModel.accountExists(user_id)):
      account = DropboxModel.getAccountByUserId(user_id)
      account.access_token = access_token
      account.save()
      return redirect(reverse('home'))
    else:
      account_name = str(int(time.time()))
      dropbox_account = DropboxModel(owner = request.user, access_token = access_token, user_id = user_id, account_name = account_name)
      dropbox_account.save()
      context = dropbox_account.createContext()
      return render(request, 'rename.html', context)
  except dropbox.client.DropboxOAuth2Flow.BadRequestException, e:
    return HttpResponse(status=400)
  except dropbox.client.DropboxOAuth2Flow.BadStateException, e:
    return redirect(reverse('addDropbox'))
  except dropbox.client.DropboxOAuth2Flow.CsrfException, e:
    return HttpResponse(status = 403)
  except dropbox.client.DropboxOAuth2Flow.NotApprovedException, e:
    return redirect(reverse('home'))
  except dropbox.client.DropboxOAuth2Flow.ProviderException, e:
    return HttpResponse(status = 403)


@login_required
def addAccounts(request):
  context = {}
  return render(request, 'addAccounts.html', context)

@login_required
def rename(request, old_account_name, account_type):
  if request.method == "GET":
    context = {}
    return render(request, 'addAccounts.html', context)
  elif request.method == "POST":
    form = AccountNameForm(request.POST)
    if not form.is_valid():
      print "Form invalid"
      return render(request, 'addAccounts.html', context)
    else:
      model_classname = ""
      #Check if account_type is valid. It is possible for user to change value of account_type. 
      if account_type in model_dict:
        model_classname = model_dict[account_type]
      else:
        return redirect(reverse('home'))
      account = model_classname.getAccountByName(request.user, old_account_name)
      if account:
        new_account_name = form.cleaned_data['new_account_name']
        if(model_classname.nameTaken(request.user,new_account_name)):
          context = account.createContext()
          return render(request, 'rename.html', context)
        else:
          account.account_name = new_account_name
          account.save()
          return redirect(reverse('home'))
      else:
        print "NO ACCOUNT"
        return redirect(reverse('home'))




def register(request):
  context = {}
  if request.method == 'GET':
    context['form'] = RegistrationForm()
    return render(request, 'register.html', context)
  else:
    form = RegistrationForm(request.POST)
    context['form'] = form
    # Validates the form.
    if not form.is_valid():
      return render(request, 'register.html', context)
    else:
    # If we get here the form data was valid.  Register.
      new_user = User.objects.create_user(username=form.cleaned_data['email'], 
                                  password=form.cleaned_data['password1'], 
                                  first_name=form.cleaned_data['first_name'], 
                                  last_name=form.cleaned_data['last_name'])
      new_user.is_active = False
      new_user.save()
      tokenstring = default_token_generator.make_token(new_user)
      dashlocation = tokenstring.index("-")
      length = len(tokenstring)
      token = tokenstring[dashlocation+1:length]
      new_user.email = token
      new_user.save()
      my_user = MyUser(user=new_user)
      my_user.save()
      email_body = "Enter this link in your browser to register your account.\n"
      link = "http://%s%s" %(request.get_host(),'/drive/verify/'+new_user.email)
      context['email'] = email_body
      context['link'] = link
      return render(request, 'confirm.html', context)

@transaction.atomic
def verify(request, token):
    context = {}
    try:
        user = User.objects.get(email=token)
        user.is_active = True
        user.save()
        return redirect(reverse('home'))
    except Exception:
        return redirect(reverse('home'))

















