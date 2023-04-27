from django.urls import path
from . import views

urlpatterns = [
    path('instructor/', views.InstructorList.as_view()),
    path('instructor/dashboard/<int:pk>/', views.InstructorDashboard.as_view()),
    path('instructor/<int:pk>/', views.InstructorDetail.as_view()),
    path('instructor/change-password/<int:instructor_id>/', views.instructor_change_password),
    path('instructor-login', views.instructor_login),
    path('verify-instructor/<int:instructor_id>/', views.verify_instructor_via_otp),
    path('instructor-forgot-password/', views.instructor_forgot_password),
    path('instructor-reset-password/<int:instructor_id>/', views.instructor_reset_password),

    path('category/', views.CategoryList.as_view()),

    path('course/', views.CourseList.as_view()),

    path('course/<int:pk>/', views.CourseDetailView.as_view()),

    path('module/', views.ModuleList.as_view()),

    #all modules for a specified course
     path('course-modules/<int:course_id>', views.CourseModuleList.as_view()),

    #For a specified instructor
    path('instructor-courses/<int:instructor_id>', views.InstructorCourseList.as_view()),

    #Specific course as taught by instructor
    path('instructor-course-detail/<int:pk>', views.InstructorCourseDetail.as_view()), 

    #For a specified module
    path('module/<int:pk>', views.ModuleDetailView.as_view()),

    path('search-courses/<str:searchstring>', views.CourseList.as_view()),

   

    #Pages
    path('pages/', views.FlatPagesList.as_view()),
    path('pages/<int:pk>/<str:page_slug>/', views.FlatPagesDetail.as_view()),

    #Student
    path('student/',views.StudentList.as_view()),
    path('user/dashboard/<int:pk>/', views.StudentDashboard.as_view()),
    path('user-login',views.student_login),
    path('student/<int:pk>/', views.StudentDetail.as_view()),
    path('student-enroll-course/',views.StudentEnrollCourseList.as_view()),
    path('verify-student/<int:student_id>/', views.verify_student_via_otp),
    path('fetch-enroll-status/<int:student_id>/<int:course_id>',views.fetch_enroll_status),
    path('student-forgot-password/', views.student_forgot_password),
    path('student-reset-password/<int:student_id>/', views.student_reset_password),

    path('fetch-enrolled-students/<int:course_id>',views.EnrolledStudentList.as_view()),
    path('fetch-enrolled-courses/<int:student_id>',views.EnrolledStudentList.as_view()),
    path('fetch-all-enrolled-students/<int:instructor_id>',views.EnrolledStudentList.as_view()),
    
    #Send Message-Instructor
    path('send-message/<int:instructor_id>/<int:student_id>',views.save_instructor_student_msg),

    #Send Announcement-Instructor
    path('send-group-message/<int:instructor_id>',views.save_instructor_group_message),

    #Get Messages-Instructor
    path('get-messages/<int:instructor_id>/<int:student_id>',views.InstructorStudentMessageList.as_view()),

    #Fetch all instructors whose a student is enrolled in
    path('fetch-my-instructors/<int:student_id>',views.MyInstructorList.as_view()),

    # Assignments
    path('assignment/', views.AssignmentList.as_view()),
    path('assignment/<int:pk>', views.AssignmentDetail.as_view()),
    
    # path('student-course-assignment/<int:course_id>', views.view_instructor_course_assignments),
    path('view-course-assignment/<int:instructor_id>/<int:course_id>', views.view_instructor_course_assignments),
    path('assignmentResponse/', views.AssignmentResponseList.as_view()),
    path('assignmentResponse/<int:pk>/', views.AssignmentResponseDetail.as_view()),
]