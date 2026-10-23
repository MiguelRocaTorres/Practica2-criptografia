import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from measure import index_of_coincidence


def test_index_of_coincidence_b1_text1():
    text_1 = """CRYPTANALYSIS"""
    expected_ic_1 = 0.0385
    assert abs(index_of_coincidence(text_1) - expected_ic_1) < 0.001


def test_index_of_coincidence_b1_text2():
    text_2 = """THEINDEXOFCOINCIDENCE"""
    expected_ic_2 = 0.0810

    assert abs(index_of_coincidence(text_2) - expected_ic_2) < 0.001