from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.forms import PasswordChangeForm

import re
from django.core.exceptions import ValidationError

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, HTML

from django.contrib.auth.models import User
from .models import Profile, Resource, TimeBlock, Announcement, Reservation
from .models import Organization, EmailFilter, School

from .deep_fried_form import DeepFriedForm


# from django.conf import settings
class SignUpForm(UserCreationForm):
    '''Extend the UserCreationForm to create a 
    custom signup form
    '''

    # Add the email field to the user creation form
    email = forms.EmailField(max_length=254, help_text='Required. Provide a valid email address.')

    class Meta:
        model = User
        fields = 'username', 'email', 'password1', 'password2'

    def clean_email(self):
        '''Validate teacher email
        '''
        new_user_email = self.cleaned_data['email']
        new_user_domain = re.search("[^@]+\w+$", new_user_email).group()

        if User.objects.filter(email=new_user_email).exists():
            # Check for existing user-email
            raise ValidationError("A user with that email already exists")

        if (not Organization.objects.filter(domain=new_user_domain).exists()):
            # Check to see if domain is not authorized by the system (domain doesn't exist)
            raise ValidationError(f'To signup for Aion, your organization must be a member of the Aion community.')

        # Retrieve the org / filters for the new user
        # user_org = Organization.objects.filter(domain=new_user_domain)
        email_filters = EmailFilter.objects.filter(organization__domain=new_user_domain)

        for f in email_filters:
            # Check to see if new email contains a dissallowed email filter
            if (bool(re.search("^" + f.phrase, new_user_email))):
                raise ValidationError('Your email is not allowed to access Aion.')

        return new_user_email

    def __init__(self, *args, **kwargs):
        '''Extend Crispy Forms helper and layout objects.
        '''
        super(SignUpForm, self).__init__(*args, **kwargs)

        # Create the label for email
        self.fields['email'].label = "Email"

        # Get the crispy helper and layout objects ready
        self.helper = FormHelper(self)
        self.helper.layout = Layout()
        self.helper.layout.append(
            DeepFriedForm(
                submit_text='Register',
                cancel_url='/signin/',
                cancel_text='Sign In'
            )
        )
        self.helper.form_show_labels = False  # surpress labels


class LogInForm(AuthenticationForm):
    '''Custom Login Form
    '''

    class Meta:
        model = User
        fields = 'username', 'password'

    def __init__(self, *args, **kwargs):
        '''Extend Crispy Forms layout objects.
        '''

        super(LogInForm, self).__init__(*args, **kwargs)

        # Get the crispy helper and layout objects ready
        self.helper = FormHelper(self)
        self.helper.layout = Layout()
        self.helper.layout.append(
            DeepFriedForm(
                submit_text="Sign In",
                cancel_url="/signup/",
                cancel_text="Sign Up"
            )
        )
        self.helper.form_show_labels = False  # surpress labels


'''Custom User and Profile Form
'''


class UserForm(forms.ModelForm):
    '''User Form
    '''

    class Meta:
        model = User
        fields = ('first_name', 'last_name')

    '''Extend Crispy Forms helper and layout objects.
    '''

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        # Get the crispy helper and layout objects ready
        self.helper = FormHelper(self)
        self.helper.layout = Layout()
        self.helper.layout.append(
            DeepFriedForm(
                render_buttons=False
            )
        )
        # self.helper.form_show_labels = False # surpress labels
        self.helper[0:2].wrap_together(Fieldset, '{{ request.user }}')
        self.helper.form_tag = False


