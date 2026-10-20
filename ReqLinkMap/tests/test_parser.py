import unittest

from req_link_map.parser import build_graph, merge_requirements, parse_pages


class ParserTests(unittest.TestCase):
    def test_parses_versioned_headers_across_pages(self) -> None:
        requirements = parse_pages(
            [
                "Introduction\nREQ-1000v2 Power control\nPurpose:\nKeep power stable.",
                "- 2 -\nContinued text.\nREQ - 2000v5 Recovery handling\nRecover safely.",
            ],
            "sample.pdf",
        )

        self.assertEqual([item.id for item in requirements], ["REQ-1000", "REQ-2000"])
        self.assertEqual(requirements[0].pages, [1, 2])
        self.assertEqual(requirements[1].version, "5")

    def test_resolves_spaced_ids_and_exact_names(self) -> None:
        requirements = parse_pages(
            [
                "REQ-1000v2 Power control\nSee REQ - 2000 and Recovery handling.\n"
                "REQ-2000v1 Recovery handling\nRecover safely.",
            ],
            "sample.pdf",
        )

        graph = build_graph(requirements)
        edge_types = {(edge["target"], edge["type"]) for edge in graph["edges"]}
        self.assertEqual(edge_types, {("REQ-2000", "id"), ("REQ-2000", "name")})

    def test_keeps_missing_and_direct_references_visible(self) -> None:
        requirements = parse_pages(
            ["REQ-1000v1 Source\nSee REQ-9999 and https://example.test/REQ-2000."],
            "sample.pdf",
        )

        graph = build_graph(requirements)

        self.assertEqual({node["id"] for node in graph["nodes"]}, {"REQ-1000", "REQ-2000", "REQ-9999"})
        self.assertEqual({edge["type"] for edge in graph["edges"]}, {"id", "direct"})

    def test_merge_prefers_latest_version(self) -> None:
        older = parse_pages(["REQ-1000v1 Old title\nOld text"], "old.pdf")
        newer = parse_pages(["REQ-1000v3 New title\nNew text"], "new.pdf")

        merged = merge_requirements([*older, *newer])

        self.assertEqual([(item.version, item.title) for item in merged], [("3", "New title")])


if __name__ == "__main__":
    unittest.main()