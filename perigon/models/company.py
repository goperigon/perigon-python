# coding: utf-8

"""
Perigon API

The Perigon API provides access to comprehensive news and web content data. To use the API, simply sign up for a Perigon Business Solutions account to obtain your API key. Your available features may vary based on your plan. See the Authentication section for details on how to use your API key.

The version of the OpenAPI document: 1.0.0
Contact: data@perigon.io
Generated by OpenAPI Generator (https://openapi-generator.tech)

Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations

import json
import pprint
import re  # noqa: F401
from typing import Any, ClassVar, Dict, List, Optional, Set

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictInt, StrictStr
from typing_extensions import Self

from perigon.models.symbol_holder import SymbolHolder
from perigon.models.web_resources import WebResources


class Company(BaseModel):
    """
    Company
    """  # noqa: E501

    id: Optional[StrictStr] = None
    name: Optional[StrictStr] = None
    updated_at: Optional[StrictStr] = Field(default=None, alias="updatedAt")
    primary_record_id: Optional[StrictStr] = Field(
        default=None, alias="primaryRecordId"
    )
    alt_names: Optional[List[StrictStr]] = Field(default=None, alias="altNames")
    domains: Optional[List[StrictStr]] = None
    monthly_visits: Optional[StrictInt] = Field(default=None, alias="monthlyVisits")
    global_rank: Optional[StrictInt] = Field(default=None, alias="globalRank")
    description: Optional[StrictStr] = None
    ceo: Optional[StrictStr] = None
    industry: Optional[StrictStr] = None
    sector: Optional[StrictStr] = None
    country: Optional[StrictStr] = None
    full_time_employees: Optional[StrictInt] = Field(
        default=None, alias="fullTimeEmployees"
    )
    address: Optional[StrictStr] = None
    city: Optional[StrictStr] = None
    state: Optional[StrictStr] = None
    zip: Optional[StrictStr] = None
    logo: Optional[StrictStr] = None
    favicon: Optional[StrictStr] = None
    is_etf: Optional[StrictBool] = Field(default=None, alias="isEtf")
    is_actively_trading: Optional[StrictBool] = Field(
        default=None, alias="isActivelyTrading"
    )
    is_fund: Optional[StrictBool] = Field(default=None, alias="isFund")
    is_adr: Optional[StrictBool] = Field(default=None, alias="isAdr")
    symbols: Optional[List[SymbolHolder]] = None
    naics: Optional[StrictStr] = None
    sic: Optional[StrictStr] = None
    year_founded: Optional[StrictInt] = Field(default=None, alias="yearFounded")
    revenue: Optional[StrictStr] = None
    web_resources: Optional[WebResources] = Field(default=None, alias="webResources")
    __properties: ClassVar[List[str]] = [
        "id",
        "name",
        "updatedAt",
        "primaryRecordId",
        "altNames",
        "domains",
        "monthlyVisits",
        "globalRank",
        "description",
        "ceo",
        "industry",
        "sector",
        "country",
        "fullTimeEmployees",
        "address",
        "city",
        "state",
        "zip",
        "logo",
        "favicon",
        "isEtf",
        "isActivelyTrading",
        "isFund",
        "isAdr",
        "symbols",
        "naics",
        "sic",
        "yearFounded",
        "revenue",
        "webResources",
    ]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of Company from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of each item in symbols (list)
        _items = []
        if self.symbols:
            for _item_symbols in self.symbols:
                if _item_symbols:
                    _items.append(_item_symbols.to_dict())
            _dict["symbols"] = _items
        # override the default output from pydantic by calling `to_dict()` of web_resources
        if self.web_resources:
            _dict["webResources"] = self.web_resources.to_dict()
        # set to None if id (nullable) is None
        # and model_fields_set contains the field
        if self.id is None and "id" in self.model_fields_set:
            _dict["id"] = None

        # set to None if name (nullable) is None
        # and model_fields_set contains the field
        if self.name is None and "name" in self.model_fields_set:
            _dict["name"] = None

        # set to None if updated_at (nullable) is None
        # and model_fields_set contains the field
        if self.updated_at is None and "updated_at" in self.model_fields_set:
            _dict["updatedAt"] = None

        # set to None if primary_record_id (nullable) is None
        # and model_fields_set contains the field
        if (
            self.primary_record_id is None
            and "primary_record_id" in self.model_fields_set
        ):
            _dict["primaryRecordId"] = None

        # set to None if alt_names (nullable) is None
        # and model_fields_set contains the field
        if self.alt_names is None and "alt_names" in self.model_fields_set:
            _dict["altNames"] = None

        # set to None if domains (nullable) is None
        # and model_fields_set contains the field
        if self.domains is None and "domains" in self.model_fields_set:
            _dict["domains"] = None

        # set to None if monthly_visits (nullable) is None
        # and model_fields_set contains the field
        if self.monthly_visits is None and "monthly_visits" in self.model_fields_set:
            _dict["monthlyVisits"] = None

        # set to None if global_rank (nullable) is None
        # and model_fields_set contains the field
        if self.global_rank is None and "global_rank" in self.model_fields_set:
            _dict["globalRank"] = None

        # set to None if description (nullable) is None
        # and model_fields_set contains the field
        if self.description is None and "description" in self.model_fields_set:
            _dict["description"] = None

        # set to None if ceo (nullable) is None
        # and model_fields_set contains the field
        if self.ceo is None and "ceo" in self.model_fields_set:
            _dict["ceo"] = None

        # set to None if industry (nullable) is None
        # and model_fields_set contains the field
        if self.industry is None and "industry" in self.model_fields_set:
            _dict["industry"] = None

        # set to None if sector (nullable) is None
        # and model_fields_set contains the field
        if self.sector is None and "sector" in self.model_fields_set:
            _dict["sector"] = None

        # set to None if country (nullable) is None
        # and model_fields_set contains the field
        if self.country is None and "country" in self.model_fields_set:
            _dict["country"] = None

        # set to None if full_time_employees (nullable) is None
        # and model_fields_set contains the field
        if (
            self.full_time_employees is None
            and "full_time_employees" in self.model_fields_set
        ):
            _dict["fullTimeEmployees"] = None

        # set to None if address (nullable) is None
        # and model_fields_set contains the field
        if self.address is None and "address" in self.model_fields_set:
            _dict["address"] = None

        # set to None if city (nullable) is None
        # and model_fields_set contains the field
        if self.city is None and "city" in self.model_fields_set:
            _dict["city"] = None

        # set to None if state (nullable) is None
        # and model_fields_set contains the field
        if self.state is None and "state" in self.model_fields_set:
            _dict["state"] = None

        # set to None if zip (nullable) is None
        # and model_fields_set contains the field
        if self.zip is None and "zip" in self.model_fields_set:
            _dict["zip"] = None

        # set to None if logo (nullable) is None
        # and model_fields_set contains the field
        if self.logo is None and "logo" in self.model_fields_set:
            _dict["logo"] = None

        # set to None if favicon (nullable) is None
        # and model_fields_set contains the field
        if self.favicon is None and "favicon" in self.model_fields_set:
            _dict["favicon"] = None

        # set to None if is_etf (nullable) is None
        # and model_fields_set contains the field
        if self.is_etf is None and "is_etf" in self.model_fields_set:
            _dict["isEtf"] = None

        # set to None if is_actively_trading (nullable) is None
        # and model_fields_set contains the field
        if (
            self.is_actively_trading is None
            and "is_actively_trading" in self.model_fields_set
        ):
            _dict["isActivelyTrading"] = None

        # set to None if is_fund (nullable) is None
        # and model_fields_set contains the field
        if self.is_fund is None and "is_fund" in self.model_fields_set:
            _dict["isFund"] = None

        # set to None if is_adr (nullable) is None
        # and model_fields_set contains the field
        if self.is_adr is None and "is_adr" in self.model_fields_set:
            _dict["isAdr"] = None

        # set to None if symbols (nullable) is None
        # and model_fields_set contains the field
        if self.symbols is None and "symbols" in self.model_fields_set:
            _dict["symbols"] = None

        # set to None if naics (nullable) is None
        # and model_fields_set contains the field
        if self.naics is None and "naics" in self.model_fields_set:
            _dict["naics"] = None

        # set to None if sic (nullable) is None
        # and model_fields_set contains the field
        if self.sic is None and "sic" in self.model_fields_set:
            _dict["sic"] = None

        # set to None if year_founded (nullable) is None
        # and model_fields_set contains the field
        if self.year_founded is None and "year_founded" in self.model_fields_set:
            _dict["yearFounded"] = None

        # set to None if revenue (nullable) is None
        # and model_fields_set contains the field
        if self.revenue is None and "revenue" in self.model_fields_set:
            _dict["revenue"] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of Company from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "id": obj.get("id"),
                "name": obj.get("name"),
                "updatedAt": obj.get("updatedAt"),
                "primaryRecordId": obj.get("primaryRecordId"),
                "altNames": obj.get("altNames"),
                "domains": obj.get("domains"),
                "monthlyVisits": obj.get("monthlyVisits"),
                "globalRank": obj.get("globalRank"),
                "description": obj.get("description"),
                "ceo": obj.get("ceo"),
                "industry": obj.get("industry"),
                "sector": obj.get("sector"),
                "country": obj.get("country"),
                "fullTimeEmployees": obj.get("fullTimeEmployees"),
                "address": obj.get("address"),
                "city": obj.get("city"),
                "state": obj.get("state"),
                "zip": obj.get("zip"),
                "logo": obj.get("logo"),
                "favicon": obj.get("favicon"),
                "isEtf": obj.get("isEtf"),
                "isActivelyTrading": obj.get("isActivelyTrading"),
                "isFund": obj.get("isFund"),
                "isAdr": obj.get("isAdr"),
                "symbols": (
                    [SymbolHolder.from_dict(_item) for _item in obj["symbols"]]
                    if obj.get("symbols") is not None
                    else None
                ),
                "naics": obj.get("naics"),
                "sic": obj.get("sic"),
                "yearFounded": obj.get("yearFounded"),
                "revenue": obj.get("revenue"),
                "webResources": (
                    WebResources.from_dict(obj["webResources"])
                    if obj.get("webResources") is not None
                    else None
                ),
            }
        )
        return _obj
