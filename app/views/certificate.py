from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User, Group
from datetime import date, datetime, timedelta, timezone
from django.db import transaction
from django.contrib.sessions.models import Session
from django.core.paginator import Paginator
from ..forms import *
from ..models import *
from ..email import *
from django.db.models import Q

def index(request):
    page = 'Certificate'
    try:
        if request.session.get('group') != 'Admin':
            return HttpResponseRedirect("/")
        
        if request.method == "POST":
            form = CertificateForm(request.POST)
            if form.is_valid():
                # Get the cleaned data
                name = form.cleaned_data['name']
                email = form.cleaned_data['email']
                details = form.cleaned_data['details']  # Quill editor's HTML content
                signatory = form.cleaned_data['signatory']
                
                # Send the certificate
                try:
                    send_certificate(name, email, details, signatory)
                    messages.success(request, 'Certificate Sent Successfully')
                except Exception as send_error:
                    messages.error(request, f"Failed to send certificate: {str(send_error)}")
                
                return HttpResponseRedirect("/certificate")
            else:
                messages.warning(request, form.errors)
        
        # Display the form for GET requests
        form = CertificateForm()
        return render(request, 'app/certificate.html', {'page': page, 'form': form})
    
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return HttpResponseRedirect("/certificate")
