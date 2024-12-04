from unittest import TestCase

from active_collab_app.statistics import Counter, Statistics


class TestCounter(TestCase):
    def test_counter(self):
        cnt = Counter()
        self.assertEqual(0, cnt.get())
        cnt.increment()
        self.assertEqual(1, cnt.get())
        cnt.increment()
        self.assertEqual(2, cnt.get())
        cnt.reset()
        self.assertEqual(0, cnt.get())


class TestStatistics(TestCase):
    def test_projects(self):
        stats = Statistics()
        values = stats.get()
        self.assertEqual(0, values["projects"])
        stats.projects.increment()
        values = stats.get()
        self.assertEqual(1, values["projects"])
        stats.reset_all()
        values = stats.get()
        self.assertEqual(0, values["projects"])
