# jobpositionsguide_project/jobpositions/views.py
from django.shortcuts import render, get_object_or_404
from .models import JobPosition,Billing,Institution
import re
import time
import requests
def job_positions_list(request):
    job_positions = JobPosition.objects.all()

    # Handle search functionality
    query = request.GET.get('q')
    if query:
        job_positions = job_positions.filter(title__icontains=query)

    context = {
        'job_positions': job_positions,
    }
    return render(request, 'index.html', {'job_positions': job_positions})


def perform_translation(input_text, input_lang, output_lang):
    url = f'https://translate.googleapis.com/translate_a/single?client=gtx&sl={input_lang}&tl={output_lang}&dt=t&q={input_text}'
    response = requests.get(url)
    translation = response.json()
    translation="".join(map(lambda item: item[0], translation[0]))
    return translation
def job_position_detail(request, job_position_id):

    job_position = get_object_or_404(JobPosition, id=job_position_id)
    cleaned_description = re.sub(r'(\bQ\d+:|\bA\d+:)\s*', '', job_position.description)
    cleaned_skills = "\n".join(line for line in job_position.skills.splitlines() if line.strip())
    cleaned_proceedings = "\n".join(line for line in job_position.proceedings.splitlines() if line.strip())
    if request.method == 'POST':
        start=time.time()
        selected_language = request.POST.get('lang')
        description=perform_translation("Description", 'en', selected_language)
        data=perform_translation(cleaned_description, 'en', selected_language)
        skills=perform_translation(cleaned_skills, 'en', selected_language)
        skills=[line.strip() for line in skills.split('\n') if line.strip()]
        text_lines = [line.strip() for line in data.split('\n') if line.strip()]
        SkillsYouNeed=perform_translation('Skills You Need', 'en', selected_language)
        Proceedings=perform_translation('How to become '+job_position.title, 'en', selected_language)
        proceeding=perform_translation(cleaned_proceedings, 'en', selected_language)
        proceeding = [string.replace('\r', '') for string in proceeding.split("\n")]
        
        context = {
            'job_position':job_position,
            'cleaned_text':text_lines,
            'description':description,
            'skills':skills,
            'SkillsYouNeed':SkillsYouNeed,
            'Proceedings':Proceedings,
            'proceedings':proceeding
        }
       
        return render(request, 'job_position_detail.html', context)
    else:
        # Assuming data is the text you provided
        text_lines = [line.strip() for line in cleaned_description.split('\n') if line.strip()]
        skills=[line.strip() for line in cleaned_skills.split('\n') if line.strip()]
        proceeding = [string.replace('\r', '') for string in cleaned_proceedings.split("\n")]
        context = {
            'job_position':job_position,
            'job_position_title':job_position.title.upper(),
            'cleaned_text':text_lines,
            'description':"Description",
            'skills':skills,
            'SkillsYouNeed':"Skills You Need",
            'Proceedings':'How to become '+job_position.title,
            'proceedings':proceeding
        }
       
        return render(request, 'job_position_detail.html', context)
    
    
    


from django.db.models import Count


from .models import ContactMessage
from django.shortcuts import render, redirect
from django.db.models import Count
from .models import JobPosition
from .forms import ContactForm, ContactMessage  # Import your form and model

def category_buttons(request):
    category_counts = JobPosition.objects.values('category').annotate(position_count=Count('id'))

    category_counts_dict = [item['position_count'] for item in category_counts]
    
    if request.method == 'POST':  # Handle the form submission only for POST requests
        form = ContactForm(request.POST)
        if form.is_valid():
            # Create a new instance of the ContactMessage model and save it to the database
            contact_message = ContactMessage(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                phone_number=form.cleaned_data['phone_number'],
                message=form.cleaned_data['message']
            )
            contact_message.save()
            # Redirect to a success page or any other desired action
            #return redirect('success_page')
    else:
        form = ContactForm()

    context = {
        "total_category": str(sum(category_counts_dict)),
        "form": form
    }
    return render(request, 'category_buttons.html', context)
