import unittest
from types import SimpleNamespace

from cogs.owner import Owner


class OwnerSearchFilterTests(unittest.TestCase):
    def _message(self, author_id=1, content="", mention_ids=None):
        if mention_ids is None:
            mention_ids = []
        return SimpleNamespace(
            author=SimpleNamespace(id=author_id),
            clean_content=content,
            mentions=[SimpleNamespace(id=mention_id) for mention_id in mention_ids],
        )

    def test_matches_when_all_filters_match(self):
        message = self._message(author_id=42, content="hello world", mention_ids=[99])
        self.assertTrue(
            Owner._matches_search_filters(
                message,
                user=SimpleNamespace(id=42),
                message_query="world",
                mentions=SimpleNamespace(id=99),
            )
        )

    def test_rejects_when_author_does_not_match(self):
        message = self._message(author_id=5, content="hello world")
        self.assertFalse(
            Owner._matches_search_filters(message, user=SimpleNamespace(id=42))
        )

    def test_rejects_when_message_text_does_not_match(self):
        message = self._message(author_id=42, content="hello world")
        self.assertFalse(
            Owner._matches_search_filters(message, message_query="nope")
        )

    def test_rejects_when_mention_does_not_match(self):
        message = self._message(author_id=42, content="hello world", mention_ids=[50])
        self.assertFalse(
            Owner._matches_search_filters(message, mentions=SimpleNamespace(id=99))
        )


if __name__ == "__main__":
    unittest.main()
