# decorator branch: created to handle the check on the user type for access

from django.shortcuts import redirect

def user_type_required(user_types):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            # Assuming you have the UserProfile related to the User
            user_profile = request.user.profile
            if user_profile.user_type in user_types:
                # User has the required user_type, allow access to the view
                return view_func(request, *args, **kwargs)
            else:
                # User doesn't have the required user_type, redirect to a different view
                return redirect('access_denied_view')
        return wrapper
    return decorator