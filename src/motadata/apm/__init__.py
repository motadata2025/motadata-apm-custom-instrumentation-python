#
#   Copyright (c) Motadata 2026. All rights reserved.
#
#   This source code is the property of Motadata and constitutes
#   proprietary and confidential information. Unauthorized copying, distribution,
#   modification, or use of this file, via any medium, is strictly prohibited
#   unless prior written permission is obtained from Motadata.
#
#   For inquiries, contact: engg@motadata.com
#

"""
Motadata APM Custom Instrumentation for Python
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Lightweight OpenTelemetry utility for adding safe, prefixed span attributes.

Usage::

    from motadata.apm import CustomInstrumentation

    # Scalar attributes examples
    CustomInstrumentation.set("user.id", 12345)
    CustomInstrumentation.set("user.name", "john.doe")
    CustomInstrumentation.set("request.success", True)

    # List attributes example
    CustomInstrumentation.set_str_list("tags", ["api", "production", "critical"])

All attribute keys are automatically prefixed with ``apm.``
(e.g. ``apm.user.id``, ``apm.user.name``).
"""

from .custom_instrumentation import CustomInstrumentation
 
__all__ = [ "CustomInstrumentation", ]

__version__ = "1.0.0"
