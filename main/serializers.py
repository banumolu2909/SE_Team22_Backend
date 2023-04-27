from rest_framework import serializers
from django.core.mail import send_mail
from . import models
from django.contrib.flatpages.models import FlatPage

class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Instructor
        fields = ['id','full_name', 'bio', 'email', 'qualification', 'mobile_number','login_via_otp','profile_image', 'password','otp_digit','instructor_courses']
        depth = 1 
        # def __init__(self,*args, **kwargs): 
        #     super(InstructorSerializer, self).__init__(*args, **kwargs)
        #     request = self.context.get('request')
        #     self.Meta.depth = 0
        #     if request and request.method == 'GET':
        #         self.Meta.depth = 1

    def create(self,validate_data):
        email = self.validated_data['email']
        otp_digit = self.validated_data['otp_digit']
        instance = super(InstructorSerializer,self).create(validate_data)
        send_mail(
                'Verify Account',
                'Please verify your account',
                'srichandanach09@gmail.com',
                [email],
                fail_silently = False,
                html_message = f'<p>Your one-time-password is <p>{otp_digit}<p/><p/>'
            )
        return instance

class InstructorDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Instructor
        fields = ['total_courses', 'total_students', 'total_modules']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CourseCategory
        fields = ['id','title','description']

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields = ['id','category','instructor','title','description', 'course_image', 'technologies','course_modules', 'total_enrolled_students', 'course_assignments']
        depth = 1 #to retrieve the next level relationship

    def __init__(self, *args, **kwargs):
        super(CourseSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')

        if request and request.method=='POST':
            self.Meta.depth = 0
        else:
            self.Meta.depth = 2
    
class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Module
        fields = ['id','course','title','description','video','remarks']

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Student
        fields = ['id','full_name', 'email', 'username', 'password','login_via_otp', 'interested_categories','profile_image', 'otp_digit']

    def create(self,validate_data):
        email = self.validated_data['email']
        otp_digit = self.validated_data['otp_digit']
        instance = super(StudentSerializer,self).create(validate_data)
        send_mail(
                'Verify Account',
                'Please verify your account',
                'srichandanach09@gmail.com',
                [email],
                fail_silently = False,
                html_message = f'<p>Your one-time-password is <p> {otp_digit} <p/><p/>'
            )
        return instance
    
class StudentDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Student
        fields = ['total_courses']

class StudentCourseEnrollSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StudentCourseEnrollment
        fields = ['id','course','student','enrolled_time']
        depth = 1

    def __init__(self, *args, **kwargs):
        super(StudentCourseEnrollSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')

        if request and request.method=='POST':
            self.Meta.depth = 0
        else:
            self.Meta.depth = 2


class FlatPagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlatPage
        fields = ['id','title','content','url']

class InstructorStudentChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.InstructorStudentChat
        fields = ['id','instructor','student','msg_from','msg_text','msg_time']

class AssignmentSerializer(serializers.ModelSerializer):
    # deadline = 
    # deadline = datetime.strptime(my_date, "%d-%b-%Y-%H:%M:%S")
    class Meta:
        model = models.Assignments
        fields = ['id', 'course', 'instructor', 'title', 'description', 'deadline', 'assignment_file', 'assignmentSubmissions']
        depth=1
    
    def __init__(self, *args, **kwargs):
        super(AssignmentSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')

        if request and request.method=='POST':
            self.Meta.depth = 0
        else:
            self.Meta.depth = 2

class AssignmentResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AssignmentResponse
        fields = ['id', 'assignment', 'course', 'student', 'reponse_text', 'submission_file', 'submission_time', 'grade']
        depth=1

    def __init__(self, *args, **kwargs):
        super(AssignmentResponseSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')

        if request and request.method=='POST':
            self.Meta.depth = 0
        else:
            self.Meta.depth = 2
    