import sys
import json
from biobench.db.db import main_pool
from psycopg2.extras import RealDictCursor

import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict


assessment_id = '01983bd9-e505-7f40-94e1-cc136494a57f'
fields = [
    "precision",
    "completeness",
    "factual_accuracy",
    "format_compliance",
    "hallucination_rate",
    "numerical_accuracy",
    "plausible_error_rate",
    "uncertainty_handling",
]

with main_pool.getconn() as conn:
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            """
            SELECT result FROM complete_tasks WHERE assessment_id = %s
            """,
            (assessment_id,)
        )
        rows = cur.fetchall()

results = [row["result"] for row in rows]

agg = {}
for field in fields:
    values = [r.get(field) for r in results if r.get(field) is not None]
    if values:
        agg[field] = sum(values) / len(values)
    else:
        agg[field] = None

print(json.dumps(agg, indent=2, ensure_ascii=False))

# Преобразуем результаты в матрицу: строки — задачи, столбцы — метрики
matrix = []
for r in results:
    row = [r.get(field) for field in fields]
    matrix.append(row)

matrix = np.array(matrix, dtype=np.float32)

if matrix.size > 0:
    plt.figure(figsize=(10, max(4, len(matrix) * 0.5)))
    im = plt.imshow(matrix, aspect='auto', cmap='viridis', interpolation='nearest')
    plt.colorbar(im, label='Score')
    plt.xticks(np.arange(len(fields)), fields, rotation=45, ha='right')
    plt.yticks(np.arange(len(matrix)), [f'Task {i+1}' for i in range(len(matrix))])
    # Подписи значений
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            val = matrix[i, j]
            if not np.isnan(val):
                plt.text(j, i, f'{val:.2f}', ha='center', va='center', color='w', fontsize=8)
    plt.title('Heatmap of Task Results')
    plt.tight_layout()
    plt.show()
else:
    print('Нет данных для построения heatmap')

# --- Хитмап по средним значениям (agg) ---
agg_matrix = np.array([[agg[field] if agg[field] is not None else np.nan for field in fields]], dtype=np.float32)

plt.figure(figsize=(10, 2))
im = plt.imshow(agg_matrix, aspect='auto', cmap='viridis', interpolation='nearest')
plt.colorbar(im, label='Average Score')
plt.xticks(np.arange(len(fields)), fields, rotation=45, ha='right')
plt.yticks([0], ['average'])
# Подписи значений
for j in range(agg_matrix.shape[1]):
    val = agg_matrix[0, j]
    if not np.isnan(val):
        plt.text(j, 0, f'{val:.2f}', ha='center', va='center', color='w', fontsize=10)
plt.title('Average Metrics Heatmap')
plt.tight_layout()
plt.show()

# --- Сравнение моделей по всем ассессментам (группировка по model) ---

# Сгруппируем все assessment_id по model
with main_pool.getconn() as conn:
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT id, model FROM assessments")
        assessments = cur.fetchall()

model_to_assessments = defaultdict(list)
for ass in assessments:
    model_to_assessments[ass['model']].append(ass['id'])

model_names = sorted(model_to_assessments.keys())
agg_rows = []
for model in model_names:
    all_results = []
    for ass_id in model_to_assessments[model]:
        with main_pool.getconn() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT result FROM complete_tasks WHERE assessment_id = %s", (ass_id,))
                rows = cur.fetchall()
        results = [json.loads(row["result"]) if isinstance(row["result"], str) else row["result"] for row in rows]
        all_results.extend(results)
    agg = []
    for field in fields:
        values = [r.get(field) for r in all_results if r.get(field) is not None]
        agg.append(sum(values) / len(values) if values else np.nan)
    agg_rows.append(agg)

if agg_rows:
    agg_matrix = np.array(agg_rows, dtype=np.float32)
    n_models = len(model_names)
    # Высота: минимум 3, максимум 1.5*число моделей, чтобы полосы были толстыми
    fig_height = max(3, min(1.5 * n_models, 10))
    plt.figure(figsize=(1.5*len(fields), fig_height))
    im = plt.imshow(agg_matrix, aspect='equal', cmap='RdYlGn', interpolation='nearest')
    plt.colorbar(im, label='Average Score', shrink=0.8, pad=0.02)
    plt.xticks(np.arange(len(fields)), fields, rotation=35, ha='right', fontsize=12)
    plt.yticks(np.arange(n_models), model_names, fontsize=13)
    plt.xlabel('Metric', fontsize=14)
    plt.ylabel('Model', fontsize=14)
    # Подписи значений и белая рамка
    for i in range(agg_matrix.shape[0]):
        for j in range(agg_matrix.shape[1]):
            val = agg_matrix[i, j]
            if not np.isnan(val):
                plt.text(j, i, f'{val:.2f}', ha='center', va='center', color='black', fontsize=13, fontweight='bold', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.18', alpha=0.92))
    plt.title('Model Comparison Heatmap', fontsize=16, pad=18)
    plt.tight_layout(rect=[0, 0, 1, 0.97])
    plt.show()
else:
    print('Нет данных для построения heatmap по моделям')

    # Для этих полей инвертируем значения (1-value)
    # УБРАНО: инверсия для hallucination_rate и plausible_error_rate
    im = plt.imshow(agg_matrix, aspect='equal', cmap='RdYlGn', interpolation='nearest')
    plt.colorbar(im, label='Average Score', shrink=0.8, pad=0.02)
    plt.xticks(np.arange(len(fields)), fields, rotation=35, ha='right', fontsize=12)
    plt.yticks(np.arange(n_models), model_names, fontsize=13)
    plt.xlabel('Metric', fontsize=14)
    plt.ylabel('Model', fontsize=14)
    # Подписи значений и белая рамка
    for i in range(agg_matrix.shape[0]):
        for j in range(agg_matrix.shape[1]):
            # Для подписей тоже инвертируем, если нужно
            orig_val = agg_matrix[i, j]
            if fields[j] in invert_fields:
                val = 1 - orig_val
            else:
                val = orig_val
            if not np.isnan(val):
                plt.text(j, i, f'{val:.2f}', ha='center', va='center', color='black', fontsize=13, fontweight='bold', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.18', alpha=0.92))
    plt.title('Model Comparison Heatmap', fontsize=16, pad=18)
    plt.tight_layout(rect=[0, 0, 1, 0.97])
    plt.show()
