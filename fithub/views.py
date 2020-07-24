import json
from channels.http import AsgiRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core import serializers
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from .models import UserDetail, StudentHistory, Course, CourseStudents, Post


@csrf_exempt
def signup(request: AsgiRequest):
    if request.method == 'POST':
        body = json.loads(request.body)
        username = body['username']
        email = body['email']
        password = body['password']
        phone = body['phone']
        license_number = body['license_number']
        user = User.objects.create_user(username, email, password)
        detail = UserDetail(user=user, phone=phone,
                            license_number=license_number, balance=0)
        detail.save()
        return JsonResponse({"status": "ok", "user_id": user.pk, "license_number": license_number}, status=HTTP_200_OK)
    return JsonResponse({"status": "error"}, status=HTTP_400_BAD_REQUEST)


@csrf_exempt
def login(request: AsgiRequest):
    if request.method == 'POST':
        body = json.loads(request.body)
        username = body['username']
        password = body['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            detail = UserDetail.objects.get(user=user)
            return JsonResponse({"status": "ok", "user_id": user.pk, "license_number": detail.license_number}, status=HTTP_200_OK)
    return JsonResponse({"status": "error"}, status=HTTP_400_BAD_REQUEST)


@csrf_exempt
def insert_history(request: AsgiRequest):
    if request.method == 'POST':
        body = json.loads(request.body)
        user_id = body['user_id']
        history_type = body['history_type']
        details = body['details']
        value = body['value']
        user = User.objects.get(pk=user_id)
        student_history = StudentHistory(
            user=user, history_type=history_type, details=details, value=value)
        student_history.save()
        return JsonResponse({"status": "ok", "student_history": student_history.pk}, status=HTTP_200_OK)
    return JsonResponse({"status": "error"}, status=HTTP_400_BAD_REQUEST)


@csrf_exempt
def get_history(request: AsgiRequest):
    if request.method == 'POST':
        body = json.loads(request.body)
        user_id = body['user_id']
        histories = StudentHistory.objects.filter(user=user_id)
        histories_json = json.loads(serializers.serialize('json', histories))
        return JsonResponse({"status": "ok", "histories": histories_json}, status=HTTP_200_OK)
    return JsonResponse({"status": "error"}, status=HTTP_400_BAD_REQUEST)


@csrf_exempt
def add_course(request: AsgiRequest):
    if request.method == 'POST':
        body = json.loads(request.body)
        user_id = body['user_id']
        name = body['name']
        price = body['price']
        user = User.objects.get(pk=user_id)
        if UserDetail.objects.get(user=user).license_number is not None:
            course = Course(
                creator=user, name=name, price=price)
            course.save()
            return JsonResponse({"status": "ok", "course_id": course.pk}, status=HTTP_200_OK)
    return JsonResponse({"status": "error"}, status=HTTP_400_BAD_REQUEST)


@csrf_exempt
def enroll_course(request: AsgiRequest):
    if request.method == 'POST':
        body = json.loads(request.body)
        user_id = body['user_id']
        course_id = body['course_id']
        user = User.objects.get(pk=user_id)
        course = Course.objects.get(pk=course_id)
        course_student = CourseStudents(course=course, user=user)
        course_student.save()
        return JsonResponse({"status": "ok", "course_student_id": course_student.pk}, status=HTTP_200_OK)
    return JsonResponse({"status": "error"}, status=HTTP_400_BAD_REQUEST)


@csrf_exempt
def left_course(request: AsgiRequest):
    if request.method == 'POST':
        body = json.loads(request.body)
        course_student_id = body['course_student_id']
        course_student = CourseStudents.objects.get(pk=course_student_id)
        course_student.delete()
        return JsonResponse({"status": "ok"}, status=HTTP_200_OK)
    return JsonResponse({"status": "error"}, status=HTTP_400_BAD_REQUEST)


@csrf_exempt
def add_post(request: AsgiRequest):
    if request.method == 'POST':
        body = json.loads(request.body)
        course_id = body['course_id']
        text = body['text']
        order = body['order']
        course = Course.objects.get(pk=course_id)
        post = Post(course=course, text=text, order=order)
        post.save()
        return JsonResponse({"status": "ok", "post_id": post.pk}, status=HTTP_200_OK)
    return JsonResponse({"status": "error"}, status=HTTP_400_BAD_REQUEST)


@csrf_exempt
def edit_post(request: AsgiRequest):
    if request.method == 'POST':
        body = json.loads(request.body)
        post_id = body['post_id']
        text = body['text']
        order = body['order']
        post = Post.objects.get(pk=post_id)
        post.text = text
        post.order = order
        post.save()
        return JsonResponse({"status": "ok", "post_id": post.pk}, status=HTTP_200_OK)
    return JsonResponse({"status": "error"}, status=HTTP_400_BAD_REQUEST)


@csrf_exempt
def delete_post(request: AsgiRequest):
    if request.method == 'POST':
        body = json.loads(request.body)
        post_id = body['post_id']
        post = Post.objects.get(pk=post_id)
        post.delete()
        return JsonResponse({"status": "ok"}, status=HTTP_200_OK)
    return JsonResponse({"status": "error"}, status=HTTP_400_BAD_REQUEST)


@csrf_exempt
def get_course_posts(request: AsgiRequest):
    if request.method == 'POST':
        body = json.loads(request.body)
        course_id = body['course_id']
        posts = Post.objects.filter(course_id=course_id)
        posts_json = json.loads(serializers.serialize('json', posts))
        return JsonResponse({"status": "ok", "posts": posts_json}, status=HTTP_200_OK)
    return JsonResponse({"status": "error"}, status=HTTP_400_BAD_REQUEST)


@csrf_exempt
def get_courses(request: AsgiRequest):
    if request.method == 'POST':
        courses = Course.objects.all()
        courses_json = json.loads(serializers.serialize('json', courses))
        return JsonResponse({"status": "ok", "courses": courses_json}, status=HTTP_200_OK)
    return JsonResponse({"status": "error"}, status=HTTP_400_BAD_REQUEST)


@csrf_exempt
def get_my_courses(request: AsgiRequest):
    if request.method == 'POST':
        body = json.loads(request.body)
        user_id = body['user_id']
        my_courses = CourseStudents.objects.filter(user=user_id)
        my_courses_json = json.loads(serializers.serialize('json', my_courses))
        return JsonResponse({"status": "ok", "courses": my_courses_json}, status=HTTP_200_OK)
    return JsonResponse({"status": "error"}, status=HTTP_400_BAD_REQUEST)