class ProfileForm(forms.ModelForm):
    '''Profile Form
    '''

    class Meta:
        model = Profile
        fields = ('location',)

    def __init__(self, *args, **kwargs):
        '''Extend Crispy Forms helper and layout objects.
        '''

        super(ProfileForm, self).__init__(*args, **kwargs)

        self.fields["location"].queryset = School.objects.filter(organization=kwargs['instance'].organization).order_by(
            'name')
        # Get the crispy helper and layout objects ready
        self.helper = FormHelper(self)
        self.helper.layout = Layout()

        self.helper.layout.append(
            DeepFriedForm(
                submit_text="Save Profile",
                cancel_url="/home/",
                cancel_text="Cancel"
            )
        )

        self.helper.layout.insert(
            0,  # Index of layout items.
            HTML(
                '<div class="alert alert-block alert-danger">Choosing a building is required for making reservations.</div>'
            ),
        )
        self.helper.form_tag = False
        # self.helper.form_show_labels = False # surpress labels


class EditSchoolAdminForm(forms.ModelForm):
    '''Custom Profile form to edit school admin access
    '''

    class Meta:
        model = Profile
        fields = ('school_admin',)

    def __init__(self, *args, **kwargs):
        '''Extend crispy forms layout objects
        '''
        super(EditSchoolAdminForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout()
        self.helper.layout.append(
            DeepFriedForm(
                submit_text="Update Access",
            )
        )
        self.helper.form_show_labels = False  # surpress labels


class EditTimeBlockForm(forms.ModelForm):
    '''Custom Edit Blocks Form
    for building admins
    '''

    class Meta:
        model = TimeBlock
        fields = ('name', 'sequence', 'enabled')

    def __init__(self, *args, **kwargs):
        '''Extend Crispy Forms layout objects.
        '''

        super(EditTimeBlockForm, self).__init__(*args, **kwargs)
        # Get the crispy helper and layout objects ready
        self.helper = FormHelper(self)
        self.helper.layout = Layout()
        self.helper.layout.append(
            DeepFriedForm(
                submit_text="Update Block",
            )
        )

        self.helper.form_show_labels = False  # surpress labels


class DeleteTimeBlockForm(forms.ModelForm):
    '''Custom Delete block Form for building admins
    '''

    class Meta:
        model = TimeBlock
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        '''Extend Crispy Forms layout objects.
        '''

        super(DeleteTimeBlockForm, self).__init__(*args, **kwargs)
        # Get the crispy helper and layout objects ready
        self.helper = FormHelper(self)
        self.helper.layout = Layout()
        self.helper.layout.append(
            DeepFriedForm(
                render_buttons=False,
                render_delete_buttons=True,
                delete_text='DELETE BLOCK',
            )
        )

        self.helper.form_show_labels = False  # surpress labels


# from django.forms import DateField, SelectDateWidget
class NewTimeBlockForm(forms.ModelForm):
    '''Custom Create Block Form
    for Building Admins
    '''

    class Meta:
        model = TimeBlock
        fields = ('name', 'sequence',)

    def __init__(self, *args, **kwargs):
        '''Extend Crispy Forms layout objects.
        '''
        super(NewTimeBlockForm, self).__init__(*args, **kwargs)
        # Get the crispy helper
        self.helper = FormHelper(self)
        self.helper.layout = Layout()
        self.helper.layout.append(
            DeepFriedForm(
                submit_text='Create New Block',
            )
        )
        self.helper.form_show_labels = False


class DeleteAnnouncementForm(forms.Form):
    def __init__(self, *args, **kwargs):
        '''Extend Crispy Forms layout objects.
        '''

        super(DeleteAnnouncementForm, self).__init__(*args, **kwargs)
        # Get the crispy helper and layout objects ready
        self.helper = FormHelper(self)
        self.helper.layout = Layout()
        self.helper.layout.append(
            DeepFriedForm(
                render_buttons=False,
                render_delete_buttons=True,
                delete_text='DELETE ANNOUNCEMENT',
            )
        )
        self.helper.form_show_labels = False  # surpress labels


class NewAnnouncementForm(forms.ModelForm):
    '''Form for building admins to create announcments
    '''

    class Meta:
        model = Announcement
        fields = ('title', 'message', 'publish_on', 'expires_on')

    def __init__(self, *args, **kwargs):
        '''Extend Crispy Forms layout objects.
        '''

        super(NewAnnouncementForm, self).__init__(*args, **kwargs)
        # Get the crispy helper and layout objects ready
        self.helper = FormHelper(self)
        self.helper.layout = Layout()
        self.helper.layout.append(
            DeepFriedForm(
                submit_text="Create Announcement",
            )
        )
        self.helper.form_show_labels = False  # surpress labels


class EditAnnouncementForm(forms.ModelForm):
    '''Form for building admins to edit announcments
    '''

    class Meta:
        model = Announcement
        fields = ('title', 'message', 'publish_on', 'expires_on')

    def __init__(self, *args, **kwargs):
        '''Extend Crispy Forms layout objects.
        '''

        super(EditAnnouncementForm, self).__init__(*args, **kwargs)
        # Get the crispy helper and layout objects ready
        self.helper = FormHelper(self)
        self.helper.layout = Layout()
        self.helper.layout.append(
            DeepFriedForm(
                submit_text="Update Announcement",
            )
        )
        self.helper.form_show_labels = False  # surpress labels


class AdminNewAnnouncementForm(NewAnnouncementForm):
    class Meta:
        model = Announcement
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AdminNewAnnouncementForm, self).__init__(*args, **kwargs)

        self.helper.form_show_labels = True


