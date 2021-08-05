"""Views.py"""
from django.shortcuts import render

# Decorator for school admin views
from django.contrib.auth.decorators import user_passes_test

# Update Profile
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseRedirect
from django.contrib import messages

# User Signup
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .tokens import account_activation_token

# User Activation
from django.utils.encoding import force_text
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.utils.http import urlsafe_base64_decode

# App Views
from .models import Profile, TimeBlock, Resource, School, Reservation, Announcement
from .forms import UserForm, ProfileForm, SignUpForm, ContactForm
from .forms import AjaxMakeReservationForm, AjaxCancelReservationForm, AjaxBookmarkForm
from datetime import date
from django.shortcuts import get_object_or_404

# Building Admin Views
from .forms import NewResourceForm, EditResourceForm, DeleteResourceForm
from .forms import NewTimeBlockForm, EditTimeBlockForm, DeleteTimeBlockForm
from .forms import EditSchoolAdminForm, NewAnnouncementForm, AdminNewAnnouncementForm
from .forms import EditAnnouncementForm, DeleteAnnouncementForm, AdminEditAnnouncementForm
from .forms import BulkReservationForm

# Ajax
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.core import serializers
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError

from reservations.functions import get_current_time


def is_school_admin(user):
    '''Decorator for school admin views
    @returns: Boolean
    @exampleusage:

        @user_passes_test(is_school_admin)
        def my_view_function(request):
            ...
        
    '''
    return user.profile.school_admin
    

@login_required
@user_passes_test(is_school_admin)
def building_admin(request):
    school = request.user.profile.location
    number_of_resources = Resource.objects.filter(school=school).count()
    number_of_time_blocks = TimeBlock.objects.filter(school=school).count()
    context = { 
        'school':school, 
        'number_of_resources':number_of_resources,
        'number_of_time_blocks':number_of_time_blocks
    }
    return render(request, 'reservations/building_admin/building_admin.html', context)
    

@login_required
@user_passes_test(is_school_admin)
def edit_resources(request):
    '''Building admins select a resource
    to edit
    '''
    user_school = request.user.profile.location
    resources = Resource.objects.filter(school=user_school).filter(deleted=False).order_by('name')
    context = {
        'resources':resources,
    }
    return render(request, 'reservations/building_admin/edit_resources.html', context)
    

@login_required
@user_passes_test(is_school_admin)
def edit_resource(request, resource_id):
    '''Building admins can edit a resource
    '''
    resource = get_object_or_404(Resource, pk=resource_id)

    if(resource.school != request.user.profile.location and resource.deleted is False):
        '''Building admins must belong to same school as resource
        '''
        return redirect('edit_resources')
    
    if request.method == 'POST':
        edit_resource_form = EditResourceForm(request.POST, instance=resource)
        
        if edit_resource_form.is_valid():
            edit_resource_form.save()
        return redirect('edit_resources')
        
    else:
        edit_resource_form = EditResourceForm(instance=resource)
    
    
    context = {'edit_resource_form': edit_resource_form, 'resource': resource}
    
    return render(
        request, 'reservations/building_admin/edit_resource_form.html', context
    )


@login_required
@user_passes_test(is_school_admin)
def delete_resource(request, resource_id):
    '''Building admins can delete a resource
    '''
    resource = get_object_or_404(Resource, pk=resource_id)

    if(resource.school != request.user.profile.location):
        '''Building admins must belong to same school as resource
        '''
        return redirect('edit_resources')
    
    if request.method == 'POST':
        delete_resource_form = DeleteResourceForm(request.POST, instance=resource)
        
        if delete_resource_form.is_valid():
            resource.enabled=False
            resource.deleted=True
            resource.deleted_on=date.today()
            resource.save()
            delete_resource_form.save()
        return redirect('edit_resources')
        
    else:
        delete_resource_form = DeleteResourceForm(instance=resource)
    
    context = {'delete_resource_form': delete_resource_form,'resource':resource}
    
    return render(
        request, 'reservations/building_admin/delete_resource_form.html', context
    )
    

