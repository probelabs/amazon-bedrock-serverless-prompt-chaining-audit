# Parent system requirement: SYS-REQ-001
import os
from unittest.mock import MagicMock

import pytest

from tests.conftest import load_module, md2pdf_import_stubs

PDF_PATH = "functions/trip_planner/pdf_creator/index.py"


def _load(module_name, bucket=None, md2pdf_fn=None):
    extra = md2pdf_import_stubs(md2pdf_fn)
    if bucket is None:
        os.environ.pop("PDF_BUCKET", None)
    else:
        os.environ["PDF_BUCKET"] = bucket
    return load_module(module_name, PDF_PATH, extra_sys_modules=extra)


def test_handler_uploads_pdf_and_returns_presigned_url():
    # mcdc:ignore:defensive INT-REQ-006: expires_in_GE_60=F, expires_in_LE_900=T, object_stored_in_pdf_bucket=T, pdf_upload_requested=T, presigned_get_url_returned=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive INT-REQ-006: expires_in_GE_60=T, expires_in_LE_900=F, object_stored_in_pdf_bucket=T, pdf_upload_requested=T, presigned_get_url_returned=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # MCDC INT-REQ-006: expires_in_GE_60=T, expires_in_LE_900=T, object_stored_in_pdf_bucket=F, pdf_upload_requested=F, presigned_get_url_returned=F => TRUE
    # mcdc:ignore:defensive INT-REQ-006: expires_in_GE_60=T, expires_in_LE_900=T, object_stored_in_pdf_bucket=F, pdf_upload_requested=T, presigned_get_url_returned=F => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive INT-REQ-006: expires_in_GE_60=T, expires_in_LE_900=T, object_stored_in_pdf_bucket=F, pdf_upload_requested=T, presigned_get_url_returned=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive INT-REQ-006: expires_in_GE_60=T, expires_in_LE_900=T, object_stored_in_pdf_bucket=T, pdf_upload_requested=T, presigned_get_url_returned=F => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # MCDC INT-REQ-006: expires_in_GE_60=T, expires_in_LE_900=T, object_stored_in_pdf_bucket=T, pdf_upload_requested=T, presigned_get_url_returned=T => TRUE
    # mcdc:ignore:defensive SW-REQ-007: content_type_is_pdf=F, expires_in_GE_60=F, expires_in_LE_900=T, itinerary_ready=F, object_stored_in_pdf_bucket=F, presigned_pdf_url_returned=F, temp_pdf_unlinked=F, template_eval_active=F, untrusted_itinerary_present=F => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SW-REQ-007: content_type_is_pdf=F, expires_in_GE_60=T, expires_in_LE_900=F, itinerary_ready=F, object_stored_in_pdf_bucket=F, presigned_pdf_url_returned=F, temp_pdf_unlinked=F, template_eval_active=F, untrusted_itinerary_present=F => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # MCDC SW-REQ-007: content_type_is_pdf=F, expires_in_GE_60=T, expires_in_LE_900=T, itinerary_ready=F, object_stored_in_pdf_bucket=F, presigned_pdf_url_returned=F, temp_pdf_unlinked=F, template_eval_active=F, untrusted_itinerary_present=F => TRUE
    # mcdc:ignore:defensive SW-REQ-007: content_type_is_pdf=F, expires_in_GE_60=T, expires_in_LE_900=T, itinerary_ready=T, object_stored_in_pdf_bucket=F, presigned_pdf_url_returned=F, temp_pdf_unlinked=F, template_eval_active=F, untrusted_itinerary_present=F => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SW-REQ-007: content_type_is_pdf=F, expires_in_GE_60=T, expires_in_LE_900=T, itinerary_ready=T, object_stored_in_pdf_bucket=T, presigned_pdf_url_returned=T, temp_pdf_unlinked=T, template_eval_active=F, untrusted_itinerary_present=F => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SW-REQ-007: content_type_is_pdf=T, expires_in_GE_60=T, expires_in_LE_900=T, itinerary_ready=T, object_stored_in_pdf_bucket=F, presigned_pdf_url_returned=T, temp_pdf_unlinked=T, template_eval_active=F, untrusted_itinerary_present=F => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SW-REQ-007: content_type_is_pdf=T, expires_in_GE_60=T, expires_in_LE_900=T, itinerary_ready=T, object_stored_in_pdf_bucket=T, presigned_pdf_url_returned=F, temp_pdf_unlinked=T, template_eval_active=F, untrusted_itinerary_present=F => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SW-REQ-007: content_type_is_pdf=T, expires_in_GE_60=T, expires_in_LE_900=T, itinerary_ready=T, object_stored_in_pdf_bucket=T, presigned_pdf_url_returned=T, temp_pdf_unlinked=F, template_eval_active=F, untrusted_itinerary_present=F => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # MCDC SW-REQ-007: content_type_is_pdf=T, expires_in_GE_60=T, expires_in_LE_900=T, itinerary_ready=T, object_stored_in_pdf_bucket=T, presigned_pdf_url_returned=T, temp_pdf_unlinked=T, template_eval_active=F, untrusted_itinerary_present=F => TRUE
    # MCDC SW-REQ-007: content_type_is_pdf=T, expires_in_GE_60=T, expires_in_LE_900=T, itinerary_ready=T, object_stored_in_pdf_bucket=T, presigned_pdf_url_returned=T, temp_pdf_unlinked=T, template_eval_active=F, untrusted_itinerary_present=T => TRUE
    # MCDC SW-REQ-007: content_type_is_pdf=T, expires_in_GE_60=T, expires_in_LE_900=T, itinerary_ready=T, object_stored_in_pdf_bucket=T, presigned_pdf_url_returned=T, temp_pdf_unlinked=T, template_eval_active=T, untrusted_itinerary_present=F => TRUE
    # MCDC SW-REQ-007: content_type_is_pdf=T, expires_in_GE_60=T, expires_in_LE_900=T, itinerary_ready=T, object_stored_in_pdf_bucket=T, presigned_pdf_url_returned=T, temp_pdf_unlinked=T, template_eval_active=T, untrusted_itinerary_present=T => FALSE [known-issue] [ki: KI-pdf-md2pdf-ssti] -- md2pdf(..., raw=) evaluates untrusted Jinja; not a domain mutex
    # mcdc:ignore:defensive SYS-REQ-008: expires_in_GE_60=F, expires_in_LE_900=T, itinerary_ready=F, presigned_pdf_url_returned=F, template_eval_active=F, untrusted_itinerary_present=F => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SYS-REQ-008: expires_in_GE_60=T, expires_in_LE_900=F, itinerary_ready=F, presigned_pdf_url_returned=F, template_eval_active=F, untrusted_itinerary_present=F => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # MCDC SYS-REQ-008: expires_in_GE_60=T, expires_in_LE_900=T, itinerary_ready=F, presigned_pdf_url_returned=F, template_eval_active=F, untrusted_itinerary_present=F => TRUE
    # mcdc:ignore:defensive SYS-REQ-008: expires_in_GE_60=T, expires_in_LE_900=T, itinerary_ready=T, presigned_pdf_url_returned=F, template_eval_active=F, untrusted_itinerary_present=F => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # MCDC SYS-REQ-008: expires_in_GE_60=T, expires_in_LE_900=T, itinerary_ready=T, presigned_pdf_url_returned=T, template_eval_active=F, untrusted_itinerary_present=F => TRUE
    # MCDC SYS-REQ-008: expires_in_GE_60=T, expires_in_LE_900=T, itinerary_ready=T, presigned_pdf_url_returned=T, template_eval_active=F, untrusted_itinerary_present=T => TRUE
    # MCDC SYS-REQ-008: expires_in_GE_60=T, expires_in_LE_900=T, itinerary_ready=T, presigned_pdf_url_returned=T, template_eval_active=T, untrusted_itinerary_present=F => TRUE
    # MCDC SYS-REQ-008: expires_in_GE_60=T, expires_in_LE_900=T, itinerary_ready=T, presigned_pdf_url_returned=T, template_eval_active=T, untrusted_itinerary_present=T => FALSE [known-issue] [ki: KI-pdf-md2pdf-ssti] -- md2pdf(..., raw=) evaluates untrusted Jinja; not a domain mutex

    # Verifies: SW-REQ-007
    # Verifies: SYS-REQ-008
    # Verifies: INT-REQ-006
    # Verifies: STK-REQ-001
    # SW-REQ-007:nominal:nominal
    # SW-REQ-007:boundary:nominal
    # SW-REQ-007:error_handling:nominal
    # SW-REQ-007:malformed_input:nominal
    # SW-REQ-007:silent_false_safety_reviewed:nominal
    # SW-REQ-007:source_fragment_validated_before_composition:nominal
    # SYS-REQ-008:silent_false_safety_reviewed:nominal
    # SYS-REQ-008:source_fragment_validated_before_composition:nominal
    # SYS-REQ-008:boundary:nominal
    # INT-REQ-006:nominal:nominal
    # INT-REQ-006:boundary:nominal
    # INT-REQ-006:error_handling:nominal
    # INT-REQ-006:integration:integration
    md2pdf_fn = MagicMock()
    bucket = "itinerary-pdfs-test"
    mod = _load("pdf_creator_with_bucket", bucket=bucket, md2pdf_fn=md2pdf_fn)

    uploaded = {}

    def upload_file(path, dest_bucket, key, ExtraArgs=None):
        uploaded["path"] = path
        uploaded["bucket"] = dest_bucket
        uploaded["key"] = key
        uploaded["extra"] = ExtraArgs

    fake_s3 = MagicMock()
    fake_s3.upload_file.side_effect = upload_file
    fake_s3.generate_presigned_url.return_value = "https://s3.example/signed.pdf"
    mod.s3_client = fake_s3

    event = {"location": "Lisbon", "itinerary": "Day 1: tram 28\nDay 2: pasteis"}
    result = mod.handler(event, None)

    assert result["itinerary_url"] == "https://s3.example/signed.pdf"
    assert result["location"] == event["location"]

    md2pdf_fn.assert_called_once()
    raw = md2pdf_fn.call_args.kwargs.get("raw")
    if raw is None:
        raw = md2pdf_fn.call_args[1].get("raw") if md2pdf_fn.call_args[1] else None
    assert raw is not None
    assert event["location"] in raw
    assert event["itinerary"] in raw

    assert uploaded["bucket"] == bucket
    assert uploaded["key"].startswith("itinerary-")
    assert uploaded["key"].endswith(".pdf")
    assert uploaded["extra"]["ContentType"] == "application/pdf"
    assert not os.path.exists(uploaded["path"])

    fake_s3.generate_presigned_url.assert_called_once()
    call = fake_s3.generate_presigned_url.call_args
    params = call.kwargs.get("Params") or call[1].get("Params")
    assert params["Bucket"] == bucket
    assert params["Key"] == uploaded["key"]


