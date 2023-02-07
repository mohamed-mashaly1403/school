import json

from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
import time
from django.contrib import messages
# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from live.models import CloseLive
from orders.models import Order
import random

@user_passes_test(lambda u: u.is_staff)
def startLive(request,course,order,classno):
    roomid = order + str(classno)
    appID ='4bce2e802a5646a89835b1532ce8af71'
    appCertificate ='8dd20bc3d33c4c7d9646522038cb661f'
    user = str(request.user.id)
    user_name = request.user.first_name
    from live.RtmTokenBuilder import RtmTokenBuilder, Role_Rtm_User
    expirationTimeInSeconds = 3600
    currentTimestamp = int(time.time())
    privilegeExpiredTs = currentTimestamp + expirationTimeInSeconds
    token = RtmTokenBuilder.buildToken(appID, appCertificate, user, Role_Rtm_User, privilegeExpiredTs)
    try:
        CloseLive.objects.filter(order="serviceWorker.js").delete()
    except:
        pass
    if order =="serviceWorker.js":
        pass
    else:
        live = CloseLive( order=order,classno=classno)
        # CloseLive.objects.get_or_create(order=order)
        try:
            live.save()
        except:
            pass

    context = {
        "token": json.dumps(token),
        "user":json.dumps(str(user)),
        "user_name":json.dumps(str(user_name)),
        "course":json.dumps(str(course)),
        "order":json.dumps(str(order)),
        "roomid":json.dumps(str(roomid)),
        'appID': appID,
        'appCertificate': appCertificate,
    }
    print(order)

    return render(request,'startLive.html',context)



@login_required(login_url='login')
def joinLive(request,course,order,classno):
    roomid = order + str(classno)
    url = request.META.get('HTTP_REFERER')
    try:
        CloseLive.objects.filter(order=order).exists()
        appID ='4bce2e802a5646a89835b1532ce8af71'
        appCertificate ='8dd20bc3d33c4c7d9646522038cb661f'
        user = str(request.user.id)
        user_name = str(request.user.first_name)

        from live.RtmTokenBuilder import RtmTokenBuilder, Role_Rtm_User
        expirationTimeInSeconds = 36000
        currentTimestamp = int(time.time())
        privilegeExpiredTs = currentTimestamp + expirationTimeInSeconds
        token = RtmTokenBuilder.buildToken(appID, appCertificate, user, Role_Rtm_User, privilegeExpiredTs)

        context = {
            'token': token,
            'user':user,
            'user_name':user_name,
            'course':course,
            'order':order,
            'roomid':roomid,
            'appID':appID,
            'appCertificate':appCertificate,

        }
        return render(request, 'joinLive.html', context)
    except:
        messages.error(request, _('meeting not open '))
        return redirect(url)

@csrf_exempt
def closeLive(request):
    data = json.loads(request.body)
    try:
        member = CloseLive.objects.get(
            order=data['order'],
                )
        member.delete()
    except:
        pass

    return JsonResponse('Member deleted', safe=False)

def closepage(request):
    try:
        orderr=request.GET.get('order')
        CloseLive.objects.filter(order=orderr).delete()
    except:
        pass

    return render(request, 'closepage.html')

