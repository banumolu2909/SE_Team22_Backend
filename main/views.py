from django.utils import timezone
from django.shortcuts import render
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt            #to submit form in django
from django.contrib.flatpages.models import FlatPage
from django.http import JsonResponse,HttpResponse
from rest_framework.pagination import PageNumberPagination

from .serializers import InstructorSerializer, CategorySerializer, CourseSerializer, ModuleSerializer,StudentSerializer,FlatPagesSerializer, StudentCourseEnrollSerializer, InstructorDashboardSerializer, InstructorStudentChatSerializer, AssignmentResponseSerializer,AssignmentSerializer, StudentDashboardSerializer
from . import models
from rest_framework.response import Response
from django.db.models import Q
from rest_framework import generics
from rest_framework import permissions
from django.core.mail import send_mail
from datetime import datetime as dt
from random import randint

# class StandardResultsSetPagination(PageNumberPagination):
#     page_size = 4
#     page_size_query_param = 'page_size'
#     max_page_size = 4

#To get a list of instructors
class InstructorList(generics.ListCreateAPIView):
    queryset = models.Instructor.objects.all()
    serializer_class = InstructorSerializer
    #permission_classes = [permissions.IsAuthenticated]

#To view,update or delete a particular instructor
class InstructorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Instructor.objects.all()
    serializer_class = InstructorSerializer
    #permission_classes = [permissions.IsAuthenticated]