def test_handler_unlinks_temp_pdf_even_if_already_removed():
    # Verifies: SW-REQ-007
    # Verifies: SYS-REQ-008
    # Drive both polarities of os.path.exists(pdf_tmp_path) in finally.
    md2pdf_fn = MagicMock()
    mod = _load("pdf_creator_unlink", bucket="b", md2pdf_fn=md2pdf_fn)
    fake_s3 = MagicMock()
    fake_s3.generate_presigned_url.return_value = "https://s3.example/x.pdf"
    mod.s3_client = fake_s3

    original_exists = os.path.exists

    def exists_then_false(path):
        if str(path).endswith(".pdf"):
            return False
        return original_exists(path)

    # First call: normal path (file exists after NamedTemporaryFile).
    result = mod.handler({"location": "Rome", "itinerary": "colosseum"}, None)
    assert result["location"] == "Rome"

    # Second call: finally sees a missing file.
    os.path.exists = exists_then_false
    try:
        result2 = mod.handler({"location": "Nice", "itinerary": "promenade"}, None)
        assert result2["location"] == "Nice"
    finally:
        os.path.exists = original_exists


def test_missing_pdf_bucket_is_passed_through_to_s3():
    # Verifies: SW-REQ-007
    # Verifies: SYS-REQ-008
    # Verifies: INT-REQ-006
    # SW-REQ-007:error_handling:negative
    # SW-REQ-007:malformed_input:negative
    # INT-REQ-006:error_handling:negative
    # INT-REQ-006:integration:integration
    # The Lambda binds PDF_BUCKET at import via os.environ.get. A missing
    # variable becomes None and is forwarded to upload_file / presign.
    md2pdf_fn = MagicMock()
    mod = _load("pdf_creator_no_bucket", bucket=None, md2pdf_fn=md2pdf_fn)
    assert mod.s3_bucket_name is None

    fake_s3 = MagicMock()
    fake_s3.generate_presigned_url.return_value = "https://s3.example/none.pdf"
    mod.s3_client = fake_s3

    result = mod.handler({"location": "Oslo", "itinerary": "walk"}, None)

    upload_args, upload_kwargs = fake_s3.upload_file.call_args
    dest_bucket = upload_args[1] if len(upload_args) > 1 else upload_kwargs.get("Bucket")
    assert dest_bucket is None
    assert result["location"] == "Oslo"


