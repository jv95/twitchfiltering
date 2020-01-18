from django.shortcuts import render


def index(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        with open('jv95/messages_from_contact.txt', 'a') as myfile:
            myfile.write(name + ' ' + email + ' ' + message + '\n')

    return render(request, 'jv95/templates/index.html')