@login_required
@user_passes_test(is_school_admin)
def new_resource(request):
    '''Building admins can create a new resource
    '''
    if request.method == 'POST':
        new_resource_form = NewResourceForm(request.POST)
        
        if new_resource_form.is_valid():
            resource_name = new_resource_form.cleaned_data['name']
            user_school = request.user.profile.location
            
            if(Resource.objects.filter(name=resource_name).filter(school=user_school).filter(deleted=False).exists()):
                messages.error(request, 'This resource already exists')
            
            else:
                new_resource = Resource(name=resource_name, school=user_school)
                new_resource.save()
                return redirect('building_admin')
            
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        new_resource_form = NewResourceForm()
        
    return render(request, 'reservations/building_admin/new_resource_form.html', {
        'new_resource_form': new_resource_form,
    })


@login_required
@user_passes_test(is_school_admin)
def edit_time_block(request, time_block_id):
    '''Building admins can edit a block
    '''
    time_block = get_object_or_404(TimeBlock, pk=time_block_id)
    if(time_block.school != request.user.profile.location):
        '''Building admins must belong to same school as block
        '''
        return redirect('edit_time_blocks')
    
    if request.method == 'POST':
        edit_time_block_form = EditTimeBlockForm(request.POST, instance=time_block)
        
        if edit_time_block_form.is_valid():
            edit_time_block_form.save()
        return redirect('edit_time_blocks')
        
    else:
        edit_time_block_form = EditTimeBlockForm(instance=time_block)
    
    
    context = {'edit_time_block_form': edit_time_block_form, 'time_block': time_block,}
    
    return render(
        request, 'reservations/building_admin/edit_time_block_form.html', context
    )
    
    
@login_required
@user_passes_test(is_school_admin)
def edit_time_blocks(request):
    '''Building admins select a resource
    to edit
    '''
    user_school = request.user.profile.location
    time_blocks = TimeBlock.objects.filter(school=user_school).filter(deleted=False)
    context = {
        'time_blocks':time_blocks,
    }
    return render(request, 'reservations/building_admin/edit_time_blocks.html', context) 


@login_required
@user_passes_test(is_school_admin)
def delete_time_block(request, time_block_id):
    '''Building admins can delete a block
    '''
    time_block = get_object_or_404(TimeBlock, pk=time_block_id)

    if(time_block.school != request.user.profile.location or time_block.deleted):
        '''Building admins must belong to same school as resource
        '''
        return redirect('edit_time_blocks')
    
    if request.method == 'POST':
        delete_time_block_form = DeleteTimeBlockForm(request.POST, instance=time_block)
        
        if delete_time_block_form.is_valid():
            time_block.enabled=False
            time_block.deleted=True
            time_block.deleted_on=date.today()
            time_block.save()
            delete_time_block_form.save()
        return redirect('edit_time_blocks')
        
    else:
        delete_time_block_form = DeleteTimeBlockForm(instance=time_block)
    
    context = {'delete_time_block_form': delete_time_block_form,'time_block':time_block}
    
    return render(
        request, 'reservations/building_admin/delete_time_block_form.html', context
    )
     
@login_required
@user_passes_test(is_school_admin)
def new_time_block(request):
    '''Admins can create new blocks for their school 
    '''
    if request.method=="POST":
        new_time_block_form = NewTimeBlockForm(request.POST)
        
        if(new_time_block_form.is_valid()):
            time_block_name = new_time_block_form.cleaned_data['name']
            time_block_sequence = new_time_block_form.cleaned_data['sequence']
            user_school = request.user.profile.location
            
            if(TimeBlock.objects.filter(name=time_block_name).filter(school=user_school).filter(deleted=False).exists()):
                messages.error(request, 'This block already exists')
            else:
                new_time_block = TimeBlock(name=time_block_name, sequence=time_block_sequence, school=user_school)
                new_time_block.save()
                return redirect('building_admin')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        new_time_block_form = NewTimeBlockForm()
        
    context = {'new_time_block_form':new_time_block_form,}
    
    return render(request, 'reservations/building_admin/new_time_block_form.html', context)


