"""
Unit tests for Shovels API Pydantic models.

Tests validation, defaults, and error cases for all model classes.
"""

import pydantic
import pytest

from src.models.shovels_models import (
    PermitSearchResult,
    ContractorSearchResult,
    GeoResult,
    PermitDetail,
    ContractorDetail,
    SearchResponse,
    PermitsSearchParams,
    ContractorsSearchParams,
    GeoParams,
    ErrorResponse,
    Tag,
    UsageInfo,
    ContractorEmployee,
    ContractorMetric,
)


# ─── Search result models ─────────────────────────────────

class TestPermitSearchResult:
    """PermitSearchResult validation tests."""

    def test_valid_permit(self):
        data = {
            "id": "abc123",
            "number": "RE2303928",
            "type": "electrical - 1 & 2 unit residential",
            "status": "active",
            "job_value_cents": 500000,
            "city": "OAKLAND",
            "state": "CA",
            "contractor_id": "KOm4dMLIuT",
            "resource": "shovels://permits/abc123",
        }
        result = PermitSearchResult(**data)
        assert result.id == "abc123"
        assert result.number == "RE2303928"
        assert result.type == "electrical - 1 & 2 unit residential"
        assert result.status == "active"
        assert result.job_value_cents == 500000
        assert result.city == "OAKLAND"
        assert result.state == "CA"
        assert result.contractor_id == "KOm4dMLIuT"
        assert result.resource == "shovels://permits/abc123"

    def test_minimal_permit(self):
        """Only required fields (id, resource)."""
        result = PermitSearchResult(id="x", resource="shovels://permits/x")
        assert result.id == "x"
        assert result.resource == "shovels://permits/x"
        # Optional fields should have defaults
        assert result.number == ""
        assert result.job_value_cents is None

    def test_missing_id_raises(self):
        with pytest.raises(pydantic.ValidationError):
            PermitSearchResult(resource="shovels://permits/x")

    def test_missing_resource_raises(self):
        with pytest.raises(pydantic.ValidationError):
            PermitSearchResult(id="x")


class TestContractorSearchResult:
    """ContractorSearchResult validation tests."""

    def test_valid_contractor(self):
        data = {
            "id": "cnt-123",
            "name": "ABC Construction",
            "classification": "General",
            "city": "Austin",
            "state": "TX",
            "license_number": "LIC12345",
            "resource": "shovels://contractors/cnt-123",
        }
        result = ContractorSearchResult(**data)
        assert result.id == "cnt-123"
        assert result.name == "ABC Construction"
        assert result.license_number == "LIC12345"

    def test_minimal_contractor(self):
        result = ContractorSearchResult(id="x", resource="shovels://contractors/x")
        assert result.name == ""
        assert result.city is None


class TestGeoResult:
    """GeoResult validation tests."""

    def test_valid_geo(self):
        data = {
            "geo_id": "geo_tx_austin",
            "level": "city",
            "display_name": "Austin, TX",
            "state_code": "TX",
        }
        result = GeoResult(**data)
        assert result.geo_id == "geo_tx_austin"
        assert result.display_name == "Austin, TX"
        assert result.state_code == "TX"

    def test_geo_without_state_code(self):
        """state_code is optional."""
        result = GeoResult(
            geo_id="geo_tx",
            level="state",
            display_name="Texas",
        )
        assert result.geo_id == "geo_tx"
        assert result.state_code is None


# ─── Full detail models ───────────────────────────────────

class TestPermitDetail:
    """PermitDetail validation tests."""

    def test_valid_full_permit(self):
        data = {
            "id": "p123",
            "number": "RE2303928",
            "type": "electrical",
            "status": "active",
            "description": "Full electrical rewiring",
            "job_value_cents": 500000,
            "fees_cents": 25000,
            "property_type": "Residential",
            "city": "OAKLAND",
            "state": "CA",
            "tags": ["electrical", "residential"],
        }
        result = PermitDetail(**data)
        assert result.id == "p123"
        assert result.job_value_cents == 500000
        assert result.tags == ["electrical", "residential"]

    def test_all_optional_fields_can_be_none(self):
        """All non-required fields should accept None."""
        result = PermitDetail(id="p123")
        assert result.number == ""
        assert result.job_value_cents is None
        assert result.tags == []


class TestContractorDetail:
    """ContractorDetail validation tests."""

    def test_valid_full_contractor(self):
        data = {
            "id": "c123",
            "name": "ABC Corp",
            "classification_derived": "General",
            "license_number": "LIC-001",
            "total_job_value_cents": 1000000,
        }
        result = ContractorDetail(**data)
        assert result.name == "ABC Corp"
        assert result.total_job_value_cents == 1000000

    def test_minimal_contractor_detail(self):
        result = ContractorDetail(id="c123")
        assert result.license_number is None
        assert result.active_permits_count is None


# ─── Generic SearchResponse ──────────────────────────────

