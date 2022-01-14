
from django.shortcuts import redirect, render


from Notifs.models import Inboxnotif
# def ShowNotificationsUrl(request):
#     url = request.META.get('HTTP_REFERER')
#     user = request.user
#     Inboxnotif.objects.filter(recipient=user, is_read=False).update(is_read=True)
#     print('test')
#     return redirect(url)

def DeleteNotification(request, noti_id):
    url = request.META.get('HTTP_REFERER')

    Inboxnotif.objects.filter(id=noti_id).delete()
    return redirect(url)


