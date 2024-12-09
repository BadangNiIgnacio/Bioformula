from django.core.mail import send_mail, EmailMultiAlternatives
from datetime import date, datetime, timedelta, timezone
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from weasyprint import HTML
from io import BytesIO
def generate_certificate_pdf(name, details, signatory):
    # Render the certificate HTML
    html_content = render_to_string('app/emails/certificate.html', {
        'name': name,
        # 'inclusive_date': inclusive_date,    
        'details': details,
        'signatory': signatory,
    })
    # Create a BytesIO object to store PDF
    pdf_file = BytesIO()
    # Generate PDF using WeasyPrint
    HTML(string=html_content).write_pdf(pdf_file)
    return pdf_file

def send_registration_success_email(firstname, email, id):
    subject = 'Badang ni Ignacio - Validate Your Account'
    message = 'Validate your account to sign in to your account'
    from_email = 'biofarmula3@gmail.com'
    recipient_list = [email]
    html_message = '<h4>Hi ' + firstname + '<p>Welcome to Badang ni Ignacio, Please validate your account with the link provided below:</p> </h4>'
    html_message += "<p><a href='http://localhost:8000/validation/" + str(id) + "'>Click here to validate your account</a></p>"
    send_mail(subject, message, from_email, recipient_list, html_message=html_message)


def send_reservation_confirmation(customer_name, customer_email, event_type, start, end, notes, contact_email, contact_phone, farm_name, website_url):
    subject = 'Your Reservation is Confirmed!'
    html_message = render_to_string('app/emails/reserve.html', {
        'customer_name': customer_name,
        'event_type': event_type,    
        'start': start,
        'end': end,
        'notes': notes,
        'contact_email': contact_email,
        'contact_phone': contact_phone,
        'restaurant_name': farm_name,
        'website_url': website_url,
        'year': datetime.now().year,
    })
    plain_message = strip_tags(html_message)
    from_email = 'biofarmula3@gmail.com'
    to = customer_email

    email = EmailMultiAlternatives(subject, plain_message, from_email, [to])
    email.attach_alternative(html_message, "text/html")
    email.send()

def send_reservation_pending(customer_name, customer_email, event_type, start, end, notes, contact_email, contact_phone, farm_name, website_url):
    subject = 'Your have a pending reservation!'
    html_message = render_to_string('app/emails/pending.html', {
        'customer_name': customer_name,
        'event_type': event_type,    
        'start': start,
        'end': end,
        'notes': notes,
        'contact_email': contact_email,
        'contact_phone': contact_phone,
        'restaurant_name': farm_name,
        'website_url': website_url,
        'year': datetime.now().year,
    })
    plain_message = strip_tags(html_message)
    from_email = 'biofarmula3@gmail.com'
    to = 'biofarmula3@gmail.com'

    email = EmailMultiAlternatives(subject, plain_message, from_email, [to])
    email.attach_alternative(html_message, "text/html")
    email.send()



def send_reservation_reschedule(customer_name, customer_email, event_type, start, end, notes, contact_email, contact_phone, farm_name, website_url):
    subject = 'Your Reservation is Re-Scheduled'
    html_message = render_to_string('app/emails/resched.html', {
        'customer_name': customer_name,
        'event_type': event_type,    
        'start': start,
        'end': end,
        'notes': notes,
        'contact_email': contact_email,
        'contact_phone': contact_phone,
        'restaurant_name': farm_name,
        'website_url': website_url,
        'year': datetime.now().year,
    })
    plain_message = strip_tags(html_message)
    from_email = 'biofarmula3@gmail.com'
    to = customer_email

    email = EmailMultiAlternatives(subject, plain_message, from_email, [to])
    email.attach_alternative(html_message, "text/html")
    email.send()

def send_reservation_cancelled(customer_name, customer_email, event_type, start, end, notes, contact_email, contact_phone, farm_name, website_url):
    subject = 'Your Reservation is Cancelled'
    html_message = render_to_string('app/emails/cancelled.html', {
        'customer_name': customer_name,
        'event_type': event_type,    
        'start': start,
        'end': end,
        'notes': notes,
        'contact_email': contact_email,
        'contact_phone': contact_phone,
        'restaurant_name': farm_name,
        'website_url': website_url,
        'year': datetime.now().year,
    })
    plain_message = strip_tags(html_message)
    from_email = 'biofarmula3@gmail.com'
    to = customer_email

    email = EmailMultiAlternatives(subject, plain_message, from_email, [to])
    email.attach_alternative(html_message, "text/html")
    email.send()

def send_password_reset(contact_email, customer_email, farm_name, website_url, customer_name, contact_phone, id):
    subject = 'Password Reset'
    html_message = render_to_string('app/emails/forgot-password.html', {
        'customer_name': customer_name,
        'customer_email': customer_email,    
        'contact_email': contact_email,
        'contact_phone': contact_phone,
        'restaurant_name': farm_name,
        'website_url': website_url,
        'year': datetime.now().year,
        'id': id,
    })
    plain_message = strip_tags(html_message)
    from_email = 'biofarmula3@gmail.com'
    to = customer_email

    email = EmailMultiAlternatives(subject, plain_message, from_email, [to])
    email.attach_alternative(html_message, "text/html")
    email.send()



def send_certificate(name, email, details, signatory):
    pdf_file = generate_certificate_pdf(name, details, signatory)
    subject = "Here's is your certificate"
    html_message = render_to_string('app/emails/certificate.html', {
        'name': name,    
        'details': details,
        'signatory': signatory,
    })

    plain_message = strip_tags(html_message)
    from_email = 'biofarmula3@gmail.com'
    to = email

    email = EmailMultiAlternatives(subject, plain_message, from_email, [to])
    email.attach_alternative(html_message, "text/html")
    email.attach(f'{name}_certificate.pdf', pdf_file.getvalue(), 'application/pdf')
    email.send()


def send_annoucement(subject, body, email, name):
    html_message = render_to_string('app/emails/annoucement.html', {
        'name': name,
        'subject': subject,    
        'body': body,
    })

    plain_message = strip_tags(html_message)
    from_email = 'biofarmula3@gmail.com'
    to = email

    email = EmailMultiAlternatives(subject, plain_message, from_email, [to])
    email.attach_alternative(html_message, "text/html")
    email.send()