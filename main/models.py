from django.db import models
from django.core.mail import send_mail
from django.core.validators import FileExtensionValidator

# Create your models here.

#Instructor Model
class Instructor(models.Model):
    full_name = models.CharField(max_length=100)
    bio = models.TextField(null=True)
    email = models.EmailField(max_length=100)
    qualification = models.CharField(max_length=200)
    mobile_number= models.CharField(max_length=200, null=True)
    profile_image = models.ImageField(upload_to= 'instructor_profile_imgs/', null=True)
    password = models.CharField(max_length=100, blank=True, null=True)
    login_time = models.DateTimeField(auto_now_add=True)
    logout_time = models.DateTimeField(auto_now_add=True)
    verify_status = models.BooleanField(default=False)
    otp_digit = models.CharField(max_length=10, null=True)
    login_via_otp = models.BooleanField(default=False)

    # def __str__(self):
    #     return self.full_name; 

    class Meta:
        verbose_name_plural = "1. Instructors"

    def total_courses(self):
        totalCourses = Course.objects.filter(instructor = self).count()
        return totalCourses
    
    def total_students(self):
        totalStudents = StudentCourseEnrollment.objects.filter(course__instructor = self).count()
        return totalStudents
    
    def total_modules(self):
        totalModules = Module.objects.filter(course__instructor = self).count()
        return totalModules


#Student model
class Student(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    username = models.CharField(max_length=100, null=True)
    password = models.CharField(max_length=100)
    interested_categories = models.TextField()
    profile_image = models.ImageField(upload_to= 'student_profile_imgs/', null=True)
    mobile_number = models.IntegerField(null=True, default=1234567890)
    address = models.TextField(null=True, default='Bloomington')
    login_time = models.DateTimeField(auto_now_add=True)
    logout_time = models.DateTimeField(auto_now_add=True)
    verify_status = models.BooleanField(default=False)
    otp_digit = models.CharField(max_length=10, null=True)
    login_via_otp = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name;  

    class Meta:
        verbose_name_plural = "4. Students"
    
    def total_courses(self):
        totalCourses = StudentCourseEnrollment.objects.filter(student = self).count()
        return totalCourses



#Course Category Model
class CourseCategory(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        verbose_name_plural = "2. Course Categories"

    def __str__(self) -> str:
        return self.title;                  #returning just the title from course category

#Course model
class Course(models.Model):
    category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name='instructor_courses')
    title = models.CharField(max_length=100)
    description = models.TextField()
    course_image = models.ImageField(upload_to= 'course_imgs/', null=True)
    technologies = models.TextField(null=True)

    class Meta:
        verbose_name_plural = "3. Courses"

    def total_enrolled_students(self):
        total_enrolled_students = StudentCourseEnrollment.objects.filter(course = self).count()
        return total_enrolled_students

    def __str__(self):
        return self.title;  
 
#Module model
class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="course_modules")
    title = models.CharField(max_length=100)
    description = models.TextField()
    video = models.FileField(upload_to= 'module_videos/', null=True)
    remarks = models.TextField(null=True)

    class Meta:
        verbose_name_plural = "5. Modules" 

#Student Course Enrollment
class StudentCourseEnrollment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrolled_courses')
    student= models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrolled_student')
    enrolled_time = models.DateTimeField(auto_now_add=True) 

    class Meta:
        verbose_name_plural = "6. Enrolled Courses"

    def __str__(self):
        return f"{self.course}-{self.student}" 


# Messages
class InstructorStudentChat(models.Model):
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    msg_text = models.TextField()
    msg_from = models.CharField(max_length=100)
    msg_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "7. Instructor Student Messages"

class Assignments(models.Model):
    course=models.ForeignKey(Course, on_delete=models.CASCADE, related_name="course_assignments")
    instructor=models.ForeignKey(Instructor, on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    description=models.TextField(null=True)
    creation_time=models.DateTimeField(auto_now_add=True)
    deadline=models.DateTimeField()
    assignment_file=models.FileField(upload_to ='assignments/', null=True)
    
    class Meta:
        verbose_name_plural = "8. Assignments" 

class AssignmentResponse(models.Model):
    assignment=models.ForeignKey(Assignments, on_delete=models.CASCADE, related_name="assignmentSubmissions")
    course=models.ForeignKey(Course, on_delete=models.CASCADE)
    student=models.ForeignKey(Student, on_delete=models.CASCADE)
    reponse_text=models.TextField(null=True, default='Submission Done')
    submission_file=models.FileField(upload_to ='responses/', null=True)
    submission_time=models.DateTimeField(auto_now_add=True)
    grade=models.FloatField(default=0)
    
    class Meta:
        verbose_name_plural = "9. Assignment Responses"