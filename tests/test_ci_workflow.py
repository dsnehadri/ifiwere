"""The GitHub Actions workflow must keep running this suite.

The YAML check needs PyYAML, which is not in the standard library, so it
skips when PyYAML is missing; the structural checks below run either way.
"""

import os
import re
import unittest

import jsdata

WORKFLOW = os.path.join(jsdata.REPO_ROOT, ".github", "workflows", "tests.yml")
TEST_COMMAND = "python3 -m unittest discover -s tests"


def read():
    with open(WORKFLOW, encoding="utf-8") as fh:
        return fh.read()


class WorkflowTests(unittest.TestCase):

    def test_the_workflow_exists(self):
        self.assertTrue(os.path.isfile(WORKFLOW), "%s is missing" % WORKFLOW)

    def test_it_runs_the_same_command_as_a_developer_does(self):
        self.assertIn(TEST_COMMAND, read())

    def test_it_triggers_on_push_and_pull_request(self):
        text = read()
        self.assertRegex(text, r"(?m)^on:")
        self.assertRegex(text, r"(?m)^\s+push:")
        self.assertRegex(text, r"(?m)^\s+pull_request:")

    def test_actions_are_pinned_to_a_major_version(self):
        uses = re.findall(r"uses:\s*(\S+)", read())
        self.assertTrue(uses, "the workflow uses no actions")
        for ref in uses:
            with self.subTest(action=ref):
                self.assertRegex(ref, r"@v\d+$", "action is not pinned to a major version")

    def test_the_token_is_read_only(self):
        # The suite only reads the checkout; nothing should be able to write
        # back to the repository from CI.
        self.assertRegex(read(), r"(?m)^permissions:\s*$")
        self.assertRegex(read(), r"(?m)^\s+contents:\s*read\s*$")

    def test_it_has_no_secrets_and_no_deploy_step(self):
        text = read()
        self.assertNotIn("secrets.", text)
        for word in ("deploy", "publish", "release", "npm publish", "gh-pages"):
            with self.subTest(word=word):
                self.assertNotIn(word, text.lower())

    def test_the_yaml_parses(self):
        try:
            import yaml
        except ImportError:
            self.skipTest("PyYAML is not installed")
        data = yaml.safe_load(read())
        self.assertIn("jobs", data)
        # `on:` is YAML 1.1 truthy, so PyYAML gives back the boolean True.
        triggers = data.get("on", data.get(True))
        self.assertIsNotNone(triggers, "the workflow has no triggers")
        self.assertEqual(set(triggers), {"push", "pull_request"})
        self.assertEqual(data.get("permissions"), {"contents": "read"})
        steps = data["jobs"]["unittest"]["steps"]
        self.assertTrue(any(TEST_COMMAND in (s.get("run") or "") for s in steps))


if __name__ == "__main__":
    unittest.main()
