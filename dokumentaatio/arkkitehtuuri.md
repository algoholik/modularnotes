# Arkkitehtuurikuvaus


## Rakenne

Sovelluksen rakenne jakaantuu kolmeen osaan:

![Pakkausrakenne](./kuvat/monoa_packaging.png)

*ui* -moduuli sisältää sovelluksen käyttöliittymäkoodin jaettuna luokittain eri alimoduleihin.
*monoa_service* -moduuli sisältää sovelluslogiikan ja toimii viestinviejänä tasojen 1 ja 3 välillä.
*entities* -moduuli pitää sisällään sovelluksessa käytetyt objektiluokat.
*database* -moduuli vastaa sovelluksen datan tallentamisesta tietokantatiedostoon.


## Käyttöliittymä

Sovelluksen käyttöliittymä koostuu kahdeksasta luokasta, joilla jokaisella on oma vastuualue sovelluksen
toiminnallisuuksien visualisoinnissa.

![Käyttöliittymäluokkien rakenne](./kuvat/monoa_ui_structure.png)

1. MonoaMainWindow
   - Sovellusikkunan "kattoluokka", joka piirtää sovellusikkunan sekä jakaa sen kahteen osaan:
     - Sovelluksen käyttöliittymä (MonoaUI)
     - Statuspalkki
     - (jatkossa myös mahdollisesti työkalupalkki)

2. MonoaUI
   - Käyttöliittymän "kattoluokka", joka jakaa näkymän kahteen alaluokkaan:
     - MonoaBrowser
     - MonoaNoteViewer

3. MonoaBrowser
   - MonoaBrowser vastaa notes-listauksen piirtämisestä ja toiminnallisuuksista.

4. MonoaListItem
   - MonoaListItem vastaa notes-listauksen yksittäisen noten esittämisestä sekä muutosten kommunikoinnista 
   editorin ja sovelluslogiikan suuntaan.

5. MonoaNoteViewer
   - Vastaa muokattavaksi valitun noten sisällön ja toiminnallisuuksien piirtämisestä.

6. MonoaNoteContainer
   - Vastaa snip-objektien esittämisestä listana muokkauksen alla olevan noten sisällä sekä snipeihin 
   kohdistuvista toiminnallisuuksista.

7. MonoaSnipEditor
   - Vastaa yksittäisen noten sisältämän snipin piirtämisestä tietoineen ja toiminnallisuuksineen.

8. MonoaTextEdit
   - Custom PyQt-luokka QTextEdit-luokan pohjalta, joka tarjoaa dynaamisesti tekstisisällön mukaan 
   venyvän tekstieditorin sekä aktiivisen rivin korostustoiminnallisuuden.


## Sovelluslogiikka

Sovelluslogiikasta vastaa pakkauksen *monoa_service* luokka _MonoaService_, tarjoten käyttöliittymälle 
metodeja joilla tallentaa ja saada ajantasainen sisältö esiin käyttäjälle.

_(Työn alla...)_


## Tietojen tallentaminen

Pakkaus *database.db_handler* tarjoaa sovelluslogiikasta huolehtivalle MonoaService -luokalle valikoiman 
funktioita joilla käyttäjän luoma ja muokkaama data tallennetaan sqlite3 -tietokantatiedostoon.
