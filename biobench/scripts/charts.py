import sys
import json
from biobench.db.db import main_pool
from psycopg2.extras import RealDictCursor

import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
import os

# Set professional style
plt.style.use('default')
plt.rcParams.update({
    'font.size': 12,
    'font.family': 'DejaVu Sans',
    'axes.titlesize': 16,
    'axes.labelsize': 14,
    'xtick.labelsize': 11,
    'ytick.labelsize': 11,
    'legend.fontsize': 12,
    'figure.titlesize': 18,
    'axes.grid': False,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.spines.bottom': False,
    'axes.spines.left': False,
    'axes.edgecolor': '#333333',
    'axes.linewidth': 0,
    'xtick.color': '#333333',
    'ytick.color': '#333333',
    'xtick.bottom': False,
    'ytick.left': False
})

# Создаем папку для сохранения графиков
output_dir = 'charts_output'
os.makedirs(output_dir, exist_ok=True)

assessment_id = '01983bd9-e505-7f40-94e1-cc136494a57f'
fields = [
    "precision",
    "completeness",
    "format_compliance",
    "hallucination_rate",
    "numerical_accuracy",
    "plausible_error_rate",
    "uncertainty_handling",
]

# Поля, для которых нужно инвертировать значения (меньше = лучше)
invert_fields = {"hallucination_rate", "plausible_error_rate"}

with main_pool.getconn() as conn:
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            """
            SELECT ct.result, t.body 
            FROM complete_tasks ct
            JOIN tasks t ON ct.task_id = t.id
            WHERE ct.assessment_id = %s
            """,
            (assessment_id,)
        )
        rows = cur.fetchall()

results = []
for row in rows:
    result = row["result"]
    body = row["body"] if isinstance(row["body"], dict) else json.loads(row["body"])

    # Добавляем информацию о типах в результат
    result_with_types = result.copy() if isinstance(result, dict) else json.loads(result) if isinstance(result,
                                                                                                        str) else result
    result_with_types['task_type'] = body.get('content', {}).get('type', 'Unknown')
    result_with_types['cognitive_type'] = body.get('cognitiveType', 'Unknown')

    results.append(result_with_types)

agg = {}
for field in fields:
    values = [r.get(field) for r in results if r.get(field) is not None]
    if values:
        agg[field] = sum(values) / len(values)
    else:
        agg[field] = None

print(json.dumps(agg, indent=2, ensure_ascii=False))

# --- Хитмап по средним значениям (agg) ---
agg_matrix = np.array([[agg[field] if agg[field] is not None else np.nan for field in fields]], dtype=np.float32)

# Инвертируем значения для соответствующих полей
agg_matrix_display = agg_matrix.copy()
for j, field in enumerate(fields):
    if field in invert_fields and not np.isnan(agg_matrix_display[0, j]):
        agg_matrix_display[0, j] = 1 - agg_matrix_display[0, j]

plt.figure(figsize=(14, 3))

# Возвращаемся к прежним цветам, но делаем их более чувствительными
from matplotlib.colors import LinearSegmentedColormap

sensitive_cmap = LinearSegmentedColormap.from_list('sensitive',
                                                   ['#ff7f7f', '#ffbf7f', '#ffff7f', '#bfff7f', '#7fff7f'], N=256)

im = plt.imshow(agg_matrix_display, aspect='auto', cmap=sensitive_cmap, interpolation='nearest', vmin=0.2, vmax=0.8)

# Добавляем более крупную шкалу без подписей
cbar = plt.colorbar(im, shrink=0.8, pad=0.02, aspect=15)
cbar.set_ticks([])  # Убираем все подписи

# Форматируем названия полей для лучшей читаемости
field_labels = []
for field in fields:
    if field in invert_fields:
        # Для инвертированных полей добавляем "1 - " в начало
        label = f"1 - {field.replace('_', ' ').title()}"
    else:
        label = field.replace('_', ' ').title()
    field_labels.append(label)
plt.xticks(np.arange(len(fields)), field_labels, rotation=25, ha='right', fontsize=13, fontweight='500')
plt.yticks([0], ['Average'], fontsize=14, fontweight='500')

