# Modular Notes App 0.1.0

Eli tuttavallisemmin *MoNoA*, on modulaarinen muistiinpanosovellus, jossa käyttäjä hallinnoi
muistiinpanojaan (ja ajatustyötään) koostamalla isompia kokonaisuuksia (documents) pienistä palasista
(snippets).


## Dokumentaatio

- [Vaatimusmäärittely](https://github.com/algoholik/modularnotes/blob/main/dokumentaatio/vaatimusmaarittely.md)


## Asennus

1. Asenna ensin riippuvuudet:
```bash
poetry install
```

2. Suorita vaadittavat alustukset:
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


Raportti generoituu _htmlcov_-hakemistoon.
