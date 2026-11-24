>> ## ✨ Key Features & Technical Highlights
>> * **100-Word Chunking Algorithm:** Solves the 512-token truncation limit in SentenceTransformers, delivering realistic semantic scores (40–87/100).
>> * **Canonical Skill Normalization:** Boundary regex `(?<!\w)alias(?!\w)` maps aliases (`PowerBI` ➔ `Power BI`, `Data Analytics` ➔ `Data Analysis`, `MS Excel` ➔ `Excel`).
>> * **Automated Tie-Breaking:** Candidates with identical skill percentages (e.g., 22%) are tie-broken based on semantic similarity (29 > 25 > 21).
>> * **Fault-Tolerant Batching:** Corrupted or unreadable image-only PDFs are isolated as `Status: Failed` without stopping remaining evaluations.
>> 
>> ---
>> 
>> ## 🛠️ Technology Stack
>> * **Frontend:** React.js, JSX, CSS3, Vite
>> * **Backend:** FastAPI, Python 3.12, Uvicorn ASGI
>> * **Document Processing:** PyMuPDF (`fitz`)
>> * **AI Model:** SentenceTransformers (`all-MiniLM-L6-v2`), Scikit-learn
>> * **Database:** SQLite3 (`hirematch.db`)
>> 
>> ---
>> 
>> ## 🚀 How to Run Locally
>> 
>> ### 1. Backend Setup
>> ```bash
>> python -m venv .venv
>> .venv\Scripts\Activate.ps1
>> pip install -r backend/requirements.txt
>> uvicorn backend.main:app --reload
At line:3 char:2
+ [![Python](https://img.shields.io/badge/Python-3.12-blue.svg?logo=pyt ...
+  ~
Missing type name after '['.
At line:3 char:73
+ ... ttps://img.shields.io/badge/Python-3.12-blue.svg?logo=python&logoColo ...
+                                                                 ~
The ampersand (&) character is not allowed. The & operator is reserved for future use; wrap an ampersand in double quotation marks ("&") to pass it as part of a string.
At line:4 char:2
+ [![FastAPI](https://img.shields.io/badge/FastAPI-0.142-009688.svg?log ...
+  ~
Missing type name after '['.
At line:4 char:79
+ ... //img.shields.io/badge/FastAPI-0.142-009688.svg?logo=fastapi&logoColo ...
+                                                                 ~
The ampersand (&) character is not allowed. The & operator is reserved for future use; wrap an ampersand in double quotation marks ("&") to pass it as part of a string.
At line:5 char:2
+ [![React](https://img.shields.io/badge/React-18.x-61DAFB.svg?logo=rea ...
+  ~
Missing type name after '['.
At line:5 char:72
+ ... ttps://img.shields.io/badge/React-18.x-61DAFB.svg?logo=react&logoColo ...
+                                                                 ~
The ampersand (&) character is not allowed. The & operator is reserved for future use; wrap an ampersand in double quotation marks ("&") to pass it as part of a string.
At line:6 char:2
+ [![Sentence--Transformers](https://img.shields.io/badge/Sentence--Tra ...
+  ~
Missing type name after '['.
At line:7 char:2
+ [![SQLite](https://img.shields.io/badge/SQLite-3-003B57.svg?logo=sqli ...
+  ~
Missing type name after '['.
At line:7 char:72
+ ... https://img.shields.io/badge/SQLite-3-003B57.svg?logo=sqlite&logoColo ...
+                                                                 ~
The ampersand (&) character is not allowed. The & operator is reserved for future use; wrap an ampersand in double quotation marks ("&") to pass it as part of a string.
At line:11 char:4
+ ---
+    ~
Missing expression after unary operator '-'.
Not all parse errors were reported.  Correct the reported errors and try again.
    + CategoryInfo          : ParserError: (:) [], ParentContainsErrorRecordException
    + FullyQualifiedErrorId : MissingTypename
 