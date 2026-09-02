# Publication plan

## Recommended canonical locations

| Purpose | Location | Recommended address |
| --- | --- | --- |
| Working specification and contributions | Public GitHub repository | `https://github.com/Scoston/ai-forensic-readiness` |
| Project landing page | GitHub Pages initially | `https://scoston.github.io/ai-forensic-readiness/` |
| Citable release archive | Zenodo GitHub integration | DOI assigned to each tagged release |
| Practitioner distribution | LinkedIn and Substack | Case-based posts linking to the canonical GitHub release |
| Later flagship paper | SSRN or arXiv | After controlled reference cases produce results |

GitHub should remain the canonical working source. Other channels should link back to the tagged specification rather than host competing versions.

## Pre-publication checklist

- [ ] Confirm author name, biography, and contact route.
- [ ] Confirm the repository name and public visibility.
- [ ] Review the CC BY 4.0 and Apache-2.0 split.
- [ ] Replace placeholder schema `$id` values after the final repository URL is confirmed.
- [ ] Confirm whether the draft should use “Dr. Stephen Coston” or “Stephen Coston” in citation metadata.
- [ ] Run `python scripts/validate.py`.
- [ ] Review Mermaid rendering on GitHub after the first push.
- [ ] Review the PDF and Markdown specification side by side.
- [ ] Enable private vulnerability reporting and branch protection.
- [ ] Create the `v0.1.0-draft` GitHub release only after the repository renders correctly.

## GitHub publication sequence

After final review:

```bash
git init -b main
git add .
git commit -m "Publish AI Forensic Readiness v0.1 discussion draft"
gh repo create Scoston/ai-forensic-readiness --public --source . --remote origin --push
```

Recommended repository settings:

- Require a pull request for changes to `main` after the initial release.
- Require the validation workflow to pass.
- Enable Discussions for broader practitioner questions.
- Enable private vulnerability reporting.
- Disable wiki initially so project knowledge remains version-controlled.
- Add repository topics: `ai-security`, `digital-forensics`, `incident-response`, `agentic-ai`, `dfir`, `ocsf`, `ai-governance`.

## GitHub Pages

The `docs/` directory contains an initial landing page. Configure Pages to deploy from the `main` branch and `/docs` folder. Use the generated site as the stable introduction; link technical readers to the versioned specification.

## Zenodo and DOI

1. Sign into Zenodo using the GitHub account that owns the repository.
2. Enable the repository in Zenodo’s GitHub integration.
3. Create the GitHub release `v0.1.0-draft`.
4. Confirm the archived metadata, authorship, license, and files.
5. Add the resulting version DOI and concept DOI to `CITATION.cff`, the README, and the project site.

Use the concept DOI when citing the evolving project and the version DOI when citing the exact draft reviewed.

## Public-review sequence

1. Publish the repository and v0.1 discussion-draft release.
2. Open a 45-day comment period using labeled proposal issues.
3. Publish one concise launch article explaining the investigation gap.
4. Publish Case 001 rather than a second abstract thought-leadership post.
5. Invite named review from DFIR, AI platform, IAM, privacy, governance, OCSF, and observability practitioners.
6. Record accepted, deferred, and rejected changes in public issues and the changelog.
7. Release v0.2 only after controlled-case evidence changes or validates the model.

## Naming posture

Use **AI Forensic Readiness** as the category and **Agentic Incident Response** as an operational subdomain. Do not describe v0.1 as an industry standard. Preferred language is “working model,” “discussion draft,” or “open practitioner specification.”

