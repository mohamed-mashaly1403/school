from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
import django.core.mail

# Create your views here.
from django.template.loader import render_to_string

from Teachers.form import TeacherProfileForm
from Teachers.models import TeacherProfile


def TeacherDashboard(request):
    return
@login_required(login_url='login')
def teacherProfile(request):

        have_account = TeacherProfile.objects.filter(user=request.user).exists()

        if have_account:
            accepted = TeacherProfile.objects.filter(is_accepted=True, user=request.user).exists()
            Regected = TeacherProfile.objects.filter(is_Regicted=True, user=request.user).exists()
            if accepted:
                return redirect('TeacherDashboard')
            else:
                if Regected:

                    return render(request, 'teachers/regicted.html')
                else:

                    return render(request, 'teachers/waitForReview.html')

        else:
            if request.method == 'POST':
                form = TeacherProfileForm(request.POST,request.FILES)
                print(form.errors)
                if form.is_valid():
                    animal = form.save(commit=False)
                    animal.user = request.user
                    animal.save()
                    messages.success(request, 'Your Account will be reviewed and will back to you soon')
                    mail_subject = 'Teacher registration'
                    mail_body = render_to_string('teachers/teacherRegistrationMail.html', {
                        'user': request.user.email,

                    })
                    to_email = 'first_man@windowslive.com'
                    send_mail = django.core.mail.EmailMessage(mail_subject, mail_body, to=[to_email])
                    send_mail.send()
                    return render(request, 'teachers/waitForReview.html')
                else:
                    print('not vaild')
            else:
                print('not post')
                form = TeacherProfileForm()
            context = {
                'form': form
            }

            return render(request, 'teachers/teacherRegister.html', context)


