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

from pydantic import BaseModel, ConfigDict, StrictStr
from typing_extensions import Self


class WebResources(BaseModel):
    """
    WebResources
    """  # noqa: E501

    careers: Optional[StrictStr] = None
    about: Optional[StrictStr] = None
    blog: Optional[StrictStr] = None
    events: Optional[StrictStr] = None
    sitemap: Optional[StrictStr] = None
    updates: Optional[StrictStr] = None
    linkedin: Optional[StrictStr] = None
    facebook: Optional[StrictStr] = None
    instagram: Optional[StrictStr] = None
    medium: Optional[StrictStr] = None
    reddit: Optional[StrictStr] = None
    threads: Optional[StrictStr] = None
    tiktok: Optional[StrictStr] = None
    x: Optional[StrictStr] = None
    wellfound: Optional[StrictStr] = None
    youtube: Optional[StrictStr] = None
    wikipedia: Optional[StrictStr] = None
    __properties: ClassVar[List[str]] = [
        "careers",
        "about",
        "blog",
        "events",
        "sitemap",
        "updates",
        "linkedin",
        "facebook",
        "instagram",
        "medium",
        "reddit",
        "threads",
        "tiktok",
        "x",
        "wellfound",
        "youtube",
        "wikipedia",
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
        """Create an instance of WebResources from a JSON string"""
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
        # set to None if careers (nullable) is None
        # and model_fields_set contains the field
        if self.careers is None and "careers" in self.model_fields_set:
            _dict["careers"] = None

        # set to None if about (nullable) is None
        # and model_fields_set contains the field
        if self.about is None and "about" in self.model_fields_set:
            _dict["about"] = None

        # set to None if blog (nullable) is None
        # and model_fields_set contains the field
        if self.blog is None and "blog" in self.model_fields_set:
            _dict["blog"] = None

        # set to None if events (nullable) is None
        # and model_fields_set contains the field
        if self.events is None and "events" in self.model_fields_set:
            _dict["events"] = None

        # set to None if sitemap (nullable) is None
        # and model_fields_set contains the field
        if self.sitemap is None and "sitemap" in self.model_fields_set:
            _dict["sitemap"] = None

        # set to None if updates (nullable) is None
        # and model_fields_set contains the field
        if self.updates is None and "updates" in self.model_fields_set:
            _dict["updates"] = None

        # set to None if linkedin (nullable) is None
        # and model_fields_set contains the field
        if self.linkedin is None and "linkedin" in self.model_fields_set:
            _dict["linkedin"] = None

        # set to None if facebook (nullable) is None
        # and model_fields_set contains the field
        if self.facebook is None and "facebook" in self.model_fields_set:
            _dict["facebook"] = None

        # set to None if instagram (nullable) is None
        # and model_fields_set contains the field
        if self.instagram is None and "instagram" in self.model_fields_set:
            _dict["instagram"] = None

        # set to None if medium (nullable) is None
        # and model_fields_set contains the field
        if self.medium is None and "medium" in self.model_fields_set:
            _dict["medium"] = None

        # set to None if reddit (nullable) is None
        # and model_fields_set contains the field
        if self.reddit is None and "reddit" in self.model_fields_set:
            _dict["reddit"] = None

        # set to None if threads (nullable) is None
        # and model_fields_set contains the field
        if self.threads is None and "threads" in self.model_fields_set:
            _dict["threads"] = None

        # set to None if tiktok (nullable) is None
        # and model_fields_set contains the field
        if self.tiktok is None and "tiktok" in self.model_fields_set:
            _dict["tiktok"] = None

        # set to None if x (nullable) is None
        # and model_fields_set contains the field
        if self.x is None and "x" in self.model_fields_set:
            _dict["x"] = None

        # set to None if wellfound (nullable) is None
        # and model_fields_set contains the field
        if self.wellfound is None and "wellfound" in self.model_fields_set:
            _dict["wellfound"] = None

        # set to None if youtube (nullable) is None
        # and model_fields_set contains the field
        if self.youtube is None and "youtube" in self.model_fields_set:
            _dict["youtube"] = None

        # set to None if wikipedia (nullable) is None
        # and model_fields_set contains the field
        if self.wikipedia is None and "wikipedia" in self.model_fields_set:
            _dict["wikipedia"] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of WebResources from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "careers": obj.get("careers"),
                "about": obj.get("about"),
                "blog": obj.get("blog"),
                "events": obj.get("events"),
                "sitemap": obj.get("sitemap"),
                "updates": obj.get("updates"),
                "linkedin": obj.get("linkedin"),
                "facebook": obj.get("facebook"),
                "instagram": obj.get("instagram"),
                "medium": obj.get("medium"),
                "reddit": obj.get("reddit"),
                "threads": obj.get("threads"),
                "tiktok": obj.get("tiktok"),
                "x": obj.get("x"),
                "wellfound": obj.get("wellfound"),
                "youtube": obj.get("youtube"),
                "wikipedia": obj.get("wikipedia"),
            }
        )
        return _obj
