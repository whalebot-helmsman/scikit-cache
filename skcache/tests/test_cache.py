import skcache

import unittest

import sklearn.ensemble


side_effect = ''
modifier = 'affected'

def reset_side_effect():
    global side_effect
    side_effect = ''

def times_side_effects_happen():
    global side_effect
    return len(side_effect) / len(modifier)

def side_effected():
    global side_effect
    side_effect = side_effect + modifier

class Tester:
    def __init__(self):
        self.a = 1
        self.b = 2

    def mutate(self):
        self.a = 2 * self.a
        self.b = self.b * self.b
        side_effected()

class TestCached(unittest.TestCase):

    def test_return_self_from_bound(self):
        A = Tester()
        mutate_1 = skcache.return_self_from_bound(A.mutate)
        ret, self_ret = mutate_1()
        self.assertEqual(None, ret)
        self.assertEqual(self_ret, A)

    def test_field_of_cached_is_assignable(self):
        A = skcache.Cached(Tester())
        A.a = 56
        self.assertEqual(56, A.a)

    def test_is_cache_works(self):
        reset_side_effect()

        skcache.default_memory.clear()

        A = skcache.Cached(Tester())
        B = skcache.Cached(Tester())
        C = Tester()

        C.mutate()
        self.assertEqual(times_side_effects_happen(), 1)

        A.mutate()
        self.assertEqual(A.a, C.a)
        self.assertEqual(A.b, C.b)
        self.assertEqual(times_side_effects_happen(), 2)

        B.mutate()
        self.assertEqual(B.a, C.a)
        self.assertEqual(B.b, C.b)
        self.assertEqual(times_side_effects_happen(), 2)

    def test_is_cache_sklearn_cloneable(self):
        C1 = sklearn.ensemble.GradientBoostingClassifier()
        C2 = skcache.Cached(sklearn.ensemble.GradientBoostingClassifier())
        C3 = sklearn.base.clone(C2)
        self.assertNotEqual(C3.__class__, C1.__class__)
        self.assertEqual(C3.__class__, C2.__class__)
        self.assertEqual(C3.__getattr__(skcache.Cached.PROXIED).__class__, C1.__class__)
        self.assertEqual(C2.__getattr__(skcache.Cached.PROXIED).__class__, C1.__class__)
