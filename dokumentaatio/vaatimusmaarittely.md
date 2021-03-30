# Vaatimusmäärittely

## Sovelluksen tarkoitus

**MoNoA** -sovelluksen avulla käyttäjä voi koostaa isompia muistiinpanoja _notes_, pienemmistä osatekijöistä _snippets_. 
Nämä pienemmät *snippetit* voivat olla joko ns. globaaleja (kun päivität yhtä snippettiä yhdessä muistiinpanossa
päivittyvät kaikki sen instanssit kaikissa muissakin muistiinpanoissa joissa sitä esiintyy), tai paikallisia
(snippetin muokkaus ei vaikuta muualle). 

MoNoA soveltuu ajatustyöhön, jossa käytetään toistuvasti samoja pienempiä elementtejä, ja siksi se soveltuu hyvin esimerkiksi tehtävä- ja ostoslistojen tekemiseen, tai vaikkapa koodinpätkien hallinnointiin.


## Käyttäjät

Alkuvaiheessa sovelluksella on ainoastaan yksi käyttäjärooli eli _normaali käyttäjä_. Myöhemmin sovellukseen saatetaan lisätä joko mahdollisuus suojata yksittäisiä muistiinpanoja salasanalla, tai kokonaan usean käyttäjän mahdollistava _käyttäjätilien hallinta_.


## Käyttöliittymäluonnos

Sovellus koostuu kahdesta eri päänäkymästä:

1. Muokkausnäkymä:
   - muistiinpanon valinta
   - muistiinpanon muokkaus
     - snippetin lisäys muistiinpanoon
     - snippetin poisto muistiinpanosta
   - lista snippeteistä

2. Hahmotusnäkymä:
   - lista muistiinpanoista ja snippeteistä
   - mahdollisuus lajitella muistiinpanoja ja snippettejä niiden sisällön mukaan


## Perusversion tarjoama toiminnallisuus

- Käyttäjä voi luoda muistiinpanoja
- Käyttäjä voi muuttaa osan muistiinpanon sisällöstä snippetiksi
- Käyttäjä voi lisätä luotuja snippettejä osaksi muistiinpanoja
- Käyttäjä voi määritellä onko snippetti globaali vai paikallinen


## Jatkokehitysideoita

Perusversion jälkeen MoNoAa voisi jatkokehittää ominaisuuksilla kuten:

- Useita erilaisia snippettejä:
  - Teksti
  - Todo-listaus
  - Laskukaava
  - Dynaaminen linkki (esim. kalenterimerkintään)
- Käyttäjä voisi löytää helposti muita samankaltaisia muistiinpanoja:
  - Muistiinpanot joissa esiintyy eniten samoja snippettejä
  - Muistiinpanot joissa esiintyy eniten samoja sanoja
- Muistiinpanojen exporttaus haluttuun formaattiin: 
  - markdown
  - html
  - pdf
- Salasanasuojatut muistiinpanot
- Mahdollisuus jakaa muistiinpanoja muille käyttäjille
- Jaetut muistiinpanot usean käyttäjän kesken