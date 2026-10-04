# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: CC-BY-4.0

"""Regression checks for agent-readable documentation validation."""

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from bs4 import BeautifulSoup
from mkdocs.commands.build import build
from mkdocs.config import load_config

from check_agent_docs import check, expected_markdown_path


class AgentDocsCheckTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.root = Path(self.temporary_directory.name)
        self.site = self.root / "site"
        self.site.mkdir()

    def write_index(self, *pages):
        entries = "".join(
            f"- [{title}](https://docs.agntcy.org/{path}): {description}\n"
            for title, path, description in pages
        )
        (self.site / "llms.txt").write_text(
            "# Agntcy\n\n> Open infrastructure for agents.\n\n"
            "## AGNTCY Hub\n\n" + entries,
            encoding="utf-8",
        )

    def write_page(self, path, content="# Example\n"):
        output = self.site / path
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(content, encoding="utf-8")

    def test_missing_navigated_page_is_reported(self):
        self.write_index(("Home", "index.md", "Start here."))
        self.write_page("index.md")

        with self.assertRaisesRegex(ValueError, "guide/index.md"):
            check(self.site, {Path("index.md"), Path("guide/index.md")})

    def test_missing_generated_twin_is_reported(self):
        self.write_index(("Guide", "guide/index.md", "Read the guide."))

        with self.assertRaisesRegex(ValueError, "no generated page"):
            check(self.site, {Path("guide/index.md")})

    def test_unresolved_macro_is_reported(self):
        self.write_index(("Home", "index.md", "Start here."))
        self.write_page("index.md", "See [[ agntcy.dir_url ]].\n")

        with self.assertRaisesRegex(ValueError, "Unresolved AGNTCY macro"):
            check(self.site, {Path("index.md")})

    def test_pretty_url_paths_match_mkdocs_output(self):
        self.assertEqual(expected_markdown_path(Path("index.md")), Path("index.md"))
        self.assertEqual(
            expected_markdown_path(Path("guide/setup.md")),
            Path("guide/setup/index.md"),
        )


class BuiltSiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary_directory = tempfile.TemporaryDirectory()
        cls.site = Path(cls.temporary_directory.name) / "site"
        root = Path(__file__).resolve().parents[2]
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "mkdocs",
                "build",
                "--config-file",
                str(root / "mkdocs" / "mkdocs.yml"),
                "--site-dir",
                str(cls.site),
            ],
            cwd=root,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode:
            cls.temporary_directory.cleanup()
            raise AssertionError(result.stdout + result.stderr)

    @classmethod
    def tearDownClass(cls):
        cls.temporary_directory.cleanup()

    def test_code_language_survives_rendering(self):
        content = (self.site / "contributing" / "index.md").read_text(encoding="utf-8")
        self.assertIn('Is displayed as:\n\n```python\nprint("Hello, World!")', content)

        for page in (
            "coffee-agntcy/get-started/index.md",
            "coffee-agntcy/identity-coffee-agntcy/index.md",
        ):
            with self.subTest(page=page):
                content = (self.site / page).read_text(encoding="utf-8")
                self.assertEqual(content.count("```mermaid\n"), 3)

    def test_head_links_resolve_to_generated_files(self):
        for page in (
            Path("index.html"),
            Path("contributing/index.html"),
            Path("oasf/oasf-sdk/index.html"),
        ):
            with self.subTest(page=page):
                html = (self.site / page).read_text(encoding="utf-8")
                soup = BeautifulSoup(html, "html.parser")
                alternate = soup.find("link", rel="alternate", type="text/markdown")
                describedby = soup.find("link", rel="describedby", type="text/plain")
                self.assertEqual(alternate["href"], "index.md")
                self.assertTrue((self.site / page.parent / alternate["href"]).is_file())
                self.assertTrue(
                    (self.site / page.parent / describedby["href"]).is_file()
                )
                self.assertIsNone(soup.select_one(".agntcy-agent-entry"))

    def test_unlisted_markdown_does_not_break_build(self):
        root = Path(__file__).resolve().parents[2]
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            docs = temporary / "docs"
            shutil.copytree(root / "docs", docs)
            (docs / "internal-notes.md").write_text(
                "# Internal notes\n", encoding="utf-8"
            )
            site = temporary / "site"
            config = load_config(
                config_file=str(root / "mkdocs" / "mkdocs.yml"),
                docs_dir=str(docs),
                site_dir=str(site),
            )
            build(config)
            self.assertTrue((site / "internal-notes" / "index.html").is_file())
            self.assertNotIn(
                "internal-notes", (site / "llms.txt").read_text(encoding="utf-8")
            )


if __name__ == "__main__":
    unittest.main()
