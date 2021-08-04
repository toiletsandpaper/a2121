from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import Http404, JsonResponse, HttpResponse
from analytics.models import LifetimeAionStat, LifetimeSchoolStat
from reservations.models import Organization

def access_allowed(user):
    '''This function is passed to the 'user_passes_test' decorator
    '''
    # Only superusers allowed
    if not user.is_superuser:
        raise Http404
        
    return user
 
    
# Create your views here.
@user_passes_test(access_allowed)
@login_required
def dashboard(request):
    '''View to render primary dashboard page
    '''
    # Only superusers allowed
    if not request.user.is_superuser:
        # raise Http404
        return HttpResponse('nope')
    return render(request, 'analytics/dashboard.html', {})


@user_passes_test(access_allowed)
@login_required
def ajax_lifetime_aion_stats(request):
    totals = LifetimeAionStat.objects.filter(pk=1)
    data = {
        'labels':['Reservations', 'Users', 'Resources', 'Time Blocks'],
        'chart_data':[
            totals[0].reservations,
            totals[0].users, 
            totals[0].resources,
            totals[0].time_blocks, 
        ],
        'Total Lifetime Reservations':totals[0].reservations,
        'Total Lifetime Users':totals[0].users,
        'Total Lifetime Resources':totals[0].resources,
        'Total Lifetime Timeblocks':totals[0].time_blocks,
    }
    
    return JsonResponse(data)
    
    
@user_passes_test(access_allowed)
@login_required
def ajax_lifetime_school_stats(request):
    '''Returns school datasets based on org
    example:
    
    {
        labels:['Users', 'Resources', 'Time Blocks']
    },{
        datasets:{
            'wps':[{
                'label': 'WTHS',
                'data': [20,20,20],
            },{
                'label': 'South',
                'data': [20,20,20],
            }],
            'bps':[{
                'label': 'Madison Park',
                'data': [20,20,20],
            }],
            ...
        }
    }
    '''
    
    response = {'labels':['Users', 'Resources', 'Time Blocks']}
    
    orgs = Organization.objects.all()
    
    datasets={}
    
    for org in orgs:
        dataset = []
        schools = LifetimeSchoolStat.objects.filter(organization=org)
        
        for school in schools:
            dataset.append({
                'label':school.school.name, 
                'data':[school.users, school.resources, school.time_blocks]
            })
        
        datasets[org.name]=dataset
   
    response['datasets'] = datasets
    
    return JsonResponse(response)
    