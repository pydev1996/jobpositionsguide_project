# jobpositionsguide_project/jobpositions/views.py
from django.shortcuts import render, get_object_or_404
from .models import JobPosition

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
print(f"{translation.origin} ({translation.src}) --> {translation.text} ({translation.dest})")
# ... Other imports and code ...

def job_position_detail(request, job_position_id):
    translator = Translator()
    job_position = get_object_or_404(JobPosition, id=job_position_id)
   
    if request.method == 'POST':
        selected_language = request.POST.get('lang')
        description=translator.translate("Description", dest=selected_language.lower())
        SkillsYouNeed=translator.translate("Skills You Need!", dest=selected_language.lower())
        Proceedings=translator.translate("Proceedings", dest=selected_language.lower())
        skills = [string.replace('\r', '') for string in job_position.skills.split("\n")]
        skill=[]
        for s in skills:
            sk=translator.translate(s, dest=selected_language.lower())
            skill.append(sk.text)
        
        proceedings = [string.replace('\r', '') for string in job_position.proceedings.split("\n")]
        proceeding=[]
        for s in proceedings:
            sk=translator.translate(s, dest=selected_language.lower())
            proceeding.append(sk.text)

        description_lines = job_position.description.strip().split('\n')

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
        return render(request, 'job_position_detail.html', context)
    
    else:
        description=translator.translate("Description")
        SkillsYouNeed=translator.translate("Skills You Need!")
        Proceedings=translator.translate("Proceedings")
        description_lines = job_position.description.strip().split('\n')

        skills = [string.replace('\r', '') for string in job_position.skills.split("\n")]
        proceedings = [string.replace('\r', '') for string in job_position.proceedings.split("\n")]
        

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



def category_buttons(request):
    return render(request, 'category_buttons.html')
def about(request):
    return render(request, 'about.html')

def job_positions_by_category(request, category):
    query = request.GET.get('q')
    job_positions = JobPosition.objects.filter(category=category)

    if query:
        job_positions = job_positions.filter(title__icontains=query)

    context = {
        'category': category,
        'job_positions': job_positions,
    }
    return render(request, 'job_positions_by_category.html', context)

