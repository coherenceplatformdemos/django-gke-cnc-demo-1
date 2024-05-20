from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .tasks import queue, count_words_at_url

def home(request):
    return HttpResponse("Hello, world. You're at the counter index.")

@csrf_exempt
def count(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            url = data.get("url")
            if url:
                queue.enqueue(count_words_at_url, url)
                return JsonResponse({"status": "success", "message": f"URL {url} has been queued for word counting."})
            else:
                return JsonResponse({"status": "error", "message": "URL not provided in the request body."}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON body."}, status=400)
    else:
        return JsonResponse({"status": "error", "message": "Only POST requests are allowed."}, status=405)