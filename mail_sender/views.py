from django.shortcuts import render
import time
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from .authhelper import get_signin_url, get_token_from_code, get_access_token
from .outlookservice import get_me, get_my_messages
from .confirm_gen import ConfirmForm
from .confirm_vlz import ConfirmFormVLZ
from django.core.files.storage import FileSystemStorage
from .customise_general import customise_general
from .get_parameters import getParameters
# from .ckeditor_form import EmailComponent
from .summernote_form import EmailComponent
from TaaraMail.settings import MEDIA_ROOT
from .get_base64_encoded_img import replace_src_for_MIME


def home(request):
    redirect_uri = request.build_absolute_uri(reverse('mail_sender:gettoken'))
    sign_in_url = get_signin_url(redirect_uri)
    context = {'signin_url': sign_in_url}
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
        response = HttpResponseRedirect(reverse("mail_sender:customise"))
        response.set_cookie("html_code_email", "NIL")
        return response
    return render(request, 'upload.html')


def customise(request):
    access_token = get_access_token(request=request,
                                    redirect_uri=request.build_absolute_uri(reverse('mail_sender:gettoken')))

    parameters = getParameters(filename=request.session['filename'])

    form = EmailComponent(request.POST)

    if request.method == 'POST':
        parameter_count = 1
        if 'parameter_count' in request.COOKIES:
            parameter_count = int(request.COOKIES['parameter_count'])
        request.COOKIES['parameter_count'] = '1'
        parameter_list = {}
        for x in range(1, parameter_count + 1):
            i = str(x)
            gen_para = 'gen-para-' + i
            gen_para_value = 'gen-para-' + i + '-value'
            gen_para_blank_check = 'gen-para-' + i + '-blank-check'
            gen_para_not_blank_check = 'gen-para-' + i + '-not-blank-check'

            parameter_list[request.POST[gen_para]] = request.POST[gen_para_value]

        subject = request.POST['email-part-subject']
        body = "Sample Body"

        if form.is_valid():
            body = form.data['content']
            body, attachments = replace_src_for_MIME(body=body)
        else:
            form = EmailComponent()

        customise_general(access_token, request.session['filename'], parameter_list, subject, body,
                          attachments=attachments)
        response = HttpResponseRedirect(reverse("mail_sender:confirm_gen"))
        response.delete_cookie("html_code_email")
        return response
    return render(request, 'customise-general.html', {'form': form, 'parameters': parameters, 'media_root': MEDIA_ROOT})


def confirm_gen(request):
    request.COOKIES['parameter_count'] = '1'
    form = ConfirmForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            answer = form.cleaned_data['like']
            answer = dict(form.fields['like'].choices)[answer]

            if answer == "Yes":
                return HttpResponseRedirect(reverse("mail_sender:customise"))
            else:
                return HttpResponseRedirect(reverse("mail_sender:customise_vlz"))
        else:
            form = ConfirmForm()
    return render(request, 'confirm_gen.html', {'form': form})


def customise_vlz(request):
    access_token = get_access_token(request=request,
                                    redirect_uri=request.build_absolute_uri(reverse('mail_sender:gettoken')))

    parameters = getParameters(request.session['vlz_report'])
    if request.method == 'POST':
        parameter_count = 1
        if 'parameter_count' in request.COOKIES:
            parameter_count = int(request.COOKIES['parameter_count'])
        request.COOKIES['parameter_count'] = '1'
        parameter_list = {}
        for x in range(1, parameter_count + 1):
            i = str(x)
            vlz_para = 'vlz-para-' + i
            vlz_para_value = 'vlz-para-' + i + '-value'
            vlz_para_blank_check = 'vlz-para-' + i + '-blank-check'
            vlz_para_not_blank_check = 'vlz-para-' + i + '-not-blank-check'

            parameter_list[request.POST[vlz_para]] = request.POST[vlz_para_value]

        subject = request.POST['email-part-subject']
        body = "sample email body"
        customise_general(access_token=access_token, filename=request.session['vlz_report'],
                          parameter_dict=parameter_list, subject=subject, body=body)
        return HttpResponseRedirect(reverse("mail_sender:confirm_vlz"))
    return render(request, "customise_vlz.html", {'parameters': parameters})


def confirm_vlz(request):
    request.COOKIES['parameter_count'] = '1'
    form = ConfirmFormVLZ(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            answer = form.cleaned_data['selection']
            answer = dict(form.fields['selection'].choices)[answer]

            if answer == "Yes":
                return HttpResponseRedirect(reverse("mail_sender:customise_vlz"))
            else:
                return HttpResponseRedirect(reverse("mail_sender:send"))
        else:
            form = ConfirmFormVLZ()
    return render(request, 'confirm_vlz.html', {'form': form})


def summernote_upload(request):
    render("This works")