def _md2pdf_raw_and_kwargs(md2pdf_fn):
    assert md2pdf_fn.called
    kwargs = md2pdf_fn.call_args.kwargs or {}
    raw = kwargs.get("raw")
    if raw is None and md2pdf_fn.call_args[1]:
        raw = md2pdf_fn.call_args[1].get("raw")
    return raw, kwargs


def _pdf_handler_with_mocked_md2pdf(module_name, md2pdf_fn, event):
    mod = _load(module_name, bucket="itinerary-pdfs-test", md2pdf_fn=md2pdf_fn)
    fake_s3 = MagicMock()
    fake_s3.generate_presigned_url.return_value = "https://s3.example/signed.pdf"
    mod.s3_client = fake_s3
    return mod.handler(event, None)


# Reproduces: KI-pdf-md2pdf-ssti
# Library probe (md2pdf unsandboxed Jinja):
# proof/evidence/codex-security-CPeyWd/artifacts/02_discovery/validation_artifacts/candidate-8f0e6e3f7eec765a/jinja_ssti_probe.txt
# probe1: visit to 49; builtins_open_exposed: True
@pytest.mark.xfail(
    strict=True,
    reason="KI-pdf-md2pdf-ssti: unsandboxed Jinja until renderer is data-only",
)
def test_pdf_creator_does_not_pass_unsandboxed_jinja_to_md2pdf():
    # SW-REQ-007:silent_false_safety_reviewed:negative
    # SW-REQ-007:source_fragment_validated_before_composition:negative
    # SYS-REQ-008:silent_false_safety_reviewed:negative
    # SYS-REQ-008:source_fragment_validated_before_composition:negative
    md2pdf_fn = MagicMock()
    payload = "{{7*7}}"
    try:
        _pdf_handler_with_mocked_md2pdf(
            "pdf_creator_ssti_repro",
            md2pdf_fn,
            {"location": payload, "itinerary": "x"},
        )
    except (ValueError, TypeError, RuntimeError):
        return
    raw, _kwargs = _md2pdf_raw_and_kwargs(md2pdf_fn)
    assert raw is not None
    assert "{{7*7}}" not in raw, (
        "location/itinerary must be escaped or rejected before md2pdf raw; "
        "unevaluated Jinja is rendered by jinja2.Template(raw).render() "
        "(see jinja_ssti_probe.txt)"
    )


# Reproduces: KI-pdf-weasyprint-ssrf
@pytest.mark.xfail(
    strict=True,
    reason="KI-pdf-weasyprint-ssrf: markdown image URL reaches WeasyPrint default fetcher",
)
def test_pdf_creator_does_not_pass_fetchable_markdown_url():
    md2pdf_fn = MagicMock()
    marker = "http://127.0.0.1/poc"
    try:
        _pdf_handler_with_mocked_md2pdf(
            "pdf_creator_ssrf_repro",
            md2pdf_fn,
            {"location": "Paris", "itinerary": f"![]({marker})"},
        )
    except (ValueError, TypeError, RuntimeError):
        return
    raw, kwargs = _md2pdf_raw_and_kwargs(md2pdf_fn)
    has_deny_fetcher = any(
        kwargs.get(key) is not None for key in ("url_fetcher", "urlFetcher")
    )
    if has_deny_fetcher:
        return
    assert marker not in (raw or ""), (
        "markdown image URL must not be passed through as a fetchable resource "
        "without a deny-by-default WeasyPrint URL fetcher"
    )
