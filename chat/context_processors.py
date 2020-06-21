from .models import UserList


def user(request):
    if hasattr(request, 'user'):
        try:
            u = UserList.objects.get(user__username=request.user.username)
            return{
                'userlist_user': u
            }
        except UserList.DoesNotExist:
            return{}