@login_required
def announcements(request):
    '''View for users to read announcments
    '''
    global_announcements = Announcement.objects.filter(
            expires_on__gte=date.today()
        ).filter(
            publish_on__lte=date.today()
        ).filter(
            system_wide=True
        )
    org_announcements = Announcement.objects.filter(
            expires_on__gte=date.today()
        ).filter(
            publish_on__lte=date.today()
        ).filter(
            organization_wide=True
        ).filter(
            system_wide=False
        ).filter(
            organization=request.user.profile.location.organization
        )
    local_announcements = Announcement.objects.filter(
            school=request.user.profile.location
        ).filter(
            expires_on__gte=date.today()
        ).filter(
            publish_on__lte=date.today()
        ).filter(
            system_wide=False
        ).filter(
            organization_wide=False
        )
    
    context={
        'global_announcements':global_announcements,
        'org_announcements':org_announcements,
        'local_announcements':local_announcements,
    }
    return render(request, 'reservations/announcements.html', context)

@login_required
@user_passes_test(is_school_admin)
def new_announcement(request):
    '''View for building admins to create announcments
    '''
    if request.method=="POST":
        if request.user.is_superuser:
            new_announcement_form = AdminNewAnnouncementForm(request.POST)
            
            if(new_announcement_form.is_valid()):
                announcement_school =  new_announcement_form.cleaned_data['school']
                organization_wide = new_announcement_form.cleaned_data['organization_wide']
                organization = new_announcement_form.cleaned_data['organization']
                system_wide =  new_announcement_form.cleaned_data['system_wide']
                
        else:
            new_announcement_form = NewAnnouncementForm(request.POST)
            
            if(new_announcement_form.is_valid()):
                announcement_school = request.user.profile.location
                system_wide = False
                organization_wide = False
                organization = request.user.profile.location.organization
        
        if(new_announcement_form.is_valid()):
            announcement_title= new_announcement_form.cleaned_data['title']
            announcement_message = new_announcement_form.cleaned_data['message']
            announcement_publish_on = new_announcement_form.cleaned_data['publish_on']
            announcement_expires_on = new_announcement_form.cleaned_data['expires_on']
            
            
            new_announcement = Announcement(
                title=announcement_title,
                message=announcement_message,
                publish_on=announcement_publish_on,
                expires_on=announcement_expires_on,
                school=announcement_school,
                organization_wide=organization_wide,
                organization=organization,
                system_wide=system_wide
            )
                
            new_announcement.save()
            
            return redirect('building_admin')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        if request.user.is_superuser:
            new_announcment_form = AdminNewAnnouncementForm()
        else:
            new_announcment_form = NewAnnouncementForm()
        
    context = {'new_announcement_form':new_announcment_form,}
    return render(request, 'reservations/building_admin/new_announcement_form.html', context)


@login_required
@user_passes_test(is_school_admin)
def edit_announcement(request, announcement_id):
    '''View to edit an announcement
    '''
    announcement = get_object_or_404(Announcement, pk=announcement_id)
    
    if(request.user.is_superuser):
        if request.method == 'POST':
            edit_announcement_form = AdminEditAnnouncementForm(request.POST, instance=announcement)
        else:
            edit_announcement_form = AdminEditAnnouncementForm(instance=announcement)
    elif(announcement.school == request.user.profile.location):
        if request.method == 'POST':
            edit_announcement_form = EditAnnouncementForm(request.POST, instance=announcement)
        else:
            edit_announcement_form = EditAnnouncementForm(instance=announcement)
    else:
        # Not superuser or member school
        return redirect('building_admin')
    
    context = {'edit_announcement_form': edit_announcement_form, 'announcement': announcement,}
    
    return render(request, 'reservations/building_admin/edit_announcement.html', context)
    

