import unittest
from maksukortti import Maksukortti
from kassapaate import Kassapaate

class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()

    def test_kassapaate_luodaan_oikein(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_syo_edullisesti_kateisella_kasvattaa_kassan_rahamaaraa_oikein_ja_vaihtoraha_on_oikein(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(300), 60)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100240)
        self.assertEqual(self.kassapaate.edulliset, 1)

    def test_syo_maukkaasti_kateisella_kasvattaa_kassan_rahamaaraa_oikein_ja_vaihtoraha_on_oikein(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(500), 100)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100400)
        self.assertEqual(self.kassapaate.maukkaat, 1)

    def test_syo_edullisesti_kateisella_kun_rahat_ei_riita_mikaan_ei_muutu_kassassa_ja_maksu_palautetaan(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(200), 200)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_syo_maukkaasti_kateisella_kun_rahat_ei_riita_mikaan_ei_muutu_kassassa_ja_maksu_palautetaan(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(300), 300)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_syo_edullisesti_kortilla_kun_tarpeeksi_rahaa_kortilla_veloitetaan_summa_oikein(self):
        maksukortti = Maksukortti(1000)
        self.assertEqual(self.kassapaate.syo_edullisesti_kortilla(maksukortti), True)
        self.assertEqual(str(maksukortti), "saldo: 7.6")

    def test_syo_maukkaasti_kortilla_kun_tarpeeksi_rahaa_kortilla_veloitetaan_summa_oikein(self):
        maksukortti = Maksukortti(1000)
        self.assertEqual(self.kassapaate.syo_maukkaasti_kortilla(maksukortti), True)
        self.assertEqual(str(maksukortti), "saldo: 6.0")

    def test_syo_edullisesti_kortilla_kun_tarpeeksi_rahaa_kortilla_kasvaa_myytyjen_lounaiden_maara_oikein(self):
        maksukortti = Maksukortti(1000)
        self.kassapaate.syo_edullisesti_kortilla(maksukortti)
        self.assertEqual(self.kassapaate.edulliset, 1)

    def test_syo_maukkaasti_kortilla_kun_tarpeeksi_rahaa_kortilla_kasvaa_myytyjen_lounaiden_maara_oikein(self):
        maksukortti = Maksukortti(1000)
        self.kassapaate.syo_maukkaasti_kortilla(maksukortti)
        self.assertEqual(self.kassapaate.maukkaat, 1)

    def test_syo_edullisesti_kortilla_rahat_ei_riita_korttia_ei_veloiteta_eika_myytyjen_lounaiden_maara_kasva(self):
        maksukortti = Maksukortti(200)
        self.assertEqual(self.kassapaate.syo_edullisesti_kortilla(maksukortti), False)
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(str(maksukortti), "saldo: 2.0")

    def test_syo_maukkaasti_kortilla_rahat_ei_riita_korttia_ei_veloiteta_eika_myytyjen_lounaiden_maara_kasva(self):
        maksukortti = Maksukortti(300)
        self.assertEqual(self.kassapaate.syo_maukkaasti_kortilla(maksukortti), False)
        self.assertEqual(self.kassapaate.maukkaat, 0)
        self.assertEqual(str(maksukortti), "saldo: 3.0")

    def test_syo_edullisesti_kortilla_kassan_rahamaara_ei_muutu(self):
        maksukortti_saldoa = Maksukortti(500)
        maksukortti_eisaldoa = Maksukortti(100)
        self.kassapaate.syo_edullisesti_kortilla(maksukortti_saldoa)
        self.kassapaate.syo_edullisesti_kortilla(maksukortti_eisaldoa)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_syo_maukkaasti_kortilla_kassan_rahamaara_ei_muutu(self):
        maksukortti_saldoa = Maksukortti(500)
        maksukortti_eisaldoa = Maksukortti(100)
        self.kassapaate.syo_maukkaasti_kortilla(maksukortti_saldoa)
        self.kassapaate.syo_maukkaasti_kortilla(maksukortti_eisaldoa)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_lataa_rahaa_kortille_kasvattaa_kortin_saldoa_oikein(self):
        maksukortti = Maksukortti(500)
        self.kassapaate.lataa_rahaa_kortille(maksukortti, 500)
        self.assertEqual(str(maksukortti), "saldo: 10.0")

    def test_lataa_rahaa_kortille_kasvattaa_kassan_rahamaaraa_oikein(self):
        maksukortti = Maksukortti(500)
        self.kassapaate.lataa_rahaa_kortille(maksukortti, 500)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100500)

    def test_lataa_rahaa_kortille_ei_tee_mitaan_jos_summa_on_negatiivinen(self):
        maksukortti = Maksukortti(500)
        self.kassapaate.lataa_rahaa_kortille(maksukortti, -100)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
