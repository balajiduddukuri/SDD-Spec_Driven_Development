"""
===============================================================================
Unit Tests for Spec-Driven Development (SDD) Prompt Generator
===============================================================================
Comprehensive test suite covering all personas, phases, context building,
prompt generation, serialization, and edge cases.

Run:
    pytest test_sdd_prompt_generator.py -v
    pytest test_sdd_prompt_generator.py -v --tb=short
    python -m pytest test_sdd_prompt_generator.py -v

Author : CodeMie Auto-Generator
Date   : 2026-04-01
===============================================================================
"""

import json
import pytest
from dataclasses import fields as dataclass_fields

from sdd_prompt_generator import (
    Persona,
    SDDPhase,
    SDDContext,
    SDDPromptGenerator,
    PERSONA_DESCRIPTIONS,
    SYSTEM_PROMPTS,
    USER_PROMPTS,
    generate_all_phases,
)


# ─────────────────────────────────────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────────────────────────────────────

@pytest.fixture
def default_context():
    """A minimal SDDContext with all defaults."""
    return SDDContext()


@pytest.fixture
def full_context():
    """A fully-populated SDDContext for rich testing."""
    return SDDContext(
        project_name="Payment Gateway",
        project_description="A secure payment processing gateway supporting Stripe and PayPal.",
        persona=Persona.ARCHITECT,
        phase=SDDPhase.API_DESIGN,
        tech_stack=["Java", "Spring Boot", "Kafka", "PostgreSQL"],
        domain="fintech",
        spec_format="OpenAPI 3.1",
        existing_spec='''openapi: "3.1.0"
info:
  title: Payment API
  version: "1.0.0"
paths:
  /payments:
    post:
      summary: Create payment
''',
        requirements=[
            "Process credit card payments via Stripe",
            "Process PayPal payments",
            "Support refunds within 30 days",
            "Emit payment events to Kafka",
        ],
        constraints=[
            "PCI-DSS Level 1 compliance",
            "99.99% uptime SLA",
            "Latency < 500ms at p99",
        ],
        output_format="markdown",
        verbosity="detailed",
        additional_context="Migrating from legacy SOAP-based payment system.",
    )


@pytest.fixture
def ecommerce_context():
    """An e-commerce context for demo-style testing."""
    return SDDContext(
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
        requirements=[
            "Users can browse products with search, filter, and pagination",
            "Users can add/remove items to/from shopping cart",
            "Users can place orders with multiple payment methods",
            "Admins can manage product catalog (CRUD)",
        ],
        constraints=[
            "API response time must be < 200ms at p95",
            "Must support 10,000 concurrent users",
        ],
        verbosity="detailed",
        additional_context="Migrating from a monolith to microservices.",
    )


@pytest.fixture
def minimal_context():
    """A context with minimal/empty optional fields."""
    return SDDContext(
        project_name="Bare Minimum",
        persona=Persona.QA_ENGINEER,
        phase=SDDPhase.TEST_GENERATION,
        tech_stack=["Go"],
        domain="internal tooling",
    )


# ─────────────────────────────────────────────────────────────────────────────
# 1. Enum Tests
# ─────────────────────────────────────────────────────────────────────────────

class TestPersonaEnum:
    """Tests for the Persona enum."""

    def test_all_personas_exist(self):
        expected = [
            "product_owner", "backend_developer", "frontend_developer",
            "fullstack_developer", "qa_engineer", "devops_engineer",
            "tech_lead", "architect", "technical_writer",
        ]
        actual = [p.value for p in Persona]
        assert actual == expected

    def test_persona_count(self):
        assert len(Persona) == 9

    def test_persona_lookup_by_value(self):
        assert Persona("backend_developer") == Persona.BACKEND_DEVELOPER

    def test_persona_lookup_by_name(self):
        assert Persona["ARCHITECT"] == Persona.ARCHITECT

    def test_invalid_persona_raises(self):
        with pytest.raises(ValueError):
            Persona("nonexistent_persona")


