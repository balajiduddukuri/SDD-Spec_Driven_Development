<p align="center">
  <img src="https://img.shields.io/badge/python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.8+"/>
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="MIT License"/>
  <img src="https://img.shields.io/badge/SDD-Spec%20Driven%20Dev-orange?style=for-the-badge" alt="Spec Driven Development"/>
  <img src="https://img.shields.io/badge/Zero-Dependencies-purple?style=for-the-badge" alt="Zero Dependencies"/>
  <img src="https://img.shields.io/badge/Tests-167%2B%20Cases-brightgreen?style=for-the-badge" alt="167+ Test Cases"/>
</p>

---

<h1 align="center">🚀 SDD Prompt Generator</h1>
<h3 align="center">AI-Powered Prompt Engineering for Spec-Driven Development</h3>

<p align="center">
  Generate tailored, production-ready <strong>System</strong> and <strong>User</strong> prompts for every phase of the <strong>Spec-Driven Development</strong> lifecycle — customized by persona, tech stack, domain, and project context.
</p>

---

## 📖 Table of Contents

- [What is Spec-Driven Development?](#-what-is-spec-driven-development)
- [Why This Tool?](#-why-this-tool)
- [Features](#-features)
- [Architecture Overview](#-architecture-overview)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Usage](#-usage)
  - [CLI Demo Mode](#1-cli-demo-mode)
  - [Interactive CLI](#2-interactive-cli)
  - [Programmatic / Library Usage](#3-programmatic--library-usage)
  - [Generate All Phases](#4-generate-all-phases)
  - [JSON Export](#5-json-export)
- [Personas](#-personas)
- [SDD Phases](#-sdd-phases)
- [Configuration Reference](#-configuration-reference-sddcontext)
- [Prompt Structure Deep-Dive](#-prompt-structure-deep-dive)
- [Examples](#-examples)
- [Testing](#-testing)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)
- [License](#-license)
- [Acknowledgments](#-acknowledgments)

---

## 🔍 What is Spec-Driven Development?

**Spec-Driven Development (SDD)** is a methodology where the **specification is the single source of truth** throughout the entire software development lifecycle. Unlike code-first approaches, SDD mandates that every feature begins with a formal specification — and all code, tests, documentation, and validation flow directly from it.

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐     ┌───────────────┐
│  Requirements    │────▶│  API Design   │────▶│  Contract/Schema │────▶│  Test          │
│  Specification   │     │  (Spec First) │     │  Definition      │     │  Generation    │
└─────────────────┘     └──────────────┘     └──────────────────┘     └───────────────┘
                                                                              │
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐            │
│  Documentation   │◀────│  Validation & │◀────│  Implementation  │◀───────────┘
│  Generation      │     │  Compliance   │     │  from Spec       │
└─────────────────┘     └──────────────┘     └──────────────────┘
```

### Core Principles

| Principle | Description |
|---|---|
| **Spec First** | Every feature begins with a specification before any code is written |
| **Contract as Truth** | The spec IS the documentation, the test oracle, and the implementation guide |
| **Traceability** | Every requirement maps to a spec element, test case, and code section |
| **No Spec Drift** | Any deviation of implementation from spec is treated as a bug |
| **Living Specs** | Specifications are versioned, reviewed, and evolved like code |

---

## 💡 Why This Tool?

Writing effective AI prompts for spec-driven workflows is **hard**. Each phase needs different context, each persona needs different depth, and consistency across a project is crucial.

**SDD Prompt Generator** solves this by:

| Problem | Solution |
|---|---|
| ❌ Generic, one-size-fits-all prompts | ✅ **9 personas** × **7 phases** = **63 unique prompt combinations** |
| ❌ Missing context leads to vague AI output | ✅ Rich context injection (tech stack, domain, constraints, existing specs) |
| ❌ Inconsistent prompt quality across teams | ✅ Standardized, battle-tested prompt templates |
| ❌ Time wasted crafting prompts manually | ✅ One-command generation for all phases at once |
| ❌ No traceability in AI-assisted workflows | ✅ Built-in requirement IDs, test traceability, and spec references |

---

## ✨ Features

### 🎭 Multi-Persona Support
Generate prompts tailored to **9 distinct personas** — from Product Owners defining requirements to QA Engineers generating test suites.

### 🔄 Full SDD Lifecycle Coverage
Covers all **7 phases** of the SDD lifecycle:
1. Requirement Specification
2. API / Interface Design
3. Contract / Schema Definition
4. Test Generation from Spec
5. Implementation from Spec
6. Validation & Compliance Check
7. Documentation Generation

### ⚙️ Rich Context Engine
Inject project-specific context including:
- Tech stack (languages, frameworks, databases)
- Business domain (fintech, healthcare, e-commerce, etc.)
- Existing specifications to work from
- Requirements and constraints lists
- Spec format preference (OpenAPI, AsyncAPI, GraphQL, etc.)
- Verbosity control (concise / detailed / verbose)

### 📦 Zero Dependencies
Built entirely on Python's **standard library** — no `pip install` needed beyond Python 3.8+.

### 🖥️ Multiple Interfaces
- **Interactive CLI** — guided Q&A workflow
- **Demo mode** — instant showcase with sample data
- **Programmatic API** — import and use in your own scripts/tools
- **JSON export** — pipe prompts into AI APIs or save for later

---

## 🏗️ Architecture Overview

```
┌──────────────────────────────────────────────────────────────────────┐
│                        SDDContext (dataclass)                        │
│  project_name · persona · phase · tech_stack · domain · constraints │
│  spec_format · existing_spec · requirements · verbosity             │
└────────────────────────────────┬─────────────────────────────────────┘
                                 │
                                 ▼
┌──────────────────────────────────────────────────────────────────────┐
│                     SDDPromptGenerator (class)                       │
│                                                                      │
│  ┌──────────────────────┐    ┌───────────────────────┐              │
│  │  PERSONA_DESCRIPTIONS│    │  SYSTEM_PROMPTS (7)    │              │
│  │  (9 personas)        │───▶│  Phase-specific        │──▶ System   │
│  └──────────────────────┘    │  templates with        │    Prompt   │
│                              │  persona injection     │              │
│                              └───────────────────────┘              │
│                                                                      │
│  ┌──────────────────────┐    ┌───────────────────────┐              │
│  │  Context fields      │    │  USER_PROMPTS (7)      │              │
│  │  (requirements,      │───▶│  Phase-specific        │──▶ User     │
│  │  constraints, spec)  │    │  templates with        │    Prompt   │
│  └──────────────────────┘    │  context injection     │              │
│                              └───────────────────────┘              │
│                                                                      │
│  Output: generate_prompts() → {system_prompt, user_prompt}          │
│          pretty_print()     → formatted terminal output             │
│          to_json()          → JSON with metadata + prompts          │
└──────────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌──────────────────────────────────────────────────────────────────────┐
│                    generate_all_phases() (helper)                     │
│  Loops through all 7 SDDPhase values with the same context          │
│  Returns: { "phase_name": {system_prompt, user_prompt}, ... }       │
└──────────────────────────────────────────────────────────────────────┘
```

---

## ⚡ Quick Start

```bash
# Clone the repository
git clone https://github.com/your-username/sdd-prompt-generator.git
cd sdd-prompt-generator

# Run the demo (no install needed!)
python sdd_prompt_generator.py --demo

# Or try interactive mode
python sdd_prompt_generator.py --interactive
```

```python
# Or use programmatically in 5 lines
from sdd_prompt_generator import SDDContext, SDDPromptGenerator, Persona, SDDPhase

context = SDDContext(
    project_name="Payment API",
    persona=Persona.BACKEND_DEVELOPER,
    phase=SDDPhase.API_DESIGN,
    tech_stack=["Go", "gRPC", "PostgreSQL"],
    domain="fintech",
)
prompts = SDDPromptGenerator(context).generate_prompts()
print(prompts["system_prompt"])
```

---

## 📦 Installation

### Option A: Direct Download (Simplest)

```bash
# Just grab the file — it's self-contained
curl -O https://raw.githubusercontent.com/your-username/sdd-prompt-generator/main/sdd_prompt_generator.py
```

### Option B: Clone Repository

```bash
git clone https://github.com/your-username/sdd-prompt-generator.git
cd sdd-prompt-generator
```

### Option C: As a Package Dependency

```python
# Copy sdd_prompt_generator.py into your project and import directly
from sdd_prompt_generator import SDDContext, SDDPromptGenerator, Persona, SDDPhase
```

### Requirements

| Requirement | Version |
|---|---|
| Python | 3.8+ |
| Dependencies | **None** (stdlib only: `dataclasses`, `enum`, `json`, `textwrap`) |

---

## 📘 Usage

### 1. CLI Demo Mode

Run the built-in demo with a pre-configured e-commerce platform example:

```bash
python sdd_prompt_generator.py --demo
```

**Output includes:**
- Full system prompt (Backend Developer × API Design phase)
- Full user prompt with sample requirements and constraints
- JSON export preview

---

### 2. Interactive CLI

A guided step-by-step workflow that asks for all inputs:

```bash
python sdd_prompt_generator.py --interactive
```

**Interactive flow:**
```
📋 PROJECT DETAILS
  Project Name [MyProject]: Payment Gateway
  Project Description: RESTful payment processing API

👤 PERSONA (choose one):
  1. product_owner
  2. backend_developer
  ...
  Select persona [2]: 8

🔄 SDD PHASE (choose one):
  1. requirement_specification
  2. api_interface_design
  ...
  Select phase [1]: 2

🛠️  TECH STACK (comma-separated)
  Tech Stack [Python, FastAPI]: Java, Spring Boot, Kafka

🏢 Domain [general]: fintech
📄 Spec Format [OpenAPI 3.1]: OpenAPI 3.1

📝 REQUIREMENTS (one per line, empty line to finish):
  > Process payments via Stripe and PayPal
  > Support refunds and partial refunds
  >

⚠️  CONSTRAINTS (one per line, empty line to finish):
  > PCI-DSS Level 1 compliance
  > < 500ms response time at p99
  >
```

At the end, you can also choose to:
- Generate prompts for **all 7 phases** at once
- **Export to JSON** for API integration

---

### 3. Programmatic / Library Usage

```python
from sdd_prompt_generator import SDDContext, SDDPromptGenerator, Persona, SDDPhase

# Define your context
context = SDDContext(
    project_name="Healthcare Patient Portal",
    project_description="HIPAA-compliant patient portal for scheduling, records, and messaging.",
    persona=Persona.QA_ENGINEER,
    phase=SDDPhase.TEST_GENERATION,
    tech_stack=["TypeScript", "NestJS", "MongoDB", "Jest"],
    domain="healthcare",
    spec_format="OpenAPI 3.1",
    requirements=[
        "Patients can view their medical records",
        "Patients can schedule/cancel appointments",
        "Doctors can send secure messages to patients",
        "All PHI data must be encrypted at rest and in transit",
    ],
    constraints=[
        "HIPAA compliance required",
        "SOC 2 Type II certification",
        "99.99% uptime SLA",
    ],
    verbosity="detailed",
)

# Generate prompts
generator = SDDPromptGenerator(context)

# Access individual prompts
system_prompt = generator.generate_system_prompt()
user_prompt = generator.generate_user_prompt()

# Or get both as a dict
prompts = generator.generate_prompts()

# Pretty-print to terminal
print(generator.pretty_print())

# Export as JSON
json_output = generator.to_json()
```

---

### 4. Generate All Phases

Generate prompts for **all 7 SDD phases** in a single call:

```python
from sdd_prompt_generator import SDDContext, Persona, generate_all_phases

context = SDDContext(
    project_name="Inventory Service",
    persona=Persona.FULLSTACK_DEVELOPER,
    tech_stack=["Python", "Django", "PostgreSQL", "React"],
    domain="supply chain",
    requirements=["Real-time stock tracking", "Low-stock alerts"],
)

all_prompts = generate_all_phases(context)

# all_prompts is a dict:
# {
#   "requirement_specification": {"system_prompt": "...", "user_prompt": "..."},
#   "api_interface_design":      {"system_prompt": "...", "user_prompt": "..."},
#   "contract_schema_definition": {...},
#   "test_generation_from_spec":  {...},
#   "implementation_from_spec":   {...},
#   "validation_compliance_check": {...},
#   "documentation_generation":   {...},
# }

for phase_name, prompts in all_prompts.items():
    print(f"Phase: {phase_name}")
    print(f"  System prompt length: {len(prompts['system_prompt'])} chars")
    print(f"  User prompt length:   {len(prompts['user_prompt'])} chars")
```

---

### 5. JSON Export

Export prompts with full metadata for integration with AI APIs:

```python
generator = SDDPromptGenerator(context)
json_str = generator.to_json()
print(json_str)
```

**Output structure:**
```json
{
  "metadata": {
    "project_name": "Payment Gateway",
    "persona": "architect",
    "phase": "api_interface_design",
    "tech_stack": ["Java", "Spring Boot", "Kafka"],
    "domain": "fintech",
    "spec_format": "OpenAPI 3.1"
  },
  "prompts": {
    "system_prompt": "You are a Solutions Architect who designs...",
    "user_prompt": "## Task: API / Interface Design for \"Payment Gateway\"..."
  }
}
```

---

## 🎭 Personas

Each persona injects a distinct **system-level identity** that shapes the AI's perspective, priorities, and output style.

| Enum Value | Persona | Focus Area | Best For |
|---|---|---|---|
| `PRODUCT_OWNER` | Product Owner | Business value, user stories, acceptance criteria | Requirements phase |
| `BACKEND_DEVELOPER` | Backend Developer | API design, data models, server logic | API Design, Implementation |
| `FRONTEND_DEVELOPER` | Frontend Developer | UI from specs, client-side validation | Implementation, Contract |
| `FULLSTACK_DEVELOPER` | Full-Stack Developer | End-to-end across the stack | All phases |
| `QA_ENGINEER` | QA Engineer | Test plans, contract tests, automation | Test Generation, Validation |
| `DEVOPS_ENGINEER` | DevOps Engineer | CI/CD, infrastructure, deployment | Validation, Implementation |
| `TECH_LEAD` | Tech Lead | Architecture decisions, spec governance | All phases |
| `ARCHITECT` | Solutions Architect | System design, service boundaries | Requirement, API Design |
| `TECHNICAL_WRITER` | Technical Writer | Developer docs, tutorials, guides | Documentation |

---

## 🔄 SDD Phases

| Phase | Enum Value | Description | Key Outputs |
|---|---|---|---|
| **1. Requirement Specification** | `REQUIREMENT_SPEC` | Translate business needs → testable specs | Requirement IDs, MoSCoW priorities, acceptance criteria |
| **2. API / Interface Design** | `API_DESIGN` | Design endpoints, resources, schemas | Endpoint specs, request/response schemas, auth patterns |
| **3. Contract / Schema Definition** | `CONTRACT_SCHEMA` | Define binding data contracts | JSON Schema, field constraints, mock data, versioning |
| **4. Test Generation from Spec** | `TEST_GENERATION` | Auto-derive test suites from contracts | Unit tests, contract tests, traceability matrix |
| **5. Implementation from Spec** | `IMPLEMENTATION` | Code that mirrors the spec exactly | Production code, models, validation, error handling |
| **6. Validation & Compliance** | `VALIDATION` | Detect spec drift, verify compliance | Compliance report, drift detection, severity ratings |
| **7. Documentation Generation** | `DOCUMENTATION` | API docs, tutorials, SDK examples | API reference, getting started guide, code examples |

---

## ⚙️ Configuration Reference (`SDDContext`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `project_name` | `str` | `"MyProject"` | Name of your project |
| `project_description` | `str` | `""` | What the project does |
| `persona` | `Persona` | `BACKEND_DEVELOPER` | Who is using the prompt (shapes system prompt tone) |
| `phase` | `SDDPhase` | `REQUIREMENT_SPEC` | Which SDD phase to generate prompts for |
| `tech_stack` | `List[str]` | `["Python", "FastAPI"]` | Languages, frameworks, databases, tools |
| `domain` | `str` | `"general"` | Business domain (e-commerce, fintech, healthcare, etc.) |
| `spec_format` | `str` | `"OpenAPI 3.1"` | Specification format (OpenAPI, AsyncAPI, GraphQL, Protobuf) |
| `existing_spec` | `str` | `""` | Paste an existing spec to build upon |
| `requirements` | `List[str]` | `[]` | List of business/technical requirements |
| `constraints` | `List[str]` | `[]` | Performance, compliance, compatibility limits |
| `output_format` | `str` | `"markdown"` | Desired output format |
| `verbosity` | `str` | `"detailed"` | `"concise"` / `"detailed"` / `"verbose"` |
| `additional_context` | `str` | `""` | Any extra context to inject into prompts |

---

## 🔬 Prompt Structure Deep-Dive

### System Prompt Anatomy

Every generated system prompt follows a consistent structure:

```
┌─────────────────────────────────────────────┐
│  1. PERSONA IDENTITY                        │  ← Who you are (from PERSONA_DESCRIPTIONS)
│     "You are a Solutions Architect who..."   │
├─────────────────────────────────────────────┤
│  2. ROLE & MISSION                          │  ← Phase-specific mission statement
│     "You are operating in the API Design    │
│      phase of SDD..."                       │
├─────────────────────────────────────────────┤
│  3. SDD PRINCIPLES                          │  ← Phase-relevant SDD principles
│     "Design First, Consumer-Driven,         │
│      Evolvable..."                          │
├─────────────────────────────────────────────┤
│  4. RESPONSIBILITIES                        │  ← Numbered list of specific tasks
│     "1. Define resource models..."          │
│     "2. Design request/response schemas..." │
├─────────────────────────────────────────────┤
│  5. CONTEXT INJECTION                       │  ← Tech stack, domain, spec format
│     "Tech Stack: Python, FastAPI, PG"       │
├─────────────────────────────────────────────┤
│  6. OUTPUT GUIDELINES                       │  ← Format, verbosity, specific rules
│     "Provide specs in OpenAPI 3.1 format"   │
└─────────────────────────────────────────────┘
```

### User Prompt Anatomy

```
┌─────────────────────────────────────────────┐
│  1. TASK HEADER                             │  ← Phase + project name
│     "## Task: API Design for 'PaymentAPI'"  │
├─────────────────────────────────────────────┤
│  2. PROJECT DESCRIPTION                     │  ← What the project does
├─────────────────────────────────────────────┤
│  3. REQUIREMENTS LIST                       │  ← Bulleted requirements
├─────────────────────────────────────────────┤
│  4. CONSTRAINTS LIST                        │  ← Bulleted constraints
├─────────────────────────────────────────────┤
│  5. EXISTING SPEC                           │  ← Code block (if provided)
├─────────────────────────────────────────────┤
│  6. ADDITIONAL CONTEXT                      │  ← Free-form extra info
├─────────────────────────────────────────────┤
│  7. DELIVERABLES                            │  ← Numbered "What I Need" list
│     "1. Design RESTful API endpoints..."    │
│     "2. Define resource models..."          │
└─────────────────────────────────────────────┘
```

---

## 📋 Examples

### Example 1: Backend Developer × API Design

```python
context = SDDContext(
    project_name="E-Commerce Platform",
    project_description="Modern e-commerce with catalog, cart, orders, and payments.",
    persona=Persona.BACKEND_DEVELOPER,
    phase=SDDPhase.API_DESIGN,
    tech_stack=["Python", "FastAPI", "PostgreSQL", "Redis", "Docker"],
    domain="e-commerce / retail",
    requirements=[
        "Users can browse products with search, filter, and pagination",
        "Users can add/remove items to/from shopping cart",
        "Users can place orders with multiple payment methods",
        "Admins can manage product catalog (CRUD)",
    ],
    constraints=[
        "API response time < 200ms at p95",
        "PCI-DSS compliance for payment data",
    ],
)
print(SDDPromptGenerator(context).pretty_print())
```

### Example 2: QA Engineer × Test Generation

```python
context = SDDContext(
    project_name="Healthcare Portal",
    persona=Persona.QA_ENGINEER,
    phase=SDDPhase.TEST_GENERATION,
    tech_stack=["TypeScript", "NestJS", "Jest", "Supertest"],
    domain="healthcare",
    existing_spec='{"openapi":"3.1.0","paths":{"/patients":{"get":{...}}}}',
    requirements=["100% contract coverage", "HIPAA compliance tests"],
)
```

### Example 3: Architect × All Phases

```python
context = SDDContext(
    project_name="Fraud Detection Engine",
    persona=Persona.ARCHITECT,
    tech_stack=["Java", "Spring Boot", "Kafka", "Cassandra", "TensorFlow"],
    domain="fintech / fraud detection",
    requirements=["Real-time transaction scoring", "ML model serving"],
)
all_prompts = generate_all_phases(context)
# → 7 phase outputs, each with system + user prompt
```

---

## 🧪 Testing

The project includes a comprehensive test suite with **167+ test cases** covering all combinations.

### Running Tests

```bash
# Install pytest (only dependency for testing)
pip install pytest

# Run all tests
pytest test_sdd_prompt_generator.py -v

# Run with coverage
pip install pytest-cov
pytest test_sdd_prompt_generator.py -v --cov=sdd_prompt_generator --cov-report=term-missing

# Run specific test class
pytest test_sdd_prompt_generator.py::TestSystemPromptGeneration -v

# Run the cross-matrix test (63 combinations)
pytest test_sdd_prompt_generator.py::TestCrossMatrix -v
```

### Test Coverage Summary

| Test Class | Tests | Description |
|---|---|---|
| `TestPersonaEnum` | 5 | Enum values, lookups, invalid handling |
| `TestSDDPhaseEnum` | 5 | Enum values, lookups, invalid handling |
| `TestSDDContext` | 5 | Defaults, custom values, isolation |
| `TestGlobalDictionaries` | 3 | All enum keys covered in global dicts |
| `TestHelperMethods` | 9 | `_format_list`, `_build_existing_spec_section`, etc. |
| `TestSystemPromptGeneration` | 13 | Persona/tech/domain/verbosity injection |
| `TestUserPromptGeneration` | 11 | Project, requirements, constraints, spec |
| `TestCombinedOutputMethods` | 8 | `generate_prompts()`, `pretty_print()`, `to_json()` |
| `TestGenerateAllPhases` | 6 | 7-phase generation, key matching |
| `TestEdgeCases` | 12 | Unicode, empty inputs, special chars |
| `TestCrossMatrix` | 1→63 | 9 Personas × 7 Phases parametrized |
| `TestConsistency` | 4 | Idempotency verification |
| `TestSmoke` | 3 | Overall sanity checks |
| **Total** | **~167** | **Effective test cases after parametrize** |

---

## 📁 Project Structure

```
sdd-prompt-generator/
├── sdd_prompt_generator.py        # Main module (self-contained, zero dependencies)
├── test_sdd_prompt_generator.py   # Comprehensive test suite (167+ cases)
├── sample_output.txt              # Example outputs for 5 scenarios
├── README.md                      # This file
├── LICENSE                        # MIT License
└── .gitignore                     # Python gitignore
```

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### Adding a New Persona

1. Add the enum value to `Persona` class
2. Add the description to `PERSONA_DESCRIPTIONS` dict
3. Run the cross-matrix tests to verify coverage

### Adding a New SDD Phase

1. Add the enum value to `SDDPhase` class
2. Add system prompt template to `SYSTEM_PROMPTS` dict
3. Add user prompt template to `USER_PROMPTS` dict
4. Run the full test suite to verify

### Contribution Guidelines

1. **Fork** the repository
2. **Create a feature branch**: `git checkout -b feature/add-security-persona`
3. **Write tests** for any new functionality
4. **Ensure all tests pass**: `pytest test_sdd_prompt_generator.py -v`
5. **Submit a Pull Request** with a clear description

### Code Style

- Follow PEP 8 with a line length of 100 characters
- Use type hints for all function signatures
- Add docstrings for all public methods
- Keep the zero-dependency constraint for the main module

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software...
```

---

## 🙏 Acknowledgments

- **Spec-Driven Development** methodology — inspired by API-first design, Contract Testing (Pact), and Design-by-Contract principles
- **OpenAPI Initiative** — for standardizing API specifications
- Built with ❤️ using pure Python standard library

---

<p align="center">
  <strong>⭐ Star this repo if you find it useful!</strong>
</p>

<p align="center">
  <sub>Built with 🐍 Python | Zero Dependencies | 167+ Test Cases</sub>
</p>
