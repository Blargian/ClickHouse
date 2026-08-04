from types import SimpleNamespace

import pytest

from ci.defs.defs import SYNC
from ci.jobs.scripts.job_hooks import set_sync_status_awaiting_hook as hook
from ci.jobs.scripts.workflow_hooks.pr_labels_and_category import Labels
from ci.praktika.result import Result


class FakeInfo:
    repo_name = "ClickHouse/ClickHouse"
    pr_number = 123

    def __init__(self, changed_files, labels=()):
        self._changed_files = changed_files
        self.pr_labels = list(labels)

    def get_changed_files(self):
        return self._changed_files

    def add_pr_label(self, label):
        if label not in self.pr_labels:
            self.pr_labels.append(label)

    def remove_pr_label(self, label):
        if label in self.pr_labels:
            self.pr_labels.remove(label)


@pytest.mark.parametrize(
    ("changed_files", "expected"),
    [
        (("docs/reference/example.mdx",), True),
        (
            (
                "./docs/reference/example.mdx",
                "docs/resources/changelogs/oss/2026.mdx",
            ),
            True,
        ),
        (("docs/changelogs/v26.8.1.1-stable.md",), False),
        (("docs/changelogs",), False),
        (("docs/reference/example.mdx", "src/Core/Settings.cpp"), False),
        ((), False),
        (None, False),
    ],
)
def test_is_sync_exempt_docs_only_change(changed_files, expected):
    assert hook.is_sync_exempt_docs_only_change(changed_files) is expected


def run_hook(monkeypatch, info, statuses=None):
    posted_statuses = []
    label_commands = []

    monkeypatch.setattr(hook, "Info", lambda: info)
    monkeypatch.setattr(
        hook.GH,
        "get_commit_statuses",
        lambda: {} if statuses is None else statuses,
    )
    monkeypatch.setattr(
        hook.GH,
        "post_commit_status",
        lambda **kwargs: posted_statuses.append(kwargs),
    )
    monkeypatch.setattr(
        hook.Shell,
        "check",
        lambda command, **kwargs: label_commands.append((command, kwargs)) or True,
    )

    hook.main()
    return posted_statuses, label_commands


def test_docs_only_change_is_marked_sync_exempt(monkeypatch):
    info = FakeInfo(("docs/reference/example.mdx",))

    posted_statuses, label_commands = run_hook(monkeypatch, info)

    assert info.pr_labels == [Labels.PR_SYNCED_TO_CLOUD]
    assert label_commands == [
        (
            "gh pr edit 123 --repo ClickHouse/ClickHouse "
            "--add-label pr-synced-to-cloud",
            {"verbose": True, "strict": True, "retries": 5},
        )
    ]
    assert posted_statuses == [
        {
            "name": SYNC,
            "status": Result.Status.OK,
            "description": hook.SYNC_EXEMPT_DESCRIPTION,
            "url": "",
        }
    ]


def test_changelog_change_still_requires_sync(monkeypatch):
    info = FakeInfo(("docs/changelogs/v26.8.1.1-stable.md",))

    posted_statuses, label_commands = run_hook(monkeypatch, info)

    assert label_commands == []
    assert posted_statuses == [
        {
            "name": SYNC,
            "status": Result.Status.PENDING,
            "description": "awaiting",
            "url": "",
        }
    ]


@pytest.mark.parametrize("changed_files", [None, ()])
def test_missing_changed_files_still_requires_sync(monkeypatch, changed_files):
    info = FakeInfo(changed_files)

    posted_statuses, label_commands = run_hook(monkeypatch, info)

    assert label_commands == []
    assert posted_statuses[0]["status"] == Result.Status.PENDING


def test_non_docs_change_removes_previous_exemption(monkeypatch):
    info = FakeInfo(
        ("src/Core/Settings.cpp",), labels=(Labels.PR_SYNCED_TO_CLOUD,)
    )

    posted_statuses, label_commands = run_hook(monkeypatch, info)

    assert info.pr_labels == []
    assert label_commands[0][0].endswith("--remove-label pr-synced-to-cloud")
    assert posted_statuses[0]["status"] == Result.Status.PENDING


def test_existing_docs_exemption_is_not_reposted(monkeypatch):
    info = FakeInfo(
        ("docs/reference/example.mdx",), labels=(Labels.PR_SYNCED_TO_CLOUD,)
    )
    statuses = {
        SYNC: SimpleNamespace(
            state=Result.GHStatus.SUCCESS,
            description=hook.SYNC_EXEMPT_DESCRIPTION,
        )
    }

    posted_statuses, label_commands = run_hook(monkeypatch, info, statuses)

    assert label_commands == []
    assert posted_statuses == []


def test_hook_is_not_applied_to_private_repo(monkeypatch):
    info = FakeInfo(("docs/reference/example.mdx",))
    info.repo_name = "ClickHouse/clickhouse-private"
    monkeypatch.setattr(hook, "Info", lambda: info)
    monkeypatch.setattr(
        hook.GH,
        "get_commit_statuses",
        lambda: pytest.fail("statuses should not be fetched"),
    )

    hook.main()


def test_hook_runs_during_pr_workflow_configuration():
    from ci.defs.job_configs import JobConfigs
    from ci.workflows.pull_request import workflow

    command = "python3 ./ci/jobs/scripts/job_hooks/set_sync_status_awaiting_hook.py"
    assert command in workflow.pre_hooks
    assert command not in JobConfigs.code_review.post_hooks
