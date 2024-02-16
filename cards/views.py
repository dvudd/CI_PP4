from django.shortcuts import render, redirect, get_object_or_404
from .forms import SubjectForm
from .models import Subject

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        # Render a template with user-specific content for logged-in users
        user_subjects = Subject.objects.filter(creator=request.user)
        return render(request, 'cards/home.html', {'user_subjects': user_subjects})
    else:
        # Render a generic template (index.html) for non-logged-in users
        return render(request, 'cards/index.html')


def create_subject(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.creator = request.user
            subject.save()
            return redirect('subject_detail', subject_id=subject.id)
    else:
        form = SubjectForm()
    return render(request, 'cards/create_subject.html', {'form': form})

def subject_detail(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    return render(request, 'cards/subject_detail.html', {'subject': subject})