# Подписи значений без прямоугольников
for j in range(agg_matrix.shape[1]):
    original_val = agg_matrix[0, j]
    if not np.isnan(original_val):
        # Всегда используем черный цвет для лучшей читаемости
        plt.text(j, 0, f'{original_val:.3f}', ha='center', va='center',
                 color='black', fontsize=13, fontweight='600')

plt.title('Assessment Performance Metrics', fontsize=18, pad=20, fontweight='600')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'average_metrics_heatmap.png'), dpi=300, bbox_inches='tight', transparent=True)
plt.close()
print(f'График сохранен: {output_dir}/average_metrics_heatmap.png')

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
original_agg_rows = []  # Для хранения оригинальных значений

for model in model_names:
    all_results = []
    for ass_id in model_to_assessments[model]:
        with main_pool.getconn() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """
                    SELECT ct.result, t.body 
                    FROM complete_tasks ct
                    JOIN tasks t ON ct.task_id = t.id
                    WHERE ct.assessment_id = %s
                    """,
                    (ass_id,)
                )
                rows = cur.fetchall()

        task_results = []
        for row in rows:
            result = row["result"]
            if isinstance(result, str):
                result = json.loads(result)
            task_results.append(result)

        all_results.extend(task_results)

    agg = []
    original_agg = []
    for field in fields:
        values = [r.get(field) for r in all_results if r.get(field) is not None]
        if values:
            avg_val = sum(values) / len(values)
            original_agg.append(avg_val)
            # Инвертируем для отображения, если нужно
            if field in invert_fields:
                agg.append(1 - avg_val)
            else:
                agg.append(avg_val)
        else:
            agg.append(np.nan)
            original_agg.append(np.nan)

    agg_rows.append(agg)
    original_agg_rows.append(original_agg)

if agg_rows:
    agg_matrix = np.array(agg_rows, dtype=np.float32)
    original_agg_matrix = np.array(original_agg_rows, dtype=np.float32)
    n_models = len(model_names)

    # Профессиональные размеры
    fig_width = min(16, max(12, 1.8 * len(fields)))
    fig_height = min(12, max(6, 0.8 * n_models))

    plt.figure(figsize=(fig_width, fig_height))

    # Возвращаемся к прежним цветам, но делаем их более чувствительными
    from matplotlib.colors import LinearSegmentedColormap

    sensitive_cmap = LinearSegmentedColormap.from_list('sensitive',
                                                       ['#ff7f7f', '#ffbf7f', '#ffff7f', '#bfff7f', '#7fff7f'], N=256)

    im = plt.imshow(agg_matrix, aspect='auto', cmap=sensitive_cmap, interpolation='nearest', vmin=0.1, vmax=0.8)

    # Добавляем более крупную шкалу без подписей
    cbar = plt.colorbar(im, shrink=0.9, pad=0.02, aspect=15)
    cbar.set_ticks([])  # Убираем все подписи

    # Форматируем названия полей для лучшей читаемости
    field_labels = []
    for field in fields:
        if field in invert_fields:
            # Для инвертированных полей добавляем "1 - " в начало
            label = f"1 - {field.replace('_', ' ').title()}"
        else:
            label = field.replace('_', ' ').title()
        field_labels.append(label)
    plt.xticks(np.arange(len(fields)), field_labels, rotation=30, ha='right', fontsize=13, fontweight='500')
    plt.yticks(np.arange(n_models), model_names, fontsize=13, fontweight='500')

    # Убираем подписи осей

    # Подписи значений без прямоугольников
    for i in range(agg_matrix.shape[0]):
        for j in range(agg_matrix.shape[1]):
            original_val = original_agg_matrix[i, j]
            if not np.isnan(original_val):
                # Всегда используем черный цвет для лучшей читаемости
                plt.text(j, i, f'{original_val:.3f}', ha='center', va='center',
                         color='black', fontsize=12, fontweight='600')

    plt.title('Model Performance Comparison', fontsize=18, pad=25, fontweight='600')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'model_comparison_heatmap.png'), dpi=300, bbox_inches='tight',
                transparent=True)
    plt.close()
    print(f'График сохранен: {output_dir}/model_comparison_heatmap.png')
else:
    print('Нет данных для построения heatmap по моделям')

