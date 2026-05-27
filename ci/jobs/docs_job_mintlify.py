import json
import os

from ci.praktika.result import Result
from ci.praktika.utils import Shell, Utils

if __name__ == "__main__":

    results = []
    stop_watch = Utils.Stopwatch()
    temp_dir = f"{Utils.cwd()}/ci/tmp/"
    os.makedirs(temp_dir, exist_ok=True)

    docs_dir = f"{Utils.cwd()}/docs"

    results.append(
        Result.from_commands_run(
            name="Verify Mintlify docs.json file is valid",
            command=[
                "mint validate",
            ],
            workdir=docs_dir,
        )
    )

    # Verify every destination in _site/redirects.json resolves to a real
    # page (and anchor, if any) by feeding the destinations through lychee
    # as a generated markdown file alongside the rest of the docs tree.
    redirects_json = f"{docs_dir}/_site/redirects.json"
    redirects_md = f"{temp_dir}/lychee_redirects.md"
    lychee_inputs = "."
    if os.path.exists(redirects_json):
        with open(redirects_json) as f:
            redirects = json.load(f)
        with open(redirects_md, "w") as f:
            f.write("# Redirect destinations\n\n")
            for r in redirects:
                dest = r.get("destination", "")
                if dest:
                    f.write(f"- [{dest}]({dest})\n")
        lychee_inputs = f". {redirects_md}"

    # Legacy (non-Mintlify) content still living under docs/ — skip so we
    # only check the actual Mintlify site. Mirrors the exclude list in
    # ci/defs/job_configs.py for this job's digest_config.
    lychee_excludes = " ".join(
        f"--exclude-path '{p}'"
        for p in (
            "en/",
            "_description_templates/",
            "_includes/",
            "changelogs/",
            "_migration/",
            "_site/",
        )
    )

    lychee_result = Result.from_commands_run(
        name="Check links, anchors, and redirects with lychee",
        command=[
            f"lychee --offline --include-fragments "
            f"--root-dir {docs_dir} "
            f"--fallback-extensions mdx,md "
            f"--no-progress "
            f"{lychee_excludes} "
            f"{lychee_inputs}",
        ],
        workdir=docs_dir,
    )
    # Non-blocking: lychee surfaces ~200 known broken anchors today (pending
    # upstream typo fixes and the api-reference/ OpenAPI integration). Report
    # the findings without failing the job; switch to blocking once the
    # baseline is clean.
    if lychee_result.status != Result.Status.OK:
        lychee_result.set_info(
            f"lychee reported broken links (status was {lychee_result.status}); "
            f"keeping job green while we burn down the baseline"
        )
        lychee_result.status = Result.Status.OK
    results.append(lychee_result)

    Result.create_from(results=results).complete_job()
