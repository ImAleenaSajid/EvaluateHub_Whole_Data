import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

@csrf_exempt
@require_http_methods(["POST"])
def receive_essay(request):
    if request.content_type != 'application/json':
        return JsonResponse({'error': 'Invalid content type'}, status=415)

    try:
        data = json.loads(request.body.decode('utf-8'))
        essay_text = data.get('essay', '').strip()
        test_type = data.get('test_type', '').strip().upper()  # "IELTS", "SAT", "GRE"

        print("Received:", data)  # Debug

        if not essay_text:
            return JsonResponse({'error': 'No essay received'}, status=400)
        if test_type not in ['IELTS', 'SAT', 'GRE']:
            return JsonResponse({'error': 'Invalid or missing test type. Use IELTS, SAT, or GRE.'}, status=400)

        # Prompt templates
        if test_type == 'IELTS':
            system_prompt = (
                f"You are an IELTS examiner grading Task 2. Prompt:\n\n"
                f"{data.get('prompt', '').strip()}\n\n"
                "Check topic relevance strictly. Follow:\n"
                "1) Score out of 9 on:\n"
                "- Task Response\n"
                "- Coherence and Cohesion\n"
                "- Lexical Resource\n"
                "- Grammar\n"
                "2) Average for Overall Band (1 decimal).\n"
                "3) Give brief feedback.\n"
                "4) Suggest 3 improvements.\n\n"
                "**Total output under 100 words. No score repetition.**\n\n"
                "Format:\n"
                "Task Response: <score>\n"
                "Coherence and Cohesion: <score>\n"
                "Lexical Resource: <score>\n"
                "Grammar: <score>\n"
                "Overall Band Score: <score>\n\n"
                "Feedback:\n<paragraph>\n\n"
                "Suggestions for Improvement:\n<3 bullets>\n\n"
            )

        elif test_type == 'SAT':
            system_prompt = (
                f"You are an SAT essay scorer. Prompt:\n\n"
                f"{data.get('prompt', '').strip()}\n\n"
                "Evaluate strictly. Follow:\n"
                "1) Score out of 8 on:\n"
                "- Thesis\n"
                "- Support\n"
                "- Organization\n"
                "- Evidence\n"
                "- Language Use\n"
                "2) Average for Total (1 decimal).\n"
                "3) Give concise feedback.\n"
                "4) Suggest 3 improvements.\n\n"
                "**Limit total output to 100 words. Avoid repetition.**\n\n"
                "Format:\n"
                "Thesis: <score>\n"
                "Support: <score>\n"
                "Organization: <score>\n"
                "Evidence: <score>\n"
                "Language Use: <score>\n"
                "Total Score: <score>\n\n"
                "Feedback:\n<paragraph>\n\n"
                "Suggestions for Improvement:\n<3 bullets>\n\n"
            )

        elif test_type == 'GRE':
            system_prompt = (
                f"You are grading 2 GRE essays: Issue and Argument. Prompts:\n\n"
                f"{data.get('prompt', '').strip()}\n\n"
                "Evaluate both combined. I want only one evaluation for both essays out of 6. Follow:\n"
                "1) Score out of 6 on:\n"
                "- Clarity\n"
                "- Logic\n"
                "- Development\n"
                "- Grammar\n"
                "2) Average each essay, then average both out of 6 not 12(1 decimal).\n"
                "3) Give brief combined feedback.\n"
                "4) Suggest 3 improvements.\n\n"
                "**Output must be ≤100 words. No repeating.**\n\n"
                "Format:\n"
                "Clarity: <score>\n"
                "Logic: <score>\n"
                "Development: <score>\n"
                "Grammar: <score>\n"
                "Total Score: <score>\n\n"
                "Feedback:\n<paragraph>\n\n"
                "Suggestions for Improvement:\n<3 bullets>\n\n"
            )

        # Prepare request to llama2 via Ollama
        payload = {
            "model": "llama2",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": essay_text}
            ],
            "stream": False
        }

        response = requests.post("http://localhost:11434/api/chat", json=payload)

        if response.status_code != 200:
            return JsonResponse({'error': 'Failed to get response from llama2', 'details': response.text}, status=502)

        result = response.json()
        reply = result.get("message", {}).get("content", "").strip()

        return JsonResponse({'evaluation': reply}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def generate_prompt(request):
    test_type = request.GET.get('test_type', '').strip().upper()

    if test_type not in ['IELTS', 'SAT', 'GRE-ISSUE', 'GRE-ARGUMENT']:
        return JsonResponse({'error': 'Invalid or missing test type. Use IELTS, SAT, GRE-ISSUE, or GRE-ARGUMENT.'}, status=400)

    try:
        # GRE handling
        if test_type == 'GRE-ISSUE':
            prompt_text = (
                "You are an expert GRE exam writer. Give one GRE Issue Task Essay prompt only. "
                "No other text please. No other text, instructions, headings (question, prompt) please. "
                "Don't even say 'Sure! Here's a Task 2 essay writing prompt:'. "
            )
        elif test_type == 'GRE-ARGUMENT':
            prompt_text = (
                "You are an expert GRE exam writer. Give one GRE Argument Essay Task prompt only. "
                "No other text please. No other text, instructions, headings (question, prompt) please. "
                "Don't even say 'Sure! Here's a Task 2 essay writing prompt:'. "
            )
        else:
            # IELTS or SAT
            prompt_texts = {
                'IELTS': (
                    "You are an expert IELTS exam writer. Give one Task 2 essay (writing part) prompt only. "
                    "No other text, instructions, headings (question, prompt) please. "
                    "Don't even say 'Sure! Here's a Task 2 essay writing prompt:'"
                ),
                'SAT': (
                    "You are an expert SAT exam writer. Give one SAT essay (Writing part) prompt only. "
                    "No other text please. No other text, instructions, headings (question, prompt) please. "
                    "Don't even say 'Sure! Here's a Task 2 essay writing prompt:'"
                )
            }
            prompt_text = prompt_texts[test_type]

        # Make request to LLaMA2
        payload = {
            "model": "llama2",
            "messages": [{"role": "system", "content": prompt_text}],
            "stream": False
        }

        response = requests.post("http://localhost:11434/api/chat", json=payload)

        if response.status_code != 200:
            return JsonResponse({'error': 'Failed to get prompt from LLaMA2', 'details': response.text}, status=502)

        result = response.json()
        prompt = result.get("message", {}).get("content", "").strip()

        return JsonResponse({'prompt': prompt}, status=200)

    except Exception as e:
        return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)
