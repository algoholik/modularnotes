import unittest
from maksukortti import Maksukortti

class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(1000)

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)

    def test_kortin_saldo_alussa_oikein(self):
        self.assertEqual(str(self.maksukortti), "saldo: 10.0")

    def test_rahan_lataaminen_kasvattaa_saldoa_oikein(self):
        self.maksukortti.lataa_rahaa(1550)
        self.assertEqual(str(self.maksukortti), "saldo: 25.5")

    def test_saldo_vahenee_oikein_jos_rahaa_tarpeeksi(self):
        self.assertEqual(self.maksukortti.ota_rahaa(1000), True)

    def test_saldo_ei_muutu_jos_rahat_ei_riita(self):
        self.assertEqual(self.maksukortti.ota_rahaa(1200), False)
