# PSIV - TRAKING

proves de moment (eliminar)

output7(short):   resultat profe: (baixades 2/ pujades 6)  -- resultat nostre (baixades 2/ pujades 7) 

output2 (middle):   resultat profe: (baixades 7/ pujades 5)  -- resultat nostre (baixades 8 / pujades 5) 

output3 (shadow):   resultat profe: (baixades 10/ pujades 3)  -- resultat nostre (baixades 10/ pujades 3 ) 

output5 (long1):   resultat profe: (baixades 24/ pujades 8)  -- resultat nostre (baixades 31/ pujades 17) 

output6 (long2):   resultat profe: (baixades 133/ pujades 6)  -- resultat nostre (baixades 153/ pujades 14) 

## Objectiu
L'objectiu d'aquest repte és saber quants automobils es mouen en cada un dels carrils d'entrada / sortida.

El seguiment dobjectes és una tasca important en la visió artificial. Els algorismes de seguiment d'objectes són una part integral de moltes aplicacions de visió per ordinador que processen el flux de vídeo de les càmeres.

## Codi
El projecte conté els següents arxius *.py*:
1. ``traking.py ``: Conté el codi principal del projecte, a l'executarlo es posa en funcionament tot el sistema de detcció,traking i contador de cotxes.
2. ``CentroidTraker.py``: Conte la classe CentroidTraker la cual utilitzem per poder fer el traking de cotxes en temps real.
## Solució

### Zona Detecció
Per fer el recompte de quants automòbils pugen o baixen, primer de tot hem limitat la zona de vídeo per guanyar velocitat i reduir computacions innecessàries i soroll ja que només interessa els automòbils que pugen o baixen de la part inferior de la carretera, obviant la carretera superior amb moviments d'esquerra a dreta.

Per tant la "camara de seguretat" o el video es limiteria en aquest espai *Figura 1*:

