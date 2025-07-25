# Open Genes AI Benchmark (GooseBench)

## Overview
Open Genes AI Benchmark is a framework for benchmarking and evaluating AI models on scientific data extraction tasks from research articles. It supports multiple AI models, automated benchmarking, customizable tasks, detailed scoring, and visualization of results.

## Features
- Supports OpenAI and Gemini models for scientific data extraction
- Automated benchmarking pipeline for reproducible evaluation
- Customizable tasks and assessments
- Comprehensive scoring and evaluation metrics:
  - Factual accuracy
  - Completeness
  - Precision
  - Hallucination rate
  - Plausible error rate
  - Format compliance
  - Numerical accuracy
  - Uncertainty handling
- Visualization scripts for performance metrics
- Utilities for document conversion (DOC/DOCX to PDF)

## Project Structure
- `biobench/` — Core benchmarking logic, models, tasks, assessments, and scripts
- `biobench/scripts/` — Utility scripts (charts, document conversion)
- `biobench/models/` — Model wrappers for OpenAI and Gemini
- `biobench/tasks/`, `biobench/assessments/`, `biobench/scorers/` — Task and scoring logic
- `data/` — Data and supplementary files
- `docs/` — Documentation

## Installation
1. **Python version:** Python 3.12+
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Configuration
Set the following environment variables as needed:

### Model and API
- `BASE_URL` — Base URL for OpenAI-compatible API (OpenAI model)
- `API_KEY` — API key for OpenAI-compatible API
- `GEMINI_API_KEY` — API key for Gemini model
- `MAX_TOKENS` — Maximum number of tokens in response (default: 75)
- `TEMPERATURE` — Model creativity from 0.0 to 1.0 (default: 0.5)

### Database (operational)
- `DATABASE_URL` — PostgreSQL connection

### Database (generation)
- `MYSQL_HOST` — MySQL host
- `MYSQL_USER` — MySQL user
- `MYSQL_PASSWORD` — MySQL password
- `MYSQL_DATABASE` — MySQL database name
  
These are used for task generation in `biobench/task_generator/generator.py` 

### Script-specific
- `soffice` (LibreOffice) — For document conversion, ensure `soffice` is in your PATH or specify its path in the script argument.

## Usage

### Benchmarking with OpenAI-compatible models
```bash
python -m biobench.pipeline
```

### Benchmarking with Gemini
```bash
python -m biobench.pipeline_gemini
```

Add your own pipeline for other modeltypes.

### Generating Charts
```bash
python biobench/scripts/charts.py
```
- Outputs performance heatmaps to `biobench/charts_output/`

### Converting Documents to PDF
```bash
python biobench/scripts/convert_docs_to_pdf.py
```
- Converts all `.doc`/`.docx` files in `data/supp/` to PDF using LibreOffice (`soffice`).

## Scoring Metrics
- **precision**: Correct facts in extraction
- **completeness**: Coverage of key information
- **hallucination_rate**: Fabricated information rate
- **plausible_error_rate**: Realistic but incorrect information rate
- **format_compliance**: Output format correctness
- **numerical_accuracy**: Correctness of numerical values
- **uncertainty_handling**: Proper handling of missing/uncertain data

## Contributing
Contributions are welcome! Please open issues or pull requests for improvements, bug fixes, or new features.
