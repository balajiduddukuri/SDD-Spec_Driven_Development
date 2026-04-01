"""
===============================================================================
Spec-Driven Development (SDD) Prompt Generator
===============================================================================
Generates tailored system and user prompts for AI-assisted Spec-Driven
Development workflows. Takes various persona and context inputs to produce
focused, actionable prompts for each phase of the SDD lifecycle.

Usage:
    python sdd_prompt_generator.py

Phases Covered:
    1. Requirement Specification
    2. API / Interface Design
    3. Contract / Schema Definition
    4. Test Generation from Spec
    5. Implementation from Spec
    6. Validation & Compliance Check
    7. Documentation Generation

Author : CodeMie Auto-Generator
Date   : 2026-04-01
===============================================================================
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict
from enum import Enum
import json
import textwrap


# ─────────────────────────────────────────────────────────────────────────────
# Enums & Data Models
# ─────────────────────────────────────────────────────────────────────────────

class Persona(Enum):
    """Supported personas that influence prompt tone and depth."""
    PRODUCT_OWNER = "product_owner"
    BACKEND_DEVELOPER = "backend_developer"
    FRONTEND_DEVELOPER = "frontend_developer"
    FULLSTACK_DEVELOPER = "fullstack_developer"
    QA_ENGINEER = "qa_engineer"
    DEVOPS_ENGINEER = "devops_engineer"
    TECH_LEAD = "tech_lead"
    ARCHITECT = "architect"
    TECHNICAL_WRITER = "technical_writer"


class SDDPhase(Enum):
    """Phases in the Spec-Driven Development lifecycle."""
    REQUIREMENT_SPEC = "requirement_specification"
    API_DESIGN = "api_interface_design"
    CONTRACT_SCHEMA = "contract_schema_definition"
    TEST_GENERATION = "test_generation_from_spec"
    IMPLEMENTATION = "implementation_from_spec"
    VALIDATION = "validation_compliance_check"
    DOCUMENTATION = "documentation_generation"


@dataclass
class SDDContext:
    """Captures all contextual inputs for prompt generation."""
    project_name: str = "MyProject"
    project_description: str = ""
    persona: Persona = Persona.BACKEND_DEVELOPER
    phase: SDDPhase = SDDPhase.REQUIREMENT_SPEC
    tech_stack: List[str] = field(default_factory=lambda: ["Python", "FastAPI"])
    domain: str = "general"
    spec_format: str = "OpenAPI 3.1"
    existing_spec: str = ""
    requirements: List[str] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)
    output_format: str = "markdown"
    verbosity: str = "detailed"  # "concise" | "detailed" | "verbose"
    additional_context: str = ""


# ─────────────────────────────────────────────────────────────────────────────
# Persona Descriptions (used inside system prompts)
# ─────────────────────────────────────────────────────────────────────────────

PERSONA_DESCRIPTIONS: Dict[Persona, str] = {
    Persona.PRODUCT_OWNER: (
        "You are a seasoned Product Owner focused on business value, user stories, "
        "acceptance criteria, and ensuring technical specs align with stakeholder needs."
    ),
    Persona.BACKEND_DEVELOPER: (
        "You are an expert Backend Developer skilled in API design, data modelling, "
        "server-side logic, and building robust, scalable services from specifications."
    ),
    Persona.FRONTEND_DEVELOPER: (
        "You are a skilled Frontend Developer who consumes API specs to build "
        "responsive UIs, handles client-side validation, and ensures great UX aligned with contracts."
    ),
    Persona.FULLSTACK_DEVELOPER: (
        "You are a proficient Full-Stack Developer comfortable working across the "
        "entire stack—from API spec to database schema to UI components."
    ),
    Persona.QA_ENGINEER: (
        "You are a meticulous QA Engineer who derives comprehensive test plans, "
        "test cases, and automated tests directly from specifications and contracts."
    ),
    Persona.DEVOPS_ENGINEER: (
        "You are a DevOps Engineer focused on CI/CD pipelines, infrastructure as code, "
        "deployment specs, and ensuring spec compliance in automated workflows."
    ),
    Persona.TECH_LEAD: (
        "You are a Tech Lead responsible for architectural decisions, code reviews, "
        "spec governance, and ensuring the team follows spec-driven development practices."
    ),
    Persona.ARCHITECT: (
        "You are a Solutions Architect who designs system-level specifications, "
        "defines service boundaries, data contracts, and integration patterns."
    ),
    Persona.TECHNICAL_WRITER: (
        "You are a Technical Writer who transforms specs into clear, developer-friendly "
        "documentation, tutorials, and integration guides."
    ),
}


# ─────────────────────────────────────────────────────────────────────────────
# System Prompt Templates (per SDD Phase)
# ─────────────────────────────────────────────────────────────────────────────

SYSTEM_PROMPTS: Dict[SDDPhase, str] = {
    SDDPhase.REQUIREMENT_SPEC: textwrap.dedent("""\
        {persona_description}

        ## Role & Mission
        You are operating in the **Requirement Specification** phase of Spec-Driven Development (SDD).
        Your goal is to help translate business needs into precise, unambiguous, and testable
        technical requirements that will serve as the single source of truth for all downstream work.

        ## Spec-Driven Development Principles
        - **Spec First**: Every feature begins with a specification before any code is written.
        - **Contract as Truth**: The spec IS the documentation, the test oracle, and the implementation guide.
        - **Traceability**: Every requirement must be traceable to a spec element and vice versa.
        - **Collaboration**: Specs are living documents refined through team feedback.

        ## Your Responsibilities
        1. Elicit and refine functional and non-functional requirements.
        2. Structure requirements in a machine-readable, verifiable format.
        3. Define clear acceptance criteria for each requirement.
        4. Identify ambiguities, conflicts, and missing edge cases.
        5. Map requirements to spec sections (endpoints, schemas, events, etc.).

        ## Tech Stack Context
        {tech_stack}

        ## Domain Context
        {domain}

        ## Output Guidelines
        - Format: {output_format}
        - Verbosity: {verbosity}
        - Always include requirement IDs (e.g., REQ-001).
        - Tag each requirement with priority (MUST / SHOULD / COULD / WONT).
    """),

    SDDPhase.API_DESIGN: textwrap.dedent("""\
        {persona_description}

        ## Role & Mission
        You are operating in the **API / Interface Design** phase of Spec-Driven Development.
        Your goal is to design clean, RESTful (or appropriate paradigm) API interfaces that
        faithfully represent the agreed-upon requirements.

        ## Spec-Driven Development Principles
        - **Design First**: The API contract is defined before implementation begins.
        - **Consumer-Driven**: APIs are shaped by consumer needs, validated via contract tests.
        - **Evolvable**: Specs support versioning, deprecation, and backward compatibility.

        ## Your Responsibilities
        1. Define resource models, endpoints, methods, and status codes.
        2. Design request/response schemas with proper validation rules.
        3. Specify authentication, authorization, and rate-limiting patterns.
        4. Handle pagination, filtering, sorting, and error responses.
        5. Ensure idempotency, cacheability, and HATEOAS where appropriate.

        ## Spec Format: {spec_format}
        ## Tech Stack: {tech_stack}
        ## Domain: {domain}

        ## Output Guidelines
        - Format: {output_format}
        - Verbosity: {verbosity}
        - Provide specs in {spec_format} format when applicable.
        - Include example request/response payloads.
    """),

    SDDPhase.CONTRACT_SCHEMA: textwrap.dedent("""\
        {persona_description}

        ## Role & Mission
        You are operating in the **Contract / Schema Definition** phase of SDD.
        Your goal is to produce precise, versioned data contracts and schemas that serve as
        binding agreements between producers and consumers.

        ## Spec-Driven Development Principles
        - **Schema as Contract**: Schemas define the exact shape of data exchanged.
        - **Validation at Boundaries**: Every service boundary validates against the contract.
        - **Breaking Change Detection**: Schema evolution must be tracked and communicated.

        ## Your Responsibilities
        1. Define JSON Schema / Protobuf / Avro / GraphQL schemas as needed.
        2. Specify required vs. optional fields, types, formats, and constraints.
        3. Define enumerations, discriminators, and polymorphic models.
        4. Version schemas and document migration paths.
        5. Generate mock data that conforms to schemas.

        ## Spec Format: {spec_format}
        ## Tech Stack: {tech_stack}
        ## Domain: {domain}

        ## Output Guidelines
        - Format: {output_format}
        - Verbosity: {verbosity}
        - Provide complete, valid schema definitions.
        - Include inline descriptions for every field.
    """),

    SDDPhase.TEST_GENERATION: textwrap.dedent("""\
        {persona_description}

        ## Role & Mission
        You are operating in the **Test Generation from Spec** phase of SDD.
        Your goal is to derive comprehensive, automated test suites directly from the specification,
        ensuring every spec element has corresponding test coverage.

        ## Spec-Driven Development Principles
        - **Spec = Test Oracle**: Tests are generated FROM the spec, not written independently.
        - **Contract Testing**: Producer and consumer tests validate spec compliance.
        - **Living Tests**: When the spec changes, tests are regenerated or updated.

        ## Your Responsibilities
        1. Generate unit tests for each schema and validation rule.
        2. Create integration/contract tests for each endpoint.
        3. Produce boundary, edge-case, and negative test scenarios.
        4. Define test data fixtures aligned with schema constraints.
        5. Map each test to its source requirement (traceability matrix).

        ## Tech Stack: {tech_stack}
        ## Domain: {domain}

        ## Output Guidelines
        - Format: {output_format}
        - Verbosity: {verbosity}
        - Use testing frameworks appropriate for the tech stack.
        - Include test IDs linked to requirement IDs.
        - Cover happy path, error paths, and edge cases.
    """),

    SDDPhase.IMPLEMENTATION: textwrap.dedent("""\
        {persona_description}

        ## Role & Mission
        You are operating in the **Implementation from Spec** phase of SDD.
        Your goal is to write production-quality code that faithfully implements the specification,
        ensuring the code is a direct reflection of the spec with no undocumented behavior.

        ## Spec-Driven Development Principles
        - **Spec Compliance**: Code MUST match the spec exactly—no more, no less.
        - **Code Generation**: Where possible, generate boilerplate from the spec (models, routes, validators).
        - **No Spec Drift**: Implementation divergence from spec is treated as a bug.

        ## Your Responsibilities
        1. Implement endpoints, handlers, and business logic per the spec.
        2. Generate data models and validation from schema definitions.
        3. Wire up authentication, authorization, and middleware per spec.
        4. Implement error handling matching spec-defined error responses.
        5. Add inline comments referencing spec sections.

        ## Tech Stack: {tech_stack}
        ## Domain: {domain}

        ## Output Guidelines
        - Format: {output_format}
        - Verbosity: {verbosity}
        - Write clean, well-documented, production-ready code.
        - Reference spec sections in docstrings and comments.
        - Follow SOLID principles and the project's coding standards.
    """),

    SDDPhase.VALIDATION: textwrap.dedent("""\
        {persona_description}

        ## Role & Mission
        You are operating in the **Validation & Compliance Check** phase of SDD.
        Your goal is to verify that the implementation strictly conforms to the specification
        and identify any drift, gaps, or inconsistencies.

        ## Spec-Driven Development Principles
        - **Continuous Validation**: Spec compliance is checked in CI/CD pipelines.
        - **Drift Detection**: Automated tools compare implementation against spec.
        - **Audit Trail**: Every deviation is logged and must be resolved.

        ## Your Responsibilities
        1. Compare implementation against spec (endpoint-by-endpoint).
        2. Validate response schemas against contract definitions.
        3. Check for undocumented endpoints or fields (spec drift).
        4. Verify error codes, headers, and status codes match spec.
        5. Produce a compliance report with pass/fail per spec element.

        ## Spec Format: {spec_format}
        ## Tech Stack: {tech_stack}
        ## Domain: {domain}

        ## Output Guidelines
        - Format: {output_format}
        - Verbosity: {verbosity}
        - Produce a structured compliance report.
        - Flag deviations with severity (CRITICAL / MAJOR / MINOR / INFO).
    """),

    SDDPhase.DOCUMENTATION: textwrap.dedent("""\
        {persona_description}

        ## Role & Mission
        You are operating in the **Documentation Generation** phase of SDD.
        Your goal is to transform the specification into clear, comprehensive, and
        developer-friendly documentation that accelerates onboarding and integration.

        ## Spec-Driven Development Principles
        - **Docs from Spec**: Documentation is generated/derived from the spec, ensuring accuracy.
        - **Single Source of Truth**: The spec is THE documentation—rendered for humans.
        - **Always Current**: Doc generation is automated and runs on every spec change.

        ## Your Responsibilities
        1. Generate API reference documentation from the spec.
        2. Write getting-started guides and integration tutorials.
        3. Create example workflows with request/response samples.
        4. Document authentication flows, error handling, and rate limits.
        5. Produce SDK usage examples in relevant languages.

        ## Spec Format: {spec_format}
        ## Tech Stack: {tech_stack}
        ## Domain: {domain}

        ## Output Guidelines
        - Format: {output_format}
        - Verbosity: {verbosity}
        - Use clear headings, code blocks, and tables.
        - Include runnable code examples.
        - Target audience: developers integrating with the API.
    """),
}


# ─────────────────────────────────────────────────────────────────────────────
# User Prompt Templates (per SDD Phase)
# ─────────────────────────────────────────────────────────────────────────────

USER_PROMPTS: Dict[SDDPhase, str] = {
    SDDPhase.REQUIREMENT_SPEC: textwrap.dedent("""\
        ## Task: Requirement Specification for "{project_name}"

        **Project Description:**
        {project_description}

        **Business Requirements to Analyze:**
        {requirements_list}

        **Known Constraints:**
        {constraints_list}

        {existing_spec_section}

        {additional_context_section}

        ### What I Need:
        1. Break down each business requirement into precise technical requirements.
        2. Assign requirement IDs (REQ-001, REQ-002, ...) with MoSCoW priority.
        3. Define clear acceptance criteria for each requirement.
        4. Identify gaps, ambiguities, or conflicts in the requirements.
        5. Map each requirement to potential spec elements (endpoints, schemas, events).
        6. Suggest non-functional requirements (performance, security, scalability).

        Please produce a complete **Requirements Specification Document**.
    """),

    SDDPhase.API_DESIGN: textwrap.dedent("""\
        ## Task: API / Interface Design for "{project_name}"

        **Project Description:**
        {project_description}

        **Requirements to Design For:**
        {requirements_list}

        **Known Constraints:**
        {constraints_list}

        {existing_spec_section}

        {additional_context_section}

        ### What I Need:
        1. Design RESTful API endpoints covering all requirements.
        2. Define resource models with relationships.
        3. Specify HTTP methods, URL patterns, query parameters, and headers.
        4. Design request/response schemas with validation rules.
        5. Define error response format and status codes.
        6. Include authentication and authorization requirements.
        7. Provide the spec in **{spec_format}** format.
        8. Include example request/response payloads for each endpoint.
    """),

    SDDPhase.CONTRACT_SCHEMA: textwrap.dedent("""\
        ## Task: Contract / Schema Definition for "{project_name}"

        **Project Description:**
        {project_description}

        **Schemas to Define:**
        {requirements_list}

        **Known Constraints:**
        {constraints_list}

        {existing_spec_section}

        {additional_context_section}

        ### What I Need:
        1. Define complete data schemas for all entities and DTOs.
        2. Specify field types, formats, constraints, and validation rules.
        3. Define required vs. optional fields with sensible defaults.
        4. Create enum definitions for all categorical fields.
        5. Design schema versioning strategy.
        6. Provide mock data samples conforming to each schema.
        7. Output schemas in **{spec_format}** format.
    """),

    SDDPhase.TEST_GENERATION: textwrap.dedent("""\
        ## Task: Test Generation from Spec for "{project_name}"

        **Project Description:**
        {project_description}

        **Spec / Contract to Generate Tests From:**
        {existing_spec_section}

        **Test Scope Requirements:**
        {requirements_list}

        **Known Constraints:**
        {constraints_list}

        {additional_context_section}

        ### What I Need:
        1. Generate unit tests for all schema validations.
        2. Create API contract tests for each endpoint (happy path + error paths).
        3. Design boundary and edge-case test scenarios.
        4. Produce a traceability matrix (Test ID → Requirement ID → Spec Element).
        5. Create reusable test fixtures and factories.
        6. Include performance/load test scenarios where applicable.
        7. Use testing frameworks appropriate for **{tech_stack}**.
    """),

    SDDPhase.IMPLEMENTATION: textwrap.dedent("""\
        ## Task: Implementation from Spec for "{project_name}"

        **Project Description:**
        {project_description}

        **Spec / Contract to Implement:**
        {existing_spec_section}

        **Implementation Requirements:**
        {requirements_list}

        **Known Constraints:**
        {constraints_list}

        {additional_context_section}

        ### What I Need:
        1. Implement all endpoints / handlers defined in the spec.
        2. Generate data models and validation logic from schemas.
        3. Implement business logic per the requirements.
        4. Wire authentication, authorization, and middleware.
        5. Implement spec-defined error handling and response codes.
        6. Add docstrings referencing spec sections.
        7. Use **{tech_stack}** with project coding standards.
        8. Ensure the code is production-ready with proper logging and error handling.
    """),

    SDDPhase.VALIDATION: textwrap.dedent("""\
        ## Task: Validation & Compliance Check for "{project_name}"

        **Project Description:**
        {project_description}

        **Spec / Contract to Validate Against:**
        {existing_spec_section}

        **Implementation to Validate:**
        {requirements_list}

        **Known Constraints:**
        {constraints_list}

        {additional_context_section}

        ### What I Need:
        1. Endpoint-by-endpoint comparison: spec vs. implementation.
        2. Schema compliance check for all request/response models.
        3. Detection of undocumented endpoints or fields (spec drift).
        4. Validation of error codes, headers, and status codes.
        5. A structured compliance report with severity ratings.
        6. Remediation recommendations for each deviation.
        7. Overall compliance score and summary.
    """),

    SDDPhase.DOCUMENTATION: textwrap.dedent("""\
        ## Task: Documentation Generation for "{project_name}"

        **Project Description:**
        {project_description}

        **Spec / Contract to Document:**
        {existing_spec_section}

        **Documentation Requirements:**
        {requirements_list}

        **Known Constraints:**
        {constraints_list}

        {additional_context_section}

        ### What I Need:
        1. API Reference Documentation with all endpoints, parameters, and schemas.
        2. Getting Started guide with authentication setup.
        3. Integration tutorial with step-by-step code examples.
        4. Error handling guide with all error codes and resolution steps.
        5. SDK usage examples in languages relevant to **{tech_stack}**.
        6. Changelog template for spec versioning.
        7. FAQ section addressing common integration questions.
    """),
}


# ─────────────────────────────────────────────────────────────────────────────
# Prompt Generator Class
# ─────────────────────────────────────────────────────────────────────────────

class SDDPromptGenerator:
    """
    Generates system and user prompts for each phase of Spec-Driven Development
    based on the provided context (persona, phase, tech stack, domain, etc.).
    """

    def __init__(self, context: SDDContext):
        self.context = context

    # ── Helpers ──────────────────────────────────────────────────────────

    def _format_list(self, items: List[str], prefix: str = "-") -> str:
        if not items:
            return "_None provided._"
        return "\n".join(f"{prefix} {item}" for item in items)

    def _build_existing_spec_section(self) -> str:
        if not self.context.existing_spec.strip():
            return "**Existing Spec:** _No existing spec provided. Design from scratch._"
        return f"**Existing Spec / Contract:**\n```\n{self.context.existing_spec}\n```"

    def _build_additional_context_section(self) -> str:
        if not self.context.additional_context.strip():
            return ""
        return f"**Additional Context:**\n{self.context.additional_context}"

    # ── System Prompt ────────────────────────────────────────────────────

    def generate_system_prompt(self) -> str:
        """Build the system prompt for the selected phase and persona."""
        template = SYSTEM_PROMPTS[self.context.phase]
        return template.format(
            persona_description=PERSONA_DESCRIPTIONS[self.context.persona],
            tech_stack=", ".join(self.context.tech_stack),
            domain=self.context.domain,
            spec_format=self.context.spec_format,
            output_format=self.context.output_format,
            verbosity=self.context.verbosity,
        )

    # ── User Prompt ──────────────────────────────────────────────────────

    def generate_user_prompt(self) -> str:
        """Build the user prompt for the selected phase with full context."""
        template = USER_PROMPTS[self.context.phase]
        return template.format(
            project_name=self.context.project_name,
            project_description=self.context.project_description or "_No description provided._",
            requirements_list=self._format_list(self.context.requirements),
            constraints_list=self._format_list(self.context.constraints),
            existing_spec_section=self._build_existing_spec_section(),
            additional_context_section=self._build_additional_context_section(),
            spec_format=self.context.spec_format,
            tech_stack=", ".join(self.context.tech_stack),
        )

    # ── Combined Output ──────────────────────────────────────────────────

    def generate_prompts(self) -> Dict[str, str]:
        """Return both system and user prompts as a dictionary."""
        return {
            "system_prompt": self.generate_system_prompt(),
            "user_prompt": self.generate_user_prompt(),
        }

    def pretty_print(self) -> str:
        """Return a nicely formatted string showing both prompts."""
        prompts = self.generate_prompts()
        separator = "=" * 80
        return (
            f"\n{separator}\n"
            f"  SDD PROMPT GENERATOR OUTPUT\n"
            f"  Project : {self.context.project_name}\n"
            f"  Persona : {self.context.persona.value}\n"
            f"  Phase   : {self.context.phase.value}\n"
            f"{separator}\n\n"
            f"{'─' * 40} SYSTEM PROMPT {'─' * 40}\n\n"
            f"{prompts['system_prompt']}\n\n"
            f"{'─' * 40} USER PROMPT {'─' * 40}\n\n"
            f"{prompts['user_prompt']}\n\n"
            f"{separator}\n"
        )

    def to_json(self) -> str:
        """Export prompts along with metadata as JSON."""
        return json.dumps(
            {
                "metadata": {
                    "project_name": self.context.project_name,
                    "persona": self.context.persona.value,
                    "phase": self.context.phase.value,
                    "tech_stack": self.context.tech_stack,
                    "domain": self.context.domain,
                    "spec_format": self.context.spec_format,
                },
                "prompts": self.generate_prompts(),
            },
            indent=2,
        )


# ─────────────────────────────────────────────────────────────────────────────
# Convenience Function: Generate All Phases for a Context
# ─────────────────────────────────────────────────────────────────────────────

def generate_all_phases(base_context: SDDContext) -> Dict[str, Dict[str, str]]:
    """
    Generate system + user prompts for ALL SDD phases using the same base context.
    Returns a dict keyed by phase name.
    """
    results = {}
    for phase in SDDPhase:
        ctx = SDDContext(
            project_name=base_context.project_name,
            project_description=base_context.project_description,
            persona=base_context.persona,
            phase=phase,
            tech_stack=base_context.tech_stack,
            domain=base_context.domain,
            spec_format=base_context.spec_format,
            existing_spec=base_context.existing_spec,
            requirements=base_context.requirements,
            constraints=base_context.constraints,
            output_format=base_context.output_format,
            verbosity=base_context.verbosity,
            additional_context=base_context.additional_context,
        )
        gen = SDDPromptGenerator(ctx)
        results[phase.value] = gen.generate_prompts()
    return results


# ─────────────────────────────────────────────────────────────────────────────
# Interactive CLI (runs when script is executed directly)
# ─────────────────────────────────────────────────────────────────────────────

def interactive_mode():
    """Run the prompt generator in interactive CLI mode."""
    print("=" * 70)
    print("  🚀 Spec-Driven Development (SDD) Prompt Generator")
    print("=" * 70)

    # ── Gather Inputs ────────────────────────────────────────────────────
    print("\n📋 PROJECT DETAILS")
    project_name = input("  Project Name [MyProject]: ").strip() or "MyProject"
    project_desc = input("  Project Description: ").strip()

    print("\n👤 PERSONA (choose one):")
    for i, p in enumerate(Persona, 1):
        print(f"  {i}. {p.value}")
    persona_idx = int(input("  Select persona [2]: ").strip() or "2") - 1
    persona = list(Persona)[max(0, min(persona_idx, len(Persona) - 1))]

    print("\n🔄 SDD PHASE (choose one):")
    for i, ph in enumerate(SDDPhase, 1):
        print(f"  {i}. {ph.value}")
    phase_idx = int(input("  Select phase [1]: ").strip() or "1") - 1
    phase = list(SDDPhase)[max(0, min(phase_idx, len(SDDPhase) - 1))]

    print("\n🛠️  TECH STACK (comma-separated)")
    tech_input = input("  Tech Stack [Python, FastAPI]: ").strip()
    tech_stack = [t.strip() for t in tech_input.split(",")] if tech_input else ["Python", "FastAPI"]

    domain = input("\n🏢 Domain [general]: ").strip() or "general"
    spec_format = input("📄 Spec Format [OpenAPI 3.1]: ").strip() or "OpenAPI 3.1"

    print("\n📝 REQUIREMENTS (one per line, empty line to finish):")
    requirements = []
    while True:
        req = input("  > ").strip()
        if not req:
            break
        requirements.append(req)

    print("\n⚠️  CONSTRAINTS (one per line, empty line to finish):")
    constraints = []
    while True:
        con = input("  > ").strip()
        if not con:
            break
        constraints.append(con)

    existing_spec = input("\n📎 Paste existing spec (or press Enter to skip): ").strip()
    additional = input("💬 Additional context (or press Enter to skip): ").strip()

    print("\n📊 VERBOSITY:")
    print("  1. concise")
    print("  2. detailed")
    print("  3. verbose")
    verb_idx = input("  Select [2]: ").strip() or "2"
    verbosity_map = {"1": "concise", "2": "detailed", "3": "verbose"}
    verbosity = verbosity_map.get(verb_idx, "detailed")

    # ── Build Context & Generate ─────────────────────────────────────────
    context = SDDContext(
        project_name=project_name,
        project_description=project_desc,
        persona=persona,
        phase=phase,
        tech_stack=tech_stack,
        domain=domain,
        spec_format=spec_format,
        existing_spec=existing_spec,
        requirements=requirements,
        constraints=constraints,
        output_format="markdown",
        verbosity=verbosity,
        additional_context=additional,
    )

    generator = SDDPromptGenerator(context)
    print(generator.pretty_print())

    # ── Optional: Generate All Phases ────────────────────────────────────
    all_phases = input("\nGenerate prompts for ALL phases? (y/N): ").strip().lower()
    if all_phases == "y":
        all_results = generate_all_phases(context)
        for phase_name, prompts in all_results.items():
            print(f"\n{'=' * 60}")
            print(f"  Phase: {phase_name}")
            print(f"{'=' * 60}")
            print(f"\n--- SYSTEM PROMPT ---\n{prompts['system_prompt'][:300]}...\n")
            print(f"--- USER PROMPT ---\n{prompts['user_prompt'][:300]}...\n")

    # ── Optional: Export JSON ────────────────────────────────────────────
    export = input("\nExport to JSON? (y/N): ").strip().lower()
    if export == "y":
        filename = f"sdd_prompts_{project_name.lower().replace(' ', '_')}.json"
        with open(filename, "w") as f:
            f.write(generator.to_json())
        print(f"\n✅ Exported to {filename}")


# ─────────────────────────────────────────────────────────────────────────────
# Demo Mode (non-interactive example)
# ─────────────────────────────────────────────────────────────────────────────

def demo():
    """Run a demo with sample inputs to showcase the generator."""
    print("\n🎯 Running SDD Prompt Generator Demo...\n")

    context = SDDContext(
        project_name="E-Commerce Platform",
        project_description=(
            "A modern e-commerce platform with product catalog, shopping cart, "
            "order management, payment processing, and user authentication."
        ),
        persona=Persona.BACKEND_DEVELOPER,
        phase=SDDPhase.API_DESIGN,
        tech_stack=["Python", "FastAPI", "PostgreSQL", "Redis", "Docker"],
        domain="e-commerce / retail",
        spec_format="OpenAPI 3.1",
        existing_spec="",
        requirements=[
            "Users can browse products with search, filter, and pagination",
            "Users can add/remove items to/from shopping cart",
            "Users can place orders with multiple payment methods",
            "Admins can manage product catalog (CRUD)",
            "System must support real-time inventory tracking",
            "Authentication via JWT with refresh tokens",
        ],
        constraints=[
            "API response time must be < 200ms at p95",
            "Must support 10,000 concurrent users",
            "PCI-DSS compliance for payment data",
            "GDPR compliance for user data",
            "Must be backward compatible with mobile app v2.x",
        ],
        output_format="markdown",
        verbosity="detailed",
        additional_context="The platform is migrating from a monolith to microservices.",
    )

    generator = SDDPromptGenerator(context)
    print(generator.pretty_print())
    print("\n📦 JSON Export Preview (first 500 chars):")
    print(generator.to_json()[:500] + "...")


# ─────────────────────────────────────────────────────────────────────────────
# Entry Point
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys

    if "--demo" in sys.argv:
        demo()
    elif "--interactive" in sys.argv:
        interactive_mode()
    else:
        print("Usage:")
        print("  python sdd_prompt_generator.py --demo          Run demo with sample data")
        print("  python sdd_prompt_generator.py --interactive   Run interactive CLI mode")
        print()
        print("Or import and use programmatically:")
        print("  from sdd_prompt_generator import SDDContext, SDDPromptGenerator, Persona, SDDPhase")
        print()
        # Default: run demo
        demo()
