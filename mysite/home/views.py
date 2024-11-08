from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from .models import Contact
from django.shortcuts import render, redirect
from .models import Certi
from django.db import connection
from django.http import HttpResponse
from .forms import certiform
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .forms import OrdersForm
from .models import Orders
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from .models import Registration
from django.db import connection
from django.http import HttpResponseBadRequest
from django.core.exceptions import ValidationError
from django.http import HttpResponseForbidden
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from .forms import contactform
from django.conf import settings
import os


def favicon(request):
    return HttpResponse(
        status=204
    )  # Return an empty response with status code 204 (No Content)


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect("home")
        else:
            return HttpResponse("Invalid Credentials..!!")
    return render(request, "login.html")


@login_required(login_url="/login/")
def contact(request):
    try:
        contact = Contact.objects.get(staff=request.user)
    except Contact.DoesNotExist:
        # If no contact details exist for the user, create a new Contact instance
        contact = Contact(staff=request.user)

    if request.method == "POST":
        form = contactform(request.POST, instance=contact)
        if form.is_valid():
            # Save the form data, which will update or create the contact details
            form.save()
            messages.success(request, "Contact details updated successfully.")
            return redirect("profile")
    else:
        # Create a form instance with the existing contact details
        form = contactform(instance=contact)

    context = {
        "form": form,
    }
    return render(request, "contact.html", context)


"""
def orders(request):
    if request.method == 'POST':
        form = OrdersForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('orders')  # Redirect to a success page
    else:
        form = OrdersForm()
    return render(request, 'orders.html', {'form': form})
"""


def is_admin(user):
    return user.is_superuser


def orders(request):
    items = Orders.objects.all()
    if request.method == "POST":
        form = OrdersForm(request.POST, request.FILES)  # Include request.FILES
        if form.is_valid():
            form.save()
            return redirect("orders")
    else:
        form = OrdersForm()
    context = {
        "items": items,
        "form": form,
    }
    return render(request, "orders.html", context)



def signup(request):
    if request.method == "POST":
        uname = request.POST.get("username")
        email = request.POST.get("email")
        pass1 = request.POST.get("password1")
        pass2 = request.POST.get("password2")
        if pass1 != pass2:
            return HttpResponse("password doesn't match")
        else:
            my_user = User.objects.create_user(uname, email, pass1)
            my_user.save()
            return redirect("login")
    return render(request, "signup.html")


def logoutpage(request):
    logout(request)
    return redirect("login")


@login_required(login_url="/login/")
@user_passes_test(is_admin, login_url="/login/")
def student1(request):
    workers = User.objects.all()
    context = {"workers": workers}
    return render(request, "student1.html", context)

from datetime import datetime
from collections import defaultdict
@login_required(login_url="/login/")
def studentdetail(request, pk):
    try:
        # Retrieve user and contact information
        workers = User.objects.get(id=pk)
        contact = Contact.objects.get(staff=workers)

        # Retrieve orders related to the user and sort by start_date
        orders_stu = Orders.objects.filter(staff=workers).order_by('start_date')

        # Count orders by year and month
        orders_count_by_month = defaultdict(int)

        for order in orders_stu:
            if order.start_date:  # Check if start_date exists
                year_month = order.start_date.strftime('%Y-%m')  # Format to Year-Month
                orders_count_by_month[year_month] += 1  # Increment the count for that month

        # Prepare data for the chart
        labels = sorted(orders_count_by_month.keys())  # Sorted list of Year-Month
        data = [orders_count_by_month[label] for label in labels]  # Corresponding order counts

        # Retrieve the projects associated with this student (workers)
        projects = Project.objects.filter(user=workers)

    except User.DoesNotExist:
        # Handle the case where the user is not found
        return render(request, "user_not_found.html")
    except Contact.DoesNotExist:
        # Handle the case where the contact is not found
        contact = None

    context = {
        "workers": workers,
        "contact": contact,
        "orders_stu": orders_stu,  # Pass sorted orders to the context
        "labels": labels,  # Month-Year labels for the chart
        "data": data,      # Order counts for the chart
        "projects": projects,  # Add the projects to the context
    }

    return render(request, "studentdetail.html", context)


# views.py