def institutions(request):
    billing_data_list = Billing.objects.filter(payment_status__contains='Paid')
    billing_data = []

    for billing_data_item in billing_data_list:
        try:
            # Use get instead of filter if you expect only one Institution per billing object
            institution = Institution.objects.get(username__contains=billing_data_item.username)
            billing_data.append(institution)
        except Institution.DoesNotExist:
            # Handle the case where the institution does not exist
            pass
    print(billing_data)
    return render(request, 'insitutions.html', {'billing_data_list': billing_data})


from django.shortcuts import render, redirect
from .models import Institutor
from .forms import InstitutorSignUpForm  # Assuming you create a form for the signup

def institutor_signup(request):
    if request.method == 'POST':
        form = InstitutorSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # You may redirect to a success page or perform additional actions
            return redirect('institutor_login')
    else:
        form = InstitutorSignUpForm()

    return render(request, 'signup.html', {'form': form})
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import InstitutorLoginForm
from django.contrib.auth import logout
from easygui import msgbox
def institutor_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            institutor = Institutor.objects.get(username=username)

            if institutor.password == password:
                logout(request)
                # Password is correct, log in the institutor
                request.session['username'] = institutor.username  # Store institutor ID in session
                return redirect('institutorhomepage')
            else:
                messages.error(request, 'Invalid username or password.')

        except Institutor.DoesNotExist:
            messages.error(request, 'Invalid username or password.')


    return render(request, 'login.html')
from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    # Redirect to a login page or another appropriate page after logout
    return redirect('institutor_login')  # Replace 'login_page' with the actual URL name for your login page

def institutorhomepage(request):
    institutor_username = request.session.get('username')
    billing_data_list=Institution.objects.filter(username__icontains=institutor_username)
    payment_status_list=Billing.objects.filter(username__icontains=institutor_username,payment_status__contains='Pending')

    return render(request, 'institutor.html', {'institutor_username': institutor_username,'billing_data_list':billing_data_list,'payment_status_list':payment_status_list})
from datetime import datetime, timedelta

def one_month_later(original_date_str):
    # Convert the original date string to a datetime object
    original_date = datetime.strptime(original_date_str, "%Y-%m-%d")

    # Calculate one month later
    one_month_later_date = original_date + timedelta(days=30)

    # Format the result as a string
    one_month_later_date_str = one_month_later_date.strftime("%Y-%m-%d")

    return one_month_later_date_str
def billing_details(request):
    institutor_username = request.session.get('username')
    billing_data_list=Billing.objects.filter(username__icontains=institutor_username)
    # for i in billing_data_list:
    #     print(one_month_later(i.billing_date))
    return render(request, 'billing_details.html',{'billing_data_list':billing_data_list})

def payment(request):
    return render(request, 'payment.html')
def about(request):
    return render(request, 'about.html')
def gallery(request):
    return render(request, 'gallery.html')
def contact(request):
    return render(request, 'contact.html')
def search(request):
    query = request.GET.get('q')
    #job_positions = JobPosition.objects.all

    if query:
        job_positions = JobPosition.objects.filter(title__icontains=query)
    else:
        job_positions = JobPosition.objects.all()

    context = {
        'job_positions': job_positions,
    }
    return render(request, 'search.html',context)
from django.template.defaultfilters import upper
def job_positions_by_category(request, category):
    query = request.GET.get('q')
    job_positions = JobPosition.objects.filter(category=category)
    
    #print(job_positions)
    if query:
        job_positions = job_positions.filter(title__icontains=query)
    #job_positions = [{'title': upper(job_position.title)} for job_position in job_positions]
    context = {
        'category': category,
        'job_positions': job_positions,
    }
    return render(request, 'job_positions_by_category.html', context)

# your_app/views.py
from django.shortcuts import render, redirect
from .forms import BillingForm

def add_billing(request):
    username = request.session.get('username')
    if request.method == 'POST':
        form = BillingForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            new_billing = Billing(username=username, payment_status='Pending')
            new_billing.save()
            return redirect('institutorhomepage')  # Redirect to a success page or another view
    else:
        form = BillingForm()

    return render(request, 'billing_form.html', {'form': form})


# your_app/views.py
from django.shortcuts import render, get_object_or_404
from .models import Billing

def billing_detail(request, billing_id):
    billing_data = get_object_or_404(Institution, pk=billing_id)
   
    return render(request, 'billing_detail.html', {'billing_data': billing_data})
