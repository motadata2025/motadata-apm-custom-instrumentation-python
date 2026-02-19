# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-02-17

### Added
- Initial release of Motadata APM Custom Instrumentation for Python.
- Core utility `CustomInstrumentation` for setting span attributes.
- Support for type-safe scalar attributes (`bool`, `int`, `float`, `str`).
- Support for list attributes with automatic `None` filtering.
- Automatic key namespacing with `apm.` prefix.
- Thread-safe implementation using OpenTelemetry's context.
- Standard Python `Exception` handling for all error scenarios.
- Comprehensive documentation and usage examples.
