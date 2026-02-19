#
#   Copyright (c) Motadata 2026. All rights reserved.
#
#   This source code is the property of Motadata and constitutes
#   proprietary and confidential information. Unauthorized copying, distribution,
#   modification, or use of this file, via any medium, is strictly prohibited
#   unless prior written permission is obtained from Motadata.
#
#   Unauthorized access or use of this software may result in legal action
#   and/or prosecution to the fullest extent of the law.
#
#   This software is provided "AS IS," without warranties of any kind, express
#   or implied, including but not limited to implied warranties of
#   merchantability or fitness for a particular purpose. In no event shall
#   Motadata be held liable for any damages arising from the use
#   of this software.
#
#   For inquiries, contact: engg@motadata.com
#

"""
Utility class for setting custom instrumentation attributes on OpenTelemetry spans.

This module provides functionality for:

- Setting scalar attributes (``bool``, ``int``, ``float``, ``str``) on the current span
- Setting list attributes (``Sequence[bool]``, ``Sequence[int]``, ``Sequence[float]``, ``Sequence[str]``) on the current span
- Validation of attribute keys and values with descriptive error messages

All attribute keys are automatically prefixed with ``apm.`` unless already present.
This ensures consistent namespacing for APM-related attributes across the application.

**Thread-safe:** All methods operate on the current span context which is thread-local.
The class depends only on the OpenTelemetry ``trace.get_current_span()`` method for span access.

.. versionadded:: 1.0.0
"""

import math
import re
from typing import Optional, Sequence, Union

from opentelemetry import trace

# Supported scalar types for the ``set`` method.
_ScalarValue = Union[bool, int, float, str]

_DEFAULT_PREFIX = "apm."

_KEY_VALIDATION_PATTERN = re.compile(r"^[a-zA-Z0-9.]+$")


