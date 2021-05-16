# Modular Notes App 0.5.0

Eli tuttavallisemmin *MoNoA*, on modulaarinen muistiinpanosovellus, jossa käyttäjä hallinnoi
muistiinpanojaan (ja ajatustyötään) koostamalla isompia kokonaisuuksia (notes) pienistä palasista
(snips).


## Tilannekatsaus su 16.5.2021

- Ohjelman voi onnistuneesti suorittaa kunhan on ensin tehnyt tarvittavat alustustoimenpiteet
- Käyttäjä voi luoda uusia noteja
- Käyttäjä voi muokata noten otsikkoa
- Käyttäjä voi luoda uusia snippejä noten sisään
- Käyttäjä voi selata noteja listalla
- Käyttäjä voi etsiä noteja hakutoiminnolla
- Käyttäjä voi exportata noten sisällön tekstitiedostoksi
- Notet ja snipit tallentuvat reaaliajassa sqlite3-tietokantaan


## Uusin Release

- [Release Viikko 7](https://github.com/algoholik/modularnotes/releases/tag/viikko7)


## Dokumentaatio

- [Käyttöohje](https://github.com/algoholik/modularnotes/blob/main/dokumentaatio/kayttoohje.md)
- [Vaatimusmäärittely](https://github.com/algoholik/modularnotes/blob/main/dokumentaatio/vaatimusmaarittely.md)
- [Arkkitehtuurikuvaus](https://github.com/algoholik/modularnotes/blob/main/dokumentaatio/arkkitehtuuri.md)
- [Testausdokumentaatio](https://github.com/algoholik/modularnotes/blob/main/dokumentaatio/testaus.md)
- [Tuntikirjanpito](https://github.com/algoholik/modularnotes/blob/main/dokumentaatio/tuntikirjanpito.md)


## Asennus

1. Asenna ensin riippuvuudet:
```bash
poetry install
```

2. Suorita vaadittavat alustustoimenpiteet:
```bash
poetry run invoke build
```

3. Käynnistä MoNoA-sovellus:
```bash
poetry run invoke start
```


## Ohjelman suorittaminen

Ohjelma suoritetaan komennolla:
```bash
poetry run invoke start
```


## Testaus


### Testit
Testit saa ajettua komennolla:
```bash
poetry run invoke test
```


### Testikattavuus
Testikattavuusraportin voi generoida komennolla:
```bash
poetry run invoke coverage-report
```


Raportti generoituu projektin juurihakemistoon kansion _htmlcov_ alle.



## Linting


### Pylint
Linttaa komennolla:
```bash
poetry run invoke lint
```
