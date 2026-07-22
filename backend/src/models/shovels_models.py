"""
Pydantic models for the Shovels API MCP Server.

Defines request/response models for permits, contractors,
decisions, and geo endpoints.
"""

from pydantic import BaseModel, Field
from typing import Generic, Optional, TypeVar, Any
from datetime import date


# ─── Search result items (compact, progressive disclosure) ───

class PermitSearchResult(BaseModel):
    """Compact permit record returned in search mode."""

    id: str = Field(..., description="Permit ID")
    number: str = Field(default="", description="Permit number")
    type: str = Field(default="", description="Permit type (e.g. 'electrical - 1 & 2 unit residential')")
    status: str = Field(default="", description="Permit status (final, in_review, inactive, active)")
    job_value_cents: Optional[int] = Field(default=None, description="Job value in cents")
    city: Optional[str] = Field(default=None, description="City from embedded address")
    state: Optional[str] = Field(default=None, description="State from embedded address")
    contractor_id: Optional[str] = Field(default=None, description="Associated contractor ID")
    resource: str = Field(..., description="URI to fetch full record (e.g. shovels://permits/<id>)")


class ContractorSearchResult(BaseModel):
    """Compact contractor record returned in search mode."""

    id: str = Field(..., description="Contractor ID")
    name: str = Field(default="", description="Contractor name")
    classification: str = Field(default="", description="Trade classification")
    city: Optional[str] = Field(default=None, description="City")
    state: Optional[str] = Field(default=None, description="State")
    license_number: Optional[str] = Field(default=None, description="License number")
    resource: str = Field(..., description="URI to fetch full record")


class DecisionSearchResult(BaseModel):
    """Compact decision record returned in search mode."""

    id: str = Field(..., description="Decision ID")
    category: str = Field(default="", description="Decision category (e.g. Rezoning, Variance)")
    status: str = Field(default="", description="Decision status")
    date: Optional[str] = Field(default=None, description="Decision date")
    description: Optional[str] = Field(default=None, description="Short description")
    resource: str = Field(..., description="URI to fetch full record")


class GeoResult(BaseModel):
    """Geo-resolution result from shovels_geo."""

    geo_id: str = Field(..., description="Shovels geo_id to pass to other tools")
    level: str = Field(..., description="Resolution level: address, city, county, jurisdiction, state")
    display_name: str = Field(..., description="Human-readable name")
    state_code: Optional[str] = Field(default=None, description="Two-letter state code")


# ─── Full detail records (fetch mode) ───

class PermitDetail(BaseModel):
    """Full permit record returned when id is supplied."""

    id: str = Field(..., description="Permit ID")
    number: str = Field(default="", description="Permit number")
    type: str = Field(default="", description="Permit type")
    status: str = Field(default="", description="Permit status")
    status_effective_date: Optional[str] = Field(default=None, description="Date status became effective")
    description: Optional[str] = Field(default=None, description="Permit description")
    job_value_cents: Optional[int] = Field(default=None, description="Job value in cents")
    fees_cents: Optional[int] = Field(default=None, description="Total fees in cents")
    property_assess_market_value_cents: Optional[int] = Field(default=None, description="Assessed market value in cents")
    property_year_built: Optional[int] = Field(default=None, description="Year built")
    property_square_footage: Optional[int] = Field(default=None, description="Square footage")
    property_lot_size_sqft: Optional[int] = Field(default=None, description="Lot size in sq ft")
    property_type: Optional[str] = Field(default=None, description="Property type")
    address_street: Optional[str] = Field(default=None, description="Street address")
    city: Optional[str] = Field(default=None, description="City")
    state: Optional[str] = Field(default=None, description="State")
    zip_code: Optional[str] = Field(default=None, description="ZIP code")
    contractor_id: Optional[str] = Field(default=None, description="Associated contractor ID")
    contractor_name: Optional[str] = Field(default=None, description="Contractor name")
    tags: list[str] = Field(default_factory=list, description="Permit tags")
    permit_from: Optional[str] = Field(default=None, description="Permit start date")
    permit_to: Optional[str] = Field(default=None, description="Permit end date")
    created_at: Optional[str] = Field(default=None, description="Record created date")
    updated_at: Optional[str] = Field(default=None, description="Record last updated date")


class ContractorDetail(BaseModel):
    """Full contractor record returned when id is supplied."""

    id: str = Field(..., description="Contractor ID")
    name: str = Field(default="", description="Contractor name")
    classification_derived: str = Field(default="", description="Trade classification")
    license_number: Optional[str] = Field(default=None, description="License number")
    license_status: Optional[str] = Field(default=None, description="License status")
    phone: Optional[str] = Field(default=None, description="Phone number")
    email: Optional[str] = Field(default=None, description="Email address")
    address_street: Optional[str] = Field(default=None, description="Street address")
    city: Optional[str] = Field(default=None, description="City")
    state: Optional[str] = Field(default=None, description="State")
    zip_code: Optional[str] = Field(default=None, description="ZIP code")
    total_job_value_cents: Optional[int] = Field(default=None, description="Total job value in cents")
    active_permits_count: Optional[int] = Field(default=None, description="Number of active permits")
    created_at: Optional[str] = Field(default=None, description="Record created date")


