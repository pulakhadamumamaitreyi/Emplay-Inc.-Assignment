import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Prompt
from django.conf import settings

redis_client = settings.REDIS_CLIENT


def prompt_list(request):
    if request.method == 'GET':
        prompts = list(Prompt.objects.values())
        return JsonResponse(prompts, safe=False)

    elif request.method == 'POST':
        data = json.loads(request.body)

        prompt = Prompt.objects.create(
            title=data['title'],
            content=data['content'],
            complexity=data['complexity']
        )

        return JsonResponse({
            "id": str(prompt.id),
            "message": "Created successfully"
        })


def prompt_detail(request, id):
    try:
        prompt = Prompt.objects.get(id=id)

        # Redis view count
        key = f"prompt:{id}:views"
        redis_client.incr(key)
        view_count = redis_client.get(key).decode()

        return JsonResponse({
            "id": str(prompt.id),
            "title": prompt.title,
            "content": prompt.content,
            "complexity": prompt.complexity,
            "created_at": prompt.created_at,
            "view_count": view_count
        })

    except Prompt.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)
