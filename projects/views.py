from django.contrib import messages
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from .forms import ContactMessageForm
from .models import Category, Project, Tag


def project_data(project):
    images = [{'url': image.image.url, 'caption': image.caption} for image in project.images.all()]
    if project.image and not images:
        images = [{'url': project.image.url, 'caption': ''}]
    return {
        'id': project.id, 'title': project.title, 'description': project.description,
        'category': project.category.slug if project.category else 'uncategorized',
        'category_name': project.category.name if project.category else 'Uncategorized',
        'tags': list(project.tags.values_list('name', flat=True)),
        'date': project.project_date.isoformat() if project.project_date else '',
        'image': project.image.url if project.image else (images[0]['url'] if images else ''),
        'images': images, 'video': project.video.url if project.video else '',
        'steps': [{'title': step.title, 'description': step.description} for step in project.steps.all()],
        'components': [{'name': item.component_name, 'quantity': item.quantity, 'notes': item.notes} for item in project.components.all()],
        'codeLink': project.github_url, 'videoLink': project.youtube_url,
    }


def home(request):
    projects = Project.objects.select_related('category').prefetch_related('tags', 'images', 'steps', 'components')
    payload = [project_data(project) for project in projects]
    categories = Category.objects.annotate(project_count=Count('projects')).order_by('name')
    context = {
        'project_data': payload,
        'category_data': [{'slug': category.slug, 'name': category.name, 'count': category.project_count} for category in categories],
        'all_count': projects.count(), 'tags': Tag.objects.order_by('name'),
        'contact_form': ContactMessageForm(),
    }
    return render(request, 'index.html', context)


@require_POST
def contact(request):
    form = ContactMessageForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, 'Thank you for your message. I will get back to you soon!')
    else:
        messages.error(request, 'Please check the form and try again.')
    return redirect('/#contact')


def project_api(request):
    query = request.GET.get('q', '').strip()
    projects = Project.objects.select_related('category').prefetch_related('tags', 'images', 'steps', 'components')
    if query:
        projects = projects.filter(Q(title__icontains=query) | Q(description__icontains=query) | Q(category__name__icontains=query) | Q(tags__name__icontains=query) | Q(components__component_name__icontains=query)).distinct()
    return JsonResponse({'projects': [project_data(project) for project in projects]})