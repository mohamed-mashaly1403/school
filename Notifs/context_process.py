from Notifs.models import Inboxnotif


def CountNotifications(request):
    count_notifications = None
    try:

        if request.user.is_authenticated:
            count_notifications = Inboxnotif.objects.filter(recipient=request.user, is_read=False).count()

        return {'count_notifications': count_notifications}
    except:
        return {'count_notifications': ''}

def ShowNotifications(request):
    try:
        user = request.user
        notifications = Inboxnotif.objects.filter(recipient=user).order_by('-created')
        return {'notifications': notifications}
    except:
        return {'notifications': ''}