class DecisionDetail(BaseModel):
    """Full decision record returned when id is supplied."""

    id: str = Field(..., description="Decision ID")
    category: str = Field(default="", description="Decision category (e.g. Rezoning, Variance)")
    status: str = Field(default="", description="Decision status")
    date: Optional[str] = Field(default=None, description="Decision date")
    description: Optional[str] = Field(default=None, description="Full description")
    address_street: Optional[str] = Field(default=None, description="Street address")
    city: Optional[str] = Field(default=None, description="City")
    state: Optional[str] = Field(default=None, description="State")
    zip_code: Optional[str] = Field(default=None, description="ZIP code")
    geo_id: Optional[str] = Field(default=None, description="Associated geo_id")
    created_at: Optional[str] = Field(default=None, description="Record created date")


# ─── Generic search response ───

T = TypeVar("T")


class SearchResponse(BaseModel, Generic[T]):
    """Generic paginated response from Shovels API."""

    items: list[T] = Field(default_factory=list, description="Result items")
    size: int = Field(default=0, description="Number of items in this page")
    next_cursor: Optional[str] = Field(default=None, description="Cursor for next page (null if no more pages)")
    credits_remaining: Optional[int] = Field(default=None, description="API credits remaining for this key")


# ─── Request models ───

class PermitsSearchParams(BaseModel):
    """Parameters for searching permits."""

    geo_id: str = Field(..., min_length=1, description="Required: geo_id from shovels_geo")
    permit_from: str = Field(..., description="Required: start date (YYYY-MM-DD)")
    permit_to: str = Field(..., description="Required: end date (YYYY-MM-DD)")
    permit_tags: Optional[list[str]] = Field(default=None, description="Filter by tags; prefix '-' to exclude")
    permit_status: Optional[list[str]] = Field(default=None, description="Filter by status: final, in_review, inactive, active")
    permit_min_job_value: Optional[int] = Field(default=None, description="Minimum job value in cents")
    contractor_classification_derived: Optional[list[str]] = Field(default=None, description="Filter by contractor classification")
    cursor: Optional[str] = Field(default=None, description="Pagination cursor")
    size: int = Field(default=20, ge=1, le=100, description="Results per page (max 100)")


class PermitsFetchParams(BaseModel):
    """Parameters for fetching full permit records by ID."""

    ids: list[str] = Field(..., min_length=1, description="One or more permit IDs")


class ContractorsSearchParams(BaseModel):
    """Parameters for searching contractors."""

    geo_id: str = Field(..., min_length=1, description="Required: geo_id from shovels_geo")
    permit_from: str = Field(..., description="Required: start date (YYYY-MM-DD)")
    permit_to: str = Field(..., description="Required: end date (YYYY-MM-DD)")
    contractor_classification_derived: Optional[list[str]] = Field(default=None, description="Filter by classification")
    contractor_name: Optional[str] = Field(default=None, min_length=3, description="Name search (min 3 chars)")
    contractor_min_total_job_value: Optional[int] = Field(default=None, description="Minimum total job value in cents")
    cursor: Optional[str] = Field(default=None, description="Pagination cursor")
    size: int = Field(default=20, ge=1, le=100, description="Results per page (max 100)")


class ContractorsFetchParams(BaseModel):
    """Parameters for fetching full contractor records by ID."""

    ids: list[str] = Field(..., min_length=1, description="One or more contractor IDs")


class DecisionsSearchParams(BaseModel):
    """Parameters for searching decisions."""

    geo_id: str = Field(..., min_length=1, description="Required: state or place geo_id (ZIP not supported)")
    decision_from: str = Field(..., description="Required: start date (YYYY-MM-DD)")
    decision_to: str = Field(..., description="Required: end date (YYYY-MM-DD)")
    category: Optional[list[str]] = Field(default=None, description="Filter by category (e.g. Rezoning, Variance)")
    decision_q: Optional[str] = Field(default=None, max_length=100, description="Text search (max 100 chars)")
    cursor: Optional[str] = Field(default=None, description="Pagination cursor")
    size: int = Field(default=20, ge=1, le=100, description="Results per page (max 100)")


class DecisionsFetchParams(BaseModel):
    """Parameters for fetching full decision records by ID."""

    ids: list[str] = Field(..., min_length=1, max_length=50, description="Decision IDs (max 50)")


class GeoParams(BaseModel):
    """Parameters for geo resolution."""

    query: str = Field(..., min_length=1, description="Free-text address, city, county, jurisdiction, or state")
    level: Optional[str] = Field(default=None, description="Target level: address, city, county, jurisdiction, state")


class ErrorResponse(BaseModel):
    """Error response from the API."""

    error: str = Field(..., description="Error code")
    message: str = Field(..., description="Human-readable error message")
    details: Optional[Any] = Field(default=None, description="Additional error details")
