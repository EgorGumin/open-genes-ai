import json
from typing import Optional
import re

from biobench.ai_model import AIModel
from biobench.scorers.score_result import ScoreResult
from biobench.scorers.scorer import Scorer, ScoringModel
from biobench.tasks.task_body_dto import ScoringConfig


class AIScorer(Scorer):
    scoring_model: ScoringModel = "AI"

    def __init__(self, ai_model: AIModel):
        self.ai_model = ai_model

    def score(self, solution: str, reference: str, text: str, scoring: Optional[ScoringConfig] = None) -> ScoreResult:
        prompt = f"""
You are an expert evaluator for scientific paper data extraction. Evaluate the extracted information against the ground truth using the following metrics. Return ONLY a JSON object with numeric scores.

Count each discrete piece of information as one fact:
- "N=16.4" = 1 fact
- "Mean age 19.8 years" = 1 fact  
- "RCT design" = 1 fact

METRICS:

factual_accuracy: Compare extracted facts with ground truth. 
Calculation: (number of matching facts between extracted and ground truth) / (total facts in ground truth)
Range: 0-1

completeness: Check if all key information from ground truth was extracted.
Calculation: (number of ground truth key points found in extracted) / (total key points in ground truth)
Key points include: study design, sample size, duration, primary outcomes, statistical significance, effect sizes, main findings, limitations, conclusions
Range: 0-1

precision: Verify accuracy of extracted information.
Calculation: (number of correct facts in extracted) / (total facts in extracted)
Range: 0-1
Example calculation for precision:
Extracted: [A, B, C, D, E] (5 facts)
Correct: [A, C] (2 facts)  
Precision = 2/5 = 0.4

hallucination_rate: Identify fabricated information not present in source.
Calculation: (number of fabricated facts not in source) / (total facts in extracted)
Fabricated facts: information completely absent from source, impossible values (N=50,000 in small clinic study), non-existent statistical tests, made-up references
Range: 0-1

plausible_error_rate: Identify realistic-looking but incorrect information.
Calculation: (number of realistic-looking but incorrect facts) / (total facts in extracted)
Examples: numbers in reasonable range but wrong (N=1,200 vs actual N=1,247), correct terminology but wrong values (p<0.01 vs actual p<0.001), similar but incorrect study designs
Range: 0-1

uncertainty_indication: Check if model expresses uncertainty when information is unclear/missing.
Scoring: 1.0 if appropriately says "not specified/unclear/unknown" when info missing, 0.5 if partial, 0.0 if missing
- 1.0 if model indicates uncertainty AND (completeness < 1.0 OR numerical_accuracy < 1.0)
- 0.5 if partial uncertainty indication  
- 0.0 if no uncertainty indicated when needed
- null if completeness = 1.0 AND numerical_accuracy = 1.0 (perfect extraction)
should be null if extraction is nearly perfect (completeness >= 0.8 AND numerical_accuracy >= 0.8)
Appropriate uncertainty: "not specified" when info truly missing, "approximately" for unclear numbers, "unclear from text" when ambiguous

error_explanation: Evaluate if model explains why certain information couldn't be extracted.
Scoring: 1.0 if provides clear explanations why data unavailable, 0.5 if partial explanation, 0.0 if no explanation
- 1.0 if model explains missing data AND completeness < 0.8
- 0.5 if partial explanation
- 0.0 if no explanation when significant data missing
- null if completeness >= 0.8 (minor gaps don't need explanation)
should be null if extraction is nearly perfect (completeness >= 0.8 AND numerical_accuracy >= 0.8)

format_compliance: Check if output follows requested structure/format.
Scoring: 1.0 if follows requested format exactly, 0.5 if mostly follows, 0.0 if wrong format

numerical_accuracy: Compare numerical values (sample sizes, statistics, percentages).
Calculation: (number of correct numerical values) / (total numerical values in ground truth)
Return null if no numbers present in ground truth
Return 0 if answer not contains numbers, but they are present in ground truth
Range: 0-1 or null

summary: Provide a brief summary of the evaluation in maximum 3 sentences.


<task>{text}</task>
<ground_truth>{reference}</ground_truth>
<extracted_information>{solution}</extracted_information>

Return evaluation as JSON with scores for each metric:
    """
        print(f"{solution} \n\n {reference}")
        response = self.ai_model.query(prompt, [])

        print(f"DEBUG: response = {response}")

        # Use regex to extract the first JSON object from the response
        match = re.search(r'\{.*\}', response, re.DOTALL)
        if match:
            result = json.loads(match.group(0))
            print(result)
        else:
            raise ValueError('No valid JSON object found in model response')


        score = max(0.0, min(1.0, float(result.get('score', 0.0))))
        reason = result.get('reason', 'No reason provided')

        return ScoreResult(score=score, reason=reason)