class TestSDDPhaseEnum:
    """Tests for the SDDPhase enum."""

    def test_all_phases_exist(self):
        expected = [
            "requirement_specification", "api_interface_design",
            "contract_schema_definition", "test_generation_from_spec",
            "implementation_from_spec", "validation_compliance_check",
            "documentation_generation",
        ]
        actual = [p.value for p in SDDPhase]
        assert actual == expected

    def test_phase_count(self):
        assert len(SDDPhase) == 7

    def test_phase_lookup_by_value(self):
        assert SDDPhase("api_interface_design") == SDDPhase.API_DESIGN

    def test_phase_lookup_by_name(self):
        assert SDDPhase["VALIDATION"] == SDDPhase.VALIDATION

    def test_invalid_phase_raises(self):
        with pytest.raises(ValueError):
            SDDPhase("unknown_phase")


# ─────────────────────────────────────────────────────────────────────────────
# 2. SDDContext Tests
# ─────────────────────────────────────────────────────────────────────────────

class TestSDDContext:
    """Tests for SDDContext dataclass."""

    def test_default_values(self, default_context):
        ctx = default_context
        assert ctx.project_name == "MyProject"
        assert ctx.project_description == ""
        assert ctx.persona == Persona.BACKEND_DEVELOPER
        assert ctx.phase == SDDPhase.REQUIREMENT_SPEC
        assert ctx.tech_stack == ["Python", "FastAPI"]
        assert ctx.domain == "general"
        assert ctx.spec_format == "OpenAPI 3.1"
        assert ctx.existing_spec == ""
        assert ctx.requirements == []
        assert ctx.constraints == []
        assert ctx.output_format == "markdown"
        assert ctx.verbosity == "detailed"
        assert ctx.additional_context == ""

    def test_custom_values(self, full_context):
        ctx = full_context
        assert ctx.project_name == "Payment Gateway"
        assert ctx.persona == Persona.ARCHITECT
        assert ctx.phase == SDDPhase.API_DESIGN
        assert "Java" in ctx.tech_stack
        assert ctx.domain == "fintech"
        assert len(ctx.requirements) == 4
        assert len(ctx.constraints) == 3

    def test_field_count(self):
        """Ensure no fields are accidentally added or removed."""
        assert len(dataclass_fields(SDDContext)) == 13

    def test_mutable_defaults_are_independent(self):
        """Each instance should have its own list copies."""
        ctx1 = SDDContext()
        ctx2 = SDDContext()
        ctx1.requirements.append("REQ-A")
        assert "REQ-A" not in ctx2.requirements

    def test_tech_stack_mutable_default_independence(self):
        ctx1 = SDDContext()
        ctx2 = SDDContext()
        ctx1.tech_stack.append("Rust")
        assert "Rust" not in ctx2.tech_stack


# ─────────────────────────────────────────────────────────────────────────────
# 3. Global Dictionaries Coverage Tests
# ─────────────────────────────────────────────────────────────────────────────

class TestGlobalDictionaries:
    """Ensure PERSONA_DESCRIPTIONS, SYSTEM_PROMPTS, USER_PROMPTS cover all enums."""

    def test_persona_descriptions_cover_all_personas(self):
        for persona in Persona:
            assert persona in PERSONA_DESCRIPTIONS, f"Missing description for {persona}"
            assert len(PERSONA_DESCRIPTIONS[persona]) > 20

    def test_system_prompts_cover_all_phases(self):
        for phase in SDDPhase:
            assert phase in SYSTEM_PROMPTS, f"Missing system prompt for {phase}"
            assert len(SYSTEM_PROMPTS[phase]) > 50

    def test_user_prompts_cover_all_phases(self):
        for phase in SDDPhase:
            assert phase in USER_PROMPTS, f"Missing user prompt for {phase}"
            assert len(USER_PROMPTS[phase]) > 50


# ─────────────────────────────────────────────────────────────────────────────
# 4. SDDPromptGenerator — Helper Methods
# ─────────────────────────────────────────────────────────────────────────────

