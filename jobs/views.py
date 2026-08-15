from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import timezone

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib.units import mm

from .models import Job, JobApplication, ContactMessage


# =========================================================
# JOB LIST
# =========================================================

def job_list(request):

    query = request.GET.get("q", "").strip()
    company = request.GET.get("company", "").strip()

    jobs = Job.objects.all()

    # SEARCH
    if query:
        jobs = jobs.filter(
            title__icontains=query
        ) | jobs.filter(
            company__icontains=query
        ) | jobs.filter(
            skills__icontains=query
        )

    # COMPANY FILTER
    if company:
        jobs = jobs.filter(
            company__iexact=company
        )

    return render(
        request,
        "jobs/job_list.html",
        {
            "jobs": jobs,
            "query": query,
            "company": company,
        }
    )


# =========================================================
# APPLY JOB
# =========================================================

@login_required
def apply_job(request, job_id):

    job = get_object_or_404(Job, id=job_id)

    if request.method == "POST":

        application = JobApplication.objects.create(
            job=job,
            user=request.user,
            full_name=request.POST.get("full_name"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
            resume=request.FILES.get("resume"),
            cover_letter=request.POST.get("cover_letter")
        )

        return render(
            request,
            "jobs/application_success.html",
            {
                "job": job,
                "application": application
            }
        )

    return render(
        request,
        "jobs/apply.html",
        {
            "job": job
        }
    )


# =========================================================
# DOWNLOAD APPLICATION PDF
# =========================================================

@login_required
def download_application_pdf(request, application_id):

    application = get_object_or_404(
        JobApplication,
        id=application_id,
        user=request.user
    )

    response = HttpResponse(
        content_type="application/pdf"
    )

    response["Content-Disposition"] = (
        f'attachment; filename="CareerHub_Application_{application.id}.pdf"'
    )

    document = SimpleDocTemplate(
        response,
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "CareerHubTitle",
        parent=styles["Title"],
        fontSize=24,
        leading=30,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#2563eb"),
        spaceAfter=8
    )

    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        fontSize=10,
        leading=14,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#64748b"),
        spaceAfter=15
    )

    heading_style = ParagraphStyle(
        "Heading",
        parent=styles["Heading2"],
        fontSize=14,
        textColor=colors.HexColor("#111827"),
        spaceBefore=12,
        spaceAfter=8
    )

    normal_style = ParagraphStyle(
        "NormalCustom",
        parent=styles["Normal"],
        fontSize=10,
        leading=15,
        textColor=colors.HexColor("#374151")
    )

    story = []

    story.append(
        Paragraph(
            "CareerHub AI",
            title_style
        )
    )

    story.append(
        Paragraph(
            "JOB APPLICATION CONFIRMATION",
            subtitle_style
        )
    )

    status_table = Table(
        [
            [
                Paragraph("<b>APPLICATION STATUS</b>", normal_style),
                Paragraph("<b>SUBMITTED</b>", normal_style)
            ]
        ],
        colWidths=[75 * mm, 75 * mm]
    )

    status_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, -1),
                colors.HexColor("#eff6ff")
            ),
            (
                "TEXTCOLOR",
                (1, 0),
                (1, 0),
                colors.HexColor("#2563eb")
            ),
            (
                "BOX",
                (0, 0),
                (-1, -1),
                0.8,
                colors.HexColor("#bfdbfe")
            ),
            (
                "INNERGRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.HexColor("#dbeafe")
            ),
            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                10
            ),
            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                10
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                10
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                10
            )
        ])
    )

    story.append(status_table)

    story.append(Spacer(1, 12))

    story.append(
        Paragraph(
            "Application Details",
            heading_style
        )
    )

    applied_date = timezone.localtime(
        application.applied_at
    ).strftime(
        "%d %B %Y, %I:%M %p"
    )

    application_data = [
        [
            Paragraph("<b>Application ID</b>", normal_style),
            Paragraph(
                f"CHAI-{application.id:05d}",
                normal_style
            )
        ],
        [
            Paragraph("<b>Applied Date</b>", normal_style),
            Paragraph(
                applied_date,
                normal_style
            )
        ],
        [
            Paragraph("<b>Job Title</b>", normal_style),
            Paragraph(
                application.job.title,
                normal_style
            )
        ],
        [
            Paragraph("<b>Company</b>", normal_style),
            Paragraph(
                application.job.company,
                normal_style
            )
        ],
        [
            Paragraph("<b>Location</b>", normal_style),
            Paragraph(
                application.job.location,
                normal_style
            )
        ],
        [
            Paragraph("<b>Job Type</b>", normal_style),
            Paragraph(
                application.job.job_type,
                normal_style
            )
        ]
    ]

    application_table = Table(
        application_data,
        colWidths=[50 * mm, 100 * mm]
    )

    application_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (0, -1),
                colors.HexColor("#f8fafc")
            ),
            (
                "BOX",
                (0, 0),
                (-1, -1),
                0.8,
                colors.HexColor("#e2e8f0")
            ),
            (
                "INNERGRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.HexColor("#e2e8f0")
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "TOP"
            )
        ])
    )

    story.append(application_table)

    story.append(
        Paragraph(
            "Applicant Details",
            heading_style
        )
    )

    applicant_data = [
        [
            Paragraph("<b>Full Name</b>", normal_style),
            Paragraph(application.full_name or "", normal_style)
        ],
        [
            Paragraph("<b>Email</b>", normal_style),
            Paragraph(application.email or "", normal_style)
        ],
        [
            Paragraph("<b>Phone</b>", normal_style),
            Paragraph(application.phone or "", normal_style)
        ]
    ]

    applicant_table = Table(
        applicant_data,
        colWidths=[50 * mm, 100 * mm]
    )

    applicant_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (0, -1),
                colors.HexColor("#f8fafc")
            ),
            (
                "BOX",
                (0, 0),
                (-1, -1),
                0.8,
                colors.HexColor("#e2e8f0")
            ),
            (
                "INNERGRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.HexColor("#e2e8f0")
            )
        ])
    )

    story.append(applicant_table)

    if application.cover_letter:

        story.append(
            Paragraph(
                "Cover Letter",
                heading_style
            )
        )

        story.append(
            Paragraph(
                application.cover_letter.replace(
                    "\n",
                    "<br/>"
                ),
                normal_style
            )
        )

    story.append(Spacer(1, 25))

    story.append(
        Paragraph(
            "Thank you for applying through CareerHub AI.",
            subtitle_style
        )
    )

    story.append(
        Paragraph(
            "Please keep this document for your records.",
            subtitle_style
        )
    )

    document.build(story)

    return response


# =========================================================
# MY APPLICATIONS
# =========================================================

@login_required
def my_applications(request):

    applications = (
        JobApplication.objects
        .filter(user=request.user)
        .select_related("job")
        .order_by("-applied_at")
    )

    return render(
        request,
        "jobs/my_applications.html",
        {
            "applications": applications,
            "total_applications": applications.count()
        }
    )


# =========================================================
# CONTACT
# =========================================================

def contact(request):

    if request.method == "POST":

        ContactMessage.objects.create(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            message=request.POST.get("message")
        )

        return render(
            request,
            "contact_success.html"
        )

    return render(
        request,
        "contact.html"
    )