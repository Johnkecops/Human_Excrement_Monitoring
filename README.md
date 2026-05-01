# POE.LOG — Water Intake Applet Based on Human Excrement

**Authors:** Nadine Swastika, Winda Hasuki, Sava Savero, Putri Gabriella Satya, Arli Aditya Parikesit  
**Affiliation:** Department of Bioinformatics, Indonesia International Institute for Life Sciences (i3L), Jakarta  
**Reference:** Swastika N. et al. (2021). Water Intake Applet Based on Human Excrement. *Jurnal Riset Informatika*, 3(2), 109–118. https://www.researchgate.net/publication/349782022_WATER_INTAKE_APPLET_BASED_ON_HUMAN_EXCREMENT

---

## What this app does

People miss dehydration because they don't pay attention to urine color or stool consistency — two things the body makes visible every day. This app lets you log both and get feedback tied to clinical reference scales.

Urine color maps to four hydration levels, based on standard clinical color charts. Stool consistency follows the Bristol Stool Chart (Types 1–7). Every entry is timestamped and saved locally, so you can look back at patterns over time.

---

## Project structure

```
Human Excrement/
├── water_intake_logic.py   # Core logic: mappings, result dicts, history I/O
├── app.py                  # Streamlit frontend (7 pages)
├── requirements.txt        # Python dependencies
├── history.log             # Created automatically on first submission
└── README.md               # This file
```

---

## Requirements

- Python 3.9 or higher
- pip

---

## Installation

Download this folder, then install the one dependency:

```bash
pip install -r requirements.txt
```

Or directly:

```bash
pip install streamlit
```

---

## Running the core Python logic

`water_intake_logic.py` works without Streamlit. Import it directly for testing or to plug the logic into another script.

```python
from water_intake_logic import (
    get_urine_result,
    get_stool_result,
    append_to_history,
    read_history,
    clear_history,
)

# Urine color index 0–5 (0 = very pale, 5 = dark brown)
result = get_urine_result(4)
print(result["message"])   # → "You seem to be dehydrated."
print(result["advice"])    # → "Please drink more water!"

# Bristol stool type 1–7
result = get_stool_result(3)
print(result["message"])   # → "Your stool is normal."

# Log an entry
append_to_history("Pee", result["log_label"])

# Read history (newest first)
entries = read_history()
for entry in entries:
    print(entry)

# Clear log
clear_history()
```

### Urine color index reference

| Index | Color | Hydration status |
|-------|-------|-----------------|
| 0 | Very pale yellow | Hydrated |
| 1 | Pale yellow | Hydrated |
| 2 | Light yellow | Hydrated |
| 3 | Dark yellow | Acceptable — drink soon |
| 4 | Amber | Dehydrated |
| 5 | Dark brown | Severely dehydrated |

### Bristol stool type reference

| Type | Description | Result |
|------|-------------|--------|
| 1 | Separate hard lumps | Severe abnormality |
| 2 | Lumpy, sausage-like | Mild abnormality |
| 3 | Sausage with surface cracks | Normal |
| 4 | Smooth, soft sausage | Normal |
| 5 | Soft blobs with clear edges | Lack of fiber |
| 6 | Mushy, fluffy consistency | Mild abnormality |
| 7 | Liquid consistency | Severe abnormality |

---

## Running the Streamlit app

From the project directory:

```bash
streamlit run app.py
```

The browser opens automatically at `http://localhost:8501`. If it doesn't:

```bash
streamlit run app.py --server.port 8501
```

Then open `http://localhost:8501` manually.

### App pages

| Page | How to reach it | What it does |
|------|----------------|--------------|
| Menu | Opens on launch | Navigate to Pee Log, Poo Log, Settings, or History |
| Pee Log | Menu → Pee Log | Six color swatches; pick the one matching your urine |
| Pee Result | After color selection | Shows hydration status and advice; Submit saves to history |
| Poo Log | Menu → Poo Log | Seven Bristol stool types; pick the one that matches |
| Poo Result | After type selection | Shows stool assessment and advice; Submit saves to history |
| History | Menu → View History | Timestamped log of all submissions, newest first |
| Settings | Menu → Settings | Toggle notifications; set sleep hours to block alerts |

---

## History log format

Each submission appends one line to `history.log` in the project directory:

```
2026-05-01 09:14:32 - Pee = Hydrated
2026-05-01 09:14:55 - Stool = Normal
```

Plain text. Open it in any editor or process it with standard shell tools.

---

## Limitations

This is a screening tool, not a diagnostic device. It cannot replace a clinical assessment. If you keep seeing "Severely dehydrated" or "Severe abnormality" results, see a doctor. The Bristol Stool Chart is a general reference — it was not designed for self-diagnosis, and this app does not add any medical intelligence on top of it.

---

## Citation

If you use this application in research or teaching, cite the original paper:

> Swastika, N., Hasuki, W., Savero, S., Satya, P. G., & Parikesit, A. A. (2021). Water Intake Applet Based on Human Excrement. *Jurnal Riset Informatika*, 3(2), 109–118. https://www.researchgate.net/publication/349782022_WATER_INTAKE_APPLET_BASED_ON_HUMAN_EXCREMENT