class TestHelperMethods:
    """Tests for _format_list, _build_existing_spec_section, _build_additional_context_section."""

    def test_format_list_with_items(self, full_context):
        gen = SDDPromptGenerator(full_context)
        result = gen._format_list(["Alpha", "Beta", "Gamma"])
        assert "- Alpha" in result
        assert "- Beta" in result
        assert "- Gamma" in result
        assert result.count("\n") == 2  # 3 items, 2 newlines

    def test_format_list_empty(self, default_context):
        gen = SDDPromptGenerator(default_context)
        result = gen._format_list([])
        assert result == "_None provided._"

    def test_format_list_custom_prefix(self, default_context):
        gen = SDDPromptGenerator(default_context)
        result = gen._format_list(["One", "Two"], prefix="*")
        assert "* One" in result
        assert "* Two" in result

    def test_build_existing_spec_section_empty(self, default_context):
        gen = SDDPromptGenerator(default_context)
        result = gen._build_existing_spec_section()
        assert "No existing spec provided" in result

    def test_build_existing_spec_section_with_spec(self, full_context):
        gen = SDDPromptGenerator(full_context)
        result = gen._build_existing_spec_section()
        assert "```" in result
        assert "Payment API" in result

    def test_build_additional_context_empty(self, default_context):
        gen = SDDPromptGenerator(default_context)
        result = gen._build_additional_context_section()
        assert result == ""

    def test_build_additional_context_with_text(self, full_context):
        gen = SDDPromptGenerator(full_context)
        result = gen._build_additional_context_section()
        assert "Additional Context" in result
        assert "SOAP" in result

    def test_build_existing_spec_whitespace_only(self):
        ctx = SDDContext(existing_spec="   ")
        gen = SDDPromptGenerator(ctx)
        result = gen._build_existing_spec_section()
        assert "No existing spec provided" in result

    def test_build_additional_context_whitespace_only(self):
        ctx = SDDContext(additional_context="   ")
        gen = SDDPromptGenerator(ctx)
        result = gen._build_additional_context_section()
        assert result == ""


# ─────────────────────────────────────────────────────────────────────────────
# 5. SDDPromptGenerator — System Prompt Generation
# ─────────────────────────────────────────────────────────────────────────────

class TestSystemPromptGeneration:
    """Tests for generate_system_prompt() across all phases and personas."""

    def test_system_prompt_contains_persona_description(self, full_context):
        gen = SDDPromptGenerator(full_context)
        prompt = gen.generate_system_prompt()
        assert "Solutions Architect" in prompt  # Persona.ARCHITECT

    def test_system_prompt_contains_tech_stack(self, full_context):
        gen = SDDPromptGenerator(full_context)
        prompt = gen.generate_system_prompt()
        assert "Java" in prompt
        assert "Spring Boot" in prompt

    def test_system_prompt_contains_domain(self, full_context):
        gen = SDDPromptGenerator(full_context)
        prompt = gen.generate_system_prompt()
        assert "fintech" in prompt

    def test_system_prompt_contains_verbosity(self, full_context):
        gen = SDDPromptGenerator(full_context)
        prompt = gen.generate_system_prompt()
        assert "detailed" in prompt

    @pytest.mark.parametrize("phase", list(SDDPhase))
    def test_system_prompt_generation_all_phases(self, phase):
        ctx = SDDContext(phase=phase)
        gen = SDDPromptGenerator(ctx)
        prompt = gen.generate_system_prompt()
        assert isinstance(prompt, str)
        assert len(prompt) > 100
        # Should contain persona description
        assert PERSONA_DESCRIPTIONS[ctx.persona][:30] in prompt

    @pytest.mark.parametrize("persona", list(Persona))
    def test_system_prompt_generation_all_personas(self, persona):
        ctx = SDDContext(persona=persona, phase=SDDPhase.IMPLEMENTATION)
        gen = SDDPromptGenerator(ctx)
        prompt = gen.generate_system_prompt()
        assert PERSONA_DESCRIPTIONS[persona][:30] in prompt

    def test_requirement_spec_phase_keywords(self):
        ctx = SDDContext(phase=SDDPhase.REQUIREMENT_SPEC)
        prompt = SDDPromptGenerator(ctx).generate_system_prompt()
        assert "Requirement Specification" in prompt
        assert "acceptance criteria" in prompt.lower() or "Acceptance" in prompt

    def test_api_design_phase_keywords(self):
        ctx = SDDContext(phase=SDDPhase.API_DESIGN)
        prompt = SDDPromptGenerator(ctx).generate_system_prompt()
        assert "API" in prompt
        assert "Interface Design" in prompt or "API" in prompt

    def test_contract_schema_phase_keywords(self):
        ctx = SDDContext(phase=SDDPhase.CONTRACT_SCHEMA)
        prompt = SDDPromptGenerator(ctx).generate_system_prompt()
        assert "Contract" in prompt or "Schema" in prompt

    def test_test_generation_phase_keywords(self):
        ctx = SDDContext(phase=SDDPhase.TEST_GENERATION)
        prompt = SDDPromptGenerator(ctx).generate_system_prompt()
        assert "Test" in prompt

    def test_implementation_phase_keywords(self):
        ctx = SDDContext(phase=SDDPhase.IMPLEMENTATION)
        prompt = SDDPromptGenerator(ctx).generate_system_prompt()
        assert "Implementation" in prompt

    def test_validation_phase_keywords(self):
        ctx = SDDContext(phase=SDDPhase.VALIDATION)
        prompt = SDDPromptGenerator(ctx).generate_system_prompt()
        assert "Validation" in prompt or "Compliance" in prompt

    def test_documentation_phase_keywords(self):
        ctx = SDDContext(phase=SDDPhase.DOCUMENTATION)
        prompt = SDDPromptGenerator(ctx).generate_system_prompt()
        assert "Documentation" in prompt


