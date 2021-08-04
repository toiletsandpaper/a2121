# Aion

Aion is a scheduling application for schools created with Python and Django.

Schools often share resources between classrooms. We believe scheduling and 
reserving  resources like computer labs and laptop carts is easier with a 
block-based tool like Aion.

# Getting Started

## Installation and requirements
Aion requires Python 3.6+, PostgreSQL, an email service (ie. SendGrid),
and OS-specific dependancy tools.

After creating the superuser, use the django shell to manually create a profile
for the admin account.

In the admin site: Create organizations, email filters, and schools.

## Progress
1. Blank Cloud9 workspace created
2. Installed Python 3.6, VirtualEnv, and Django 2.1
3. Created Django Project (Aion)
4. Custom Cloud9 Runner (Command: aion/aion/settings.py | Runner: Aion Runner.run)
5. Created Django App (reservations)
8. Installed Crispy Forms
9. Configured Crispy Forms for Bootstrap4
10. Got the new blg-Admin feature working
11. Created decorator permission for school-admin
12. Built a signup module
13. Wrote all the main functionality
14. Wrote all the building admin functionaility
15. Created custom forms (extended crispy forms)
16. Created announcement feature for blg admins
17. Bulk reservation feature!
18. Background tasks added via django_cron

### Changes in v2.0
1. Supports multiple orgs
2. Supports multiple schools within an org 
3. Updated nomenclature for models (Resources, Blocks)
4. Users select their school within their org
5. Announcements feature
6. School admin level
7. Super admin level
8. Bulk reservations
9. Built-in account management
10. Bookmark Resources feature added

#### Built as a learning project by [Jeff.how](http://jeff.how)
[jeff@jeff.how](mailto:jeff.how)