from django.db.models import Count
from django.shortcuts import render, redirect
from .models import Certi, Registration
from .forms import certiform
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required(login_url="/login/")
def certi(request):
    # Fetch all Certi events with their registration counts using Django ORM
    items = Certi.objects.annotate(registration_count=Count('registration'))

    # Handle form submission for adding a new event
    if request.method == "POST":
        form = certiform(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Event Added Successfully")
            return redirect("certi")
    else:
        form = certiform()

    context = {
        "items": items,
        "form": form,
    }
    return render(request, "certi.html", context)


from django.shortcuts import render, redirect
from .models import Certi, Registration
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

@login_required
def register_for_event(request, event_id):
    try:
        event = Certi.objects.get(id=event_id)
    except Certi.DoesNotExist:
        messages.error(request, "Event not found.")
        return redirect('certi')

    # Check if user is already registered for this event
    if Registration.objects.filter(event=event, user=request.user).exists():
        messages.info(request, "You are already registered for this event.")
        return redirect('certi')

    # Register the user for the event
    Registration.objects.create(event=event, user=request.user)

    # Use get_registration_count method to get the updated count
    new_count = event.get_registration_count()

    # Return updated registration count to the frontend
    return JsonResponse({
        'success': True,
        'new_count': new_count,
        'message': "You have successfully registered for the event."
    })


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Certi, Registration

@login_required(login_url="/login/")
def unregister_for_event(request, event_id):
    try:
        # Find the event
        event = Certi.objects.get(id=event_id)
    except Certi.DoesNotExist:
        messages.error(request, "Event not found.")
        return redirect('certi')  # Redirect to the events page if the event is not found

    # Check if the user is registered for this event
    registration = Registration.objects.filter(event=event, user=request.user).first()

    if not registration:
        messages.info(request, "You are not registered for this event.")
        return redirect('certi')

    # Delete the registration
    registration.delete()
    messages.success(request, "You have successfully unregistered from the event.")
    return redirect('certi')


from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from .models import Certi, Registration

@login_required(login_url="/login/")
def event_details(request, event_id):
    # Get the event object
    event = get_object_or_404(Certi, id=event_id)
    
    # Get all the users who have registered for this event
    registered_users = Registration.objects.filter(event=event).select_related('user')
    
    context = {
        'event': event,
        'registered_users': registered_users
    }
    
    return render(request, 'event_details.html', context)


@login_required(login_url="/login/")
def certidel(request, pk):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM home_certi WHERE id = %s", [pk])
        item = cursor.fetchone()
    
    if not item:
        # Handle the case where the item is not found
        return HttpResponse(status=404)
    
    if request.method == "POST":
        # Delete registrations associated with this event
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM home_registration WHERE event_id = %s", [pk])  # Use event_id
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM home_certi WHERE id = %s", [pk])  # Delete the certi record
        return redirect("certi")
    
    return render(request, "certidel.html", {"item": item})




@login_required(login_url="/login/")
def certiupdate(request, pk):
    item = get_object_or_404(Certi, pk=pk)
    if request.method == "POST":
        form = certiform(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Event Updated Successfully")
            return redirect("certi")
    else:
        form = certiform(instance=item)
    
    context = {
        "form": form,
        "item": item,  # Ensure item is included in context
    }
    return render(request, "certiupdate.html", context)



@login_required(login_url="/login/")
def ordersupdate(request, pk):
    # Retrieve the existing order instance by primary key (pk)
    try:
        order_instance = Orders.objects.get(pk=pk)
    except Orders.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == "POST":
        form = OrdersForm(request.POST, request.FILES, instance=order_instance)
        if form.is_valid():
            # Save the form data to the existing instance
            orders_instance = form.save(commit=False)

            # Handle file upload
            uploaded_file = request.FILES.get("certificate")
            if uploaded_file:
                # Ensure the destination folder exists
                certificate_folder = os.path.join(settings.MEDIA_ROOT, "certificates")
                os.makedirs(certificate_folder, exist_ok=True)

                # Save the uploaded file to the destination folder
                certificate_path = os.path.join(certificate_folder, uploaded_file.name)
                with open(certificate_path, "wb") as destination:
                    for chunk in uploaded_file.chunks():
                        destination.write(chunk)

                # Save the file path to the database
                orders_instance.certificate = "certificates/" + uploaded_file.name

            # Save the updated instance
            orders_instance.save()

            return redirect("home")  # Make sure 'home' is the correct pattern name
    else:
        # Initialize the form with the existing instance data
        form = OrdersForm(instance=order_instance)

    context = {"form": form}
    return render(request, "ordersupdate.html", context)



@login_required(login_url="/login/")
def ordersdel(request, pk):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM home_orders WHERE id = %s", [pk])
        item = cursor.fetchone()
    if not item:
        # Handle the case where the item is not found
        return HttpResponse(status=404)
    if request.method == "POST":
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM home_orders WHERE id = %s", [pk])
        return redirect("home")
    return render(request, "ordersdel.html", {"item": item})


@login_required(login_url="/login/")
def display(request):
    return render(request, "display.html")



from collections import defaultdict
from django.db.models.functions import TruncMonth
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import User, Contact, Orders,Project

@login_required(login_url="/login/")
def student_index(request):
    user = request.user

    try:
        contact = Contact.objects.get(staff=user)
    except Contact.DoesNotExist:
        contact = None  # Handle case where contact does not exist

    # Retrieve orders related to the user and annotate by month-year
    orders_stu = Orders.objects.filter(staff=user)

    # Annotate with month-year and sort them by start_date
    orders_stu = orders_stu.annotate(month_year=TruncMonth('start_date')).order_by('start_date')

    # Grouping orders by month-year
    grouped_orders = defaultdict(list)
    for order in orders_stu:
        month_year = order.start_date.strftime('%Y-%m')  # Format as YYYY-MM
        grouped_orders[month_year].append(order)

    # Retrieve projects related to the user
    projects = Project.objects.filter(user=user)

    context = {
        "user": user,
        "contact": contact,
        "grouped_orders": grouped_orders,  # Pass grouped orders to the context
        "projects": projects,  # Add the projects to the context
    }

    return render(request, "student_index.html", context)



@login_required(login_url="/login/")
def index(request):
    orders_stu = Orders.objects.all()
    contacts = Contact.objects.all()
    total_users = User.objects.count()
    grouped_contacts = {}
    for contact in contacts:
        branch_section_key = (contact.branch, contact.section)
        if branch_section_key not in grouped_contacts:
            grouped_contacts[branch_section_key] = []
        grouped_contacts[branch_section_key].append(contact)
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM home_certi")
        certies = cursor.fetchall()
    if request.method == "POST":
        form = OrdersForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.staff = request.user
            instance.save()
            return redirect("home")
    else:
        form = OrdersForm()
    context = {
        "orders_stu": orders_stu,
        "form": form,
        "certies": certies,
        "total_users": total_users,
        "grouped_contacts": grouped_contacts,
    }
    return render(request, "index.html", context)


@login_required(login_url="/login/")
def view_students(request):
    # Fetch all contacts
    contacts = Contact.objects.all()
    workers = User.objects.all()
    # Group contacts by branch and section
    grouped_contacts = {}
    for contact in contacts:
        branch_section_key = (contact.branch, contact.section)
        if branch_section_key not in grouped_contacts:
            grouped_contacts[branch_section_key] = []
        grouped_contacts[branch_section_key].append(contact)
    context = {"grouped_contacts": grouped_contacts, "workers": workers}
    return render(request, "view_students.html", context)


def view_students_by_branch_section(request, branch, section):
    # Fetch contacts for the specified branch and section
    contacts = Contact.objects.filter(branch=branch, section=section)
    workers = User.objects.all()
    context = {
        "branch": branch,
        "section": section,
        "contacts": contacts,
        "workers": workers,
    }
    return render(request, "view_students_by_branch_section.html", context)


def certi_list(request):
    certifications = Certi.objects.all()
    context = {"certifications": certifications}
    return render(request, "certi_list.html", context)


@login_required(login_url="/login/")
def certi_detail(request, pk):
    certi = get_object_or_404(Certi, pk=pk)
    # Debugging statements
    print("Current User:", request.user)
    print("Certification Owner:", certi.user)
    print("Is Staff:", request.user.is_staff)
    # Ensure that the user is authenticated and is the owner of the certification
    if request.user.is_authenticated and request.user == certi.user:
        if request.method == "POST":
            certi.is_completed = request.POST.get("is_completed", False)
            # Update is_approved if the certification is marked as completed
            if certi.is_completed:
                certi.is_approved = True
            certi.save()
            messages.success(request, "Certification status updated successfully")
        context = {
            "certi": certi,
            "user": request.user,  # Add the user to the context
        }
        return render(request, "certi_detail.html", context)
    # Debugging statement
    print("Permission Denied")
    return HttpResponseForbidden(
        "You do not have permission to view this certification."
    )


def total_users_view(request):
    # Query all users
    all_users = User.objects.all()
    total_users = all_users.count()
    context = {"total_users": total_users}

    return render(request, "total_users.html", context)


@login_required(login_url="/login/")
def profile(request):
    try:
        contact = Contact.objects.get(staff=request.user)
    except Contact.DoesNotExist:
        contact = None
    return render(request, "profile.html", {"contact": contact})


from django.shortcuts import render, get_object_or_404, redirect
from .models import Project
from .forms import ProjectForm

# View for creating a project
# View to display all projects


# View to display all projects
@login_required(login_url="/login/")
def project_list(request):
    projects = Project.objects.filter(user=request.user)
    print(f"Projects for user {request.user}: {projects}")  # Debugging line
    return render(request, 'project_list.html', {'projects': projects})

# View to create a new project
@login_required(login_url="/login/")
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user  # Associate the project with the current user
            project.save()
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'create_project.html', {'form': form})

# View to edit a project
@login_required(login_url="/login/")
def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'create_project.html', {'form': form})

# View to delete a project
@login_required(login_url="/login/")
def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    project.delete()
    return redirect('project_list')



from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Certi, Registration
from django.contrib.auth.decorators import login_required

@login_required(login_url="/login/")
def event_list(request):
    events = Certi.objects.all()

    # Handle registration toggle
    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        event = Certi.objects.get(id=event_id)
        registration = Registration.objects.filter(event=event, user=request.user)

        if 'register' in request.POST:  # User wants to register
            if not registration.exists():
                Registration.objects.create(event=event, user=request.user)
                messages.success(request, f"Successfully registered for {event.event_name}")
            else:
                messages.info(request, f"You are already registered for {event.event_name}")
        elif 'unregister' in request.POST:  # User wants to unregister
            if registration.exists():
                registration.delete()
                messages.success(request, f"Successfully unregistered from {event.event_name}")
            else:
                messages.info(request, f"You are not registered for {event.event_name}")

    # Pass events to the template
    for event in events:
        event.registration_count = event.get_registration_count()  # Count the registrations
    
    return render(request, 'certi.html', {
        'events': events,
    })