print(f'\nВсе графики сохранены в папку: {output_dir}/')

# --- Анализ распределения по типам задач ---

# Подсчет распределения по типам
type_counts = defaultdict(int)
cognitive_type_counts = defaultdict(int)
type_performance = defaultdict(list)
cognitive_type_performance = defaultdict(list)

for result in results:
    task_type = result.get('task_type', 'Unknown')
    cognitive_type = result.get('cognitive_type', 'Unknown')

    type_counts[task_type] += 1
    cognitive_type_counts[cognitive_type] += 1

    # Собираем производительность по типам (используем среднее по всем метрикам)
    metric_values = []
    for field in fields:
        if field in result and result[field] is not None:
            metric_values.append(result[field])

    if metric_values:
        avg_performance = sum(metric_values) / len(metric_values)
        type_performance[task_type].append(avg_performance)
        cognitive_type_performance[cognitive_type].append(avg_performance)

print(f"\nРаспределение по типам задач:")
print(json.dumps(dict(type_counts), indent=2, ensure_ascii=False))

print(f"\nРаспределение по когнитивным типам:")
print(json.dumps(dict(cognitive_type_counts), indent=2, ensure_ascii=False))

# --- График распределения по типам задач ---
if type_counts:
    plt.figure(figsize=(12, 6))

    types = list(type_counts.keys())
    counts = list(type_counts.values())

    # Используем цвет как у OpenEnded (мятно-зеленый)
    openended_color = '#7dd3c0'  # Мятно-зеленый цвет
    bars = plt.bar(types, counts, color=openended_color, alpha=0.85)

    # Добавляем значения на столбцы
    for bar, count in zip(bars, counts):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
                 str(count), ha='center', va='bottom', fontsize=11, fontweight='600')

    plt.title('Task Distribution by Type', fontsize=16, fontweight='600', pad=20)
    plt.xticks(rotation=45, ha='right', fontsize=12)
    plt.yticks(fontsize=11)
    plt.ylabel('Number of Tasks', fontsize=13, fontweight='500')

    # Убираем обводку
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    plt.gca().tick_params(bottom=False, left=False)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'task_type_distribution.png'), dpi=300, bbox_inches='tight', transparent=True)
    plt.close()
    print(f'График сохранен: {output_dir}/task_type_distribution.png')

# --- График распределения по когнитивным типам ---
if cognitive_type_counts:
    plt.figure(figsize=(10, 6))

    cognitive_types = list(cognitive_type_counts.keys())
    cognitive_counts = list(cognitive_type_counts.values())

    # Используем цвет как у ClaimVerification (оранжевый)
    claimverification_color = '#ff8c69'  # Оранжевый цвет как у ClaimVerification
    bars = plt.bar(cognitive_types, cognitive_counts, color=claimverification_color, alpha=0.85)

    # Добавляем значения на столбцы
    for bar, count in zip(bars, cognitive_counts):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
                 str(count), ha='center', va='bottom', fontsize=11, fontweight='600')

    plt.title('Task Distribution by Cognitive Type', fontsize=16, fontweight='600', pad=20)
    plt.xticks(rotation=45, ha='right', fontsize=12)
    plt.yticks(fontsize=11)
    plt.ylabel('Number of Tasks', fontsize=13, fontweight='500')

    # Убираем обводку
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    plt.gca().tick_params(bottom=False, left=False)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'cognitive_type_distribution.png'), dpi=300, bbox_inches='tight',
                transparent=True)
    plt.close()
    print(f'График сохранен: {output_dir}/cognitive_type_distribution.png')


# --- Хитмапы производительности по типам задач для каждой модели ---

