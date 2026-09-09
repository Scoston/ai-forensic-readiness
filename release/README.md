# Release materials

- [Archived v0.1 PDF](AI_Forensic_Readiness_v0.1.pdf)
- [v0.2 discussion-draft PDF](AI_Forensic_Readiness_v0.2.pdf)
- [Practitioner briefing PDF](AI_Forensic_Readiness_Practitioner_Briefing.pdf)
- [v0.2 review notes](v0.2-review-notes.md)
- [Published v0.2 Zenodo archive](https://zenodo.org/records/22677119)
- [Publication status](../PUBLISHING.md)
- [GitHub release notes](v0.2-github-release.md) and [verified publication manifest](v0.2-publication.json)
- [Owner command for release publication and repository settings](OWNER-STEPS.md)
- [Reviewer package](reviewer-packs-v0.2.zip), [checksum](reviewer-packs-v0.2.sha256) and [review instructions](../research/review-kit.md)

The v0.2 archive has DOI [10.5281/zenodo.22677119](https://doi.org/10.5281/zenodo.22677119)
and contains the PDFs and source bundle from commit
`2db88053c8579e4db7aa6a5a45ea4c325a787ec9`. Both PDFs and every source-bundle file
were verified against that commit. The briefing has a ` (1)` suffix on Zenodo;
its contents match the file linked above.

The source and PDF bytes retain their pre-publication wording. Use the preferred
report citation in [CITATION.cff](../CITATION.cff) for the assigned DOI. The
[v0.1 DOI](https://doi.org/10.5281/zenodo.22255979) continues to identify v0.1.
Later changes to the working repository are outside the v0.2 archive.

PDFs can be rebuilt with `python scripts/build_release_pdfs.py` after installing
`requirements-release.txt`. Their manifests record source hashes for review.
