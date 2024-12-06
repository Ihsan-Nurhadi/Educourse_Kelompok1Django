# Create your views here.
from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import User , Category , Product # Pastikan model User diimpor jika diperlukan
from django.contrib import messages

# Create your views here.


def index(request):
    return render(request, "user_app/index.html")
def contact(request):
    return render(request,'user_app/contact.html')
def about(request):
    return render(request,'user_app/aboutus.html')
def team(request):
    return render(request,'user_app/team.html')
def student(request):
    return render(request,'user_app/student.html')
def teacher(request):
    return render(request,'user_app/teacher.html')
def faq(request):
    return render(request,'user_app/faq.html')

def register(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST ,request.FILES)
        if form.is_valid():
            user = form.save()
            msg = 'user created'
        else:
            msg = 'form is not valid'
    else:
        form = SignUpForm()
    return render(request,'user_app/register.html', {'form': form, 'msg': msg})


def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # Sertakan request dalam pemanggilan authenticate
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                # Periksa apakah user memiliki atribut is_student atau is_teacher
                if user.is_student:
                    login(request, user)
                    return redirect('user_app:studentdashboard')
                elif user.is_teacher:
                    login(request, user)
                    return redirect('user_app:teacherdashboard')
                else:
                    msg = 'You are not authorized to login as a student or teacher.'
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating form'
    return render(request, 'user_app/login.html', {'form': form, 'msg': msg})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

@login_required
def studentdashboard(request):
    return render(request,'dashboard_app/student_dashboard.html')

@login_required
def teacherdashboard(request):
    return render(request,'dashboard_app/teachers_dashboard.html')

@login_required
def teacherscourses(request):
    category = Category.objects.filter(status=0)
    context = {'category':category}
    return render(
        request,
        'dashboard_app/teacherscourses.html', context
    )

@login_required
def productcourses(request, slug):
    if(Category.objects.filter(slug=slug, status=0)):
        product = Product.objects.filter(category__slug=slug)
        category = Category.objects.filter(slug=slug).first()
        context = {'product' : product, 'category' : category}
        return render(request, "dashboard_app/productcourses.html", context)
    else:
        messages.warning(request, "No such category found")
        return redirect('teacherscourses')

@login_required
def productdetails(request, cate_slug, prod_slug):
    if(Category.objects.filter(slug=cate_slug, status=0)):
        if(Product.objects.filter(slug=prod_slug, status=0)):
            products = Product.objects.filter(slug=prod_slug, status=0).first
            context = {'products':products}
        else:
            messages.warning(request, "No such product found")
            return redirect('productcourses')
    else:
        messages.warning(request, "No such category found")
        return redirect('teacherscourses')
    return render(request,"dashboard_app/productdetails.html", context)

@login_required
def studentprofile(request):
    # Mendapatkan objek User untuk pengguna yang sedang login
    user_profile = request.user  # Mengakses pengguna yang login langsung dari request.user
    
    # Kirim profil pengguna ke template
    return render(
        request,
        'dashboard_app/student_profile.html',
        {
            'user_profile': user_profile,  # Pass objek user ke template
        }
    )
@login_required
def teacherprofile(request):
    user_profile = request.user
    
    # Kirim profil pengguna ke template
    return render(
        request,
        'dashboard_app/teacher_profile.html',
        {
            'user_profile': user_profile,
        }
    )