# jobpositionsguide_project/jobpositions/views.py
from django.shortcuts import render, get_object_or_404
from .models import JobPosition
import re
import time

def job_positions_list(request):
    job_positions = JobPosition.objects.all()

    # Handle search functionality
    query = request.GET.get('q')
    if query:
        job_positions = job_positions.filter(title__icontains=query)

    context = {
        'job_positions': job_positions,
    }
    return render(request, 'home.html', {'job_positions': job_positions})
from googletrans import Translator, constants
from pprint import pprint
# init the Google API translator
translator = Translator()

# translate a spanish text to arabic for instance
translation = translator.translate("Hola Mundo", dest="hi")
#print(f"{translation.origin} ({translation.src}) --> {translation.text} ({translation.dest})")
# ... Other imports and code ...

def job_position_detail(request, job_position_id):
    translator = Translator()
    job_position = get_object_or_404(JobPosition, id=job_position_id)
   
    if request.method == 'POST':
        start=time.time()
        selected_language = request.POST.get('lang')
        description=translator.translate("Description", dest=selected_language.lower())
        SkillsYouNeed=translator.translate("Skills You Need!", dest=selected_language.lower())
        Proceedings=translator.translate("How to become "+job_position.title, dest=selected_language.lower())
        cleaned_skils = "\n".join(line for line in job_position.skills.splitlines() if line.strip())
        skills = [string.replace('\r', '') for string in cleaned_skils.split("\n")]
        skill=[]
        for s in skills:
            sk=translator.translate(s, dest=selected_language.lower())
            skill.append(sk.text)
        cleaned_proceedings = "\n".join(line for line in job_position.proceedings.splitlines() if line.strip())
        proceedings = [string.replace('\r', '') for string in cleaned_proceedings.split("\n")]
        proceeding=[]
        for s in proceedings:
            sk=translator.translate(s, dest=selected_language.lower())
            proceeding.append(sk.text)
        cleaned_text = re.sub(r'(\bQ\d+:|\bA\d+:)\s*', '', job_position.description)
        cleaned_text = "\n".join(line for line in cleaned_text.splitlines() if line.strip())
        description_lines = cleaned_text.strip().split('\n')

        questions_and_answers = []
        current_question = None
    
        for line in description_lines:
            translated_line = translator.translate(line, dest=selected_language.lower())
            line_text = translated_line.text  # Get the translated text from Translated object
            if "?" in line_text:
                current_question = line_text.strip()
            else:
                # Otherwise, it's an answer
                if current_question:
                    questions_and_answers.append((current_question, line_text.strip()))
                    current_question = None

        context = {
            'job_position': job_position,
            'questions_and_answers': questions_and_answers,
            'skills': skill,
            'proceedings':proceeding,
            'description':description.text,
            'SkillsYouNeed':SkillsYouNeed.text,
            'Proceedings':Proceedings.text,
            # ...
        }
        print(time.time()-start)
        return render(request, 'job_position_detail.html', context)
    
    else:
        description=translator.translate("Description")
        SkillsYouNeed=translator.translate("Skills You Need!")
        Proceedings=translator.translate("How to become "+job_position.title)
        cleaned_text = re.sub(r'(\bQ\d+:|\bA\d+:)\s*', '', job_position.description)
        cleaned_text = "\n".join(line for line in cleaned_text.splitlines() if line.strip())
        description_lines = cleaned_text.strip().split('\n')

        cleaned_skils = "\n".join(line for line in job_position.skills.splitlines() if line.strip())
        skills = [string.replace('\r', '') for string in cleaned_skils.split("\n")]
        cleaned_proceedings = "\n".join(line for line in job_position.proceedings.splitlines() if line.strip())
        proceedings = [string.replace('\r', '') for string in cleaned_proceedings.split("\n")]
        

        questions_and_answers = []
        current_question = None

        for line in description_lines:
            translated_line = translator.translate(line)
            line_text = translated_line.text  # Get the translated text from Translated object
            if "?" in line_text:
                current_question = line_text.strip()
            else:
                # Otherwise, it's an answer
                if current_question:
                    questions_and_answers.append((current_question, line_text.strip()))
                    current_question = None

        context = {
            'job_position': job_position,
            'questions_and_answers': questions_and_answers,
            'skills': skills,
            'proceedings':proceedings,
            'description':description.text,
            'SkillsYouNeed':SkillsYouNeed.text,
            'Proceedings':Proceedings.text,
            # ...
        }
        return render(request, 'job_position_detail.html', context)



from django.db.models import Count



def category_buttons(request):
    category_counts = JobPosition.objects.values('category').annotate(position_count=Count('id'))

    #category_counts = JobPosition.objects.values('category').annotate(position_count=Count('id'))

    # Create a dictionary to store the category counts
    category_counts_dict = [item['position_count'] for item in category_counts]

    # Now you have the category counts as a dictionary
    print(sum(category_counts_dict))
    context={
        "total_category":str(sum(category_counts_dict))
    }
    #print(category_counts_dict)
    return render(request, 'category_buttons.html',context)
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
def job_positions_by_category(request, category):
    query = request.GET.get('q')
    job_positions = JobPosition.objects.filter(category=category)
    
    #print(job_positions)
    if query:
        job_positions = job_positions.filter(title__icontains=query)

    context = {
        'category': category,
        'job_positions': job_positions,
    }
    return render(request, 'job_positions_by_category.html', context)

