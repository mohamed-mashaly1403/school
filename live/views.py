from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
import time
from django.contrib import messages
# Create your views here.
from live.models import CloseLive
from orders.models import Order


@user_passes_test(lambda u: u.is_staff)
def startLive(request,course,order):
    appID = "4bce2e802a5646a89835b1532ce8af71"
    appCertificate = "8dd20bc3d33c4c7d9646522038cb661f"
    user = str(request.user.id)
    user_name = request.user.first_name
    from live.RtmTokenBuilder import RtmTokenBuilder, Role_Rtm_User
    expirationTimeInSeconds = 3600
    currentTimestamp = int(time.time())
    privilegeExpiredTs = currentTimestamp + expirationTimeInSeconds
    token = RtmTokenBuilder.buildToken(appID, appCertificate, user, Role_Rtm_User, privilegeExpiredTs)
    print("Rtm Token: {}".format(token))
    orderr = Order.objects.get(order_number=order)
    CloseLive.objects.filter(order=orderr).delete()
    llive = CloseLive(
        order=orderr
    )
    llive.save()
    context = {
        'token': str(token),
        'user':user,
        'user_name':str(user_name),
        'course':str(course),
        'order':str(orderr)

    }
    print(orderr)
    return render(request,'startLive.html',context)



@login_required(login_url='login')
def joinLive(request,course,order):
    url = request.META.get('HTTP_REFERER')
    try:
        CloseLive.objects.filter(order=order).exists()
        appID = "4bce2e802a5646a89835b1532ce8af71"
        appCertificate = "8dd20bc3d33c4c7d9646522038cb661f"
        user = str(request.user.id)
        user_name = str(request.user.first_name)

        from live.RtmTokenBuilder import RtmTokenBuilder, Role_Rtm_User
        expirationTimeInSeconds = 3600
        currentTimestamp = int(time.time())
        privilegeExpiredTs = currentTimestamp + expirationTimeInSeconds
        token = RtmTokenBuilder.buildToken(appID, appCertificate, user, Role_Rtm_User, privilegeExpiredTs)
        print("Rtm Token: {}".format(token))
        context = {
            'token': token,
            'user':user,
            'user_name':user_name,
            'course':course,
            'order':order

        }
        return render(request, 'joinLive.html', context)
    except:
        messages.error(request, _('meeting not open '))
        return redirect(url)


def closeLive(request):

    orderFromJs = request.GET.get('order')
    orderr = Order.objects.get(order_number=orderFromJs, is_ordered=True)
    CloseLive.objects.filter(order=orderr).delete()


    return redirect('closepage')

def closepage(request):

    return render(request, 'closepage.html')

