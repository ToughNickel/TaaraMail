from django.shortcuts import render
import time
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from .authhelper import get_signin_url, get_token_from_code, get_access_token
from .outlookservice import get_me, get_my_messages
from .filtered_selection import filtred_selected_mail_sender
from django.core.files.storage import FileSystemStorage


def home(request):
    redirect_uri = request.build_absolute_uri(reverse('mail_sender:gettoken'))
    sign_in_url = get_signin_url(redirect_uri)
    context = {'signin_url' : sign_in_url}
    return render(request, 'home.html', context)


def gettoken(request):
    auth_code = request.GET['code']
    redirect_uri = request.build_absolute_uri(reverse('mail_sender:gettoken'))
    token = get_token_from_code(auth_code=auth_code, redirect_uri=redirect_uri)
    access_token = token['access_token']
    user = get_me(access_token=access_token)
    refresh_token = token['refresh_token']
    expires_in = token['expires_in']

    # expires_in is in seconds
    # Get current timestamp (seconds since Unix Epoch) and
    # add expires_in to get expiration time
    # Subtract 5 minutes to allow for clock differences
    expiration = int(time.time()) + expires_in - 300

    # Save the token in the session
    request.session['access_token'] = access_token
    request.session['refresh_token'] = refresh_token
    request.session['token_expires'] = expiration
    return HttpResponseRedirect(reverse('mail_sender:upload'))


def mail(request):
    access_token = get_access_token(request, request.build_absolute_uri(reverse('mail_sender:gettoken')))
    # if no token, redirect to home
    if not access_token:
        return HttpResponseRedirect(reverse('mail_sender:home'))
    else:
        messages = get_my_messages(access_token=access_token)
        context = {'message': messages}
        return render(request, 'mail.html', context)


def send(request):
    access_token = get_access_token(request=request,
                                    redirect_uri=request.build_absolute_uri(reverse('mail_sender:gettoken')))
    if not access_token:
        return HttpResponseRedirect(reverse('mail_sender:home'))
    else:
        filtred_selected_mail_sender(access_token=access_token, filename=request.session['filename'],
                                     vlz_report=request.session['vlz_report'])
        return render(request, 'sentMail.html')


def upload(request):
    if request.method == 'POST' and request.FILES['document'] and request.FILES['vlz_report']:
        myfile = request.FILES['document']
        myfile_2 = request.FILES['vlz_report']
        fs = FileSystemStorage()
        fs.save(myfile.name, myfile)
        fs.save(myfile_2.name, myfile_2)
        request.session['filename'] = myfile.name
        request.session['vlz_report'] = myfile_2.name
        return HttpResponseRedirect(reverse("mail_sender:send"))
    return render(request, 'upload.html')