# ─────────────────────────────────────────────────────────────────────────────
# 6. SDDPromptGenerator — User Prompt Generation
# ─────────────────────────────────────────────────────────────────────────────

class TestUserPromptGeneration:
    """Tests for generate_user_prompt() across all phases."""

    def test_user_prompt_contains_project_name(self, full_context):
        gen = SDDPromptGenerator(full_context)
        prompt = gen.generate_user_prompt()
        assert "Payment Gateway" in prompt

    def test_user_prompt_contains_project_description(self, full_context):
        gen = SDDPromptGenerator(full_context)
        prompt = gen.generate_user_prompt()
        assert "secure payment processing" in prompt

    def test_user_prompt_contains_requirements(self, full_context):
        gen = SDDPromptGenerator(full_context)
        prompt = gen.generate_user_prompt()
        assert "Stripe" in prompt
        assert "PayPal" in prompt
        assert "refunds" in prompt.lower()

    def test_user_prompt_contains_constraints(self, full_context):
        gen = SDDPromptGenerator(full_context)
        prompt = gen.generate_user_prompt()
        assert "PCI-DSS" in prompt
        assert "99.99%" in prompt

    def test_user_prompt_contains_existing_spec(self, full_context):
        gen = SDDPromptGenerator(full_context)
        prompt = gen.generate_user_prompt()
        assert "Payment API" in prompt

    def test_user_prompt_contains_additional_context(self, full_context):
        gen = SDDPromptGenerator(full_context)
        prompt = gen.generate_user_prompt()
        assert "SOAP" in prompt

    def test_user_prompt_no_description(self, minimal_context):
        gen = SDDPromptGenerator(minimal_context)
        prompt = gen.generate_user_prompt()
        assert "No description provided" in prompt

    def test_user_prompt_empty_requirements(self, minimal_context):
        gen = SDDPromptGenerator(minimal_context)
        prompt = gen.generate_user_prompt()
        assert "None provided" in prompt

    @pytest.mark.parametrize("phase", list(SDDPhase))
    def test_user_prompt_generation_all_phases(self, phase):
        ctx = SDDContext(
            project_name="TestProject",
            phase=phase,
            requirements=["REQ-A"],
            constraints=["CONS-A"],
        )
        gen = SDDPromptGenerator(ctx)
        prompt = gen.generate_user_prompt()
        assert isinstance(prompt, str)
        assert "TestProject" in prompt
        assert "REQ-A" in prompt
        assert "CONS-A" in prompt

    def test_user_prompt_spec_format_in_relevant_phases(self):
        for phase in [SDDPhase.API_DESIGN, SDDPhase.CONTRACT_SCHEMA]:
            ctx = SDDContext(phase=phase, spec_format="AsyncAPI 2.6")
            prompt = SDDPromptGenerator(ctx).generate_user_prompt()
            assert "AsyncAPI 2.6" in prompt

    def test_user_prompt_tech_stack_in_relevant_phases(self):
        for phase in [SDDPhase.TEST_GENERATION, SDDPhase.IMPLEMENTATION]:
            ctx = SDDContext(phase=phase, tech_stack=["Rust", "Actix"])
            prompt = SDDPromptGenerator(ctx).generate_user_prompt()
            assert "Rust" in prompt or "Actix" in prompt


