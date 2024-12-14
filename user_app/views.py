# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUpForm, LoginForm
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import User , Category , Product, IklanPromosi # Pastikan model User diimpor jika diperlukan
from django.contrib import messages
from .forms import ProfileUpdateForm, ContactForm, IklanPromosiForm

# Create your views here.


def index(request):
    return render(request, "user_app/index.html")

def contact(request):
    msg = None
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # Menyimpan data ke database
            messages.success(request, "Terimakasih atas partisipasi Anda. Silahkan ")
            return redirect('user_app:contact')
    else:
        form = ContactForm()

    return render(request, 'user_app/contact.html', {'form': form,  'msg': msg})

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
            messages.success(request, "Anda Berhasil Mendaftar. Silahkan Masuk dengan Akun yang terdaftar")
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
    # Check if the user is a student
    if not request.user.is_student:
        messages.warning(request, "You are not authorized to access this page.")
        return redirect('index')  # Redirect to a safe page, like the home page
    return render(request, 'dashboard_app/student_dashboard.html')

@login_required
def teacherdashboard(request):
    # Check if the user is a teacher
    if not request.user.is_teacher:
        messages.warning(request, "You are not authorized to access this page.")
        return redirect('index')  # Redirect to a safe page, like the home page
    # Query semua data iklan dari database
    iklan_list = IklanPromosi.objects.all()
    return render(request, 'dashboard_app/teachers_dashboard.html', {'iklan_list': iklan_list})

@login_required
def teacherscourses(request):
    # Check if the user is a teacher
    if not request.user.is_teacher:
        messages.warning(request, "You are not authorized to access this page.")
        return redirect('index')  # Redirect to a safe page
    category = Category.objects.filter(status=0)
    context = {'category': category}
    return render(request, 'dashboard_app/teacherscourses.html', context)

@login_required
def productcourses(request, slug):
    # Check if the user is a teacher
    if not request.user.is_teacher:
        messages.warning(request, "You are not authorized to access this page.")
        return redirect('index')  # Redirect to a safe page
    if Category.objects.filter(slug=slug, status=0):
        product = Product.objects.filter(category__slug=slug)
        category = Category.objects.filter(slug=slug).first()
        context = {'product': product, 'category': category}
        return render(request, "dashboard_app/productcourses.html", context)
    else:
        messages.warning(request, "No such category found")
        return redirect('teacherscourses')

@login_required
def productdetails(request, cate_slug, prod_slug):
    # Check if the user is a teacher
    if not request.user.is_teacher:
        messages.warning(request, "You are not authorized to access this page.")
        return redirect('index')  # Redirect to a safe page
    if Category.objects.filter(slug=cate_slug, status=0):
        if Product.objects.filter(slug=prod_slug, status=0):
            products = Product.objects.filter(slug=prod_slug, status=0).first()
            context = {'products': products}
        else:
            messages.warning(request, "No such product found")
            return redirect('productcourses')
    else:
        messages.warning(request, "No such category found")
        return redirect('teacherscourses')
    return render(request, "dashboard_app/productdetails.html", context)

@login_required
def studentprofile(request):
    if not request.user.is_student:
        messages.warning(request, "You are not authorized to access this page.")
        return redirect('index')  # Redirect to a safe page, like the home page
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
def update_studentprofile(request):
    if not request.user.is_student:
        messages.warning(request, "You are not authorized to access this page.")
        return redirect('index')  # Redirect to a safe page, like the home page
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user_app:studentprofile')  
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'dashboard_app/update_student_profile.html', {'form': form})

@login_required
def teacherprofile(request):
    # Check if the user is a teacher
    if not request.user.is_teacher:
        messages.warning(request, "You are not authorized to access this page.")
        return redirect('index')  # Redirect to a safe page
    user_profile = request.user
    iklan_list = IklanPromosi.objects.all()
    return render(request, 'dashboard_app/teacher_profile.html', {'user_profile': user_profile, 'iklan_list': iklan_list})

@login_required
def update_teacherprofile(request):
    if not request.user.is_teacher:
        messages.warning(request, "You are not authorized to access this page.")
        return redirect('index')  # Redirect to a safe page
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user_app:teacherprofile')  
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'dashboard_app/update_teacher_profile.html', {'form': form})

@login_required
def buat_iklanpromosi(request):
    if not request.user.is_teacher:
        messages.warning(request, "You are not authorized to access this page.")
        return redirect('index')  # Redirect to a safe page
    if request.method == "POST":
        form = IklanPromosiForm(request.POST)
        if form.is_valid():
            form.save()  # Simpan data ke database
            return redirect('user_app:teacherprofile')  # Redirect ke halaman yang sama atau lainnya
    else:
        form = IklanPromosiForm(instance=request.user)
    user_profile = request.user
    return render(request, 'dashboard_app/buat_iklan_promosi.html', {'user_profile': user_profile,'form': form})
