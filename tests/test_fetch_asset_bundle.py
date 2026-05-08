import hashlib
import json
import shutil
import subprocess
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "fetch-asset-bundle.sh"


def make_bundle(tmp_path: Path, name: str, files: dict[str, str]) -> tuple[Path, str]:
    zip_path = tmp_path / f"{name}.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        for rel_path, content in files.items():
            zf.writestr(rel_path, content)
    digest = hashlib.sha256(zip_path.read_bytes()).hexdigest()
    return zip_path, digest


def make_template(tmp_path: Path, template_id: str, zip_path: Path, digest: str) -> Path:
    repo = tmp_path / "repo"
    template_dir = repo / "assets" / "templates" / template_id
    template_dir.mkdir(parents=True)
    (template_dir / "template.json").write_text(
        json.dumps(
            {
                "asset_bundle": {
                    "local_path": "base/",
                    "url": str(zip_path),
                    "sha256": digest,
                }
            }
        ),
        encoding="utf-8",
    )
    return repo


def run_fetch(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(SCRIPT), *args, str(repo)],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def test_template_fetch_writes_sha_marker(tmp_path):
    zip_path, digest = make_bundle(tmp_path, "bundle", {"asset.txt": "v1"})
    repo = make_template(tmp_path, "paper-house", zip_path, digest)

    result = run_fetch(repo, "--template", "paper-house")

    base = repo / "assets" / "templates" / "paper-house" / "base"
    assert result.stdout.strip() == str(base)
    assert (base / "asset.txt").read_text(encoding="utf-8") == "v1"
    assert (base / ".bundle-sha256").read_text(encoding="utf-8").strip() == digest


def test_template_fetch_skips_when_marker_matches(tmp_path):
    zip_path, digest = make_bundle(tmp_path, "bundle", {"asset.txt": "zip value"})
    repo = make_template(tmp_path, "paper-house", zip_path, digest)
    base = repo / "assets" / "templates" / "paper-house" / "base"
    base.mkdir(parents=True)
    (base / "asset.txt").write_text("cached value", encoding="utf-8")
    (base / ".bundle-sha256").write_text(f"{digest}\n", encoding="utf-8")

    run_fetch(repo, "--template", "paper-house")

    assert (base / "asset.txt").read_text(encoding="utf-8") == "cached value"


def test_template_fetch_refreshes_when_marker_missing(tmp_path):
    zip_path, digest = make_bundle(tmp_path, "bundle", {"asset.txt": "fresh"})
    repo = make_template(tmp_path, "paper-house", zip_path, digest)
    base = repo / "assets" / "templates" / "paper-house" / "base"
    base.mkdir(parents=True)
    (base / "stale.txt").write_text("stale", encoding="utf-8")

    run_fetch(repo, "--template", "paper-house")

    assert not (base / "stale.txt").exists()
    assert (base / "asset.txt").read_text(encoding="utf-8") == "fresh"
    assert (base / ".bundle-sha256").read_text(encoding="utf-8").strip() == digest


def test_refresh_template_forces_replacement(tmp_path):
    old_zip, old_digest = make_bundle(tmp_path, "old", {"asset.txt": "old"})
    repo = make_template(tmp_path, "paper-house", old_zip, old_digest)
    run_fetch(repo, "--template", "paper-house")

    new_zip, new_digest = make_bundle(tmp_path, "new", {"asset.txt": "new"})
    manifest = repo / "assets" / "templates" / "paper-house" / "template.json"
    manifest.write_text(
        json.dumps(
            {
                "asset_bundle": {
                    "local_path": "base/",
                    "url": str(new_zip),
                    "sha256": new_digest,
                }
            }
        ),
        encoding="utf-8",
    )

    run_fetch(repo, "--refresh-template", "paper-house")

    base = repo / "assets" / "templates" / "paper-house" / "base"
    assert (base / "asset.txt").read_text(encoding="utf-8") == "new"
    assert (base / ".bundle-sha256").read_text(encoding="utf-8").strip() == new_digest