# ─────────────────────────────────────────────────────────────────────────────
# 7. SDDPromptGenerator — Combined Output Methods
# ─────────────────────────────────────────────────────────────────────────────

class TestCombinedOutputMethods:
    """Tests for generate_prompts(), pretty_print(), and to_json()."""

    def test_generate_prompts_returns_dict(self, full_context):
        gen = SDDPromptGenerator(full_context)
        result = gen.generate_prompts()
        assert isinstance(result, dict)
        assert "system_prompt" in result
        assert "user_prompt" in result

    def test_generate_prompts_values_are_strings(self, full_context):
        gen = SDDPromptGenerator(full_context)
        result = gen.generate_prompts()
        assert isinstance(result["system_prompt"], str)
        assert isinstance(result["user_prompt"], str)

    def test_generate_prompts_non_empty(self, full_context):
        gen = SDDPromptGenerator(full_context)
        result = gen.generate_prompts()
        assert len(result["system_prompt"]) > 0
        assert len(result["user_prompt"]) > 0

    def test_pretty_print_contains_metadata(self, full_context):
        gen = SDDPromptGenerator(full_context)
        output = gen.pretty_print()
        assert "Payment Gateway" in output
        assert "architect" in output
        assert "api_interface_design" in output
        assert "SYSTEM PROMPT" in output
        assert "USER PROMPT" in output

    def test_pretty_print_contains_separators(self, full_context):
        gen = SDDPromptGenerator(full_context)
        output = gen.pretty_print()
        assert "=" * 80 in output
        assert "─" in output

    def test_to_json_is_valid_json(self, full_context):
        gen = SDDPromptGenerator(full_context)
        json_str = gen.to_json()
        data = json.loads(json_str)
        assert isinstance(data, dict)

    def test_to_json_metadata_fields(self, full_context):
        gen = SDDPromptGenerator(full_context)
        data = json.loads(gen.to_json())
        meta = data["metadata"]
        assert meta["project_name"] == "Payment Gateway"
        assert meta["persona"] == "architect"
        assert meta["phase"] == "api_interface_design"
        assert "Java" in meta["tech_stack"]
        assert meta["domain"] == "fintech"
        assert meta["spec_format"] == "OpenAPI 3.1"

    def test_to_json_prompts_present(self, full_context):
        gen = SDDPromptGenerator(full_context)
        data = json.loads(gen.to_json())
        assert "system_prompt" in data["prompts"]
        assert "user_prompt" in data["prompts"]
        assert len(data["prompts"]["system_prompt"]) > 0
        assert len(data["prompts"]["user_prompt"]) > 0


# ─────────────────────────────────────────────────────────────────────────────
# 8. generate_all_phases() Tests
# ─────────────────────────────────────────────────────────────────────────────

