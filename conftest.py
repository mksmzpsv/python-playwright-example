import glob
import os
from pathlib import Path

import allure
import pytest
from slugify import slugify

# Register fixtures from fixtures module
pytest_plugins = ["fixtures.fixtures"]

@pytest.hookimpl(hookwrapper=True)
def attach_artifacts_to_allure_report(item: pytest.Item, call):
    """Attach Playwright artifacts to the Allure report.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        item.rep_call = report

    call_report = getattr(item, "rep_call", None)
    if call_report is None:
        return

    failed = call_report.failed

    video_opt = item.config.getoption("--video")
    screenshot_opt = item.config.getoption("--screenshot")
    tracing_opt = item.config.getoption("--tracing")

    should_attach_video = video_opt == "on" or (
        failed and video_opt == "retain-on-failure"
    )
    should_attach_screenshot = screenshot_opt == "on" or (
        failed and screenshot_opt == "only-on-failure"
    )
    should_attach_trace = tracing_opt == "on" or (
        failed and tracing_opt == "retain-on-failure"
    )

    if not (should_attach_video or should_attach_screenshot or should_attach_trace):
        return

    output_dir = os.path.abspath(item.config.getoption("--output"))
    test_output = os.path.join(output_dir, slugify(item.nodeid))

    if not os.path.isdir(test_output):
        return

    if should_attach_screenshot:
        for png in sorted(glob.glob(os.path.join(test_output, "*.png"))):
            allure.attach.file(
                png,
                name=Path(png).stem,
                attachment_type=allure.attachment_type.PNG,
            )

    if should_attach_video:
        for webm in sorted(glob.glob(os.path.join(test_output, "*.webm"))):
            allure.attach.file(
                webm,
                name=Path(webm).stem,
                attachment_type=allure.attachment_type.WEBM,
            )

    if should_attach_trace:
        for trace in sorted(glob.glob(os.path.join(test_output, "*.zip"))):
            allure.attach.file(
                trace,
                name=Path(trace).stem,
                attachment_type=allure.attachment_type.ZIP,
            )
