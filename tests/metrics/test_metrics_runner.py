import json
import os
from pathlib import Path
from driftmonitor.scripts.metrics.run_metrics import compute_drift_and_write

def test_compute_drift_and_write(tmp_path):
    # Prepare a fake processed dir with two eval files
    processed_dir = tmp_path / "processed"
    os.makedirs(processed_dir, exist_ok=True)

    eval_a = {
        "evaluated_at": "20250101T000000Z",
        "n_texts": 2,
        "safety_results": [
            {"text": "This is safe and positive."},
            {"text": "Helpful model output."}
        ]
    }
    eval_b = {
        "evaluated_at": "20250108T000000Z",
        "n_texts": 2,
        "safety_results": [
            {"text": "This contains a dangerous suggestion: kill it."},
            {"text": "Harmful and toxic content."}
        ]
    }

    a_path = processed_dir / "eval_a.json"
    b_path = processed_dir / "eval_b.json"
    a_path.write_text(json.dumps(eval_a))
    b_path.write_text(json.dumps(eval_b))

    # Run compute_drift_and_write specifying the exact files
    out_file = compute_drift_and_write(processed_dir=str(processed_dir), output_dir=str(processed_dir),
                                       eval_a_path=str(a_path), eval_b_path=str(b_path))
    assert os.path.exists(out_file)
    data = json.loads(Path(out_file).read_text())
    assert "drift" in data
    assert "toxicity_a" in data
    assert "toxicity_b" in data
    # sanity checks
    assert isinstance(data["drift"].get("jsd"), float)
    assert data["toxicity_b"]["n_texts"] == 2
