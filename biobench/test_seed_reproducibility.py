from biobench.ai_model import AIModel
from biobench.models.gemini_model import GeminiModel
from biobench.models.open_ai_model import OpenAIModel
import difflib

# llama-3.3-70b-instruct failed with temperature=0.1 top_p=0.9 seed=42 1024 tokens
# failed max_tokens=128, temperature=0.1, top_p=0.9, seed=42
# going to use temp 0

def test_seed_reproducibility(model: AIModel, runs=5):
    prompt = "Explain quantum computing in simple terms."
    results = []

    for i in range(runs):
        res = model.query(prompt, [])
        results.append(res)
        print(f"Run {i + 1}: {res}")

    # Проверка идентичности
    unique_results = set(results)
    reproducible = len(unique_results) == 1

    print(f"\n{model.name} reproducibility: {'✅' if reproducible else '❌'}")
    print(f"Unique results: {len(unique_results)}/{runs}")

    if len(unique_results) > 1:
        print("\nDifferences between unique results:")
        unique_results_list = list(unique_results)
        for i in range(len(unique_results_list)):
            for j in range(i + 1, len(unique_results_list)):
                a = unique_results_list[i].splitlines(keepends=True)
                b = unique_results_list[j].splitlines(keepends=True)
                diff = difflib.unified_diff(a, b, fromfile=f'Result {i+1}', tofile=f'Result {j+1}', lineterm='')
                print(f"\n--- Diff between result {i+1} and {j+1} ---")
                print(''.join(diff) or '[No line-level differences]')

    return reproducible, results

# test_seed_reproducibility(OpenAIModel())
test_seed_reproducibility(GeminiModel())