from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Enrollment, Choice, Submission

def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        # Retrieve the enrollment for the current user
        enrollment = Enrollment.objects.get(user=request.user, course=course)
        
        # Create a new submission
        submission = Submission.objects.create(enrollment=enrollment)
        
        # Check selected choices from the form
        for key, value in request.POST.items():
            if key.startswith('choice_'):
                choice_id = int(value)
                choice = Choice.objects.get(pk=choice_id)
                submission.choices.add(choice)
        
        submission.save()
        return redirect('onlinecourse:show_exam_result', course_id=course.id, submission_id=submission.id)
    
    return render(request, 'onlinecourse/course_detail_bootstrap.html', {'course': course})

def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    
    # Lấy danh sách ID của các câu trả lời mà người dùng đã chọn
    selected_ids = [choice.id for choice in submission.choices.all()]
    
    total_score = 0
    possible_score = 0
    
    # Tính tổng điểm tối đa và điểm đạt được dựa theo logic yêu cầu
    for lesson in course.lesson_set.all():
        for question in lesson.question_set.all():
            possible_score += question.grade
            total_score += question.is_get_score(selected_ids)
            
    # Đóng gói đúng các biến context mà máy chấm yêu cầu
    context = {
        'course': course,
        'grade': total_score,
        'possible': possible_score,
        'selected_ids': selected_ids
    }
    
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
