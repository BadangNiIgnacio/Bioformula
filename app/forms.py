from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import *
from django.core.validators import RegexValidator

CS = [('SINGLE', 'SINGLE'), ('MARRIED', 'MARRIED'), ('SEPARATED', 'SEPARATED')]
GENDER = [('MALE', 'MALE'), ('FEMALE', 'FEMALE'), ('RATHER NOT SAY', 'RATHER NOT SAY')]
RATING = [(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')]
RESERVATION_STATUS = [('PENDING', 'PENDING'), ('RE-SCHEDULE', 'RE-SCHEDULE'), ('RESERVED', 'RESERVED'), ('CANCEL', 'CANCEL')]

alphanumeric_with_hyphen = RegexValidator(
    regex=r'^[a-zA-Z0-9- ]+$',
    message='This field can only contain letters, numbers, and hyphens.'
)

class RegisterForm(forms.Form):
    firstname = forms.CharField(max_length=150, label='First Name', validators=[alphanumeric_with_hyphen], widget=forms.TextInput(attrs={'class': 'form-control email-bt', 'placeholder': 'First Name'}))
    middlename = forms.CharField(max_length=150, label='Middle Name', validators=[alphanumeric_with_hyphen], required=False, widget=forms.TextInput(attrs={'class': 'form-control email-bt', 'placeholder': 'Middle Name'}))
    lastname = forms.CharField(max_length=150, label='Last Name', validators=[alphanumeric_with_hyphen], widget=forms.TextInput(attrs={'class': 'form-control email-bt', 'placeholder': 'Last Name'}))
    email = forms.EmailField(label='Email', required=True, widget=forms.EmailInput(attrs={'class': 'form-control email-bt', 'placeholder': 'you@gmail.com'}))

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email').upper() if cleaned_data.get('email') is not None else ''
        if User.objects.filter(username=email).exists():
            raise ValidationError("Email Address already exist")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email Address already exist")
        return cleaned_data
    
class ValidationForm(forms.Form):
    firstname = forms.CharField(max_length=150, label='First Name', validators=[alphanumeric_with_hyphen], widget=forms.TextInput(attrs={'class': 'form-control'}))
    middlename = forms.CharField(max_length=150, label='Middle Name', validators=[alphanumeric_with_hyphen], required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    lastname = forms.CharField(max_length=150, label='Last Name', validators=[alphanumeric_with_hyphen], widget=forms.TextInput(attrs={'class': 'form-control'}))
    suffix = forms.CharField(max_length=150, label='Extension', validators=[alphanumeric_with_hyphen], required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'optional'}))
    email = forms.EmailField(label='Email', required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    civil_status = forms.ChoiceField(label='Civil Status', choices=CS, widget=forms.Select(attrs={'class': 'form-control'}))
    gender = forms.ChoiceField(label='Gender', choices=GENDER, widget=forms.Select(attrs={'class': 'form-control'}))
    occupation = forms.CharField(max_length=150, label='Occupation', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(max_length=250, label='Address', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    contact_no = forms.RegexField( max_length=11, min_length=11, label='Contact No.', required=True, regex=r'^\d{11}$', error_messages={'invalid': 'Please enter a valid contact number consisting of exactly 11 digits. Letters or special characters are not allowed.', 'required': 'Contact number is required.', 'min_length': 'Contact number must be 11 digits long.', 'max_length': 'Contact number must be 11 digits long.', },widget=forms.TextInput(attrs={'class': 'form-control', 'maxlength': '11'}))
    password = forms.CharField(max_length=30, label='Password', required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(max_length=30, label='Confirm Password', required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError("The passwords do not match.")
        return cleaned_data

class ProfileForm(forms.Form):
    class Meta: model = Profile
    fields = ['image', 'firstname', 'middlename', 'lastname', 'email', 'suffix', 'civil_status', 'gender', 'occupation', 'address', 'contact_no']    
    firstname = forms.CharField(max_length=150, label='First Name', validators=[alphanumeric_with_hyphen], widget=forms.TextInput(attrs={'class': 'form-control'}))
    middlename = forms.CharField(max_length=150, label='Middle Name', validators=[alphanumeric_with_hyphen], required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    lastname = forms.CharField(max_length=150, label='Last Name', validators=[alphanumeric_with_hyphen], widget=forms.TextInput(attrs={'class': 'form-control'}))
    suffix = forms.CharField(max_length=150, label='Extension', validators=[alphanumeric_with_hyphen], required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'optional'}))
    email = forms.EmailField(label='Email', required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    civil_status = forms.ChoiceField(label='Civil Status', choices=CS, widget=forms.Select(attrs={'class': 'form-control w-100'}))
    gender = forms.ChoiceField(label='Gender', choices=GENDER, widget=forms.Select(attrs={'class': 'form-control w-100'}))
    occupation = forms.CharField(max_length=150, label='Occupation', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(max_length=250, label='Address', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    contact_no = forms.RegexField( max_length=11, min_length=11, label='Contact No.', required=True, regex=r'^\d{11}$', error_messages={'invalid': 'Please enter a valid contact number consisting of exactly 11 digits. Letters or special characters are not allowed.', 'required': 'Contact number is required.', 'min_length': 'Contact number must be 11 digits long.', 'max_length': 'Contact number must be 11 digits long.', },widget=forms.TextInput(attrs={'class': 'form-control', 'maxlength': '11'}))
    image = forms.ImageField(label='Profile Picture', required=False)

class SigninForm(forms.Form):
    email = forms.EmailField(
        label="Username", 
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'you@gmail.com'})
    )
    password = forms.CharField(
        label="Password", 
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )

class ForgotPasswordForm(forms.Form):
        email = forms.EmailField(
        label="Email address",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
        
class NewPasswordForm(forms.Form):
    password = forms.CharField(
        label='New Password', 
        required=True, 
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    confirm_password = forms.CharField(
        label='Confirm Password', 
        required=True, 
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("The two password fields must match.")
        return cleaned_data

class FertilizerSearchForm(forms.Form):
    search = forms.ModelChoiceField(queryset=FertilizersIngredients.objects.filter(fertilizer__status=True),required=False, widget=forms.Select(attrs={'class': 'form-control select-basic-single col-12', 'onchange': 'submitFertilizerForm()'}))

class PesticideSearchForm(forms.Form):
    search = forms.ModelChoiceField(queryset=PesticideIngredients.objects.filter(pesticide__status=True), required=False, widget=forms.Select(attrs={'class': 'form-control select-basic-single col-12', 'onchange': 'submitPesticideForm()'}))

class ReservationForm(forms.Form):
    event_type = forms.CharField(label='Type of event', max_length=150, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}))
    start = forms.DateField(label='Start date', widget=forms.DateInput(attrs={'class': 'form-control datepicker'}))
    end = forms.DateField(label='End date', widget=forms.DateInput(attrs={'class': 'form-control datepicker'}))

class ReservationDetailsForm(forms.Form):
    event_type = forms.CharField(label='Event Type', max_length=150, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}))
    start = forms.DateField(label='Start Date', widget=forms.DateInput(attrs={'class': 'form-control datepicker'}))
    end = forms.DateField(label='End Date', widget=forms.DateInput(attrs={'class': 'form-control datepicker'}))
    notes = forms.CharField(label='Reason/s', required=False, max_length=150, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}))
    status = forms.ChoiceField(label='Status', choices=RESERVATION_STATUS, widget=forms.Select())

class PesticideConversionForm(forms.ModelForm):
    uom_qty = forms.IntegerField(label='Amount of Pesticide', required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    uom = forms.ChoiceField(label='Unit of Measurement', required=False, widget=forms.Select())
    land_qty = forms.IntegerField(label='Land Size', required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    land = forms.ChoiceField(label='Unit of Measurement', required=False, widget=forms.Select())

    class Meta:
        model = PesticideConversion
        fields = ['uom_qty', 'uom', 'land_qty', 'land']

    def __init__(self, *args, **kwargs):
        super(PesticideConversionForm, self).__init__(*args, **kwargs)
        self.instance = kwargs.get('instance', None)
        self.fields['uom'].choices = [
            (p.uom.uom_id, p.uom.name) for p in PesticideConversion.objects.filter(pesticide_id=self.instance.pk)
        ]
        self.fields['land'].choices = [
            (p.land.land_id, p.land.name) for p in PesticideConversion.objects.filter(pesticide_id=self.instance.pk)
        ]

class FertilizerConversionForm(forms.ModelForm):
    uom_qty = forms.IntegerField(label='Amount of Fertilizer', required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    uom = forms.ChoiceField(label='Unit of Measurement', required=False, widget=forms.Select())
    land_qty = forms.IntegerField(label='Land Size', required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    land = forms.ChoiceField(label='Unit of Measurement', required=False, widget=forms.Select())

    class Meta:
        model = FertilizerConversion
        fields = ['uom_qty', 'uom', 'land_qty', 'land']

    def __init__(self, *args, **kwargs):
        super(FertilizerConversionForm, self).__init__(*args, **kwargs)
        self.instance = kwargs.get('instance', None)
        self.fields['uom'].choices = [
            (p.uom.uom_id, p.uom.name) for p in FertilizerConversion.objects.filter(fertilizer_id=self.instance.pk)
        ]
        self.fields['land'].choices = [
            (p.land.land_id, p.land.name) for p in FertilizerConversion.objects.filter(fertilizer_id=self.instance.pk)
        ]

class CertificateForm(forms.Form):
    name = forms.CharField(max_length=200, label='Full Name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(max_length=250, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    details = forms.CharField(max_length=1000, widget=forms.Textarea(attrs={'class': 'form-control'}))
    signatory = forms.CharField(max_length=1000, label='Sign by', widget=forms.TextInput(attrs={'class': 'form-control'}))
