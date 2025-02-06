from django.shortcuts import render,redirect
from .models import registration
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Post, Like, Comment, registration
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import User, Follow, Notification
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import registration
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import registration  # Import your user model



def home(request):
    return render(request, 'home.html')
def register(request):
    if request.method == 'POST':
        # Retrieve form data
        fullname=request.POST.get('fullname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        profile_pic=request.POST.get('profile_pic')
        phone_number=request.POST.get('phone_number')
        address=request.POST.get('address')
        bio=request.POST.get('bio')

        # Insert data into sphere_registration table
        new_user = registration(fullname=fullname,username=username, email=email, password=password)
        new_user.save()

        # Redirect to login or another page
        return redirect('login')
    return render(request, 'register.html')

def login(request):
    if request.method == "POST":
        # Safely retrieve email and password from the form using .get()
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            # Return an error message if either the email or password is missing
            error = "Please enter both email and password"
            return render(request, 'login.html', {'error': error})

        try:
            # Fetch the user from the database based on the email and password
            logdet = registration.objects.get(email=email, password=password)
            
            # Print the user id for debugging purposes
            print(logdet.id)

            # Store user ID in session for persistent login
            request.session['session1'] = logdet.id

            # Print the session id for debugging purposes
            print(request.session['session1'])

            # Redirect based on role or redirect to the homepage
            return redirect('homepage')  # Change 'homepage' to your actual route

        except registration.DoesNotExist:
            # If the user is not found, show an error message
            error = "Invalid email or password"
            return render(request, 'login.html', {'error': error})

    return render(request, 'login.html')

def homepage(request):
    if 'session1' not in request.session:
        return redirect('login')

    user_id = request.session['session1']
    user = registration.objects.get(id=user_id)

    if request.method == 'POST':
        content = request.POST.get('content', '')
        image = request.FILES.get('image')
        video = request.FILES.get('video')

        if content or image or video:
            Post.objects.create(user=user, content=content, image=image, video=video)
            return redirect('homepage')

    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'homepage.html', {'user': user, 'posts': posts})

def like_post(request, post_id):
    if 'session1' not in request.session:
        return JsonResponse({'error': 'User not logged in'}, status=401)

    user = registration.objects.get(id=request.session['session1'])
    post = get_object_or_404(Post, id=post_id)

    like, created = Like.objects.get_or_create(user=user, post=post)

    if not created:
        like.delete()  # Unlike if already liked
        liked = False
    else:
        liked = True

    return JsonResponse({'liked': liked, 'like_count': post.likes.count()})

def add_comment(request, post_id):
    if 'session1' not in request.session:
        return redirect('login')

    user = registration.objects.get(id=request.session['session1'])
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(user=user, post=post, content=content)
    
    return redirect('homepage')

from django.shortcuts import render, redirect
from .models import registration

def profile_view(request):
    if 'session1' in request.session:  # Check if user is logged in
        user_id = request.session['session1']
        user = registration.objects.get(id=user_id)  # Fetch user details
        return render(request, 'profile.html', {'user': user})
    else:
        return redirect('login')  # Redirect to login if not logged in

from django.shortcuts import render, redirect
from .models import registration
from django.db import IntegrityError

def update_profile(request):
    # Check if the user is logged in by verifying the session
    user_id = request.session.get('session1')
    if not user_id:
        # If no user is logged in, redirect to login page
        return redirect('login')

    try:
        # Retrieve the user's current profile information based on the user ID
        user = registration.objects.get(id=user_id)

        if request.method == 'POST':
            # Retrieve form data
            fullname = request.POST.get('fullname')
            username = request.POST.get('username')
            email = request.POST.get('email')
            phone_number = request.POST.get('phone_number')
            address = request.POST.get('address')
            bio = request.POST.get('bio')
            profile_pic = request.FILES.get('profile_pic')  # Get the uploaded file

            # Check if any required fields are missing
            if not fullname or not username or not email:
                return render(request, 'update_profile.html', {'error': 'Full name, username, and email are required', 'user': user})

            try:
                # Update the user's profile details
                user.fullname = fullname
                user.username = username
                user.email = email
                user.phone_number = phone_number
                user.address = address
                user.bio = bio

                if profile_pic:
                    # Save the uploaded profile picture
                    fs = FileSystemStorage()  # Use the default file storage
                    filename = fs.save(profile_pic.name, profile_pic)  # Save the file
                    file_url = fs.url(filename)  # Get the URL of the saved file

                    # Update the profile picture URL in the user model
                    user.profile_picture = file_url  # Make sure you have a field 'profile_picture' in your model
                user.save()

                # Redirect to the profile page or homepage after successful update
                return redirect('profile')  # Change 'profile' to your actual profile route

            except IntegrityError as e:
                # Handle errors, such as duplicate email
                return render(request, 'update_profile.html', {'error': str(e), 'user': user})

        return render(request, 'update_profile.html', {'user': user})

    except registration.DoesNotExist:
        # If the user does not exist, redirect to the login page
        return redirect('login')

