from django.shortcuts import redirect

# decorator that prevents pages that are used when logged out to redirect when attempting to access them while logged in
def login_prohibited(view_function):
    def modified_view_function(request):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return redirect('admin_home')
            else:
                return redirect('student_home')
        else:
            return view_function(request)
    return modified_view_function

def student_prohibited(view_function):
    def modified_view_function(request):
        if request.user.is_staff==False:
            return redirect('student_home')
        else:
            return view_function(request)
    return modified_view_function

def admin_prohibited(view_function):
    def modified_view_function(request):
        if request.user.is_staff:
            return redirect('admin_home')
        else:
            return view_function(request)
    return modified_view_function