#### Figura 1
| Video Rebut | Part interesada |
| -------------| ------------- | 
|![image](https://github.com/SergiTordera/PSIV---TRAKING/assets/61145059/155f3139-2361-498e-a1b3-44270e9edc3e)|![image](https://github.com/SergiTordera/PSIV---TRAKING/assets/61145059/1b3889d9-2b18-469d-8d31-f3c72cb809a2)|

### Background Substraction
Per poder detctar el moviment dels cotxes en el vídeo, hem implementat un *background substraction*, per evitar que aquest *background substraction* crei soroll  l'obtenim a partir d'una mitjana dels X frames anteriors en el moment actual del video. Per tant al calcular la diferencia absoluta obtenim els seguents resultats de moviment *Figura 2*
#### Figura 2
|Backgorund Substraction|
|-------------|
|![image](https://github.com/SergiTordera/PSIV---TRAKING/assets/61145059/0c582af3-47ab-4690-99bb-431024e1bdd1)|

### Detecció d'objectes
Una vegada tenim el moviment frame per frame apliquem un threshold on descartem tots els pixels amb valor inferior a 35 (els assigenm de color negre )  i fem una dilatació per fer els objectes detectats més estables i a partir d'aquest punt és quan obtenim les bounding box. Hem decidit realitzar una dilatació amb un kernel 7x3 (vertical) perquè les regions detectades del moviment dels automòbils moltes pegades queden partides per la meitat horitzontalment a causa de la trsanperenica del vidres frontals i darrers, d'aquesta forma amb el kernel 7x3 solucionem aquest problema com podem observar a la *Figura 3*.

#### Figura 3
|Threshold + dilatacio |
|-------------|
|![image](https://github.com/SergiTordera/PSIV---TRAKING/assets/61145059/effff532-7d3e-4e97-83b1-4cdbfed027f0)|
### Tracker

Ara ja podriem detectar les bounding box de les figures per les seves mides excloent per exemple vianants o ombres.Pero a nosaltres apart de ser capaços de detctar els objectes ens interesa poder mantenir un "traking" del ojecte durant el seu transcurs en el video. Per fer-ho i tenir un control de la identitat dels automòbils que van apareixent hem utilitzat la classe *CentroidTraker* la cual implementa un traker per objectes.

El seu funcionament es senzill, al detectar un ojecte actualitzem el posicionament de la seva bounding box i ens quedem amb el seu centroid. Si no tenim objectes detectats l'afegim i si en tenim ja de dectatas intentem associarlo a algun dels existents a traves de la distancia euclidiana mes petita. Despres de fer totes les comprobacions necessaries, registrarem l'objecte com a nou si no esta associoat a cap existent, o li actualitzarem els seus centroids.

La classe *CentroidTraker* també incorpora un sistema per detctar objectes que desapareixen i el desregistra si no els detecta en X frames. D'aquesta forma no ens interfereixen els cotxes que ja han passat i no estan mes en el video.

Finalment en la *Figura 4* podem observar un automobil detectat i amb una id assignada el qual mantindra durant tota la seva presencia en el video.
#### Figura 3
|Traking 1| Traking ...| Traking X|
|-------------|-------------|-------------|
|![image](https://github.com/SergiTordera/PSIV---TRAKING/assets/61145059/d25e34bf-4caf-4d77-826c-8c818829c7f8)|![image](https://github.com/SergiTordera/PSIV---TRAKING/assets/61145059/cdd714fc-310a-4702-8390-79c83b4c2c8d)|![image](https://github.com/SergiTordera/PSIV---TRAKING/assets/61145059/3e329801-fd8a-43c3-a855-4072e476f9e3)|

### Contador direccional

La classe *Centroid Traker* ens anira retornant el centroid dels objectes detectats juntament amb la seva id associada. Per tant tenint el moviment per cada automòbil si volem seva la seva direccio ja sigui de pujada o de baixada simplement observem la posició en la qual apareix aquest objecte, si apareix en una posició superior del vídeo i acaba a una posició inferior sabem que l'automòbil baixa, i en cas contrari l'automobil puja. D'aquesta forma, independentment de quin carril arriba o acaba podem saber la seva direcció. Igualment, els moviments que realitza l'automòbil són indiferents, ja que només ens interessen les posicions inicials i finals.

### Aventatges i Limitacions referents a la implementació

Utilitzar utilitzar un metode de detcció classic com es el nostre cas, es molt beneficios per poder mantenir una velocitat de processament i detecció en temps real,per altre banda es mes sensible a canvis de iluminació i possibles sorolls, per tant es un sistema amb bons resultats pero pot fallar en precisió. Per altre banda podriem fer utilització d'algoritmes com per exemple YOLO, aquest son molt mes precisos pero amb una velocitat de processament mes lenta, la qual ens costaria poder processar en temps real.

Es per aixó que en hem decantat per la primera opció en aquest projecte, el processat en temps real era molt important per nosaltres per poder mantenir un bon fluxe de conteig. Com que el perill sorgia de tenir una precisió baixa, hem dedicat mes esforços en fer un tracament correcte de les imatges del video rebuda, intentant eliminar sorolls i unificant bounding boxes per tenir la maxima precisió de detecció possible.

## Resultats

| Video | Real Up | Real Down | Dilate Up | Dilate Down | Close Up | Close down |
|--------|-------| -----------| ---------- | ----------| ----------| -----------|
| output7-short | 2 | 6| 2| 6| 2| 7|
| output2-middle | 7 | 5| 8| 5| 9| 5|
| output3-shadow | 10 | 3| 10| 3| 10| 3|
| output5-long1 | 24 | 8| 30| 14| 34| 18|
| output6-long2 | 133 | 6| 129| 11| 154| 24|




## Contributors
* Sergi Tordera - 1608676@uab.cat
* Eric Alcaraz - 1603504@uab.cat                
* Raul Dalgamoni - 1599225@uab.cat