#To view,update or delete a particular instructor
class InstructorDashboard(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Instructor.objects.all()
    serializer_class = InstructorDashboardSerializer

#To get a list of students
class StudentList(generics.ListCreateAPIView):
    queryset = models.Student.objects.all()
    serializer_class = StudentSerializer
    #permission_classes = [permissions.IsAuthenticated]

class StudentDashboard(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Student.objects.all()
    serializer_class = StudentDashboardSerializer


#To view,update or delete a particular studenr
class StudentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Student.objects.all()
    serializer_class = StudentSerializer
    #permission_classes = [permissions.IsAuthenticated]

@csrf_exempt
def instructor_login(request):
    email = request.POST['email']
    password = request.POST['password']
    try:
        instructorData = models.Instructor.objects.get(email=email, password=password)
        instructorData.login_time = timezone.now()
        instructorData.save(update_fields=['login_time'])
    except models.Instructor.DoesNotExist:
        instructorData = None
    if instructorData:
        if not instructorData.verify_status:
            return JsonResponse({'bool': False, 'msg':'Your account must be verified to log in'}) 
        else:
            if instructorData.login_via_otp: 
            #Send OTP via email
                otp_digit = randint(100000, 999999)
                send_mail(
                    'Verify Account',
                    'Please verify your account',
                    'srichandanach09@gmail.com',
                    [instructorData.email],
                    fail_silently = False,
                    html_message = f'<p>Your one-time-password is <p>{otp_digit}<p/><p/>'
                )
                instructorData.otp_digit = otp_digit
                instructorData.save()
                return JsonResponse({'bool': True, 'instructor_id': instructorData.id,'login_via_otp': True})
            else:
               return JsonResponse({'bool': True, 'instructor_id': instructorData.id,'login_via_otp': False})         
    else:
        return JsonResponse({'bool': False, 'msg':'Invalid Email id or Password'})
    
@csrf_exempt
def verify_instructor_via_otp(request, instructor_id):
    otp_digit = request.POST.get('otp_digit')
    verify = models.Instructor.objects.filter(id = instructor_id, otp_digit = otp_digit).first()
    if verify:
        models.Instructor.objects.filter(id = instructor_id, otp_digit = otp_digit).update(verify_status = True)
        return JsonResponse({'bool': True, 'instructor_id': verify.id})
    else:
        return JsonResponse({'bool': False, 'msg': "Please enter valid 6-digit OTP"})

@csrf_exempt
def student_login(request):
    email = request.POST['email']
    password = request.POST['password']
    try:
        studentData = models.Student.objects.get(email=email, password=password)
        studentData.login_time = timezone.now()
        studentData.save(update_fields=['login_time'])
    except models.Student.DoesNotExist:
        studentData = None
    if studentData:
        if not studentData.verify_status:
            return JsonResponse({'bool': False, 'msg':'Your account must be verified to log in'}) 
        else:
            if studentData.login_via_otp: 
            #Send OTP via email
                otp_digit = randint(100000, 999999)
                send_mail(
                    'Verify Account',
                    'Please verify your account',
                    'srichandanach09@gmail.com',
                    [studentData.email],
                    fail_silently = False,
                    html_message = f'<p>Your one-time-password is <p>{otp_digit}<p/><p/>'
                )
                studentData.otp_digit = otp_digit
                studentData.save()
                return JsonResponse({'bool': True, 'student_id': studentData.id,'login_via_otp': True})
            else:
               return JsonResponse({'bool': True, 'student_id': studentData.id,'login_via_otp': False})         
    else:
        return JsonResponse({'bool': False, 'msg':'Invalid Email id or Password'})
    
@csrf_exempt
def verify_student_via_otp(request, student_id):
    otp_digit = request.POST.get('otp_digit')
    verify = models.Student.objects.filter(id = student_id, otp_digit = otp_digit).first()
    if verify:
        models.Student.objects.filter(id = student_id, otp_digit = otp_digit).update(verify_status = True)
        return JsonResponse({'bool': True, 'student_id': verify.id})
    else:
        return JsonResponse({'bool': False})

class CategoryList(generics.ListCreateAPIView):
    queryset = models.CourseCategory.objects.all()
    serializer_class = CategorySerializer



#This returns all the courses present
class CourseList(generics.ListCreateAPIView):
    queryset = models.Course.objects.all()
    serializer_class = CourseSerializer
    # pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        qs = super().get_queryset()
        if 'res' in self.request.GET:
            limit = int(self.request.GET['res'])
            qs = models.Course.objects.all().order_by('-id')[:limit]
        if 'searchstring' in self.kwargs:
            search = self.kwargs['searchstring']
            qs = models.Course.objects.filter(Q(technologies__icontains=search) | Q(title__icontains=search))
        return qs

class CourseDetailView(generics.RetrieveAPIView):
    queryset =  models.Course.objects.all()
    serializer_class = CourseSerializer

#This class is to generate courses for corresponding instructor
class InstructorCourseList(generics.ListAPIView):
    serializer_class = CourseSerializer

    #override queryset
       # To retrieve the instructor ID from the URL, fetch the corresponding Instructor object, and return all the 
        #courses associated with that instructor. 
    def get_queryset(self):                                  
        instructor_id = self.kwargs['instructor_id']
        instructor = models.Instructor.objects.get(pk = instructor_id)
        return models.Course.objects.filter(instructor=instructor)
    
class InstructorCourseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Course.objects.all()
    serializer_class = CourseSerializer

    
class ModuleList(generics.ListCreateAPIView):
    queryset = models.Module.objects.all()
    serializer_class = ModuleSerializer


#This class is to generate all modules for a specific course
class CourseModuleList(generics.ListAPIView):
    serializer_class = ModuleSerializer

    #override queryset
       # To retrieve the course ID from the URL, fetch the corresponding course object, and return all the 
        #chapter associated with that course. 
    def get_queryset(self):                                  
        course_id = self.kwargs['course_id']
        course = models.Course.objects.get(pk = course_id)
        return models.Module.objects.filter(course=course)

class MyInstructorList(generics.ListAPIView):
    queryset = models.Course.objects.all()
    serializer_class = CourseSerializer

    def get_queryset(self):    
        if 'student_id' in self.kwargs:
            student_id = self.kwargs['student_id']
            sql = f"SELECT * FROM main_course as c, main_studentcourseenrollment as e, main_instructor as i WHERE c.instructor_id = i.id AND e.course_id = c.id AND e.student_id = {student_id} GROUP BY c.instructor_id"
            qs = models.Course.objects.raw(sql)
            print(qs)
            return qs



class ModuleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Module.objects.all()
    serializer_class = ModuleSerializer


class FlatPagesList(generics.ListAPIView):
    queryset = FlatPage.objects.all()
    serializer_class = FlatPagesSerializer

class FlatPagesDetail(generics.RetrieveAPIView):
    queryset = FlatPage.objects.all()
    serializer_class = FlatPagesSerializer

class StudentEnrollCourseList(generics.ListCreateAPIView):
    queryset = models.StudentCourseEnrollment.objects.all()
    serializer_class = StudentCourseEnrollSerializer

def fetch_enroll_status(request, student_id, course_id):
    student = models.Student.objects.get(id= student_id)
    course = models.Course.objects.get(id= course_id)
    print(student, course)
    enrollStatus = models.StudentCourseEnrollment.objects.filter(course = course, student = student).first()
   
    if enrollStatus:
        return JsonResponse({'bool': True}) 
    else:
        return JsonResponse({'bool': False})
    
class EnrolledStudentList(generics.ListAPIView):
    queryset = models.StudentCourseEnrollment.objects.all()
    serializer_class = StudentCourseEnrollSerializer

    def get_queryset(self):   
        if 'course_id' in self.kwargs:
            course_id = self.kwargs['course_id']
            course = models.Course.objects.get(pk = course_id)
            return models.StudentCourseEnrollment.objects.filter(course=course)
        elif 'instructor_id' in self.kwargs:
            instructor_id = self.kwargs['instructor_id']
            instructor = models.Instructor.objects.get(pk = instructor_id)
            return models.StudentCourseEnrollment.objects.filter(course__instructor= instructor).distinct()
        elif 'student_id' in self.kwargs:
            student_id = self.kwargs['student_id']
            student = models.Student.objects.get(pk = student_id)
            return models.StudentCourseEnrollment.objects.filter(student = student).distinct() 

        

@csrf_exempt
def instructor_change_password(request, instructor_id):
    password = request.POST['password']
    try:
        instructorData = models.Instructor.objects.get(id=instructor_id)
    except models.Instructor.DoesNotExist:
        instructorData = None
    if instructorData:
        instructorData = models.Instructor.objects.filter(id=instructor_id).update(password = password)
        return JsonResponse({'bool': True}) 
    else:
        return JsonResponse({'bool': False})

@csrf_exempt
def instructor_forgot_password(request):
    email = request.POST.get('email')
    verify = models.Instructor.objects.filter(email = email).first()
    if verify:
        link = f"http://localhost:3000/instructor-reset-password/{verify.id}"
        send_mail(
                    'Verify Account',
                    'Please verify your account',
                    'srichandanach09@gmail.com',
                    [email],
                    fail_silently = False,
                    html_message = f"<p>Your one-time-password is <p> {link} <p/><p/>"
                )
        return JsonResponse({'bool': True, 'msg': 'Please check your inbox to reset the password.'})
    else:
        return JsonResponse({'bool': False, 'msg': 'Invalid email address'})

@csrf_exempt
def instructor_reset_password(request, instructor_id):
    password = request.POST.get('password')
    verify = models.Instructor.objects.filter(id = instructor_id).first()
    if verify:
        models.Instructor.objects.filter(id = instructor_id).update(password = password)
        return JsonResponse({'bool': True, 'msg': 'Your password has been reset.'})
    else:
        return JsonResponse({'bool': False, 'msg': 'Oops! Error occurred! Please try after some time.'})

@csrf_exempt
def student_forgot_password(request):
    email = request.POST.get('email')
    verify = models.Student.objects.filter(email = email).first()
    if verify:
        link = f"http://localhost:3000/student-reset-password/{verify.id}"
        send_mail(
                    'Verify Account',
                    'Please verify your account',
                    'srichandanach09@gmail.com',
                    [email],
                    fail_silently = False,
                    html_message = f"<p>Your one-time-password is <p> {link} <p/><p/>"
                )
        return JsonResponse({'bool': True, 'msg': 'Please check your inbox to reset the password.'})
    else:
        return JsonResponse({'bool': False, 'msg': 'Invalid email address'})

@csrf_exempt
def student_reset_password(request, student_id):
    password = request.POST.get('password')
    verify = models.Student.objects.filter(id = student_id).first()
    if verify:
        models.Student.objects.filter(id = student_id).update(password = password)
        return JsonResponse({'bool': True, 'msg': 'Your password has been reset.'})
    else:
        return JsonResponse({'bool': False, 'msg': 'Oops! Error occurred! Please try after some time.'})
    


@csrf_exempt
def save_instructor_student_msg(request, instructor_id, student_id):
    instructor = models.Instructor.objects.get(id = instructor_id)
    student = models.Student.objects.get(id = student_id)
    msg_text = request.POST.get('msg_text')
    msg_from = request.POST.get('msg_from')
    msgRes = models.InstructorStudentChat.objects.create(
        instructor = instructor,
        student = student,
        msg_text = msg_text,
        msg_from = msg_from,
    )
    if msgRes:
        return JsonResponse({'bool': True, 'msg': 'The message has been sent.'})
    else:
        return JsonResponse({'bool': False, 'msg': 'Oops! Error occurred! Please try after some time.'})
    

class InstructorStudentMessageList(generics.ListAPIView):
    queryset = models.InstructorStudentChat.objects.all()
    serializer_class = InstructorStudentChatSerializer

    def get_queryset(self):                                  
        instructor_id = self.kwargs['instructor_id']
        student_id = self.kwargs['student_id']
        instructor = models.Instructor.objects.get(pk = instructor_id)
        student = models.Student.objects.get(pk = student_id)
        return models.InstructorStudentChat.objects.filter(instructor=instructor, student = student).exclude(msg_text = ' ')
    

@csrf_exempt
def save_instructor_group_message(request, instructor_id):
    instructor = models.Instructor.objects.get(id = instructor_id)
    msg_text = request.POST.get('msg_text')
    msg_from = request.POST.get('msg_from')

    enrolledList = models.StudentCourseEnrollment.objects.filter(course__instructor= instructor).distinct()
    for enrolled in enrolledList:
        msgRes = models.InstructorStudentChat.objects.create(
            instructor = instructor,
            student = enrolled.student,
            msg_text = msg_text,
            msg_from = msg_from,
        )
    if msgRes:
        return JsonResponse({'bool': True, 'msg': 'Message has been send.'})
    else:
        return JsonResponse({'bool': False, 'msg': 'Oops! Error occurred! Please try after some time.'})
    

class AssignmentList(generics.ListCreateAPIView):
    queryset = models.Assignments.objects.all()
    serializer_class = AssignmentSerializer

        
class AssignmentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Assignments.objects.all()
    serializer_class = AssignmentSerializer

class AssignmentResponseList(generics.ListCreateAPIView):
    queryset = models.AssignmentResponse.objects.all()
    serializer_class = AssignmentResponseSerializer

class AssignmentResponseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.AssignmentResponse.objects.all()
    serializer_class = AssignmentResponseSerializer

def view_instructor_course_assignments(request, instructor_id, course_id):
    instructor=models.Instructor.objects.get(id=instructor_id)
    course=models.Course.objects.get(id=course_id)
    assignment=models.Assignments.objects.filter(course=course, instructor=instructor)
    
    # print(assignment)
    response = []
    for a in assignment:
        obj = {}
        obj['id'] = a.id
        obj["title"] = a.title
        obj["creation_time"] = a.creation_time.strftime("%m/%d/%Y, %H:%M:%S")
        obj["deadline"] = a.deadline.strftime("%m/%d/%Y, %H:%M:%S")
        response.append(obj)
    
    return JsonResponse({'response': response}) 

    
    
