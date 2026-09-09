# Finish the GitHub v0.2 publication

Zenodo v0.2 is complete: [10.5281/zenodo.22677119](https://doi.org/10.5281/zenodo.22677119).
The next owner action is to publish the matching GitHub prerelease and configure
repository protection. Independent technical review remains a separate activity.

The [preparation workflow](../.github/workflows/prepare-release.yml) runs when its
implementation reaches main, and can be rerun from GitHub Actions. It verifies
the two PDFs and all 280 source files against the archived commit, creates the
`v0.2.0-draft` tag at that commit and uploads four assets to an **unpublished draft**.
See [workflow runs](https://github.com/Scoston/ai-forensic-readiness/actions/workflows/prepare-release.yml)
and the repository's [Releases page](https://github.com/Scoston/ai-forensic-readiness/releases).

## Owner command

Use an existing checkout of this repository with Git, Python 3.12 or 3.13 and
[GitHub CLI](https://cli.github.com/) installed. GitHub CLI must already be signed
in as an administrator of `Scoston/ai-forensic-readiness`; `gh auth status` checks
the active account. Do not paste credentials into an issue or chat.

From that checkout in Windows PowerShell:

```powershell
git switch main
git pull --ff-only
py scripts/finish_publication.py --apply
```

On Linux or macOS, use `python3` in place of `py`. A shallow checkout needs
`git fetch --unshallow origin` first so the archived commit is available. To
inspect the proposed actions without changing GitHub, omit `--apply`.

The command:

1. Verifies the Zenodo files, DOI, exact source commit, existing tag and assets.
2. Requires successful Python 3.12 and 3.13 validation on current main.
3. Applies [branch protection](branch-protection.json) if absent and enables
   private vulnerability reporting if needed, then verifies both settings.
4. Checks for active Zenodo release webhooks to avoid a second deposit for this
   already archived version.
5. Creates or completes the draft if needed and publishes it as a prerelease
   with the existing DOI. It preserves the original source and PDF bytes.

If an active Zenodo release webhook is found, the settings are still completed
but the release stays a draft. Turn off this repository's automatic archiving in
[Zenodo's GitHub settings](https://zenodo.org/account/settings/github/), then rerun
the same command. This avoids creating another DOI for the same v0.2 files; the
command does not change webhooks or Zenodo records.

Existing branch protection that meets or exceeds the baseline is preserved. If
an existing policy differs, review it in GitHub settings; the command refuses to
overwrite it. Permission errors require the owner to resolve access in the
normal account settings. Repeated successful runs preserve published assets and
do not move tags or republish the release.

The final JSON should report `branch_protection: verified`,
`private_vulnerability_reporting: verified` and `release: published`, with the
release URL. Until that result is verified, do not mark those owner steps complete.

## Start external review

The [review kit](../research/review-kit.md) includes a downloadable package for all
ten synthetic cases, with raw evidence hashes and empty response forms. Select
reviewers, provide one assigned case at a time and record actual findings using
the linked issue form. Invitations and independent results have not been
produced by preparing these materials. Public review remains open through
October 17, 2026.