@login_required
@user_passes_test(is_school_admin)
def delete_announcement(request, announcement_id):
    '''View to edit an announcement
    '''
    # user_school = request.user.profile.location 
    announcement = get_object_or_404(Announcement, pk=announcement_id)
    if request.user.profile.location == announcement.school or request.user.is_superuser:
        # proceed
        if request.method == 'POST':
            delete_announcement_form = DeleteAnnouncementForm(request.POST)
        
            if delete_announcement_form.is_valid():
                announcement.delete()
                return redirect('edit_announcements')
        else:
            delete_announcement_form = DeleteAnnouncementForm()
    else:
        # Only building admins or superadmins can edit this announcement
        return redirect('building_admin')
    
    context = {'delete_announcement_form': delete_announcement_form, 'announcement': announcement,}
    
    return render(request, 'reservations/building_admin/delete_announcement.html', context)    
    
    
    
@login_required
@user_passes_test(is_school_admin)
def edit_announcements(request):
    '''View lists all announcements that user can edit 
    '''
    user_school = request.user.profile.location
    
    if request.user.is_superuser:
        
        global_announcements = Announcement.objects.filter(
            expires_on__gte=date.today()
        ).filter(
            system_wide=True
        )
        
        org_announcements = Announcement.objects.filter(
            expires_on__gte=date.today()
        ).filter(
            organization_wide=True
        ).filter(
            system_wide=False
        )
        
        local_announcements = Announcement.objects.filter(
            expires_on__gte=date.today()
        ).filter(
            school=user_school
        ).filter(
            system_wide=False
        ).filter(
            organization_wide=False
        )
        
        context = {
            'global_announcements' : global_announcements,
            'org_announcements' : org_announcements,
            'local_announcements' : local_announcements
        }
        
    else:
        
        local_announcements = Announcement.objects.filter(
            expires_on__gte=date.today()
        ).filter(
            school=user_school
        )
        
        context = {'local_announcements' : local_announcements}
    
    return render(request, 'reservations/building_admin/edit_announcements.html',context)



@login_required
@user_passes_test(is_school_admin)
def select_school_users(request):
    '''Displays a list of users so building admins
    can set other users as building admins
    '''
    user_school = request.user.profile.location
    profiles = Profile.objects.filter(location=user_school).filter(email_confirmed=True).order_by('user__last_name')
    context = {'profiles':profiles,}
    return render(request, 'reservations/building_admin/school_users.html',context)


@login_required
@user_passes_test(is_school_admin)
def edit_school_admin(request, profile_id):
    '''Building admins can edit building admin access
    '''
    profile = get_object_or_404(Profile, pk=profile_id)
    
    if request.method == 'POST':
        edit_school_admin_form=EditSchoolAdminForm(request.POST, instance=profile)
    
        if edit_school_admin_form.is_valid():
            edit_school_admin_form.save();
        return redirect('select_school_users')
    
    else:
        edit_school_admin_form=EditSchoolAdminForm(instance=profile)
        
    context = {
        'edit_school_admin_form':edit_school_admin_form,
        'profile':profile,
    }
    return render(request, 'reservations/building_admin/edit_school_admin_form.html',context)


'''Some Basic Views
'''

def index(request):
    '''Index page for site
    '''
    if request.user.is_authenticated:
        return redirect('home')
        
    return render( request, 'aion/index.html')


@login_required
@transaction.atomic
def update_profile(request):
    '''View to update the User Profile
    '''
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect('/')
        else:
            messages.error(request, 'Please correct the error below.')
            # messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'reservations/profile_form.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


