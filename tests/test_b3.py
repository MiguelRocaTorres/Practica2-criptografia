import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import kasiski
CIPHERTEXT_B3 = """
ELQYR JVQDR LXEGB ELQQV ALQFE PTQOG DEZRG SIDSC PEFGO PXDOL
ELQYR JXAOA LPKGV D
"""

def test_kasiski_distances():
    expected_dists = [15, 35, 50]
    dists = kasiski.distances(CIPHERTEXT_B3, min_len=3)
    assert sorted(dists) == sorted(expected_dists), f"Distancias incorrectas: {dists}"

def test_kasiski_factor_tally():
    tally = kasiski.factor_tally(CIPHERTEXT_B3)
    assert tally.get(5) == 3, f"El factor 5 debería tener recuento 3, obtenido: {tally.get(5)}"
    best_factor = max(tally.items(), key=lambda item: item[1])[0]
    assert best_factor == 5, f"La clave detectada debería ser 5, obtenido: {best_factor}"