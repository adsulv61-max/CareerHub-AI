from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail

from .models import ChatHistory, Application, Profile

import requests
import os
from openai import OpenAI

# =========================================================
# HOME
# =========================================================

def home(request):
    return render(request, "home.html")


# =========================================================
# DASHBOARD
# =========================================================

def dashboard(request):

    if not request.user.is_authenticated:
        return redirect("/login/")

    applications = Application.objects.filter(
        user=request.user
    ).order_by("-applied_at")

    chat_history = ChatHistory.objects.filter(
        user=request.user
    ).order_by("-created_at")

    applications_count = applications.count()
    ai_chats_count = chat_history.count()

    return render(
        request,
        "dashboard.html",
        {
            "applications": applications,
            "chat_history": chat_history,
            "applications_count": applications_count,
            "ai_chats_count": ai_chats_count,
            "user": request.user,
        }
    )


# =========================================================
# LOGIN
# =========================================================

def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect("/")

        return render(
            request,
            "login.html",
            {
                "error": "Invalid username or password"
            }
        )

    return render(request, "login.html")


# =========================================================
# REGISTER
# =========================================================

def register_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:

            return render(
                request,
                "register.html",
                {
                    "error": "Passwords do not match"
                }
            )

        if User.objects.filter(
            username=username
        ).exists():

            return render(
                request,
                "register.html",
                {
                    "error": "Username already exists"
                }
            )

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect("/login/")

    return render(request, "register.html")


# =========================================================
# LOGOUT
# =========================================================

def logout_view(request):

    logout(request)

    return redirect("/")


# =========================================================
# COMPANIES
# =========================================================

def companies(request):

    return render(
        request,
        "companies.html"
    )


# =========================================================
# ABOUT
# =========================================================

def about(request):

    return render(
        request,
        "about.html"
    )


# =========================================================
# CONTACT
# =========================================================

def contact(request):

    if request.method == "POST":

        name = request.POST.get(
            "name",
            ""
        ).strip()

        email = request.POST.get(
            "email",
            ""
        ).strip()

        user_message = request.POST.get(
            "message",
            ""
        ).strip()

        try:

            send_mail(

                subject=f"CareerHub AI - Message from {name}",

                message=f"""
You received a new message from CareerHub AI.

Name: {name}
Email: {email}

Message:
{user_message}
""",

                from_email="vikrantadsul8@gmail.com",

                recipient_list=[
                    "vikrantadsul8@gmail.com"
                ],

                fail_silently=False,
            )

            return render(
                request,
                "contact.html",
                {
                    "success":
                    "✅ Message sent successfully!"
                }
            )

        except Exception as e:

            print(
                "\n================ EMAIL ERROR ================"
            )

            print(e)

            print(
                "=============================================\n"
            )

            return render(
                request,
                "contact.html",
                {
                    "success":
                    "Message received."
                }
            )

    return render(
        request,
        "contact.html"
    )


# =========================================================
# MY APPLICATIONS
# =========================================================

def my_applications(request):

    if not request.user.is_authenticated:
        return redirect("/login/")

    applications = Application.objects.filter(
        user=request.user
    ).order_by("-applied_at")

    return render(
        request,
        "my_applications.html",
        {
            "applications": applications
        }
    )


# =========================================================
# PROFILE
# =========================================================

@login_required
def profile(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    # =====================================================
    # SAVE PROFILE
    # =====================================================

    if request.method == "POST":

        profile.full_name = request.POST.get(
            "full_name",
            ""
        ).strip()

        profile.phone = request.POST.get(
            "phone",
            ""
        ).strip()

        profile.location = request.POST.get(
            "location",
            ""
        ).strip()

        profile.education = request.POST.get(
            "education",
            ""
        ).strip()

        profile.skills = request.POST.get(
            "skills",
            ""
        ).strip()

        profile.bio = request.POST.get(
            "bio",
            ""
        ).strip()

        profile.github = request.POST.get(
            "github",
            ""
        ).strip()

        profile.linkedin = request.POST.get(
            "linkedin",
            ""
        ).strip()

        # =================================================
        # PROFILE PHOTO
        # =================================================

        if request.FILES.get("profile_image"):

            profile.profile_image = request.FILES.get(
                "profile_image"
            )

        # =================================================
        # SAVE
        # =================================================

        profile.save()

        return redirect("/profile/")

    # =====================================================
    # PROFILE COMPLETION
    # =====================================================

    fields = [
        profile.full_name,
        profile.phone,
        profile.location,
        profile.education,
        profile.skills,
        profile.bio,
        profile.github,
        profile.linkedin,
        profile.profile_image,
    ]

    completed = sum(
        1
        for field in fields
        if field
    )

    completion_percentage = round(
        (completed / len(fields)) * 100
    )

    # =====================================================
    # PROFILE PAGE
    # =====================================================

    return render(
        request,
        "profile.html",
        {
            "profile": profile,
            "user": request.user,
            "completion_percentage": completion_percentage,
        }
    )


# =========================================================
# CAREERHUB AI
# =========================================================

def ai_chat(request):

    answer = ""
    selected_chat = None
    history = []

    # =====================================================
    # CHAT HISTORY
    # =====================================================

    if request.user.is_authenticated:

        history = ChatHistory.objects.filter(
            user=request.user
        ).order_by("-created_at")

    # =====================================================
    # OPEN OLD CHAT
    # =====================================================

    if request.user.is_authenticated:

        chat_id = request.GET.get("chat")

        if chat_id:

            try:

                selected_chat = ChatHistory.objects.get(
                    id=chat_id,
                    user=request.user
                )

                answer = selected_chat.answer

            except ChatHistory.DoesNotExist:

                selected_chat = None

    # =====================================================
    # NEW AI QUESTION
    # =====================================================

    if request.method == "POST":

        user_message = request.POST.get(
            "message",
            ""
        ).strip()

        if user_message:

            try:

                # =================================================
                # OPENAI CLIENT
                # =================================================

                client = OpenAI(
                    api_key=os.environ.get("OPENAI_API_KEY")
                )

                response = client.responses.create(

                    model="gpt-4o-mini",

                    instructions=(
                        "You are CareerHub AI, "
                        "a helpful career assistant. "
                        "Help students with jobs, resumes, "
                        "interviews, skills, careers and programming. "
                        "Give clear, useful and easy-to-understand answers."
                    ),

                    input=user_message
                )

                # =================================================
                # AI ANSWER
                # =================================================

                answer = response.output_text

                # =================================================
                # SAVE CHAT
                # =================================================

                if request.user.is_authenticated:

                    new_chat = ChatHistory.objects.create(

                        user=request.user,

                        question=user_message,

                        answer=answer
                    )

                    selected_chat = new_chat

                    history = ChatHistory.objects.filter(
                        user=request.user
                    ).order_by("-created_at")

            except Exception as e:

                answer = (
                    "AI Error: "
                    + str(e)
                )

        else:

            answer = "Please enter a question."

    # =====================================================
    # AI PAGE
    # =====================================================

    return render(

        request,

        "ai_chat.html",

        {
            "answer": answer,
            "history": history,
            "selected_chat": selected_chat
        }

    )