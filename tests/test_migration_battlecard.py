"""Unit tests for the growth.migration_battlecard contributed workflow package."""

import json
import re
from pathlib import Path

import jsonschema
import pytest

from tin_lite.community import ContributedPackage, validate
from tin_lite.workflow_qualification import Qualification

ROOT = Path(__file__).parents[1]
PACKAGE_DIR = ROOT / "workflow_packages" / "growth.migration_battlecard"
EVALS_DIR = ROOT / "workflow_evals" / "growth.migration_battlecard"


def extract_rubric_engine() -> dict:
    """Extract and compile the single Python block embedded in RUBRIC.md."""
    rubric_path = PACKAGE_DIR / "skills" / "migration-battlecard" / "RUBRIC.md"
    content = rubric_path.read_text(encoding="utf-8")
    blocks = re.findall(r"```python\n(.*?)\n```", content, re.DOTALL)
    assert len(blocks) == 1, "RUBRIC.md must contain exactly one embedded Python code block"
    namespace = {}
    exec(compile(blocks[0], str(rubric_path), "exec"), namespace)  # noqa: S102
    return namespace


@pytest.fixture
def rubric_engine():
    return extract_rubric_engine()


async def test_migration_battlecard_package_validates_under_tin_community():
    """Verify package passes static community validation without error."""
    package = ContributedPackage(key="growth.migration_battlecard", path=PACKAGE_DIR)
    # validate() returns None on success, raises ValueError on contract violation
    await validate(package, root=ROOT)


def test_manifest_schema_and_boundaries():
    """Verify manifest structural boundaries and strict input constraints."""
    manifest_path = PACKAGE_DIR / "workflow.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert manifest["package_format"] == "tin-workflow-package-v1"
    definition = manifest["definition"]
    assert definition["key"] == "growth.migration_battlecard"
    assert definition["executor"] == "codex.procedure"
    assert definition["schedule_modes"] == ["on_demand"]
    assert definition["version"] == "1.0.0"

    schema = definition["input_schema"]
    assert schema["type"] == "object"
    assert schema["additionalProperties"] is False
    assert set(schema["required"]) == {"project_id", "competitor_name", "competitor_domain"}

    # Every string property other than project_id must declare a maxLength
    properties = schema["properties"]
    for prop_name, prop_spec in properties.items():
        if prop_name != "project_id" and prop_spec.get("type") == "string":
            assert "maxLength" in prop_spec, f"Property {prop_name} is missing maxLength"
            assert prop_spec["maxLength"] > 0

    assert properties["project_id"]["format"] == "uuid"
    assert properties["migration_complexity"]["enum"] == ["low", "medium", "high"]

    # Procedure output boundary
    output = definition["procedure"]["output"]
    assert output["kind"] == "project.artifact"
    assert output["path"] == "reports/MIGRATION_BATTLECARD.md"
    assert output["media_type"] == "text/markdown"
    assert 1000 <= output["max_bytes"] <= 1_000_000


def test_skill_frontmatter_and_declared_resources():
    """Verify that skill frontmatter matches directory name and all resources exist."""
    skill_file = PACKAGE_DIR / "skills" / "migration-battlecard" / "SKILL.md"
    assert skill_file.is_file()

    text = skill_file.read_text(encoding="utf-8")
    assert text.startswith("---\nname: migration-battlecard\n")

    manifest = json.loads((PACKAGE_DIR / "workflow.json").read_text(encoding="utf-8"))
    declared_files = manifest["definition"]["procedure"]["skill_files"]

    for rel_path in declared_files:
        full_path = PACKAGE_DIR / rel_path
        assert full_path.is_file(), f"Declared skill file missing: {rel_path}"

    # Prompt file existence
    prompt_file = PACKAGE_DIR / manifest["definition"]["procedure"]["prompt_path"]
    assert prompt_file.is_file()
    assert len(prompt_file.read_text(encoding="utf-8").strip()) > 20


