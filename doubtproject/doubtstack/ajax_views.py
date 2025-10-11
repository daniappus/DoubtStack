from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Doubt

def fetch_replies(request, doubt_id):
    student_id = request.session.get('student_id')
    if not student_id:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    doubt = get_object_or_404(Doubt, pk=doubt_id)
    replies = doubt.replies.select_related('student', 'teacher').all()

    reply_data = []
    for r in replies:
        reply_data.append({
            'id': r.reply_id,
            'sender': 'Anonymous' if r.anonymous else (
                r.student.stu_name if r.student else r.teacher.teacher_name
            ),
            'text': r.reply_text,
            'file_url': r.file_url.url if r.file_url else None,
            'timestamp': r.created_at.strftime("%Y-%m-%d %H:%M"),
            'is_self': (r.student and r.student.pk == student_id)
        })

    return JsonResponse({'replies': reply_data})
