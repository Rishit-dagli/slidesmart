from django.shortcuts import render
from django.shortcuts import redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.views.decorators.http import require_POST


def index(request):
    context = {}

    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        context.update({'uploaded_file_url': uploaded_file_url})

    return render(request, 'index.html', context=context)


@require_POST
def receive_audio(request):
    try:
        print(request.POST)
    except:
        pass

    return redirect('index')


@require_POST
def receive_text(request):
    try:
        print(request.POST)
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        with open(myfile.name) as f:
            lines = f.readlines()
            print(lines)
    except:
        pass

    return redirect('index')