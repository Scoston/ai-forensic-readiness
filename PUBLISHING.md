# Publication and completion status

Reviewed September 8, 2026 against repository main commit
`0e65affd8ccadba15ce76f75c009a141d10560e4`, the five pre-existing open issues,
all six merged pull requests, and the source specification's build plan.

## Completed repository work

| Item | Evidence / disposition |
| --- | --- |
| Public repository and project identity | Scoston/ai-forensic-readiness; authored by Dr. Stephen Coston |
| Prose/code licensing | CC BY 4.0 prose and diagrams; Apache-2.0 schemas and code retained |
| v0.1 release and citation | Existing v0.1.0-draft archive and DOI retained; not reassigned to v0.2 |
| Initial three cases | Original synthetic bundles and 86 events preserved |
| Remaining seven research cases | Complete failure/control simulation bundles, graphs, manifests and analyst guidance |
| Reproducible control comparisons | Twenty local conditions; supplemental 001-003 models are separate from original evidence |
| Real schema identifiers | Placeholder example.org schema IDs replaced with repository paths |
| Full conformance | Draft 2020-12 validation, format support and positive/negative fixtures |
| Evidence integrity and graph references | All manifests, raw/normalized links, safe paths and graph evidence checked |
| OCSF / OpenTelemetry mappings | Local converters, source-preservation tests, concrete examples and loss disclosure |
| v0.2 synthesis and change disposition | Specification and RFC 0001; public proposal issue 12 |
| Case 003 review question | Evidence-based identity/authority/expiry response and grant-boundary tests |
| Practitioner briefing | Versioned Markdown and PDF review material |
| Review preparation | Focused review kit and blind-exercise form; invitations not sent |
| Repository navigation | README, case index, Pages landing page and assessment updated |

## External and administrative milestones

These items are not replaced by a passing test or a checked box in this repository.

| Item | Current state | Concrete remaining action |
| --- | --- | --- |
| 45-day public review | Open through October 17, 2026 | Receive, evaluate and record actual feedback |
| Named technical review | Review kit prepared; recipients not selected | Select reviewers and send invitations with explicit authorization |
| Independent reproduction / live integration | Not measured | Run the review kit against independent investigators and actual enforcement systems |
| Branch protection | main was unprotected at audit | Owner applies the prepared settings after checking the current CI job names |
| Private vulnerability reporting | Previously reported enabled; no administrative re-verification in this review | Owner confirms in repository security settings |
| v0.2 GitHub Release and Zenodo archive | Candidate files prepared; v0.1 remains the archived release | Finalize review disposition, publish the intended release, verify the new archive and then add its assigned DOI |

The connected repository tools support code, issue and pull-request work but do
not expose administration or release/Zenodo creation here. This does not block
uploading the implementation to the existing repository. Do not relabel the v0.1
DOI as v0.2 or claim the public review has finished.

## Owner branch-protection command

The prepared [branch-protection settings](release/branch-protection.json) require
pull requests and both validation matrix checks without requiring another
maintainer's approval. Confirm the emitted check names first, then run from an
owner-authenticated GitHub CLI:

```bash
gh api --method PUT repos/Scoston/ai-forensic-readiness/branches/main/protection --input release/branch-protection.json
```

This requires repository administration permission. Do not bypass existing rules
or create alternate credentials if it is denied.

## Release preparation

```bash
python -m pip install -r requirements.txt
python scripts/validate.py
python scripts/build_cases.py --check
python -m unittest discover -s tests -v
```

Use the [v0.2 release notes](release/v0.2-review-notes.md) and reviewed PDF assets.
For the evolving draft, cite an exact Git commit. Keep CITATION.cff tied to the
archived version until a new DOI is actually assigned and verified.

The GitHub Pages site continues to use main and /docs. Mermaid source has static
validation; the publication workflow and host rendering are separate checks.