def test_input_schema_validation_against_sample_payloads():
    """Verify that input_schema accepts valid inputs and rejects invalid shapes."""
    manifest = json.loads((PACKAGE_DIR / "workflow.json").read_text(encoding="utf-8"))
    schema = manifest["definition"]["input_schema"]

    valid_payload = {
        "project_id": "9f44dde4-ef47-4aa3-b8ca-959ea628963e",
        "competitor_name": "Mixpanel",
        "competitor_domain": "mixpanel.com",
        "target_persona": "Growth Engineers",
        "migration_complexity": "medium",
    }
    jsonschema.validate(valid_payload, schema)

    # Missing required field
    invalid_missing = {
        "project_id": "9f44dde4-ef47-4aa3-b8ca-959ea628963e",
        "competitor_domain": "mixpanel.com",
    }
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(invalid_missing, schema)

    # Invalid enum value
    invalid_enum = {**valid_payload, "migration_complexity": "extreme"}
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(invalid_enum, schema)

    # Exceeding maxLength
    invalid_length = {**valid_payload, "competitor_name": "x" * 81}
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(invalid_length, schema)


def test_rubric_economic_payback_engine(rubric_engine):
    """Verify the quantitative economic model embedded in RUBRIC.md."""
    calc_payback = rubric_engine["calculate_migration_payback"]
    calc_tco = rubric_engine["calculate_tco_trajectory"]
    score_feasibility = rubric_engine["score_migration_feasibility"]

    # Canonical viable migration: 40 hrs @ $120/hr ($4,800), saving $2,000/mo
    result = calc_payback(
        migration_hours=40,
        blended_hourly_rate=120,
        incumbent_monthly_cost=2500,
        target_monthly_cost=500,
    )
    assert result["migration_investment_usd"] == 4800.0
    assert result["monthly_savings_usd"] == 2000.0
    assert result["payback_months"] == 2.4
    assert result["viable"] is True
    assert result["status"] == "viable"
    assert result["annual_net_savings_usd"] == 19200.0

    # Extended payback (> 6 months but <= 12 months)
    extended = calc_payback(
        migration_hours=80,
        blended_hourly_rate=150,
        incumbent_monthly_cost=3000,
        target_monthly_cost=1500,
    )
    assert extended["payback_months"] == 8.0
    assert extended["viable"] is True
    assert extended["status"] == "extended_payback"

    # Cost-negative or neutral scenario
    neutral = calc_payback(
        migration_hours=20,
        blended_hourly_rate=100,
        incumbent_monthly_cost=1000,
        target_monthly_cost=1200,
    )
    assert neutral["viable"] is False
    assert neutral["payback_months"] is None
    assert neutral["status"] == "cost_negative_or_neutral"

    # Invalid input boundaries
    with pytest.raises(ValueError):
        calc_payback(
            migration_hours=-10,
            blended_hourly_rate=100,
            incumbent_monthly_cost=1000,
            target_monthly_cost=500,
        )

    # TCO Multi-year trajectory test
    tco = calc_tco(incumbent_base_monthly=2000, target_base_monthly=600, years=3)
    assert len(tco) == 3
    assert tco[0]["year"] == 1
    assert tco[0]["incumbent_annual_spend"] == 24000.0
    assert tco[0]["target_annual_spend"] == 7200.0
    assert tco[0]["annual_savings"] == 16800.0
    assert tco[1]["annual_savings"] > tco[0]["annual_savings"]

    # Feasibility scoring test
    feasibility = score_feasibility(
        lock_in_classes=["Class A", "Class B"],
        complexity_tier="medium",
    )
    assert 0 <= feasibility["feasibility_score"] <= 100
    assert feasibility["risk_level"] in {"low", "moderate", "elevated"}
    assert feasibility["recommended_buffer_days"] == 7


def test_qualification_spec_conformance():
    """Verify qualification.json adheres to Tin qualification contract schema."""
    qual_path = EVALS_DIR / "qualification.json"
    assert qual_path.is_file()

    qual = Qualification.model_validate_json(qual_path.read_bytes())
    assert qual.version == 1
    assert len(qual.cases) == 3
    case_ids = {c.id for c in qual.cases}
    assert case_ids == {"ordinary", "high_complexity", "low_complexity_stateless"}
    assert len(qual.rubric) == 4
    assert any("MIGRATION_BATTLECARD.md" in effect for effect in qual.effects)
