# 🤖 TAMA: Tuned Autonomous Modular Assistant

**TAMA** is a self-learning Python agent capable of transforming natural language instructions into executable functions. Designed to grow from basic symbolic reasoning to neural generalization and mutation-based learning.

---

## 📦 Current Version: `v1.0`
> Core features built and tested through **Week 1** of the learning roadmap.

---

## 🧠 What Can TAMA Do?

- Understand and parse symbolic intents from English prompts
- Generate Python function code with arguments and logic
- Validate safety of generated code via AST analysis
- Store, retrieve, and patch learned behaviors using SQLite
- Learn from fallback: if not recognized, she asks you how to solve it
- Remembers everything via `IntentVault.db`

---

## 🧱 Architecture Overview

```
User Prompt
   ↓
IntentParser (symbolic + memory)
   ↓
CodeGenerator → CodeValidator → PatchStorage
   ↓
PatchLoader → Object injection
   ↓
Execution
```

---

## 🗂️ Modules

### `nlp.py` — Intent Parser
- Extracts structured function specs from natural language
- Uses regex for known patterns
- Fallbacks to manual teaching (via `input()` prompts)
- Stores and recalls intents from `IntentVault.db`

### `generator.py` — Code Generator
- Converts intent specs into valid Python code
- Currently only handles single-function bodies
- Future: infer dependencies from body

### `validator.py` — Code Validator
- Uses `ast` to check for:
  - Dangerous nodes (`exec`, `open`, etc.)
  - Unknown imports
  - Non-functional structure
- Ensures only valid, safe Python is stored

### `loader.py` — Patch Loader
- Dynamically attaches learned functions to live objects
- Extracts function name and binds using `types.MethodType`
- Uses validator before loading

### `storage.py` — Patch Storage
- Stores code in `PatchVault.db`
- Uses content-based SHA256 hash for versioning
- Tracks dependencies and usage metadata

---

## 🧪 Example Usage

```python
bot = DynamicBot()
result = bot.learn_and_execute("Add three numbers", 1, 2, 3)
print(result)  # Output: 6
```

On first run, TAMA may ask:
```
TAMA: Hey <<User>>, not sure how to perform this task. Mind showing me how?
```

Once taught, she remembers it forever.

---

## 📘 Learning Roadmap

| Week | Theme                         | Status    |
|------|-------------------------------|-----------|
| 1    | Symbolic Core + Memory        | ✅ complete |
| 2    | Neural Matching + Mutation    | 🏗️ in progress |
| 3    | Active Learning + Dialog Loop | ⏳ planned |
| 4    | Full Autonomy & Optimization  | ⏳ planned |

---

## 📂 Databases

- `PatchVault.db`: stores all generated code + metadata
- `IntentVault.db`: stores `prompt → spec` mappings

---

## 🚧 Coming Soon (Week 2)

- `matcher.py`: neural intent matcher using MiniLM embeddings
- `mutation.py`: AST-based patch mutator for self-rewriting
- Fallback logic with similarity matching