def profile_view_home(request, email):
    user = get_object_or_404(User, email=email)
    messages_received = Message.objects.filter(receiver=user).order_by('-created_at')
    return render(request, 'profile_view.html', {
        'user': user,
        'messages_received': messages_received,
    })


from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from .models import Message, registration

def message_page(request):
    if 'session1' not in request.session:
        return redirect('login')

    user_id = request.session['session1']
    logged_in_user = registration.objects.get(id=user_id)

    # Fetch all users except the logged-in user
    users = registration.objects.exclude(id=user_id)

    return render(request, 'messages.html', {'users': users, 'logged_in_user': logged_in_user})


def chat_view(request, user_id):
    if 'session1' not in request.session:
        return redirect('login')

    sender = registration.objects.get(id=request.session['session1'])
    receiver = get_object_or_404(registration, id=user_id)

    return render(request, 'chat.html', {'receiver': receiver, 'sender': sender})


def send_message(request):
    if request.method == "POST":
        sender_id = request.session.get('session1')
        receiver_id = request.POST.get('receiver_id')
        content = request.POST.get('message')

        if sender_id and receiver_id and content.strip():
            sender = registration.objects.get(id=sender_id)
            receiver = registration.objects.get(id=receiver_id)
            message = Message.objects.create(sender=sender, receiver=receiver, content=content)
            return JsonResponse({"status": "success", "message": content, "sender": sender.fullname})
    
    return JsonResponse({"status": "error"})

def fetch_messages(request, user_id):
    sender_id = request.session.get('session1')
    receiver_id = user_id

    messages_list = Message.objects.filter(
        sender__in=[sender_id, receiver_id], receiver__in=[sender_id, receiver_id]
    ).order_by('created_at')

    messages_data = [
        {"sender": msg.sender.fullname, "content": msg.content, "created_at": msg.created_at.strftime('%H:%M')}
        for msg in messages_list
    ]
    return JsonResponse({"messages": messages_data})

from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect

def logout(request):
    # Log the user out
    auth_logout(request)
    
    # Redirect to the login page
    return redirect('login')

def update_password(request):
    if request.method == 'POST':
        # Retrieve the current password and new password
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not current_password or not new_password or not confirm_password:
            # Ensure all fields are filled out
            return render(request, 'update_password.html', {'error': 'All fields are required'})

        if new_password != confirm_password:
            # Ensure the new password and confirm password match
            return render(request, 'update_password.html', {'error': 'New passwords do not match'})

        try:
            # Fetch the user from the session
            user_id = request.session.get('session1')
            if not user_id:
                return redirect('login')  # Redirect to login if user is not logged in

            user = registration.objects.get(id=user_id)

            if user.password != current_password:
                # Ensure the current password matches
                return render(request, 'update_password.html', {'error': 'Current password is incorrect'})

            # Update the password
            user.password = new_password
            user.save()

            # Provide a success message
            messages.success(request, 'Your password has been updated successfully.')
            return redirect('homepage')  # Redirect to login page after successful password update

        except registration.DoesNotExist:
            return render(request, 'update_password.html', {'error': 'User not found'})

    return render(request, 'update_password.html')

def notifications(request):
    return render(request, 'notifications.html')


def forgot_password(request):
    email = ""  # Initialize the email variable to an empty string
    if request.method == "POST":
        email = request.POST.get("email_forgotpassword")  # Get the email from the form
        
        if email:
            # Send password reset email
            send_password_reset_email(email)
            messages.success(request, "A password reset link has been sent to your email.")
        else:
            messages.error(request, "Please enter a valid email.")

    return render(request, "forgot_password.html", {"email": email})

def send_password_reset_email(request):
    # API has been removed for security purpose
    return render(request, 'send_password_email.html')

   
def reset_password(request):
    email = request.GET.get("email")  # Get email from the URL

    if request.method == "POST":
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if new_password and confirm_password:
            if new_password == confirm_password:
                try:
                    # Find the user with the given email
                    user = registration.objects.get(email=email)
                    
                    # Update the password
                    user.password = new_password  # Change this to hashed password in production
                    user.save()

                    messages.success(request, "Your password has been reset successfully.")
                    return redirect("login")
                except registration.DoesNotExist:
                    messages.error(request, "Invalid or expired password reset link.")
            else:
                messages.error(request, "Passwords do not match!")

    return render(request, "reset_password.html")

def about(request):
    return render(request, 'about.html')
def contact(request):
    return render(request, 'contact.html')