class TestGenerateAllPhases:
    """Tests for the generate_all_phases() convenience function."""

    def test_returns_all_seven_phases(self, full_context):
        results = generate_all_phases(full_context)
        assert len(results) == 7

    def test_keys_match_phase_values(self, full_context):
        results = generate_all_phases(full_context)
        expected_keys = {phase.value for phase in SDDPhase}
        assert set(results.keys()) == expected_keys

    def test_each_phase_has_both_prompts(self, full_context):
        results = generate_all_phases(full_context)
        for phase_name, prompts in results.items():
            assert "system_prompt" in prompts, f"Missing system_prompt in {phase_name}"
            assert "user_prompt" in prompts, f"Missing user_prompt in {phase_name}"
            assert len(prompts["system_prompt"]) > 50
            assert len(prompts["user_prompt"]) > 50

    def test_persona_consistent_across_phases(self, full_context):
        results = generate_all_phases(full_context)
        persona_desc_fragment = "Solutions Architect"
        for phase_name, prompts in results.items():
            assert persona_desc_fragment in prompts["system_prompt"], (
                f"Persona not reflected in system prompt for {phase_name}"
            )

    def test_project_name_consistent_across_phases(self, full_context):
        results = generate_all_phases(full_context)
        for phase_name, prompts in results.items():
            assert "Payment Gateway" in prompts["user_prompt"], (
                f"Project name missing in user prompt for {phase_name}"
            )

    def test_does_not_mutate_original_context(self, full_context):
        original_phase = full_context.phase
        generate_all_phases(full_context)
        assert full_context.phase == original_phase


# ─────────────────────────────────────────────────────────────────────────────
# 9. Edge Cases & Boundary Tests
# ─────────────────────────────────────────────────────────────────────────────

class TestEdgeCases:
    """Edge-case and boundary tests."""

    def test_empty_project_name(self):
        ctx = SDDContext(project_name="")
        gen = SDDPromptGenerator(ctx)
        prompts = gen.generate_prompts()
        assert isinstance(prompts["system_prompt"], str)
        assert isinstance(prompts["user_prompt"], str)

    def test_very_long_project_name(self):
        long_name = "A" * 1000
        ctx = SDDContext(project_name=long_name)
        gen = SDDPromptGenerator(ctx)
        prompt = gen.generate_user_prompt()
        assert long_name in prompt

    def test_special_characters_in_project_name(self):
        ctx = SDDContext(project_name="Project <X> & 'Y' \"Z\"")
        gen = SDDPromptGenerator(ctx)
        prompt = gen.generate_user_prompt()
        assert "Project <X>" in prompt

    def test_unicode_in_requirements(self):
        ctx = SDDContext(requirements=["支持中文", "日本語サポート", "Ünïcödé"])
        gen = SDDPromptGenerator(ctx)
        prompt = gen.generate_user_prompt()
        assert "支持中文" in prompt
        assert "日本語サポート" in prompt
        assert "Ünïcödé" in prompt

    def test_empty_tech_stack(self):
        ctx = SDDContext(tech_stack=[])
        gen = SDDPromptGenerator(ctx)
        prompt = gen.generate_system_prompt()
        assert isinstance(prompt, str)

    def test_single_tech_stack_item(self):
        ctx = SDDContext(tech_stack=["Haskell"])
        gen = SDDPromptGenerator(ctx)
        prompt = gen.generate_system_prompt()
        assert "Haskell" in prompt

    def test_many_requirements(self):
        reqs = [f"Requirement #{i}" for i in range(50)]
        ctx = SDDContext(requirements=reqs)
        gen = SDDPromptGenerator(ctx)
        prompt = gen.generate_user_prompt()
        assert "Requirement #0" in prompt
        assert "Requirement #49" in prompt

    def test_existing_spec_with_code_block_chars(self):
        ctx = SDDContext(existing_spec="```yaml\nsome: value\n```")
        gen = SDDPromptGenerator(ctx)
        section = gen._build_existing_spec_section()
        assert "```" in section

    def test_verbosity_concise(self):
        ctx = SDDContext(verbosity="concise")
        gen = SDDPromptGenerator(ctx)
        prompt = gen.generate_system_prompt()
        assert "concise" in prompt

    def test_verbosity_verbose(self):
        ctx = SDDContext(verbosity="verbose")
        gen = SDDPromptGenerator(ctx)
        prompt = gen.generate_system_prompt()
        assert "verbose" in prompt

    def test_custom_spec_format(self):
        ctx = SDDContext(spec_format="GraphQL SDL", phase=SDDPhase.API_DESIGN)
        gen = SDDPromptGenerator(ctx)
        prompt = gen.generate_system_prompt()
        assert "GraphQL SDL" in prompt

    def test_output_format_in_system_prompt(self):
        ctx = SDDContext(output_format="json")
        gen = SDDPromptGenerator(ctx)
        prompt = gen.generate_system_prompt()
        assert "json" in prompt


