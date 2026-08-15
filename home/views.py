from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .models import ChatHistory, Application
import requests


# =========================
# HOME
# =========================

def home(request):
    return render(request, "home.html")


# =========================
# LOGIN
# =========================

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

        return render(request, "login.html", {
            "error": "Invalid username or password"
        })

    return render(request, "login.html")


# =========================
# REGISTER
# =========================

def register_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:

            return render(request, "register.html", {
                "error": "Passwords do not match"
            })

        if User.objects.filter(username=username).exists():

            return render(request, "register.html", {
                "error": "Username already exists"
            })

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect("/login/")

    return render(request, "register.html")


# =========================
# LOGOUT
# =========================

def logout_view(request):

    logout(request)

    return redirect("/")


# =========================
# COMPANIES
# =========================

def companies(request):

    return render(
        request,
        "companies.html"
    )


# =========================
# ABOUT
# =========================

def about(request):

    return render(
        request,
        "about.html"
    )


# =========================
# CONTACT
# =========================

def contact(request):

    if request.method == "POST":

        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        user_message = request.POST.get("message", "").strip()

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
                    "success": "✅ Message sent successfully!"
                }
            )

        except Exception as e:

            # Error terminal मध्ये दिसेल,
            # पण website वर मोठा error दाखवणार नाही.
            print("\n================ EMAIL ERROR ================")
            print(e)
            print("=============================================\n")

            return render(
                request,
                "contact.html",
                {
                    "success": "✅ Message sent successfully!"
                }
            )

    return render(request, "contact.html")


# =========================
# MY APPLICATIONS
# =========================

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


# =========================
# CAREERHUB AI
# =========================

def ai_chat(request):

    answer = ""
    selected_chat = None

    # =========================
    # GET USER CHAT HISTORY
    # =========================

    history = []

    if request.user.is_authenticated:

        history = ChatHistory.objects.filter(
            user=request.user
        ).order_by("-created_at")


    # =========================
    # OPEN OLD CHAT
    # =========================

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


    # =========================
    # NEW AI QUESTION
    # =========================

    if request.method == "POST":

        user_message = request.POST.get(
            "message",
            ""
        ).strip()

        if user_message:

            try:

                response = requests.post(

                    "http://localhost:11434/api/chat",

                    json={

                        "model": "llama3.2:1b",

                        "messages": [

                            {
                                "role": "system",

                                "content": (
                                    "You are CareerHub AI, a helpful "
                                    "career assistant. Help students "
                                    "with jobs, resumes, interviews, "
                                    "skills, careers and programming. "
                                    "Give clear and useful answers."
                                )
                            },

                            {
                                "role": "user",
                                "content": user_message
                            }

                        ],

                        "stream": False

                    },

                    timeout=120
                )

                data = response.json()


                # =========================
                # AI SUCCESS
                # =========================

                if response.status_code == 200:

                    answer = data["message"]["content"]


                    # =========================
                    # SAVE HISTORY
                    # =========================

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


                else:

                    answer = "AI Error: " + str(data)


            except requests.exceptions.ConnectionError:

                answer = (
                    "Ollama is not running. "
                    "Please start Ollama and try again."
                )


            except Exception as e:

                answer = "AI Error: " + str(e)


        else:

            answer = "Please enter a question."


    # =========================
    # SEND DATA TO HTML
    # =========================

    return render(

        request,

        "ai_chat.html",

        {
            "answer": answer,
            "history": history,
            "selected_chat": selected_chat
        }

    )