# Motadata APM Custom Instrumentation for Python

[![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![pip Version](https://img.shields.io/badge/pip-20%2B-blue.svg)](https://pip.pypa.io/)
[![OpenTelemetry](https://img.shields.io/badge/OpenTelemetry-Compatible-brightgreen.svg)](https://opentelemetry.io/)
[![License](https://img.shields.io/badge/License-Proprietary-red.svg)](LICENSE)

A lightweight, enterprise-grade utility designed to simplify custom instrumentation for Python applications using OpenTelemetry. Built as a seamless extension of Motadata Auto Instrumentation, it ensures that custom attributes can be safely added to auto-generated traces, with validated keys and consistent namespacing.

---

## Table of Contents

- [Overview](#overview)
- [Requirements](#requirements)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [API at a Glance](#api-at-a-glance)
- [Behavior & Validation](#behavior--validation)
- [Best Practices](#best-practices)
- [Support](#support)
- [License](#license)
- [Acknowledgments](#acknowledgments)

---

## Overview

Motadata APM Custom Instrumentation helps you attach business context to traces while enforcing key validation and consistent naming. Keys are normalized and namespaced automatically, and the API is simple to adopt across services.

> **Prerequisite:** Instrument your app first with **[Motadata Auto Instrumentation](https://docs.motadata.com/motadata-aiops-docs/apm/apm-in-motadata/)** so the OpenTelemetry context is available.

**Use Cases:**
- Adding business context to distributed traces
- Enriching spans with application-specific metadata
- Implementing custom APM attributes and observability markers
- Standardizing telemetry key naming across microservices

---

## Requirements

- Python 3.9+
- pip 20+
- Motadata APM agent (auto-instrumented)

---

## Installation

Install from PyPI:

```bash
pip install motadata-apm-custom-instrumentation-python
```

Install from source repository:

```bash
pip install git+https://github.com/motadata2025/motadata-apm-custom-instrumentation-python.git
```

---

## Quick Start

```python
from motadata.apm import CustomInstrumentation

CustomInstrumentation.set("apm.user.id", 12345)
CustomInstrumentation.set("apm.user.name", "john.doe")
CustomInstrumentation.set("apm.request.success", True)
CustomInstrumentation.set_str_list("apm.tags", ["api", "production", "critical"])
```

Keys are automatically prefixed with `apm.` when missing, but for consistency prefer passing prefixed keys directly.

Since this package raises exceptions at runtime for invalid inputs or span-context failures, wrap calls in `try/except` in production code:

```python
from motadata.apm import CustomInstrumentation

try:
    CustomInstrumentation.set("apm.order.id", order_id)
except Exception as err:
    logger.warning("Failed to set apm.order.id: %s", err)
```

---

## API at a Glance

### Scalar

| Method | Parameter |
|--------|-----------|
| `set(key, value)` | `bool`, `int`, `float`, or `str` |

### Collections

| Method | Parameter |
|--------|-----------|
| `set_str_list(key, values)` | `Sequence[str]` |
| `set_int_list(key, values)` | `Sequence[int]` |
| `set_float_list(key, values)` | `Sequence[float]` |
| `set_bool_list(key, values)` | `Sequence[bool]` |

---

## Behavior & Validation

- Keys are trimmed, lowercased, and auto-prefixed with `apm.` when missing.
- Only alphanumeric characters and dots are allowed in keys.
- Uses OpenTelemetry current span context (`trace.get_current_span()`) for attribute attachment.
- Scalars must not be `None`.
- Floats must be finite (no `NaN` or `Infinity`).
- List methods reject `None`/empty lists.
- `set_str_list`, `set_int_list`, and `set_bool_list` drop `None` values.
- `set_float_list` drops `None`, `NaN`, and `Infinity` values.
- Each list must retain at least one valid value after filtering.
- Raises `Exception` for invalid input or span retrieval failures.

Key rules: not null/empty, no whitespace, only alphanumeric and dots, lowercased, prefixed `apm.`.
Value rules: scalar not null, scalar float finite, list not null/empty, and list non-empty after filtering.

---

## Best Practices

- Use descriptive, hierarchical keys already prefixed with `apm.` (for example, `apm.order.id`).
- Choose correct types: IDs as integers, metrics as floats, flags as booleans.
- Use list setters for collections and let filtering happen inside the library.
- Keep key naming consistent across services to simplify querying.

---

## Support

- Email: engg@motadata.com
- Issues: GitHub Issues on this repository
- Documentation: README and inline package docstrings

When reporting issues, include:
1. Package version (`1.0.0`)
2. Python version
3. `opentelemetry-api` version
4. Full traceback
5. Minimal reproducible snippet

For contribution inquiries on this proprietary package, contact engg@motadata.com.

---

## License

**Copyright (c) 2026 Motadata. All rights reserved.**

Proprietary software; see [LICENSE](LICENSE) for full terms.

---

## Acknowledgments

Built by the Motadata Engineering Team.

Powered by [OpenTelemetry](https://opentelemetry.io/).