# ─────────────────────────────────────────────────────────────────────────────
# 10. Cross-Persona × Cross-Phase Matrix Test
# ─────────────────────────────────────────────────────────────────────────────

class TestCrossMatrix:
    """Generate prompts for every Persona × Phase combination (9×7 = 63 combos)."""

    @pytest.mark.parametrize("persona", list(Persona))
    @pytest.mark.parametrize("phase", list(SDDPhase))
    def test_every_persona_phase_combination(self, persona, phase):
        ctx = SDDContext(
            project_name="Matrix Test",
            persona=persona,
            phase=phase,
            tech_stack=["TypeScript", "NestJS"],
            domain="healthcare",
            requirements=["HIPAA compliance", "HL7 FHIR support"],
        )
        gen = SDDPromptGenerator(ctx)
        prompts = gen.generate_prompts()

        # System prompt checks
        assert PERSONA_DESCRIPTIONS[persona][:20] in prompts["system_prompt"]
        assert "TypeScript" in prompts["system_prompt"]

        # User prompt checks
        assert "Matrix Test" in prompts["user_prompt"]
        assert "HIPAA" in prompts["user_prompt"]

        # JSON export check
        data = json.loads(gen.to_json())
        assert data["metadata"]["persona"] == persona.value
        assert data["metadata"]["phase"] == phase.value


# ─────────────────────────────────────────────────────────────────────────────
# 11. Consistency & Idempotency Tests
# ─────────────────────────────────────────────────────────────────────────────

class TestConsistency:
    """Ensure repeated generation produces identical results."""

    def test_system_prompt_idempotent(self, full_context):
        gen = SDDPromptGenerator(full_context)
        p1 = gen.generate_system_prompt()
        p2 = gen.generate_system_prompt()
        assert p1 == p2

    def test_user_prompt_idempotent(self, full_context):
        gen = SDDPromptGenerator(full_context)
        p1 = gen.generate_user_prompt()
        p2 = gen.generate_user_prompt()
        assert p1 == p2

    def test_to_json_idempotent(self, full_context):
        gen = SDDPromptGenerator(full_context)
        j1 = gen.to_json()
        j2 = gen.to_json()
        assert j1 == j2

    def test_two_generators_same_context(self, full_context):
        gen1 = SDDPromptGenerator(full_context)
        gen2 = SDDPromptGenerator(full_context)
        assert gen1.generate_prompts() == gen2.generate_prompts()


# ─────────────────────────────────────────────────────────────────────────────
# 12. Regression / Smoke Tests
# ─────────────────────────────────────────────────────────────────────────────

class TestSmoke:
    """Quick smoke tests for overall sanity."""

    def test_demo_context_runs(self, ecommerce_context):
        gen = SDDPromptGenerator(ecommerce_context)
        output = gen.pretty_print()
        assert len(output) > 500

    def test_default_context_runs(self, default_context):
        gen = SDDPromptGenerator(default_context)
        prompts = gen.generate_prompts()
        assert len(prompts["system_prompt"]) > 100
        assert len(prompts["user_prompt"]) > 100

    def test_generate_all_phases_with_defaults(self, default_context):
        results = generate_all_phases(default_context)
        assert len(results) == 7
        for v in results.values():
            assert "system_prompt" in v
            assert "user_prompt" in v


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
