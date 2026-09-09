# Publication and completion status

Reviewed September 8, 2026 against repository main commit
`0e65affd8ccadba15ce76f75c009a141d10560e4`, the five pre-existing open issues,
all six merged pull requests, and the source specification's build plan.

Archival status updated September 9, 2026: Zenodo and DataCite confirm the published
[v0.2 record](https://zenodo.org/records/22677119), version `0.2.0-draft`, publication
date September 8, 2026, and DOI [10.5281/zenodo.22677119](https://doi.org/10.5281/zenodo.22677119).
Its source bundle is commit `2db88053c8579e4db7aa6a5a45ea4c325a787ec9`.

## Completed repository work

| Item | Evidence / disposition |
| --- | --- |
| Public repository and project identity | Scoston/ai-forensic-readiness; authored by Dr. Stephen Coston |
| Prose/code licensing | CC BY 4.0 prose and diagrams; Apache-2.0 schemas and code retained |
| v0.1 release and citation | Existing v0.1.0-draft archive and DOI retained; not reassigned to v0.2 |
| v0.2 archive and citation | Published on Zenodo; version DOI verified with DataCite; repository citation and Pages links updated |
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
| v0.2 Zenodo archive | Published; both PDFs and all 280 files in the ZIP match the reviewed commit | Owner removes the stale v0.1 related-work link and clarifies license scopes as described below |
| v0.2 GitHub Release | No v0.2 GitHub Release exists as of September 9, 2026 | Owner publishes the discussion-draft release from commit `2db88053c8579e4db7aa6a5a45ea4c325a787ec9` with the existing Zenodo DOI |

The connected repository tools support code, issue and pull-request work but do
not expose administration or release/Zenodo creation here. This does not block
uploading the implementation to the existing repository. Do not relabel the v0.1
DOI as v0.2 or claim the public review has finished.

## Verified v0.2 archive

The version DOI is **10.5281/zenodo.22677119**. The concept DOI
**10.5281/zenodo.22255978** links the version family, including the original
[v0.1 record](https://zenodo.org/records/22255979). DataCite reports the new DOI as
`findable`. The registered title is *AI Forensic Readiness v0.2 — Discussion Draft*
and the creator is Stephen Coston Jr., Independent Researcher.

Downloaded files were checked against Zenodo's declared sizes and MD5 checksums,
then compared byte for byte with the reviewed Git commit:

| Zenodo file | Verification |
| --- | --- |
| `AI_Forensic_Readiness_v0.2.pdf` | Matches the specification PDF and SHA-256 in `release/pdf-manifest.json` |
| `AI_Forensic_Readiness_Practitioner_Briefing (1).pdf` | Matches the repository briefing PDF and its manifest SHA-256; the download suffix is only a filename difference |
| `ai-forensic-readiness-2db88053c8579e4db7aa6a5a45ea4c325a787ec9.zip` | All 280 files match the corresponding files in the reviewed commit |

The ZIP SHA-256 is
`4fd699d4ae08a838cb9353baf95d2409e2d0620de40d5111701063f0fa08fee3`.
These checks establish archive consistency with that commit, not production
control effectiveness or independent validation of the research claims.

The archived source, PDFs and source-hash manifest remain unchanged. Their
pre-publication statements about an unassigned DOI describe the build before
deposit. The current `CITATION.cff` provides the assigned DOI and preferred report
citation. Repository updates after the archived commit require their own commit
reference.

### Owner metadata corrections on Zenodo

The published record still contains an inherited **Is identical to** relationship
to the GitHub `v0.1.0-draft` release. This incorrectly equates v0.2 with v0.1.
The current Repository URL is already correct.

1. Open [the v0.2 record](https://zenodo.org/records/22677119) while signed in as its owner and click **Edit**.
2. Under **Related works**, remove the **Is identical to** entry ending in `/releases/tag/v0.1.0-draft`. Keep the existing version history.
3. Add this license scope to **Description**: “Specification, explanatory text and diagrams are licensed under CC BY 4.0. Schemas, examples and code are licensed under Apache-2.0; see the license files in the source archive.”
4. Save and publish the metadata correction on this same record.

The archive currently lists CC BY 4.0 without this scope in its description. The
included repository contains both license files. These owner edits clarify the
metadata and do not require a new research version or replacement files.

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
Use the verified v0.2 DOI for the archived build. For subsequent changes on main,
cite an exact Git commit; keep `CITATION.cff` tied to the archived version until
another version is published and verified.

The GitHub Pages site continues to use main and /docs. Mermaid source has static
validation; the publication workflow and host rendering are separate checks.
