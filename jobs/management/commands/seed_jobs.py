from django.core.management.base import BaseCommand
from jobs.models import Job


class Command(BaseCommand):

    help = "Add sample jobs to CareerHub AI"

    def handle(self, *args, **kwargs):

        jobs = [

            {
                "title": "Python Developer",
                "company": "TCS",
                "location": "Pune, Maharashtra",
                "salary": "₹40000-60000",
                "job_type": "Full Time",
                "description": "We are looking for a Python Developer with knowledge of Python, Django, HTML, CSS and JavaScript. The candidate will work on web application and backend development.",
                "skills": "Python, Django, HTML, CSS, JavaScript",
            },

            {
                "title": "Web Developer",
                "company": "Infosys",
                "location": "Mumbai, Maharashtra",
                "salary": "₹35000-55000",
                "job_type": "Full Time",
                "description": "Develop and maintain modern websites and web applications using frontend and backend technologies.",
                "skills": "HTML, CSS, JavaScript, Python",
            },

            {
                "title": "Java Developer",
                "company": "Wipro",
                "location": "Bangalore, Karnataka",
                "salary": "₹45000-65000",
                "job_type": "Full Time",
                "description": "Work on Java based enterprise applications and backend services.",
                "skills": "Java, Spring Boot, SQL",
            },

            {
                "title": "Frontend Developer",
                "company": "Accenture",
                "location": "Pune, Maharashtra",
                "salary": "₹40000-70000",
                "job_type": "Full Time",
                "description": "Build responsive and modern user interfaces for web applications.",
                "skills": "HTML, CSS, JavaScript, React",
            },

            {
                "title": "Backend Developer",
                "company": "Microsoft",
                "location": "Hyderabad, Telangana",
                "salary": "₹60000-90000",
                "job_type": "Full Time",
                "description": "Develop scalable backend services and APIs for modern applications.",
                "skills": "Python, Django, REST API, SQL",
            },

            {
                "title": "Full Stack Developer",
                "company": "Google",
                "location": "Bangalore, Karnataka",
                "salary": "₹70000-100000",
                "job_type": "Full Time",
                "description": "Develop complete web applications using frontend and backend technologies.",
                "skills": "Python, Django, React, JavaScript",
            },

            {
                "title": "React Developer",
                "company": "Tech Mahindra",
                "location": "Pune, Maharashtra",
                "salary": "₹45000-70000",
                "job_type": "Full Time",
                "description": "Create interactive frontend applications using React.",
                "skills": "React, JavaScript, HTML, CSS",
            },

            {
                "title": "Django Developer",
                "company": "Persistent Systems",
                "location": "Pune, Maharashtra",
                "salary": "₹40000-65000",
                "job_type": "Full Time",
                "description": "Build secure and scalable web applications using Django and Python.",
                "skills": "Python, Django, REST API, PostgreSQL",
            },

            {
                "title": "Software Engineer",
                "company": "IBM",
                "location": "Bangalore, Karnataka",
                "salary": "₹50000-80000",
                "job_type": "Full Time",
                "description": "Develop software solutions and work with modern programming technologies.",
                "skills": "Python, Java, SQL, Git",
            },

            {
                "title": "Data Analyst",
                "company": "Deloitte",
                "location": "Mumbai, Maharashtra",
                "salary": "₹40000-65000",
                "job_type": "Full Time",
                "description": "Analyze business data and create meaningful reports and dashboards.",
                "skills": "Python, SQL, Excel, Power BI",
            },

            {
                "title": "Data Scientist",
                "company": "Amazon",
                "location": "Bangalore, Karnataka",
                "salary": "₹60000-100000",
                "job_type": "Full Time",
                "description": "Build data-driven models and machine learning solutions.",
                "skills": "Python, Pandas, NumPy, Machine Learning",
            },

            {
                "title": "AI/ML Engineer",
                "company": "HCL Technologies",
                "location": "Noida, Uttar Pradesh",
                "salary": "₹50000-85000",
                "job_type": "Full Time",
                "description": "Develop artificial intelligence and machine learning applications.",
                "skills": "Python, Machine Learning, AI, TensorFlow",
            },

            {
                "title": "JavaScript Developer",
                "company": "Capgemini",
                "location": "Mumbai, Maharashtra",
                "salary": "₹35000-60000",
                "job_type": "Full Time",
                "description": "Develop modern JavaScript based web applications.",
                "skills": "JavaScript, HTML, CSS, React",
            },

            {
                "title": "Android Developer",
                "company": "Zoho",
                "location": "Chennai, Tamil Nadu",
                "salary": "₹40000-65000",
                "job_type": "Full Time",
                "description": "Develop and maintain Android mobile applications.",
                "skills": "Java, Kotlin, Android",
            },

            {
                "title": "UI/UX Designer",
                "company": "Adobe",
                "location": "Noida, Uttar Pradesh",
                "salary": "₹40000-70000",
                "job_type": "Full Time",
                "description": "Design clean, modern and user-friendly digital experiences.",
                "skills": "Figma, UI Design, UX Design",
            },

            {
                "title": "DevOps Engineer",
                "company": "Oracle",
                "location": "Hyderabad, Telangana",
                "salary": "₹55000-85000",
                "job_type": "Full Time",
                "description": "Manage deployment pipelines, cloud infrastructure and automation.",
                "skills": "Linux, Docker, AWS, Git",
            },

            {
                "title": "Cloud Engineer",
                "company": "Cisco",
                "location": "Bangalore, Karnataka",
                "salary": "₹55000-90000",
                "job_type": "Full Time",
                "description": "Work with cloud infrastructure and scalable cloud services.",
                "skills": "AWS, Azure, Linux, Docker",
            },

            {
                "title": "Cyber Security Analyst",
                "company": "Wipro",
                "location": "Pune, Maharashtra",
                "salary": "₹45000-75000",
                "job_type": "Full Time",
                "description": "Monitor security systems and help protect applications and infrastructure.",
                "skills": "Cyber Security, Linux, Networking",
            },

            {
                "title": "QA Tester",
                "company": "Cognizant",
                "location": "Chennai, Tamil Nadu",
                "salary": "₹30000-50000",
                "job_type": "Full Time",
                "description": "Test applications, identify bugs and ensure software quality.",
                "skills": "Testing, Selenium, SQL",
            },

            {
                "title": "Python Developer Intern",
                "company": "Startup India",
                "location": "Pune, Maharashtra",
                "salary": "₹10000-20000",
                "job_type": "Internship",
                "description": "Learn and work on real-world Python and Django projects.",
                "skills": "Python, Django, HTML, CSS",
            },

            {
                "title": "Web Development Intern",
                "company": "Digital Labs",
                "location": "Mumbai, Maharashtra",
                "salary": "₹8000-15000",
                "job_type": "Internship",
                "description": "Work with the development team to build responsive websites.",
                "skills": "HTML, CSS, JavaScript",
            },

            {
                "title": "Software Developer Fresher",
                "company": "LTIMindtree",
                "location": "Pune, Maharashtra",
                "salary": "₹25000-40000",
                "job_type": "Full Time",
                "description": "Entry-level software development position for fresh graduates.",
                "skills": "Python, Java, SQL",
            },

            {
                "title": "SQL Developer",
                "company": "Accenture",
                "location": "Bangalore, Karnataka",
                "salary": "₹35000-60000",
                "job_type": "Full Time",
                "description": "Design queries, databases and data solutions for business applications.",
                "skills": "SQL, MySQL, Database",
            },

            {
                "title": "PHP Developer",
                "company": "WebTech Solutions",
                "location": "Pune, Maharashtra",
                "salary": "₹30000-50000",
                "job_type": "Full Time",
                "description": "Develop dynamic websites and backend applications using PHP.",
                "skills": "PHP, MySQL, HTML, CSS",
            },

            {
                "title": "Node.js Developer",
                "company": "Freshworks",
                "location": "Chennai, Tamil Nadu",
                "salary": "₹45000-70000",
                "job_type": "Full Time",
                "description": "Build scalable backend applications and APIs using Node.js.",
                "skills": "Node.js, JavaScript, Express, MongoDB",
            },

        ]

        added = 0

        for job_data in jobs:

            job, created = Job.objects.get_or_create(
                title=job_data["title"],
                company=job_data["company"],
                defaults={
                    "location": job_data["location"],
                    "salary": job_data["salary"],
                    "job_type": job_data["job_type"],
                    "description": job_data["description"],
                    "skills": job_data["skills"],
                }
            )

            if created:
                added += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"✅ {added} new jobs added successfully!"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"📊 Total jobs in CareerHub AI: {Job.objects.count()}"
            )
        )