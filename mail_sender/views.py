from django.shortcuts import render
import time
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from .authhelper import get_signin_url, get_token_from_code, get_access_token
from .outlookservice import get_me, get_my_messages
from .confirm_gen import ConfirmForm
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
        # filtred_selected_mail_sender(access_token=access_token, filename=request.session['filename'],
        #                              vlz_report=request.session['vlz_report'])
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
        request.session['parameter_count'] = 0
        return HttpResponseRedirect(reverse("mail_sender:customise"))
    return render(request, 'upload.html')


def customise(request):
    if request.method == 'POST':
        parameter_count = 1
        # parameter_count = request.session['parameter_count']
        parameter_list = []
        parameter_list_value = []
        for x in range(1,parameter_count+1):
            i = str(x)
            gen_para = 'gen-para-' + i
            gen_para_value = 'gen-para-' + i + '-value'
            gen_para_blank_check = 'gen-para-' + i + '-blank-check'
            gen_para_not_blank_check = 'gen-para-' + i + '-not-blank-check'
            parameter_list.append(gen_para)
            if request.POST.get(gen_para_not_blank_check, True):
                parameter_list_value.append("NOT-BLANK")
            elif request.POST.get(gen_para_blank_check, True):
                parameter_list_value.append("BLANK")
            else:
                parameter_list_value.append(gen_para_value)
        return HttpResponseRedirect(reverse("mail_sender:confirm_gen"))
    return render(request, 'customise-general.html')


def confirm_gen(request):
    form = ConfirmForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            answer = form.cleaned_data['yes']
            print(answer)
    return render(request, 'confirm_gen.html', {'form': form})


def customise_vlz(request):
    if request.method == 'POST':
        return HttpResponseRedirect(reverse("mail_sender:confirm_vlz"))
    return render(request, "customise_vlz.html")


def confirm_vlz(request):
    if request.method == 'GET':
        if request.POST.get('vlz-confirm-select', True):
            return HttpResponseRedirect(reverse("mail_sender:customise_vlz"))
        else:
            return HttpResponseRedirect(reverse("mail_sender:send"))
    return render(request, "confirm_vlz.html")
