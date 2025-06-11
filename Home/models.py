from django.db import models
from django.utils import timezone


class HeroSection(models.Model):
    agency_name = models.CharField(max_length=200)
    main_heading = models.CharField(max_length=500)
    description = models.TextField()
    # You might want to upload an image here
    fluid_image = models.ImageField(upload_to="hero_images/", blank=True, null=True)

    def __str__(self):
        return "Hero Section Content"


class AboutSection(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    about_image = models.ImageField(upload_to="about_images/", blank=True, null=True)
    main_description = models.TextField()

    def __str__(self):
        return "About Section Content"


class FeatureItem(models.Model):
    about_section = models.ForeignKey(
        AboutSection, on_delete=models.CASCADE, related_name="features"
    )
    icon_class = models.CharField(max_length=100)  # e.g., 'bi bi-check-circle-fill'
    heading = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return f"{self.heading} (About Feature)"


class ServiceSection(models.Model):
    intro_heading_part1 = models.CharField(max_length=200)
    intro_heading_part2 = models.CharField(max_length=200)
    summary = models.TextField()

    def __str__(self):
        return "Services Section Content"


class ServiceCard(models.Model):
    service_section = models.ForeignKey(
        ServiceSection, on_delete=models.CASCADE, related_name="cards"
    )
    icon_class = models.CharField(max_length=100)  # e.g., 'bi bi-palette'
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title


class Step(models.Model):
    step_number = models.CharField(max_length=50)
    icon_class = models.CharField(max_length=100)
    heading = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.heading


class Skill(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(
        unique=True,
        help_text="A short label for the skill, used in CSS classes (e.g., 'skill-python')",
    )

    def __str__(self):
        return self.name


# class Experience(models.Model):
#     job_title = models.CharField(max_length=200)
#     company_name = models.CharField(max_length=200)
#     duration = models.CharField(max_length=200)
#     responsibilities = models.JSONField(
#         help_text="Enter responsibilities as a JSON array of strings."
#     )  # Stores a list of strings

#     def __str__(self):
#         return f"{self.job_title} at {self.company_name}"


class Experience(models.Model):
    job_title = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    duration = models.CharField(
        max_length=100
    )  # Keep this for display (e.g., "Jan 2025 - Present")
    start_date = models.DateField(
        null=True, blank=True
    )  # New field for precise sorting
    responsibilities = models.JSONField(default=list)  # Stores a list of strings

    def __str__(self):
        return f"{self.job_title} at {self.company_name}"

    class Meta:
        # Sort by start_date in descending order (most recent first)
        # If start_date is null, those will typically appear first or last depending on DB.
        # It's best to always populate start_date.
        ordering = ["-start_date"]
        verbose_name = "Experience"
        verbose_name_plural = "Experiences"


class ContactInfo(models.Model):
    address = models.CharField(max_length=300)
    email1 = models.EmailField()
    email2 = models.EmailField(blank=True, null=True)
    # resume_link = models.URLField(
    #     blank=True, null=True, help_text="Link to your downloadable resume"
    # )
    resume_file = models.FileField(upload_to="resumes/", blank=True, null=True)

    def __str__(self):
        return "Contact Information"


# For the Blog/Call-to-Action section, you might have:
class Blog(models.Model):
    badge_text = models.CharField(max_length=50, default="Don't Miss!")
    heading = models.CharField(max_length=200)
    paragraph = models.TextField()
    feature1 = models.CharField(max_length=100)
    feature2 = models.CharField(max_length=100)
    feature3 = models.CharField(max_length=100)
    image = models.ImageField(upload_to="blog_promo_images/", blank=True, null=True)
    read_blog_url = models.URLField(default="#")
    view_all_blogs_url = models.TextField(default="{% url 'blogs' %}")
    published_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "Blog Promotion Section"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.BigIntegerField(null=True, blank=True)
    subject = models.CharField(
        max_length=200, blank=True, null=True
    )  # Subject can be optional if you want
    message = models.TextField()
    timestamp = models.DateTimeField(
        auto_now_add=True
    )  # Automatically sets the date/time when created
    is_read = models.BooleanField(default=False)  # To track if you've read the message

    class Meta:
        ordering = ["-timestamp"]  # Order by newest message first
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"

    def __str__(self):
        return f"Message from {self.name} ({self.email}) - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"


class Testimonial(models.Model):
    client_name = models.CharField(max_length=100, help_text="Name of the client.")
    client_title = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="e.g., 'CEO of XYZ Corp', 'Marketing Manager'",
    )
    company_name = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        help_text="Company the client works for (optional).",
    )
    linkedin_url = models.URLField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Optional: LinkedIn profile URL for verification.",
    )
    testimonial_text = models.TextField(help_text="The actual testimonial message.")

    client_image = models.ImageField(
        upload_to="testimonials/client_images/",
        blank=True,
        null=True,
        help_text="Optional: Upload your photo (e.g., headshot).",
    )
    company_logo = models.ImageField(
        upload_to="testimonials/company_logos/",
        blank=True,
        null=True,
        help_text="Optional: Upload your company logo.",
    )

    RATING_CHOICES = [
        (1, "1 Star"),
        (2, "2 Stars"),
        (3, "3 Stars"),
        (4, "4 Stars"),
        (5, "5 Stars"),
    ]
    rating = models.IntegerField(
        choices=RATING_CHOICES, default=5, help_text="Client's rating (1-5 stars)."
    )

    is_approved = models.BooleanField(
        default=False,
        help_text="Only approved testimonials will be shown on the website.",
    )
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-submitted_at"]
        verbose_name = "Client Testimonial"
        verbose_name_plural = "Client Testimonials"

    def __str__(self):
        approval_status = "Approved" if self.is_approved else "Pending"
        return f"Testimonial by {self.client_name} ({approval_status})"