class AdminEditAnnouncementForm(EditAnnouncementForm):
    class Meta:
        model = Announcement
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AdminEditAnnouncementForm, self).__init__(*args, **kwargs)

        self.helper.form_show_labels = True


class NewResourceForm(forms.ModelForm):
    '''Custom Create Resource Form
    for building admins
    '''

    class Meta:
        model = Resource
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        '''Extend Crispy Forms layout objects.
        '''

        super(NewResourceForm, self).__init__(*args, **kwargs)
        # Get the crispy helper and layout objects ready
        self.helper = FormHelper(self)
        self.helper.layout = Layout()
        self.helper.layout.append(
            DeepFriedForm(
                submit_text="Create Resource",
            )
        )
        self.helper.form_show_labels = False  # surpress labels


class EditResourceForm(forms.ModelForm):
    '''Custom Edit Resource Form
    for building admins
    '''

    class Meta:
        model = Resource
        fields = ('name', 'enabled')

    def __init__(self, *args, **kwargs):
        '''Extend Crispy Forms layout objects.
        '''

        super(EditResourceForm, self).__init__(*args, **kwargs)
        # Get the crispy helper and layout objects ready
        self.helper = FormHelper(self)
        self.helper.layout = Layout()
        self.helper.layout.append(
            DeepFriedForm(
                submit_text="Update Resource",
            )
        )

        self.helper.form_show_labels = False  # surpress labels


class DeleteResourceForm(forms.ModelForm):
    '''Custom Delete Resource Form for building admins
    '''

    class Meta:
        model = Resource
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        '''Extend Crispy Forms layout objects.
        '''

        super(DeleteResourceForm, self).__init__(*args, **kwargs)
        # Get the crispy helper and layout objects ready
        self.helper = FormHelper(self)
        self.helper.layout = Layout()
        self.helper.layout.append(
            DeepFriedForm(
                render_buttons=False,
                render_delete_buttons=True,
                delete_text='DELETE RESOURCE',
            )
        )

        self.helper.form_show_labels = False  # surpress labels


class PasswordResetFormAion(PasswordResetForm):
    '''Custom Password Reset Form
    '''

    def __init__(self, *args, **kwargs):
        '''Extend Crispy Forms layout objects.
        '''

        super(PasswordResetFormAion, self).__init__(*args, **kwargs)

        # Get the crispy helper and layout objects ready
        self.helper = FormHelper(self)
        self.helper.layout = Layout()
        self.helper.layout.append(
            DeepFriedForm(
                submit_text="Reset Password",
            )
        )
        self.helper.form_show_labels = False  # surpress labels


