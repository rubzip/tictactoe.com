import pytest
from app.services.rating import EloEngine

def test_compute_draw():
    r1, r2 = 1000, 1000
    new_r1, new_r2 = EloEngine.compute(r1, r2, 0.5)
    assert new_r1 == 1000
    assert new_r2 == 1000

def test_compute_win():
    r1, r2 = 1000, 1000
    new_r1, new_r2 = EloEngine.compute(r1, r2, 1.0)
    assert new_r1 > 1000
    assert new_r2 < 1000
    assert new_r1 + new_r2 == 2000

def test_compute_probability():
    r1, r2 = 1200, 1000
    e1, e2 = EloEngine.compute_probability(r1, r2)
    assert e1 > e2
    assert pytest.approx(e1 + e2) == 1.0
