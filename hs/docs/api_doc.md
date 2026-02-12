Below is a **formal API contract documentation** for the HS module.
This is structured for:

* Frontend developers (Next.js + Clerk)
* Backend refactoring
* LLM service evolution
* Future versioning

All endpoints assume:

* Base path: `/api/v1/hs/`
* Auth: `Authorization: Bearer <Clerk JWT>`
* Content-Type: `application/json`

---

# HS MODULE – API DOCUMENTATION

---

# 1️⃣ POST `/api/v1/hs/predict/`

## Purpose

Predict the most likely HS code(s) for a free-text product description.

This endpoint:

* Uses embedding similarity
* Optionally uses LLM reasoning
* Validates codes against `itc_hs_master`
* Prevents hallucinated codes

---

## Request

```json
{
  "description": "Lithium ion battery pack for electric vehicles",
  "schedule_type": "import",
  "top_k": 5
}
```

### Fields

| Field         | Type    | Required | Description                    |
| ------------- | ------- | -------- | ------------------------------ |
| description   | string  | Yes      | Product description            |
| schedule_type | string  | Yes      | `import` or `export`           |
| top_k         | integer | No       | Number of results (default: 5) |

---

## Response

```json
{
  "predictions": [
    {
      "hs_code": "85076000",
      "description": "Lithium-ion batteries",
      "policy": "Free",
      "confidence": 0.91,
      "source": "embedding+llm"
    }
  ],
  "validated": true
}
```

### Response Fields

| Field       | Description                                   |
| ----------- | --------------------------------------------- |
| predictions | Ranked HS predictions                         |
| confidence  | Score (0–1), internal similarity + LLM signal |
| source      | `embedding`, `embedding+llm`, `exact_match`   |
| validated   | Ensures HS codes exist in DB                  |

---

## Error Example

```json
{
  "error": "No valid HS codes found for the given description"
}
```

---

# 2️⃣ POST `/api/v1/hs/analyze/`

## Purpose

Analyze a **specific HS code** and return structured regulatory insight.

This endpoint:

* Validates HS code exists
* Fetches structured DB info
* Uses LLM for compliance explanation

---

## Request

```json
{
  "hs_code": "85076000",
  "schedule_type": "import"
}
```

---

## Response

```json
{
  "hs_code": "85076000",
  "description": "Lithium-ion batteries",
  "policy": "Free",
  "policy_conditions": "Subject to BIS certification",
  "chapter": 85,
  "ai_analysis": "Lithium-ion batteries are classified under Chapter 85..."
}
```

---

## Validation

* Must be 8-digit numeric
* Must exist in `itc_hs_master`
* No hallucinated codes allowed

---

# 3️⃣ POST `/api/v1/hs/ask/`

## Purpose

Ask regulatory/compliance question related to HS code or trade policy.

This is hybrid RAG:

* Semantic search in `knowledge_base`
* Structured lookup in `itc_hs_master`
* LLM generates grounded answer

---

## Request

```json
{
  "question": "Is import of lithium batteries from China restricted?"
}
```

---

## Response

```json
{
  "answer": "Lithium-ion batteries under HS 85076000 are classified as Free for import. However, BIS certification may be required...",
  "sources": [
    {
      "content": "Import policy for Chapter 85...",
      "doc_level": "notification"
    }
  ]
}
```

---

## Notes

* LLM strictly grounded to retrieved context
* Structured HS data injected into prompt
* No free-form hallucinated regulation

---

# 4️⃣ POST `/api/v1/hs/search/`

## Purpose

Search HS codes using hybrid ranking:

* LIKE query
* Embedding similarity
* Ranking merge
* Optional AI summarization

---

## Request

```json
{
  "query": "solar inverter",
  "schedule_type": "import"
}
```

---

## Response

```json
{
  "results": [
    {
      "hs_code": "85044030",
      "description": "Solar power inverters",
      "policy": "Free"
    },
    {
      "hs_code": "85044090",
      "description": "Other static converters",
      "policy": "Free"
    }
  ],
  "ai_summary": "Most relevant results fall under static converters..."
}
```

---

## Ranking Logic

1. Exact text match priority
2. Embedding similarity
3. Deduplicated merge
4. Truncated to 20 results

---

# 5️⃣ GET `/api/v1/hs/chapter/<int:chapter_num>/`

## Purpose

Return structured view of an HS chapter with AI-generated overview.

---

## Example

```
GET /api/v1/hs/chapter/85/?schedule_type=import
```

---

## Response

```json
{
  "chapter": 85,
  "overview": "Chapter 85 covers electrical machinery and equipment...",
  "codes": [
    {
      "hs_code": "8501",
      "description": "Electric motors and generators",
      "policy": "Free"
    },
    {
      "hs_code": "8504",
      "description": "Electrical transformers...",
      "policy": "Free"
    }
  ]
}
```

---

## Returns

* Level-2 and Level-4 codes
* Sorted by HS code
* AI overview grounded in chapter data

---

# 🔐 Authentication

All endpoints require:

```
Authorization: Bearer <Clerk JWT>
```

Failure response:

```json
{
  "detail": "Authentication credentials were not provided."
}
```

---

# 📊 Internal Data Sources

| Source          | Purpose                |
| --------------- | ---------------------- |
| itc_hs_master   | Structured HS + policy |
| knowledge_base  | Regulatory documents   |
| pgvector        | Embedding similarity   |
| Qwen 3B (Modal) | Reasoning layer        |

---

# 🧠 LLM Safety Principles

1. Never invent HS codes
2. All codes validated against DB
3. LLM receives only retrieved context
4. Temperature fixed low (0.1)
5. No external browsing

---

# 📦 Versioning Strategy

Current version:

```
/api/v1/hs/
```

Future:

```
/api/v2/hs/
```

When:

* Ranking logic changes
* Response schema changes
* Confidence scoring model changes

---

# 🚀 Recommended Frontend Flow

### Classification Flow

1. `/predict/`
2. User selects best match
3. `/analyze/`

---

### Search Flow

1. `/search/`
2. Display results
3. Click → `/analyze/`

---

### Compliance Q&A Flow

1. `/ask/`
2. Show answer + sources

---

# 🔎 Error Codes

| HTTP | Meaning           |
| ---- | ----------------- |
| 400  | Validation error  |
| 401  | Auth failure      |
| 404  | HS code not found |
| 500  | Internal error    |

---

# ✅ This Documentation Guarantees

* Stable contract for frontend
* Clear separation of responsibilities
* No accidental LLM drift
* Safe HS validation
* Future extensibility

---


