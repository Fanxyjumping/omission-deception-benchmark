# Omission-Based Deception Detection Benchmark

A Chinese benchmark-style dataset and task for studying **omission-based deception** in information dissemination, with a focus on LLM fine-tuning, prompting, and structured misinformation analysis.

## Motivation

Misleading information does not always rely on explicit fabrication. In many real-world scenarios, content becomes misleading by **omitting critical information**: background context, methodological constraints, comparison baselines, downstream consequences, responsible actors, or stakeholder perspectives.

Compared with conventional fake news detection, omission-based deception is more subtle. It requires models not only to understand **what is stated**, but also to reason about **what is missing** and whether such missing information is sufficient to distort the reader’s interpretation.

This repository aims to provide a structured benchmark for this problem.

## Task Definition

Given:

- `claim_text`: a propagated text snippet, short summary, or social-media-style retelling
- `context_text`: a more complete background description or factual clarification

The model is expected to:

1. Determine whether the propagated text constitutes omission-based deception
2. If yes, identify its primary omission type

### Input

```json
{
  "id": "test_0001",
  "claim_text": "A city reported 20,000 new unemployed people this month, suggesting a severe situation.",
  "context_text": "Public records show that the city had 31,000 new unemployed people last month and 28,000 in the same period last year; the current number has already declined compared with earlier stages."
}
```

### Output

```json
{
  "label": "omission-based deception",
  "omission_type": "comparative omission"
}
```

## Label Taxonomy

### Level-1 Label

- `normal`
- `omission-based deception`

### Level-2 Omission Type

For samples labeled as `omission-based deception`, the omission type belongs to one of the following categories:

- `background omission`
- `complexity omission`
- `comparative omission`
- `impact omission`
- `accountability omission`
- `stakeholder omission`

For samples labeled as `normal`, the omission type is:

- `none`

## Omission Categories

### 1. Background Omission
Critical background, timeline, prior context, or policy context is omitted, making the event hard to interpret correctly.

### 2. Complexity Omission
Important conditions, limitations, mechanisms, methods, or uncertainty are omitted, making a complex issue appear overly simple or definitive.

### 3. Comparative Omission
A number, trend, or magnitude is presented without an appropriate comparison baseline, such as historical levels, control groups, or horizontal comparison.

### 4. Impact Omission
Consequences, risks, affected scope, or downstream effects are omitted, preventing readers from assessing the significance of the event.

### 5. Accountability Omission
The responsible actor, decision-maker, executor, or accountability chain is omitted, obscuring who should be held responsible.

### 6. Stakeholder Omission
Affected groups, stakeholder positions, conflicts of interest, or multiple perspectives are omitted, leaving only a single viewpoint.

## Dataset

The current release is primarily a Chinese dataset in JSONL format, where each line is a single JSON object.

### Released Files

- `data/train.json`
  - labeled training data
- `data/test.json`
  - unlabeled test data
- `data/test_gold.json`
  - gold test labels for internal evaluation only
- `data/data.json`
  - the full dataset for archival use or further processing

### Scale

- Total: 4000
- Normal: 1000
- Omission-based deception: 3000
- Six omission categories: 500 samples each

## Evaluation Protocol

We recommend hierarchical evaluation.

### Level-1: Binary Classification
Evaluate `label` using:

- Accuracy
- Precision
- Recall
- F1

### Level-2: Omission Type Classification
Evaluate `omission_type` using:

- Accuracy
- Macro-F1

This second-level evaluation should be computed **only on samples whose true label is omission-based deception**.

## Why Hierarchical Evaluation?

This task naturally contains two levels of difficulty:

1. Detecting whether the text is misleading through omission
2. Distinguishing the kind of missing information that drives the misleading effect

A single aggregate score can hide the difference between these abilities. Hierarchical evaluation makes it easier to analyze whether a model fails at:

- omission detection
- fine-grained omission categorization
- or both

## Repository Structure

```text
.
├── README.md
├── README1.md
├── 文件说明.md
├── data
│   ├── train.json
│   ├── test.json
│   ├── test_gold.json
│   ├── data.json
│   ├── dataset_stats.json
│   ├── source_manifest.json
│   └── internal_splits
│       ├── train.jsonl
│       ├── validation.jsonl
│       └── test.jsonl
└── scripts
    └── build_omission_dataset.py
```

## Data Construction

The dataset design is inspired by the task formats, topical coverage, and field structures of multiple Hugging Face fact-checking and misinformation datasets, and reorganized into a unified Chinese benchmark-style task.

Reference sources include:

- `usr256864/averitec`
- `pszemraj/multi_fc`
- `ComplexDataLab/Misinfo_Datasets`
- `fever/fever`

A reproducible generation script is provided:

```bash
python3 scripts/build_omission_dataset.py
```

The script generates:

- `data/data.json`
- `data/dataset_stats.json`
- `data/source_manifest.json`
- `data/internal_splits/train.jsonl`
- `data/internal_splits/validation.jsonl`
- `data/internal_splits/test.jsonl`

## Suggested Baselines

This benchmark is suitable for multiple modeling setups, including:

- prompting with instruction-tuned LLMs
- supervised fine-tuning (SFT)
- LoRA / QLoRA
- encoder-based classification baselines
- joint two-stage or cascaded classifiers

A simple baseline can be constructed by:

1. Training on `train.json`
2. Holding out part of the training data for validation
3. Predicting `label` first, then `omission_type`

## Potential Use Cases

This benchmark can support:

- LLM fine-tuning research
- prompting and in-context learning
- misinformation analysis
- information completeness modeling
- teaching, coursework, and recruitment assignments

## Limitations

This benchmark has several limitations:

1. `context_text` is treated as the more complete reference context, which simplifies the problem compared with real-world fact verification.
2. Omission-based deception is inherently more subjective than standard fact verification.
3. Fine-grained omission categories may overlap in difficult edge cases.
4. The current release is primarily Chinese, which may limit direct cross-lingual comparison.

## Future Work

Potential directions for future extension include:

- multilingual versions
- stronger human-written rather than template-heavy examples
- explicit rationale annotations
- omission-intent analysis as an auxiliary task
- benchmark leaderboards and official baselines

## Disclaimer

This repository focuses on **misleadingness caused by omission of critical information** rather than generic fake news detection.  
The benchmark is intended for research, education, and model analysis purposes.

## Citation

If you use this benchmark in research, teaching, or applied projects, please cite the repository and acknowledge its use.

## Contact

Suggestions on dataset construction, taxonomy design, or evaluation protocol are welcome via issues or discussion.

## Related Work

The problem setting and omission-type design of this task were inspired by prior work on omission-based deception. This repository does not aim to strictly reproduce the original study; instead, it adapts the underlying idea into a structured Chinese benchmark-style task for LLM fine-tuning and omission analysis.

Reference:

- [arXiv:2512.01728](https://arxiv.org/abs/2512.01728)

