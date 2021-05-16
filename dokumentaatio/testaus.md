# Testausdokumentaatio

## Yksikkötestaus

### Testikattavuus

UI-kerrosta lukuunottamatta pytestin haarautumakattavuus on 61 %.

![Testikattavuus](./kuvat/pytest_coverage.png)

## Järjestelmätestaus

Sovellusta on järjestelmätestattu manuaalisesti käyttöliittymää läpikäymällä ja toisintamalla sovelluksen käyttöohjeen ohjeita.

[Vaatimusmäärittelydokumentin](https://github.com/algoholik/modularnotes/blob/main/dokumentaatio/vaatimusmaarittely.md) valmiiksi merkatut kohdat on testattu läpi.

## Sovellukseen jääneet ongelmat

Sovellus ei anna selkeitä virheilmoituksia, jos:
- käyttäjällä ei ole luku/kirjoitusoikeuksia kansioihin joissa ohjelmaa ajetaan
- asennusohjeita ei ole noudatettu huolellisesti

Ilmeisesti sovellus saattaa myös kaatua jos uusia noteja lisätään hyvin nopeaan tahtiin.
