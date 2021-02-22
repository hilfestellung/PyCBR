import unittest
from cbrlib.reasoning.Reasoner import InferenceOptions


class TestLinearReasoner(unittest.TestCase):

    def test_inference_options(self):
        opts = InferenceOptions({
            'skip': 2
        })
        self.assertEqual(opts.skip, 2)
        self.assertEqual(opts.limit, 10)
        opts = InferenceOptions({
            'limit': 20
        })
        self.assertEqual(opts.skip, 0)
        self.assertEqual(opts.limit, 20)
        opts = InferenceOptions({
            'skip': 1,
            'limit': 5
        })
        self.assertEqual(opts.skip, 1)
        self.assertEqual(opts.limit, 5)


if __name__ == '__main__':
    unittest.main()
