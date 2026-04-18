from django.db import models
from django.contrib.auth.models import User


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_class = models.CharField(max_length=2, blank=True, null=True)
    student_class = models.CharField(max_length=10, blank=True)  # '10th' or '12th'
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.student_class}"


class RIASECResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    realistic = models.FloatField(default=0)
    investigative = models.FloatField(default=0)
    artistic = models.FloatField(default=0)
    social = models.FloatField(default=0)
    enterprising = models.FloatField(default=0)
    conventional = models.FloatField(default=0)
    top_trait = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - RIASEC - {self.top_trait}"


class BigFiveResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    openness = models.FloatField(default=0)
    conscientiousness = models.FloatField(default=0)
    extraversion = models.FloatField(default=0)
    agreeableness = models.FloatField(default=0)
    neuroticism = models.FloatField(default=0)
    top_trait = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - BigFive - {self.top_trait}"


class AptitudeResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    logical = models.FloatField(default=0)
    verbal = models.FloatField(default=0)
    numerical = models.FloatField(default=0)
    spatial = models.FloatField(default=0)
    mechanical = models.FloatField(default=0)
    top_trait = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - Aptitude - {self.top_trait}"


class AcademicResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    student_class = models.CharField(max_length=10)   # '10th' or '12th'
    stream = models.CharField(max_length=20, blank=True)  # 'cs', 'bio', 'arts'
    subjects_json = models.TextField()  # JSON string of subject scores
    average_score = models.FloatField(default=0)
    top_subject = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - Academic {self.student_class} - Avg:{self.average_score}"


class AIRecommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recommendation_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - AI Rec - {self.created_at.strftime('%Y-%m-%d')}"