class PasswordResetConfirmFormAion(SetPasswordForm):
    '''Custom Password Reset Confirm Form
    '''

    def __init__(self, *args, **kwargs):
        '''Extend Crispy Forms layout objects.
        '''

        super(PasswordResetConfirmFormAion, self).__init__(*args, **kwargs)

        # Get the crispy helper and layout objects ready
        self.helper = FormHelper(self)
        self.helper.layout = Layout()
        self.helper.layout.append(
            DeepFriedForm(
                submit_text="Change Password",
            )
        )
        self.helper.form_show_labels = False  # surpress labels


class PasswordChangeFormAion(PasswordChangeForm):
    '''Custom PasswordChangeForm
    '''

    def __init__(self, *args, **kwargs):
        '''Extend Crispy Forms layout objects.
        '''

        super(PasswordChangeFormAion, self).__init__(*args, **kwargs)

        # Get the crispy helper and layout objects ready
        self.helper = FormHelper(self)
        self.helper.layout = Layout()
        self.helper.layout.append(
            DeepFriedForm(
                submit_text="Change Password",
            )
        )
        self.helper.form_show_labels = False


from .models import TimeBlock, Resource


class BulkReservationForm(forms.Form):
    from_date = forms.DateTimeField(required=True, widget=forms.DateTimeInput(
        format="%d/%m/%Y %H:%M:%S",
        attrs={'type': 'date'}))
    to_date = forms.DateTimeField(required=True, widget=forms.DateTimeInput(
        format="%d/%m/%Y %H:%M:%S",
        attrs={'type': 'date'}))

    def clean_to_date(self):
        from_date = self.cleaned_data['from_date']
        to_date = self.cleaned_data['to_date']
        if (to_date < from_date):
            raise forms.ValidationError('"To date*" cannot be before the "From date*"')

        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        return to_date

    def __init__(self, *args, **kwargs):
        '''Add the user to form constructor for use in queries
        '''
        self.user_school = kwargs.pop("user_school")
        super(BulkReservationForm, self).__init__(*args, **kwargs)
        user_school = self.user_school
        time_blocks = TimeBlock.objects.filter(school=user_school)
        time_block_choices = [(tb.id, tb.name) for tb in time_blocks]
        resources = Resource.objects.filter(school=user_school)
        resource_choices = [(r.id, r.name) for r in resources]

        self.fields['time_blocks'] = forms.MultipleChoiceField(
            widget=forms.CheckboxSelectMultiple,
            choices=time_block_choices
        )
        self.fields['resource'] = forms.ChoiceField(
            widget=forms.Select,
            choices=resource_choices
        )

        # Move resources to the beginning of the fields (OrderedDict)
        self.fields.move_to_end('resource', last=False)

        # Get the crispy helper and layout objects ready
        self.helper = FormHelper(self)
        self.helper.layout = Layout()
        self.helper.layout.append(
            DeepFriedForm(
                submit_text="Reserve",
            )
        )


''' Contact form with Django Simple Captcha
'''
from captcha.fields import CaptchaField


class ContactForm(forms.Form):
    email_from = forms.CharField(max_length=100, required=True)
    subject = forms.CharField(max_length=100, required=True)
    message = forms.CharField(widget=forms.Textarea)
    captcha = CaptchaField()

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        # Get the crispy helper and layout objects ready
        self.helper = FormHelper(self)
        self.helper.layout = Layout()
        self.helper.layout.append(
            DeepFriedForm(
                submit_text="Submit",
            )
        )


class AjaxMakeReservationForm(forms.Form):
    resource_id = forms.IntegerField(required=True)
    time_block_id = forms.IntegerField(required=True)
    date = forms.DateTimeField(required=True, widget=forms.DateTimeInput(
        format="%d/%m/%Y %H:%M:%S",
        attrs={'type': 'datetime-local'}))


class AjaxCancelReservationForm(forms.Form):
    reservation_id = forms.IntegerField(required=True)


class AjaxBookmarkForm(forms.Form):
    resource_id = forms.IntegerField(required=True)
    bookmarked = forms.CharField(max_length=5, required=True)
