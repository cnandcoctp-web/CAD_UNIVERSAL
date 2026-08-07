# Release Notes RC1

## Version

- Version: `1.0.0rc1`
- Release tag: `v1.0.0-rc1`

## Highlights

- Integrated all completed subsystems into a single release candidate.
- Added installable package metadata through [pyproject.toml](/workspaces/CAD_UNIVERSAL/EVILTECH_CAD/pyproject.toml).
- Added RC1 version surface through [main.py](/workspaces/CAD_UNIVERSAL/EVILTECH_CAD/main.py), [CORE/constants.py](/workspaces/CAD_UNIVERSAL/EVILTECH_CAD/CORE/constants.py), and [VERSION](/workspaces/CAD_UNIVERSAL/EVILTECH_CAD/VERSION).
- Added release-candidate integration coverage in [TEST/test_release_candidate.py](/workspaces/CAD_UNIVERSAL/EVILTECH_CAD/TEST/test_release_candidate.py).
- Updated [README.md](/workspaces/CAD_UNIVERSAL/EVILTECH_CAD/README.md) with launch, build, validation, and release documentation.

## Validation Summary

- Application launch: passed
- Packaging build: passed
- RC1 integration suite: `4 passed`
- Full regression suite: `113 passed`

## Artifact

- Wheel: `dist/eviltech_cad-1.0.0rc1-py3-none-any.whl`
