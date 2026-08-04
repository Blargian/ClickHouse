import shlex

from ci.defs.defs import SYNC
from ci.jobs.scripts.workflow_hooks.pr_labels_and_category import Labels
from ci.praktika.gh import GH
from ci.praktika.info import Info
from ci.praktika.result import Result
from ci.praktika.utils import Shell

# This status is a marker that the sync process can be started. Set it during
# PR workflow configuration so docs-only exemptions are visible before the
# periodic private sync workflow can create a Sync PR.

DOCS_PREFIX = "docs/"
CHANGELOGS_PREFIX = "docs/changelogs/"
SYNC_EXEMPT_DESCRIPTION = "Docs-only change, sync not required"


def is_sync_exempt_docs_only_change(changed_files):
    if not changed_files:
        return False

    for file in changed_files:
        path = file.removeprefix("./").removeprefix("/")
        if not path.startswith(DOCS_PREFIX):
            return False
        if path == CHANGELOGS_PREFIX.rstrip("/") or path.startswith(
            CHANGELOGS_PREFIX
        ):
            return False

    return True


def set_sync_exemption_label(info, exempt):
    label = Labels.PR_SYNCED_TO_CLOUD
    has_label = label in info.pr_labels
    if has_label == exempt:
        return

    if not info.pr_number:
        raise RuntimeError(
            f"Cannot update label [{label}] without a pull request number"
        )

    action = "add" if exempt else "remove"
    command = (
        f"gh pr edit {shlex.quote(str(info.pr_number))} "
        f"--repo {shlex.quote(info.repo_name)} "
        f"--{action}-label {shlex.quote(label)}"
    )
    Shell.check(command, verbose=True, strict=True, retries=5)

    if exempt:
        info.add_pr_label(label)
    else:
        info.remove_pr_label(label)


def main():
    info = Info()
    if info.repo_name != "ClickHouse/ClickHouse":
        print(f"Not applicable for repo [{info.repo_name}], skipping")
        return

    statuses = GH.get_commit_statuses()
    if statuses is None:
        print(f"Failed to fetch commit statuses, skip setting [{SYNC}]")
        return

    sync_exempt = is_sync_exempt_docs_only_change(info.get_changed_files())
    set_sync_exemption_label(info, sync_exempt)

    if sync_exempt:
        existing_status = statuses.get(SYNC)
        if (
            existing_status
            and existing_status.state == Result.GHStatus.SUCCESS
            and existing_status.description == SYNC_EXEMPT_DESCRIPTION
        ):
            print(
                f"Commit status [{SYNC}] already marks this change as sync-exempt, skipping"
            )
            return

        GH.post_commit_status(
            name=SYNC,
            status=Result.Status.OK,
            description=SYNC_EXEMPT_DESCRIPTION,
            url="",
        )
        return

    if SYNC in statuses:
        print(
            f"Commit status [{SYNC}] already exists with description "
            f"[{statuses[SYNC].description}], skipping"
        )
        return

    GH.post_commit_status(
        name=SYNC,
        status=Result.Status.PENDING,
        description="awaiting",
        url="",
    )


if __name__ == "__main__":
    main()
