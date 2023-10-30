# PSIV - TRAKING

proves de moment (eliminar)

output7(short):   resultat profe: (baixades 2/ pujades 6)  -- resultat nostre (baixades 2/ pujades 7) 

output2 (middle):   resultat profe: (baixades 7/ pujades 5)  -- resultat nostre (baixades / pujades ) 

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
|Figura 1|
|-------------|
| Video Rebut | Part interesada |
| -------------| ------------- | 
|![image](https://github.com/SergiTordera/PSIV---TRAKING/assets/61145059/155f3139-2361-498e-a1b3-44270e9edc3e)|![image](https://github.com/SergiTordera/PSIV---TRAKING/assets/61145059/1b3889d9-2b18-469d-8d31-f3c72cb809a2)|

### Background Substraction
Per poder detctar el moviment dels cotxes en el vídeo, hem implementat un *background substraction*, per evitar que aquest *background substraction* crei soroll  l'obtenim a partir d'una mitjana dels X frames anteriors en el moment actual del video. Per tant al calcular la diferencia absoluta obtenim els seguents resultats de moviment *Figura 2*


### Detecció d'objectes
Hem implementat un *background substraction* per detectar moviment al vídeo, aquest *background* l'obtenim a partir d'una mitjana dels X frames anteriors. Una vegada tenim el moviment frame per frame fem una dilatació per fer els objectes detectats més estables i a partir d'aquest punt és quan obtenim les bounding box. Hem decidit realitzar una dilatació amb un kernel 7x3 perquè les regions detectades del moviment dels automòbils moltes pegades queden partides per la meitat horitzontalment, d'aquesta forma amb el kernel 7x3 solucionem aquest problema.
### Tracker

### Contador direccional
Fem un filtratge de les bounding box per les seves mides excloent com per exemple vianants o ombres. Finalment per tenir un control de la identitat dels automòbils que van apareixent hem utilitzat el *CentroidTraker*.

Tenint el moviment per cada automòbil donada pel *CentroidTraker* simplement observem la posició en la qual apareix aquest objecte, si apareix en una posició superior del vídeo i acaba a una posició inferior sabem que l'automòbil baixa, i és una pujada en el cas contrari. D'aquesta forma, independentment de quin carril arriba o acaba podem saber la seva direcció. Igualment, els moviments que realitza l'automòbil són indiferents, ja que només ens interessen les posicions inicials i finals.
### Aventatges / Limitacions



| Step 1 | Step 2 | ... | Step X|
| -------------| ------------- | -------------|------------- |
|![image](https://github.com/DCC-UAB/xnap-project-ed_group_16/assets/61145059/bcf4c783-b62f-4cb4-9f6c-b8c16ce0bf81) |![image](https://github.com/DCC-UAB/xnap-project-ed_group_16/assets/61145059/1b424e79-c026-4b76-8189-d6a398316532)|![image](https://github.com/DCC-UAB/xnap-project-ed_group_16/assets/61145059/625a0e57-86bf-45b6-b471-7d6fffea7610)| ![image](https://github.com/DCC-UAB/xnap-project-ed_group_16/assets/61145059/89f3ab0f-c652-4472-b6af-79d388eb5a61)|


## Contributors
* Sergi Tordera - 1608676@uab.cat
* Eric Alcaraz - 1603504@uab.cat                
* Raul Dalgamoni - 1599225@uab.cat
