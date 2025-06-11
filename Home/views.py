from django.shortcuts import render, redirect, get_object_or_404
from .models import (
    HeroSection,
    AboutSection,
    ServiceSection,
    Step,
    Skill,
    Experience,
    ContactInfo,
    Blog,
    ContactMessage,
    Testimonial,
)
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
import re
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Q


def home_view(request):
    hero_content = HeroSection.objects.first()
    about_content = AboutSection.objects.first()
    service_section = ServiceSection.objects.first()
    steps = Step.objects.all()
    skills = Skill.objects.all()
    experiences = Experience.objects.all()
    contact_info = ContactInfo.objects.first()
    blog_promotion = Blog.objects.order_by("-published_date").first()

    approved_testimonials = Testimonial.objects.filter(is_approved=True).order_by(
        "-submitted_at"
    )

    # Initialize variables for BOTH forms
    contact_form_errors = {}
    contact_submitted_data = {}

    testimonial_form_errors = {}
    testimonial_submitted_data = {  # Initialize with default for select/optional fields
        "rating": "5"  # Default rating
    }

    if request.method == "POST":
        form_id = request.POST.get("form_id")

        if form_id == "contact_form_submission":
            # --- Contact Form Handling ---
            name = request.POST.get("name", "").strip()
            email = request.POST.get("email", "").strip()
            phone = request.POST.get("phone", "").strip()  # Get phone number
            subject = request.POST.get("subject", "").strip()
            message = request.POST.get("message", "").strip()

            contact_submitted_data = {
                "name": name,
                "email": email,
                "phone": phone,
                "subject": subject,
                "message": message,
            }

            # Contact Form Validation
            if not name:
                contact_form_errors["name"] = "Name is required."
            if not email:
                contact_form_errors["email"] = "Email is required."
            elif not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email):
                contact_form_errors["email"] = "Enter a valid email address."
            if not subject:
                contact_form_errors["subject"] = "Subject is required."
            if not message:
                contact_form_errors["message"] = "Message is required."
            if phone and not re.fullmatch(
                r"^\+?(\d[\d\s\-()]{7,}\d)$", phone
            ):  # Basic phone number regex
                contact_form_errors["phone"] = (
                    "Enter a valid phone number (min 8 digits)."
                )

            if not contact_form_errors:
                try:
                    if not contact_info or not contact_info.email1:
                        raise ValueError(
                            "Contact recipient email not configured in admin."
                        )

                    ContactMessage.objects.create(
                        name=name,
                        email=email,
                        phone=phone,
                        subject=subject,
                        message=message,
                    )

                    email_subject = (
                        f"New Contact Form Submission from Portfolio: {subject}"
                    )
                    email_message = (
                        f"Name: {name}\n"
                        f"Email: {email}\n"
                        f"Phone: {phone}\n"  # Include phone in email
                        f"Subject: {subject}\n\n"
                        f"Message:\n{message}"
                    )
                    send_mail(
                        email_subject,
                        email_message,
                        settings.EMAIL_HOST_USER,
                        [contact_info.email1],
                        fail_silently=False,
                    )
                    messages.success(
                        request,
                        "Your message has been sent successfully! We will get back to you soon.",
                    )
                    return redirect("home")

                except ValueError as ve:
                    messages.error(
                        request,
                        f"Configuration error: {ve}. Please contact the site administrator.",
                    )
                    contact_form_errors["general"] = str(ve)
                except Exception as e:
                    messages.error(
                        request,
                        "There was an unexpected error sending your contact message. Please try again later.",
                    )
                    contact_form_errors["general"] = str(e)

        elif form_id == "testimonial_form_submission":
            # --- Testimonial Form Handling ---
            client_name = request.POST.get("client_name", "").strip()
            client_title = request.POST.get("client_title", "").strip()
            company_name = request.POST.get("company_name", "").strip()
            linkedin_url = request.POST.get("linkedin_url", "").strip()
            testimonial_text = request.POST.get("testimonial_text", "").strip()
            rating_str = request.POST.get("rating")

            client_image = request.FILES.get("client_image")
            company_logo = request.FILES.get("company_logo")

            # Populate submitted data for repopulation in template
            testimonial_submitted_data = {
                "client_name": client_name,
                "client_title": client_title,
                "company_name": company_name,
                "linkedin_url": linkedin_url,
                "testimonial_text": testimonial_text,
                "rating": rating_str,  # Keep as string for repopulation
            }

            # Testimonial Form Validation
            if not client_name:
                testimonial_form_errors["client_name"] = "Your name is required."
            if not testimonial_text:
                testimonial_form_errors["testimonial_text"] = (
                    "Your testimonial message is required."
                )

            rating = None
            if rating_str:
                try:
                    rating = int(rating_str)
                    if not (1 <= rating <= 5):
                        testimonial_form_errors["rating"] = (
                            "Rating must be between 1 and 5."
                        )
                except ValueError:
                    testimonial_form_errors["rating"] = "Invalid rating value."
            else:
                rating = 5  # Default if not provided

            if linkedin_url:
                validator = URLValidator()
                try:
                    validator(linkedin_url)
                except ValidationError:
                    testimonial_form_errors["linkedin_url"] = (
                        "Enter a valid LinkedIn URL."
                    )

            if not testimonial_form_errors:  # If no validation errors
                try:
                    Testimonial.objects.create(
                        client_name=client_name,
                        client_title=client_title or None,  # Store None if empty string
                        company_name=company_name or None,
                        linkedin_url=linkedin_url or None,
                        testimonial_text=testimonial_text,
                        rating=rating,
                        client_image=client_image,
                        company_logo=company_logo,
                        is_approved=False,
                    )
                    messages.success(
                        request,
                        "Your testimonial has been submitted successfully and is awaiting approval!",
                    )
                    return redirect("home")

                except Exception as e:
                    messages.error(
                        request,
                        f"There was an error saving your testimonial. Please try again later. Error: {e}",
                    )
                    testimonial_form_errors["general"] = str(e)
            else:
                messages.error(
                    request, "Please correct the errors in the testimonial form."
                )

    # Context for template rendering
    context = {
        "hero_content": hero_content,
        "about_content": about_content,
        "service_section": service_section,
        "steps": steps,
        "skills": skills,
        "experiences": experiences,
        "contact_info": contact_info,
        "blog_promotion": blog_promotion,
        "approved_testimonials": approved_testimonials,
        "errors": contact_form_errors,  # 'errors' for contact form
        "submitted_data": contact_submitted_data,  # 'submitted_data' for contact form
        "testimonial_form_errors": testimonial_form_errors,  # For testimonial form errors
        "testimonial_submitted_data": testimonial_submitted_data,  # For repopulating testimonial form
    }
    return render(request, "Home/home.html", context)


def blogs(request):
    query = request.GET.get("q", "")
    blogs = Blog.objects.all()

    if query:
        blogs = blogs.filter(
            Q(heading__icontains=query)
            | Q(paragraph__icontains=query)
            | Q(badge_text__icontains=query)
        )

    paginator = Paginator(blogs, 1)  # 5 blogs per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "Home/blogs.html", {"page_obj": page_obj, "query": query})
