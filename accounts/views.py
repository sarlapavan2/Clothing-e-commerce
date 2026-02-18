
from django.shortcuts import render, redirect
from django.http import HttpResponse
from . models import Customer, OTP
from . forms import RegisterForm
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import authenticate,login,logout
# Email related modules
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib import messages



# register form
def register_page(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.email
            user.set_password(form.cleaned_data['password1'])
            user.is_active = False
            user.save()
            print("User Created")

            # OTP Creation
            code_otp = OTP.generate_otp()
            otp_expired = timezone.now() + timedelta(minutes=5)
            OTP.objects.create(user = user, otp_code = code_otp, expires_at = otp_expired)
            request.session['email'] = user.email

            # sending otp through email
            send_otp(user.email, code_otp)     
                  
            return redirect('accounts:verify')

    return render(request, 'bullshit/register.html', {'form':form})


# otp form

def otp_page(request):
    email = request.session.get('email')
    if not email:
        return redirect('accounts:register')
    
    user = Customer.objects.filter(email=email).first()

    if request.method == 'POST':
        code = request.POST.get('otp')
        print(code)
        
        otp = OTP.objects.filter(user=user, otp_code=code, expires_at__gte=timezone.now()).first()
        if otp:
            print("otp is present in DB and setting user to active")
            user.is_active = True
            user.save()
            # otp.delete()   remove OTP after use
            return redirect('accounts:login')
        else:
            # OTP wrong or expired → increase attempts
            last_otp = OTP.objects.filter(user=user).last()

            if last_otp:
                last_otp.attempts += 1
                last_otp.save()

                if last_otp.attempts > 3:
                    messages.error(
                        request, "Too many attempts. Please request new OTP.")
                    return redirect('accounts:verify')

            messages.error(request, "Invalid or expired OTP")

    return render(request, 'bullshit/verify.html')


# resend otp
def resend_otp(request):

    email = request.session.get('email')

    if not email:
        return redirect('accounts:register')

    user = Customer.objects.filter(email=email).first()

    code_otp = OTP.generate_otp()
    otp_expired = timezone.now() + timedelta(minutes=5)

    OTP.objects.create(
        user=user,
        otp_code=code_otp,
        expires_at=otp_expired
    )

    send_otp(user.email, code_otp)

    return redirect('accounts:verify')


# login form
def login_page(request):
    if request.method == 'POST':
    
        email = request.POST.get('email')
        password = request.POST.get('password')
        print('This is email from session :', email)
        print('This is password from session :', password)
        
        user = Customer.objects.filter(email=email).first()
        print(user) 

        if user and user.check_password(password):
            if not user.is_active:
                messages.error(request, "Please verify OTP first")
                return redirect('accounts:verify')
            login(request, user)
            return redirect('accounts:home')
        else:
            messages.error(request, "Invalid email or password")
    
    return render(request, 'bullshit/login.html')

# logout
def logout_page(request):
    logout(request)
    return redirect('accounts:login')



# home page
def home_page(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    return render(request, 'home.html')


# sending otp through an email
def send_otp(receiver_email, otp_code):

    subject = "Your OTP Code is :"
    sender_email = settings.DEFAULT_FROM_EMAIL or settings.EMAIL_HOST_USER

    context = {
        'otp_code': otp_code,
        'expires_in_minutes': 5,
        'site_name': '__Lookism__',
    }

    # HTML email content
    html_content = render_to_string('email/otp.html', context)

    # Plain text fallback (for email clients that don’t support HTML)
    text_content = f"Your OTP code is {otp_code}. It will expire in 5 minutes."

    try:
        email = EmailMultiAlternatives(subject, text_content, sender_email, [receiver_email])

        # Attach HTML version
        email.attach_alternative(html_content, "text/html")

        email.send()

        print("OTP email sent successfully")
        return True

    except Exception as e:
        print("OTP email failed:", e)
        return False