def signup(request):
    '''Aion Signup View 
    '''
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, '', html_message=message)
            return redirect('registration/account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})
    

def account_activation_sent(request):
    '''Account activation sent
    '''
    return render( request, 'registration/account_activation_sent.html')
    

def activate(request, uidb64, token):
    '''Activate user
    '''
    # error=''
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        # context = {'uidb64':uidb64, 'token': token, 'user' : user, 'error': error}
        return render(request, 'registration/account_activation_invalid.html')


'''App Functionality
'''


@login_required
def home(request):
    '''Home page after authentication
    '''
    if(request.user.profile.location is None):
        return redirect('update-profile')
    
    # Today's reservations for user
    todays_reservations_count = Reservation.objects.filter(
        client=request.user
    ).filter(
        date = date.today()
    ).filter(
        resource__enabled=True
    ).count()
    
    # Manage all reservations
    my_reservations_count = Reservation.objects.filter(
        client=request.user
    ).filter(
        date__gte=date.today()
    ).filter(
        resource__enabled=True
    ).count()
    
    my_announcements = Announcement.objects.filter(
            expires_on__gte=date.today()
        ).filter(
            publish_on__lte=date.today()
        ).filter(
            system_wide=True
        ).count()
        
    my_announcements += Announcement.objects.filter(
            school=request.user.profile.location
        ).filter(
            expires_on__gte=date.today()
        ).filter(
            publish_on__lte=date.today()
        ).filter(
            system_wide=False
        ).count()
    if my_announcements > 0:
        context = {
            'my_announcements':my_announcements,
            'todays_reservations': todays_reservations_count,
            'my_reservations' : my_reservations_count,
        }
        
    else:
        context={
            'todays_reservations': todays_reservations_count,
            'my_reservations' : my_reservations_count,
        }
    return render( request, 'reservations/home.html', context)

@login_required
def todays_reservations(request):
    '''My Reservations displayed by date
    '''
    reservations = Reservation.objects.filter(client=request.user).filter(date=date.today()).filter(resource__enabled=True)
    context={ 'reservations' : reservations }
    return render(request, 'reservations/todays_reservations.html', context)


@login_required
def manage_reservations(request):
    '''My Reservations displayed by date
    '''
    reservations = Reservation.objects.filter(
        client=request.user
    ).filter(
        date__gte=date.today()
    ).filter(
        resource__enabled=True
    )

    resources_in_range = Resource.objects.filter(
        reservation__client=request.user
    ).filter(
        reservation__date__gte=date.today()
    ).distinct()

    for reservation in reservations:
        reservation.timestamp = get_current_time(int(reservation.timestamp or 3600 * 12))

    context={
        'reservations' : reservations,
        'resources' : resources_in_range,
    }

    return render(request, 'reservations/manage_reservations.html', context)


@login_required
def my_resources(request):
    ''' New Reservation uses this views
    Display list of resources the user has access to.
    '''
    location = request.user.profile.location
    favorites = request.user.profile.favorites.all().order_by('name')
    resources = Resource.objects.filter(school=location).filter(enabled=True).order_by('name')
    context={
        'location':location,
        'resources':resources,
        'favorites':favorites,
    }
    return render(request, 'reservations/my_resources.html', context)


@login_required
def reserve_resource(request, resource_id):
    '''Reserve a resource block
    '''
    resource = get_object_or_404(Resource, pk=resource_id)
    auth_school = request.user.profile.location
    
    if(auth_school == resource.school and resource.enabled):
        
        # Check if this is a bookmarked resource
        bookmarked=request.user.profile.favorites.filter(pk=resource.pk).exists()

        context={
            'resource':resource,
            'bookmarked':bookmarked,
        }
        return render(request, 'reservations/reserve_resource.html', context)
    else:
        return redirect('home')
        
        
@csrf_protect
@login_required
@require_POST
def ajax_bookmark(request): 
    '''Bookmark a resource
    '''
    data={}
    form = AjaxBookmarkForm(request.POST)
    if(form.is_valid()):
        resource_id=form.cleaned_data['resource_id']
        bookmarked=form.cleaned_data['bookmarked']
        user=request.user
        resource = get_object_or_404(Resource, pk=resource_id)
        if(user.profile.location==resource.school):
            if(bookmarked=='False'):
                user.profile.favorites.add(resource)
                data['bookmarked']='True'
            else:
                user.profile.favorites.remove(resource)
                data['bookmarked']='False'
        print(bookmarked)
        return JsonResponse(data)
    else:
        return JsonResponse({'error':'invalid'})

@csrf_protect
@login_required
@require_POST
def ajax_make_reservation(request):
    '''Make a new reservation
    '''
    
    # Use form to validate and clean POST data from Ajax
    form = AjaxMakeReservationForm(request.POST)
    data = {}
    if(form.is_valid()):
        # Get data from the request POST
        resource_id = form.cleaned_data['resource_id']
        time_block_id = form.cleaned_data['time_block_id']
        requested_date = form.cleaned_data['date']
        user = request.user
        
        # Check for valid resource
        if(Resource.objects.filter(pk=resource_id).exists()):
            requested_resource = Resource.objects.get(pk=resource_id)
            if(requested_resource.enabled is False):
                data['error']='no resource'
                return JsonResponse(data)
        else:
            data['error']='no resource'
            return JsonResponse(data)
        
        if(TimeBlock.objects.filter(pk=time_block_id).exists()):    
            requested_time_block = TimeBlock.objects.get(pk=time_block_id)
        else:
            data['error']='no block'
            return JsonResponse(data)
            
        # Create new reservation instance
        new_reservation = Reservation(
            resource=requested_resource, 
            time_block=requested_time_block, 
            client=user, 
            date=requested_date
        )
        
        try:
            # Use the model's clean() function to validate
            new_reservation.clean()
            new_reservation.save()
            data['id']= new_reservation.id
        except ValidationError as e:
            msg = e.message_dict['date']
            if(len(msg[0])>0):
                data['date-error']=msg[0]
                return JsonResponse(data)
            else:
                data['error']='validation error'
                return JsonResponse(data)
        
        data['complete']='complete'
        
        return JsonResponse(data)
        
    else:
        # invalid form data
        data={'error':'invalid data'}
        return JsonResponse(data)
   
    
@csrf_protect
@login_required
@require_POST
def ajax_cancel_reservation(request):
    '''Cancel Reservations
    '''
    # Use form to validate and clean POST data from Ajax
    form = AjaxCancelReservationForm(request.POST)
    
    if(form.is_valid()):
        # Get data from the request POST
        reservation_id = form.cleaned_data['reservation_id']
        user = request.user
        
        if(Reservation.objects.filter(pk=reservation_id).exists()):
            reservation = Reservation.objects.get(pk=reservation_id)
            
            # Validate owner is trying to cancel
            if(reservation.client == user):
                reservation.delete()
                return JsonResponse({'complete':'success'})
            else:
                return JsonResponse({'error':'not owner'})
        else:
            return JsonResponse({'error':'no reservation'})
        
    else:
        return JsonResponse({'form':'invalid'})    
    
    
# Note: Add form validation and check that redirects actually work
@csrf_protect
@login_required
@require_POST
def ajax_get_reservations(request):
    '''Get all reservations for a given date/resource
    '''
    # Get data from the request
    reservation_date = request.POST.get('reservation_date', None)
    resource_id = request.POST.get('resource_id', None)
    
    user_school = request.user.profile.location
    resource = get_object_or_404(Resource, pk=resource_id)
    
    # Validate user has access to resource
    if(user_school.name != resource.school.name or resource.enabled is False):
        data = {'error':'invalid',}
        return JsonResponse(data)
        
    # Retrieve data for template
    time_blocks = list(TimeBlock.objects.filter(school=resource.school))
    reservations = Reservation.objects.filter(resource=resource_id).filter(date=reservation_date)
    data={}
    
    for i, time_block in enumerate(time_blocks): 
        data[i]={ 
            'time_block_id':time_block.id,
            'time_block_name':time_block.name,
            'resource_id':resource_id,
            'reservation_id':None,
            'reserved':'open'
        }
        for reservation in reservations:
            
            # Look for a reservation in that block
            if(reservation.time_block.id == time_block.id):
                data[i]['reservation_id'] = reservation.id 
                
                if(reservation.client == request.user): 
                    # Match was the user
                    data[i]['reserved']='user' 
                else:
                    # Match was another user
                    user = reservation.client
                    if(len(user.get_full_name())<1):
                        username = user.username
                    else:
                        username = user.get_full_name()
                    
                    display_client = f'<a href="mailto:{user.email}?subject=Your reservation of {resource.name} on {reservation.date} ({reservation.time_block.name})">{username}</a>'
                    data[i]['reserved']=display_client 
    return JsonResponse(data)
    
    
import datetime as dt
@login_required
@user_passes_test(is_school_admin)
def bulk_reservation(request):
    '''Building Admins can create bulk reservations for a resource.
    Bulk reservations will not override existing reservations by other users. 
    This view will return a list of 'conflicts' that could not be reserved.
    '''
    if request.method == 'POST':
        bulk_reservation_form=BulkReservationForm(request.POST, user_school=request.user.profile.location)
        user_school = request.user.profile.location
        # print(request.POST)
        if bulk_reservation_form.is_valid():
            resource_id = bulk_reservation_form.cleaned_data['resource']
            from_date = bulk_reservation_form.cleaned_data['from_date']
            to_date = bulk_reservation_form.cleaned_data['to_date']
            time_block_ids = bulk_reservation_form.cleaned_data['time_blocks']
            
            print(from_date, to_date)
            
            resource = get_object_or_404(Resource, pk=resource_id)
            
            if(user_school is not resource.school):
                redirect('building_admin')
            
            '''Create two empty querysets to store the reservations 
            that succeed or fail
            '''
            conflicts=Resource.objects.none()
            successes=[]
            
            # Get the number of consecutive days to reserve a resource
            days_to_reserve = (to_date - from_date).days + 1
            
            # Loop through the time_blocks
            for time_block_id in time_block_ids:
                time_block = get_object_or_404(TimeBlock, pk=time_block_id)
                
                if(user_school is not time_block.school):
                    redirect('building_admin')
                
                # Loop through the days requested    
                for d in range(days_to_reserve):
                    reservation_date = (from_date + dt.timedelta(days = d))
                    
                    try: # Make all the reservations where no conflict exists
                        reservation = Reservation(resource=resource, time_block=time_block, client=request.user, date=reservation_date)
                        reservation.save()
                        
                        # Append success list
                        successes.append(reservation)
                        
                    except: # Report the conflicts back to the context
                        reservation = Reservation.objects.filter(
                            resource=resource
                        ).filter(
                            time_block=time_block
                        ).filter(
                            client=request.user
                        ).filter(
                            date=reservation_date
                        )
                        
                        # Merge failure queryset
                        conflicts = conflicts | reservation
                        
            # Create context for report            
            context={'successes':successes, 'conflicts':conflicts, 'resource':resource}
            
            # Return the confirmation page to user
            return render(request, 'reservations/building_admin/bulk_reservation_confirm.html', context)
            
        else:
            
            context={'bulk_reservation_form':bulk_reservation_form}
            return render(request, 'reservations/building_admin/bulk_reservation_form.html', context)
    else:
        bulk_reservation_form=BulkReservationForm(user_school=request.user.profile.location)
        
    context={'bulk_reservation_form':bulk_reservation_form}
    return render(request, 'reservations/building_admin/bulk_reservation_form.html', context)
   
    
def about(request):
    return render(request, 'aion/about.html')

def tos(request):
    return render(request, 'aion/tos.html')
    
def privacy(request):
    return render(request, 'aion/privacy.html')
   
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse    
def contact(request):
    
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            subject = contact_form.cleaned_data['subject']
            email_from = contact_form.cleaned_data['email_from']
            message = contact_form.cleaned_data['message']
            try:
                send_mail(subject, message, email_from, ['jeff@jeff.how'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('contact_success')
    else:
        contact_form = ContactForm()
    
    context={ 'contact_form': contact_form }
    return render(request, 'aion/contact.html', context)

def contact_success(request):
    return render(request, 'aion/contact_success.html')
    
   
