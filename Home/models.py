from django.db import models
from django.utils import timezone
from cloudinary_storage.storage import MediaCloudinaryStorage  # Cloudinary storage


class HeroSection(models.Model):
    agency_name = models.CharField(max_length=200)
    main_heading = models.CharField(max_length=500)
    description = models.TextField()
    fluid_image = models.ImageField(
        upload_to="hero_images/",
        storage=MediaCloudinaryStorage(),
        blank=True,
        null=True,
    )

    def __str__(self):
        return "Hero Section Content"


class AboutSection(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    about_image = models.ImageField(
        upload_to="about_images/",
        storage=MediaCloudinaryStorage(),
        blank=True,
        null=True,
    )
    main_description = models.TextField()

    def __str__(self):
        return "About Section Content"


class FeatureItem(models.Model):
    about_section = models.ForeignKey(
        AboutSection, on_delete=models.CASCADE, related_name="features"
    )
    icon_class = models.CharField(max_length=100)
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
    icon_class = models.CharField(max_length=100)
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


class Experience(models.Model):
    job_title = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    duration = models.CharField(max_length=100)
    start_date = models.DateField(null=True, blank=True)
    responsibilities = models.JSONField(default=list)

    def __str__(self):
        return f"{self.job_title} at {self.company_name}"

    class Meta:
        ordering = ["-start_date"]
        verbose_name = "Experience"
        verbose_name_plural = "Experiences"


class ContactInfo(models.Model):
    address = models.CharField(max_length=300)
    email1 = models.EmailField()
    email2 = models.EmailField(blank=True, null=True)
    resume_file = models.FileField(
        upload_to="resumes/", storage=MediaCloudinaryStorage(), blank=True, null=True
    )

    def __str__(self):
        return "Contact Information"


class Blog(models.Model):
    badge_text = models.CharField(max_length=50, default="Don't Miss!")
    heading = models.CharField(max_length=200)
    paragraph = models.TextField()
    feature1 = models.CharField(max_length=100)
    feature2 = models.CharField(max_length=100)
    feature3 = models.CharField(max_length=100)
    image = models.ImageField(
        upload_to="blog_promo_images/",
        storage=MediaCloudinaryStorage(),
        blank=True,
        null=True,
    )
    read_blog_url = models.URLField(default="#")
    view_all_blogs_url = models.TextField(default="{% url 'blogs' %}")
    published_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "Blog Promotion Section"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.BigIntegerField(null=True, blank=True)
    subject = models.CharField(max_length=200, blank=True, null=True)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-timestamp"]
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"

    def __str__(self):
        return f"Message from {self.name} ({self.email}) - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"


class Testimonial(models.Model):
    client_name = models.CharField(max_length=100, help_text="Name of the client.")
    client_title = models.CharField(max_length=100, blank=True, null=True)
    company_name = models.CharField(max_length=150, blank=True, null=True)
    linkedin_url = models.URLField(max_length=200, blank=True, null=True)
    testimonial_text = models.TextField()
    client_image = models.ImageField(
        upload_to="testimonials/client_images/",
        storage=MediaCloudinaryStorage(),
        blank=True,
        null=True,
    )
    company_logo = models.ImageField(
        upload_to="testimonials/company_logos/",
        storage=MediaCloudinaryStorage(),
        blank=True,
        null=True,
    )

    RATING_CHOICES = [
        (1, "1 Star"),
        (2, "2 Stars"),
        (3, "3 Stars"),
        (4, "4 Stars"),
        (5, "5 Stars"),
    ]
    rating = models.IntegerField(choices=RATING_CHOICES, default=5)
    is_approved = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-submitted_at"]
        verbose_name = "Client Testimonial"
        verbose_name_plural = "Client Testimonials"

    def __str__(self):
        approval_status = "Approved" if self.is_approved else "Pending"
        return f"Testimonial by {self.client_name} ({approval_status})"
