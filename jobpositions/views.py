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



def job_position_detail(request, job_position_id):
    job_position = get_object_or_404(JobPosition, id=job_position_id)
    jd=[string.replace('\r', '') for string in job_position.description.split("\n")]
    skills=[string.replace('\r', '') for string in job_position.skills.split("\n")]
    return render(request, 'job_position_detail.html', {'job_position': job_position,'jd':jd,'skills':skills})



def category_buttons(request):
    return render(request, 'category_buttons.html')

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

