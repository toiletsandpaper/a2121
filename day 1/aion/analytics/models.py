from django.db import models

from reservations.models import School, Organization

# Create your models here.
class LifetimeAionStat(models.Model):
    reservations=models.IntegerField(default=0)
    users=models.IntegerField(default=0)
    resources=models.IntegerField(default=0)
    time_blocks=models.IntegerField(default=0)
    
    def __str__(self):
        return 'Totals Since Creation'
    
    
class LifetimeSchoolStat(models.Model):
    organization=models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True)
    school=models.ForeignKey(School, on_delete=models.SET_NULL, null=True, blank=True)
    users=models.IntegerField(default=0)
    resources=models.IntegerField(default=0)
    time_blocks=models.IntegerField(default=0)
    
    class Meta:
       ordering = ['organization', 'school', ]
       
    def __str__(self):
        return f'{self.organization}: {self.school} Lifetime Totals'
        