class CustomInstrumentation:
    """
    Utility class for setting custom instrumentation attributes on OpenTelemetry spans.

    All attribute keys are automatically prefixed with ``apm.`` unless already present.
    Keys are validated to contain only alphanumeric characters and dots, and are converted to lowercase for consistency.

    This is a static utility class and **must not** be instantiated.

    Supported scalar types: ``bool``, ``int``, ``float``, ``str``

    Supported list types: ``Sequence[bool]``, ``Sequence[int]``, ``Sequence[float]``, ``Sequence[str]``

    :raises Exception: if the key is invalid, value is ``None``, or if no active span is available in the current context.

    .. versionadded:: 1.0.0
    """

    def __init__(self) -> None:
        raise RuntimeError(f"{CustomInstrumentation.__name__} is a utility class and should not be instantiated")


    @staticmethod
    def _prepare_key(key: Optional[str]) -> str:
        """
        Prepares and validates the attribute key for use with OpenTelemetry spans.

        This method performs the following operations:

        1. Validates that the key is not null
        2. Trims whitespace from the key and validates that the key is not empty after trimming
        3. Validates that the key does not contain invalid whitespace characters
        4. Converts the key to lowercase for consistency
        5. Adds the "apm." prefix if not already present

        :param key: The original attribute key
        :return: The prepared key with "apm." prefix in lowercase
        :raises Exception: if the key is null, empty, or contains invalid characters
        """
        if key is None:
            raise Exception("Attribute key cannot be null")

        key = key.strip()

        if not key:
            raise Exception("Attribute key cannot be empty")

        if any(c.isspace() for c in key):
            raise Exception("Attribute key contains invalid whitespace characters")

        if not _KEY_VALIDATION_PATTERN.match(key):
            raise Exception(f"Attribute key contains invalid characters. Only alphabets, numbers, and dots are allowed: '{key}'")

        key = key.lower()

        return key if key.startswith(_DEFAULT_PREFIX) else _DEFAULT_PREFIX + key

    @staticmethod
    def _validate_value(value: object, key: str) -> None:
        """Raise if *value* is ``None``."""
        if value is None:
            raise Exception(f"Attribute value cannot be null for key: {key}")

    @staticmethod
    def _validate_list(values: Optional[Sequence[object]], key: str) -> None:
        """Raise if *values* is ``None`` or empty."""
        if values is None:
            raise Exception(f"List cannot be null for key: {key}")

        if len(values) == 0:
            raise Exception(f"List cannot be empty for key: {key}")

    @staticmethod
    def _filter_null_values(values: Sequence[object], key: str) -> list:
        """Filter out ``None`` values from a list.

        :param values: The input list to filter.
        :param key: The attribute key (used in error messages).
        :returns: A new list containing only non-``None`` values.
        :raises Exception: if the filtered list is empty.
        """
        filtered = [v for v in values if v is not None]

        if not filtered:
            raise Exception(f"List contains only null values for key: {key}")

        return filtered

    @staticmethod
    def _filter_floats(values: Sequence[object], key: str) -> list:
        """Filter out ``None``, ``NaN``, and ``Inf`` values from a float list.

        :param values: The input list to filter.
        :param key: The attribute key (used in error messages).
        :returns: A new list containing only valid float values.
        :raises Exception: if the filtered list is empty.
        """
        filtered = [
            v for v in values
            if v is not None and not math.isnan(v) and not math.isinf(v)
        ]

        if not filtered:
            raise Exception(f"List contains only invalid values for key: {key}")

        return filtered

    @staticmethod
    def _get_current_span() -> trace.Span:
        """Return the current recording span or raise."""
        try:
            span = trace.get_current_span()

            if span is None:
                raise Exception("No active span available in current context")

            return span

        except Exception as exc:
            raise Exception("Failed to retrieve current span") from exc

    @staticmethod
    def set(key: str, value: _ScalarValue) -> None:
        """Set a scalar attribute on the current span.

        Supported value types: ``bool``, ``int``, ``float``, ``str``.

        :param key: Attribute key (auto-prefixed with ``apm.`` if needed).
        :param value: The scalar value to set.
        :raises Exception: if the key is invalid, the value is ``None``,
            or a ``float`` that is ``NaN`` / ``Inf``, or if no active span is available.
        """
        key = CustomInstrumentation._prepare_key(key)

        if isinstance(value, float):
            if value is None or math.isnan(value) or math.isinf(value):
                raise Exception(f"Invalid Double value for key: {key}")
        else:
            CustomInstrumentation._validate_value(value, key)

        if not isinstance(value, (bool, int, float, str)):
            raise Exception(f"Unsupported value type '{type(value).__name__}' for key: {key}. Supported types: bool, int, float, str")

        CustomInstrumentation._get_current_span().set_attribute(key, value)

    @staticmethod
    def set_bool_list(key: str, values: Optional[Sequence[bool]]) -> None:
        """Set a boolean list attribute on the current span.

        ``None`` elements are automatically filtered out.

        :param key: Attribute key (auto-prefixed with ``apm.`` if needed).
        :param values: Sequence of booleans (must contain at least one non-``None`` value).
        :raises Exception: if the key is invalid, the list is ``None``, empty,
            or contains only ``None`` values, or if no active span is available.
        """
        key = CustomInstrumentation._prepare_key(key)

        CustomInstrumentation._validate_list(values, key)

        filtered = CustomInstrumentation._filter_null_values(values, key)

        CustomInstrumentation._get_current_span().set_attribute(key, filtered)

    @staticmethod
    def set_int_list(key: str, values: Optional[Sequence[int]]) -> None:
        """Set an integer list attribute on the current span.

        ``None`` elements are automatically filtered out.

        :param key: Attribute key (auto-prefixed with ``apm.`` if needed).
        :param values: Sequence of integers (must contain at least one non-``None`` value).
        :raises Exception: if the key is invalid, the list is ``None``, empty,
            or contains only ``None`` values, or if no active span is available.
        """
        key = CustomInstrumentation._prepare_key(key)

        CustomInstrumentation._validate_list(values, key)

        filtered = CustomInstrumentation._filter_null_values(values, key)

        CustomInstrumentation._get_current_span().set_attribute(key, filtered)

    @staticmethod
    def set_float_list(key: str, values: Optional[Sequence[float]]) -> None:
        """Set a float list attribute on the current span.

        ``None``, ``NaN``, and ``Inf`` elements are automatically filtered out.

        :param key: Attribute key (auto-prefixed with ``apm.`` if needed).
        :param values: Sequence of floats (must contain at least one valid value).
        :raises Exception: if the key is invalid, the list is ``None``, empty,
            or contains only invalid values, or if no active span is available.
        """
        key = CustomInstrumentation._prepare_key(key)

        CustomInstrumentation._validate_list(values, key)

        filtered = CustomInstrumentation._filter_floats(values, key)

        CustomInstrumentation._get_current_span().set_attribute(key, filtered)

    @staticmethod
    def set_str_list(key: str, values: Optional[Sequence[str]]) -> None:
        """Set a string list attribute on the current span.

        ``None`` elements are automatically filtered out.

        :param key: Attribute key (auto-prefixed with ``apm.`` if needed).
        :param values: Sequence of strings (must contain at least one non-``None`` value).
        :raises Exception: if the key is invalid, the list is ``None``, empty,
            or contains only ``None`` values, or if no active span is available.
        """
        key = CustomInstrumentation._prepare_key(key)

        CustomInstrumentation._validate_list(values, key)

        filtered = CustomInstrumentation._filter_null_values(values, key)

        CustomInstrumentation._get_current_span().set_attribute(key, filtered)
