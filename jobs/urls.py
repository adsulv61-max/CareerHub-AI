from django.urls import path
from . import views

urlpatterns = [

    path("", views.job_list, name="job_list"),

    path(
        "apply/<int:job_id>/",
        views.apply_job,
        name="apply_job"
    ),

    path(
        "application/<int:application_id>/pdf/",
        views.download_application_pdf,
        name="download_application_pdf"
    ),

    path(
        "my-applications/",
        views.my_applications,
        name="my_applications"
    ),

]