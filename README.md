# Modular Notes App 0.1.0

Eli tuttavallisemmin *MoNoA*, on modulaarinen muistiinpanosovellus, jossa käyttäjä hallinnoi
muistiinpanojaan (ja ajatustyötään) koostamalla isompia kokonaisuuksia (documents) pienistä palasista
(snippets).


## Tilannekatsaus ti 20.4.2021

- Ohjelman voi onnistuneesti buildaa ja starttaa
- Ulkoasu kehittynyt huomattavasti
- Käyttäjä voi luoda uusia snippettejä
- Käyttäjä voi katsoa jo luotuja snippetteja listasta
- Snippetit tallentuvat sqlite3-tietokantaan
- Testien haarautumakattavuus


## Dokumentaatio

- [Vaatimusmäärittely](https://github.com/algoholik/modularnotes/blob/main/dokumentaatio/vaatimusmaarittely.md)
- [Arkkitehtuurikuvaus](https://github.com/algoholik/modularnotes/blob/main/dokumentaatio/arkkitehtuuri.md)
- [Tuntikirjanpito](https://github.com/algoholik/modularnotes/blob/main/dokumentaatio/tuntikirjanpito.md)


## Asennus

1. Asenna ensin riippuvuudet:
```bash
poetry install
```

2. Suorita vaadittavat alustukset:
```bash
poetry run invoke build
```
(2.1. Vaihtoehtoisesti voit alustaa sovelluksen esimerkkisisällöllä demoamistarkoituksiin:)
```bash
poetry run invoke build-demo
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
