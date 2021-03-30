# Vaatimusmäärittely

## Sovelluksen tarkoitus

**MoNoA** -sovelluksen avulla käyttäjä voi koostaa isompia muistiinpanoja _notes_, pienemmistä osatekijöistä _snippets_. 
Nämä pienemmät *snippetit* voivat olla joko ns. globaaleja (kun päivität yhtä snippettiä yhdessä muistiinpanossa
päivittyvät kaikki sen instanssit kaikissa muissakin muistiinpanoissa joissa sitä esiintyy), tai paikallisia
(snippettin muokkaus ei vaikuta muualle). 

MoNoA soveltuu ajatustyöhön, jossa käytetään toistuvasti samoja pienempiä elementtejä, ja siksi se soveltuu hyvin esimerkiksi esimerkiksi tehtävä- ja ostoslistojen tekemiseen, tai vaikkapa koodinpätkien hallinnointiin.

## Käyttäjät

Alkuvaiheessa sovelluksella on ainoastaan yksi käyttäjärooli eli _normaali käyttäjä_. Myöhemmin sovellukseen saatetaan lisätä joko mahdollisuus suojata muistiinpanoja salasanalla, tai usean käyttäjän mahdollistava _käyttäjätilien hallinta_.

## Käyttöliittymäluonnos

Sovellus koostuu kahdesta eri päänäkymästä:

1. Muokkausnäkymä:
   - muistiinpanon valinta
   - muistiinpanon muokkaus
     - snippetin lisäys muistiinpanoon
     - snippetin poisto muistiinpanosta
   - lista snippeteistä

2. Hahmotusnäkymä:
   - Näkymä jossa näytetä


## Perusversion tarjoama toiminnallisuus

- Käyttäjä voi luoda muistiinpanoja
- Käyttäjä voi muuttaa osan muistiinpanon sisällöstä snippetiksi
- Käyttäjä voi lisätä luotuja snippettejä osaksi muistiinpanoja
- Käyttäjä voi määritellä onko snippetti globaali vai paikallinen


## Jatkokehitysideoita

Perusversion jälkeen MoNoAa voisi jatkokehittää ominaisuuksilla kuten:

- tehdyksi merkittyjen todojen tarkastelu
- tehdyksi merkittyjen todojen merkkaaminen tekemättömiksi
- todon tietojen editointi
- todojen järjestely tärkeysjärjestykseen
- todojen määrittely muille käyttäjille
- käyttäjätiimit, jotka näkevät kaikki yhteiset todot
- mahdollisuus useampaan erilliseen todo-listaan
- lisätään todoon kenttä, johon on mahdollista merkitä tarkempia todoon liittyviä tietoja
- käyttäjien yhteyteen salasana, joka vaaditaan kirjautuessa
- käyttäjätunnuksen (ja siihen liittyvien todojen) poisto