class TestSearchResponse:
    """Generic SearchResponse[T] tests."""

    def test_empty_response(self):
        response = SearchResponse[PermitSearchResult]()
        assert response.items == []
        assert response.size == 0
        assert response.next_cursor is None
        assert response.credits_remaining is None

    def test_with_items(self):
        items = [
            PermitSearchResult(id="1", resource="shovels://permits/1"),
            PermitSearchResult(id="2", resource="shovels://permits/2"),
        ]
        response = SearchResponse[PermitSearchResult](
            items=items,
            size=2,
            next_cursor="cursor_abc",
            credits_remaining=200,
        )
        assert len(response.items) == 2
        assert response.size == 2
        assert response.next_cursor == "cursor_abc"
        assert response.credits_remaining == 200

    def test_with_contractor_items(self):
        items = [ContractorSearchResult(id="c1", resource="r1")]
        response = SearchResponse[ContractorSearchResult](items=items, size=1)
        assert len(response.items) == 1
        assert response.items[0].id == "c1"


# ─── Request param models ────────────────────────────────

class TestPermitsSearchParams:
    """PermitsSearchParams validation tests."""

    def test_valid_params(self):
        params = PermitsSearchParams(
            geo_id="geo_tx",
            permit_from="2026-01-01",
            permit_to="2026-06-30",
        )
        assert params.geo_id == "geo_tx"
        assert params.size == 20  # default

    def test_missing_geo_id_raises(self):
        with pytest.raises(pydantic.ValidationError):
            PermitsSearchParams(permit_from="2026-01-01", permit_to="2026-06-30")

    def test_size_bounds(self):
        with pytest.raises(pydantic.ValidationError):
            PermitsSearchParams(
                geo_id="x", permit_from="2026-01-01", permit_to="2026-06-30", size=0
            )
        with pytest.raises(pydantic.ValidationError):
            PermitsSearchParams(
                geo_id="x", permit_from="2026-01-01", permit_to="2026-06-30", size=101
            )

    def test_optional_filters(self):
        params = PermitsSearchParams(
            geo_id="geo_tx",
            permit_from="2026-01-01",
            permit_to="2026-06-30",
            permit_tags=["roofing"],
            permit_status=["active"],
            permit_min_job_value=100000,
        )
        assert params.permit_tags == ["roofing"]
        assert params.permit_min_job_value == 100000


class TestContractorsSearchParams:
    """ContractorsSearchParams validation tests."""

    def test_valid_params(self):
        params = ContractorsSearchParams(
            geo_id="geo_tx",
            permit_from="2026-01-01",
            permit_to="2026-06-30",
        )
        assert params.geo_id == "geo_tx"

    def test_contractor_name_min_length(self):
        """contractor_name requires at least 3 chars."""
        with pytest.raises(pydantic.ValidationError):
            ContractorsSearchParams(
                geo_id="x",
                permit_from="2026-01-01",
                permit_to="2026-06-30",
                contractor_name="AB",  # too short
            )

    def test_contractor_name_valid(self):
        params = ContractorsSearchParams(
            geo_id="x",
            permit_from="2026-01-01",
            permit_to="2026-06-30",
            contractor_name="ABC",
        )
        assert params.contractor_name == "ABC"


class TestGeoParams:
    """GeoParams validation tests."""

    def test_valid_geo_params(self):
        params = GeoParams(query="Austin, TX")
        assert params.query == "Austin, TX"
        assert params.level is None

    def test_with_level(self):
        params = GeoParams(query="Austin, TX", level="city")
        assert params.level == "city"

    def test_missing_query_raises(self):
        with pytest.raises(pydantic.ValidationError):
            GeoParams()


class TestErrorResponse:
    """ErrorResponse validation tests."""

    def test_valid_error(self):
        err = ErrorResponse(error="not_found", message="Resource not found")
        assert err.error == "not_found"
        assert err.details is None

    def test_with_details(self):
        err = ErrorResponse(error="bad_request", message="Invalid params", details={"field": "geo_id"})
        assert err.details == {"field": "geo_id"}


# ─── New v2 models ───────────────────────────────────────

class TestTag:
    """Tag model tests."""

    def test_valid_tag(self):
        tag = Tag(tag="new_construction", description="New building construction")
        assert tag.tag == "new_construction"
        assert tag.description == "New building construction"

    def test_tag_without_description(self):
        tag = Tag(tag="alteration")
        assert tag.tag == "alteration"
        assert tag.description is None


class TestUsageInfo:
    """UsageInfo model tests."""

    def test_valid_usage(self):
        usage = UsageInfo(credits_used=1, credits_remaining=199, credits_limit=250)
        assert usage.credits_used == 1
        assert usage.credits_remaining == 199

    def test_default_values(self):
        usage = UsageInfo()
        assert usage.credits_used == 0


class TestContractorEmployee:
    """ContractorEmployee model tests."""

    def test_valid_employee(self):
        emp = ContractorEmployee(id="e1", name="Jane Smith", role="Electrician")
        assert emp.name == "Jane Smith"
        assert emp.role == "Electrician"

    def test_employee_without_role(self):
        emp = ContractorEmployee(id="e1", name="Jane Smith")
        assert emp.role is None


class TestContractorMetric:
    """ContractorMetric model tests."""

    def test_valid_metric(self):
        metric = ContractorMetric(month="2026-01", total_job_value_cents=500000, permit_count=5)
        assert metric.month == "2026-01"
        assert metric.permit_count == 5

    def test_minimal_metric(self):
        metric = ContractorMetric(month="2026-01")
        assert metric.total_job_value_cents is None
