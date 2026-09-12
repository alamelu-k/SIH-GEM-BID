from dataclasses import dataclass, field

from config.thresholds import MIN_FIELD_EXTRACTION_ACCURACY
from common.file_io import save_evaluation_report
from common.logging_config import get_logger

logger = get_logger(__name__)


@dataclass
class FieldAccuracyResult:
    field_name: str
    correct: int
    total: int

    @property
    def accuracy(self) -> float:
        return self.correct / self.total if self.total else 0.0


@dataclass
class ExtractionEvaluationReport:
    per_field: list[FieldAccuracyResult] = field(default_factory=list)
    overall_accuracy: float = 0.0
    meets_target: bool = False
    mismatches: list[dict] = field(default_factory=list)


def _values_match(predicted: str | None, expected: str) -> bool:
    
    if predicted is None:
        return False
    return predicted.strip().upper() == expected.strip().upper()


def evaluate_extraction(
    predictions: dict[str, dict[str, str | None]],
    ground_truth: dict[str, dict[str, str]],
) -> ExtractionEvaluationReport:
    
    field_totals: dict[str, FieldAccuracyResult] = {}
    mismatches: list[dict] = []
    total_correct = 0
    total_fields = 0

    for doc_id, expected_fields in ground_truth.items():
        predicted_fields = predictions.get(doc_id, {})

        for field_name, expected_value in expected_fields.items():
            predicted_value = predicted_fields.get(field_name)
            is_correct = _values_match(predicted_value, expected_value)

            if field_name not in field_totals:
                field_totals[field_name] = FieldAccuracyResult(field_name, correct=0, total=0)
            field_totals[field_name].total += 1
            total_fields += 1

            if is_correct:
                field_totals[field_name].correct += 1
                total_correct += 1
            else:
                mismatches.append(
                    {
                        "document_id": doc_id,
                        "field_name": field_name,
                        "expected": expected_value,
                        "predicted": predicted_value,
                    }
                )

    overall_accuracy = total_correct / total_fields if total_fields else 0.0

    report = ExtractionEvaluationReport(
        per_field=list(field_totals.values()),
        overall_accuracy=overall_accuracy,
        meets_target=overall_accuracy >= MIN_FIELD_EXTRACTION_ACCURACY,
        mismatches=mismatches,
    )

    logger.info(
        "Extraction accuracy: %.1f%% (target: %.1f%%) — %s",
        overall_accuracy * 100,
        MIN_FIELD_EXTRACTION_ACCURACY * 100,
        "PASS" if report.meets_target else "BELOW TARGET",
    )

    return report


def save_report(report: ExtractionEvaluationReport, path: str) -> None:
    save_evaluation_report(
        {
            "overall_accuracy": report.overall_accuracy,
            "meets_target": report.meets_target,
            "target_accuracy": MIN_FIELD_EXTRACTION_ACCURACY,
            "per_field": [
                {"field_name": r.field_name, "accuracy": r.accuracy, "correct": r.correct, "total": r.total}
                for r in report.per_field
            ],
            "mismatches": report.mismatches,
        },
        path,
    )