def create_performance_heatmap_by_type(model_name, model_results, type_field, type_name, filename_suffix):
    """Создает хитмап производительности модели по типам задач"""

    # Группируем результаты по типам
    type_performance = defaultdict(list)
    for result in model_results:
        task_type = result.get(type_field, 'Unknown')
        type_performance[task_type].append(result)

    # Вычисляем средние значения по каждой метрике для каждого типа
    type_names = sorted(type_performance.keys())
    if not type_names:
        return

    type_matrix = []
    for task_type in type_names:
        type_results = type_performance[task_type]
        type_row = []
        for field in fields:
            values = [r.get(field) for r in type_results if r.get(field) is not None]
            if values:
                type_row.append(sum(values) / len(values))
            else:
                type_row.append(np.nan)
        type_matrix.append(type_row)

    type_matrix = np.array(type_matrix, dtype=np.float32)

    # Создаем матрицу для отображения с инверсией
    type_matrix_display = type_matrix.copy()
    for i in range(type_matrix_display.shape[0]):
        for j, field in enumerate(fields):
            if field in invert_fields and not np.isnan(type_matrix_display[i, j]):
                type_matrix_display[i, j] = 1 - type_matrix_display[i, j]

    # Создаем график
    fig_width = min(14, max(10, 1.5 * len(fields)))
    fig_height = min(10, max(4, 0.8 * len(type_names)))

    plt.figure(figsize=(fig_width, fig_height))

    im = plt.imshow(type_matrix_display, aspect='auto', cmap=sensitive_cmap,
                    interpolation='nearest', vmin=0.1, vmax=0.8)

    # Добавляем шкалу без подписей
    cbar = plt.colorbar(im, shrink=0.8, pad=0.02, aspect=15)
    cbar.set_ticks([])

    # Подписи
    field_labels = []
    for field in fields:
        if field in invert_fields:
            label = f"1 - {field.replace('_', ' ').title()}"
        else:
            label = field.replace('_', ' ').title()
        field_labels.append(label)

    plt.xticks(np.arange(len(fields)), field_labels, rotation=30, ha='right', fontsize=12, fontweight='500')
    plt.yticks(np.arange(len(type_names)), type_names, fontsize=12, fontweight='500')

    # Подписи значений
    for i in range(type_matrix.shape[0]):
        for j in range(type_matrix.shape[1]):
            original_val = type_matrix[i, j]
            if not np.isnan(original_val):
                plt.text(j, i, f'{original_val:.3f}', ha='center', va='center',
                         color='black', fontsize=11, fontweight='600')

    plt.title(f'{model_name} Performance by {type_name}', fontsize=16, fontweight='600', pad=20)
    plt.tight_layout()

    filename = f'{model_name.lower().replace("-", "_").replace(".", "_")}_{filename_suffix}.png'
    plt.savefig(os.path.join(output_dir, filename), dpi=300, bbox_inches='tight', transparent=True)
    plt.close()
    print(f'График сохранен: {output_dir}/{filename}')


# Создаем комбинированные хитмапы для каждой модели
# Сначала собираем все данные одним запросом
all_model_results = {}

with main_pool.getconn() as conn:
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        # Получаем все данные одним запросом для всех моделей
        assessment_ids = []
        for model in model_names:
            assessment_ids.extend(model_to_assessments[model])

        if assessment_ids:
            placeholders = ','.join(['%s'] * len(assessment_ids))
            cur.execute(
                f"""
                SELECT ct.result, t.body, a.model
                FROM complete_tasks ct
                JOIN tasks t ON ct.task_id = t.id
                JOIN assessments a ON ct.assessment_id = a.id
                WHERE ct.assessment_id IN ({placeholders})
                """,
                assessment_ids
            )
            all_rows = cur.fetchall()

            # Группируем по моделям
            for row in all_rows:
                model = row["model"]
                if model not in all_model_results:
                    all_model_results[model] = []

                result = row["result"]
                body = row["body"] if isinstance(row["body"], dict) else json.loads(row["body"])

                result_with_types = result.copy() if isinstance(result, dict) else json.loads(result) if isinstance(
                    result, str) else result
                result_with_types['task_type'] = body.get('content', {}).get('type', 'Unknown')
                result_with_types['cognitive_type'] = body.get('cognitiveType', 'Unknown')

                all_model_results[model].append(result_with_types)

# Теперь создаем отдельные хитмапы для каждой модели
for model in model_names:
    if model in all_model_results:
        # Создаем хитмапы по типам задач и когнитивным типам
        create_performance_heatmap_by_type(model, all_model_results[model], 'task_type', 'Task Type',
                                           'task_type_performance')
        create_performance_heatmap_by_type(model, all_model_results[model], 'cognitive_type', 'Cognitive Type',
                                           'cognitive_type_performance')