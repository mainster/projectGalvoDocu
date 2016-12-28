Title:  Projekt Galvo-Scanner  
Author: Del Basso, Manuel  
Date:   WHZ, November, 2016  

Projekt __Galvo-Scanner__
=========================== 
[TOC]

<!-- - Einleitung
- Vorarbeit
    - Ursprüngliche Motivation
    - Fertigungsproblematik
    - Industriell gefertigte Aktoren
- Projektziel

- Terminologie
    - Galvanometer*
    - System
    - Modell
        - Beispiel
    - Modellbildung

- Formelzeichen und Einheiten
    - Zeitabhängige Größen
    - Konstanten

- Modellbildungsprozess
    - Generisches Modell
        - Mathematische Zusammenhänge
            - Translation und Rotation
            - Energiebilanz in allgemeiner Form
            - Impulsbilanzgleichung

    - Aktoren
        - Klassifizierung
        - Herstellerspezifikation
        - Elektrisches Teilsystemen
            - Back-EMF
            - Elektrisch generiertes Drehmoment
        - Mechanik
            - Lastmoment
            - Mechanisches Teilsystem
            - Positionssensor
        - Problematik der Sättigung
            - Testsignale, keine Sprungantwort etc.

    - Stellglied / Leistungsteil

    - Signalkonditionierung

- Angaben zur Systemdynamik
    - Spezifikationen des Gesamtsystems

- Gesamtsystem
    + Warum ARM?
- Software
    + DOXYGEN!!!
    + CMSIS

- Regelungstechnik
    + Diskretisierungsverfahren

- Geschlossene Simulationsumgebung
    + "frequency response model estimation"
    + copy ltspice conform laplace function of the estimated system 
    + Aktoren -> Simulink Modelle 
    + Endstufe -> LTspice -> MATLAB
    + Levelshifter -> LTspice -> MATLAB
    + Antialias / Rekonstruktionsfilter -> MATLAB
    +  
- Simulationen und Verifizierung
    + Step-by-Step
    + Spice: Geht die Simulation nicht ...
        + ... geht auch der Testaufbau nicht!
    + Regelalgorithmen testen:
        * RC-Glied direkt an gepufferten DAC
        * Testsignale im uC erzeugen
        * Oszibilder mit MATLAB-Simulation vergl.
- Modellparameter testen
- Hardware

- Resumee
- Quellenangaben
 -->

# Navigation #

| Tastenkombination |                              Funktion                             |
|-------------------|:-----------------------------------------------------------------:|
| __Alt+Links__     | Rücksprung zur Ausgangsposition nach Aktivierung eines Hyperlinks <br><span style="background-color: yellow"> Testen ob auch in Windows 7/10: IExplorer, firefox, Chrome </span> |

# Einleitung #
Im Rahmen der hier vorgestellten Projektarbeit wurde über einen Zeitraum von ca. 12 Monaten ein System entworfen und aufgebaut, bei dem der Projekt-Schwerpunkt ___bewusst___ nicht auf ein einzelnes Teilgebiet des Studiengangs "Nachrichtentechnik – Informationstechnik" beschränkt werden sollte. Die praxisbezogenen Kursinhalte und Laborveranstaltungen des Grundstudiums, vertiefen die erlernten theoretischen Grundlagen und zeigen teilweise auch Methoden zur (Computer-)Modellbildung und/oder Simulation im jeweiligen Teilgebiet auf. 

* Analog-/Digitaltechnik 
* Felder-Theorie (magnetische / elektrische)    
* Wechselstromlehre
* Mikrocontroller-Technik
* Hardwarebeschreibung (VHDL)
* Simulation von elektrischen Netzwerken (SPICE)
* abstrakten Systembeschreibung (Laplace, Fourier)
* Regelungstechnik
* Diskretisierung von Systemen

Einige konkreFür die Umsetzung eines  ___Systemplanung___ wie auch für die spätere Umsetzung als grundlegend und unerlässlich angesehen wird. Einige öffentliche Vorträge zum Thema "System Konzeption und Beschreibung in der Praxis" wurden am Karlsruher Institut für Technologie (KIT, Universität Karlsruhe) besucht. Dadurch konnten ergänzende Inhalte zum HsKA-Modul "Embedded Systems" erarbeitet und teils auch bei der konkreten Teilsystem-Auslegung umgesetzt werden. 

# Vorarbeit #
Es folgen einige Worte zur Frage "Wie kam es zu dem Projekt?" und "Was wurde letztendlich Umgesetzt?". Das ursprüngliche Projektvorhaben wurde nur teilweise umgesetzt, soll aber hier der Vollständigkeit halber erwähnt werden. 

## Ursprüngliche Motivation ##
Der Besuch einer mehrtägigen Schulungsveranstaltung der Firma _ANSYS_[^fnWikiAnsys] mit Schwerpunkt _ANSYS_ _Maxwell_[^fnMaxwell] sowie _ANSYS_ _Simplorer_[^fnSimplorer] im Rahmen meiner Formula Student Mitgliedschaft, weckte das Interesse an einem Projekt im Bereich "Multiphysik und Systemsimulation". Der nachfolgende Abschnitt "Projektziel" wurde der ursprünglichen Projektanfrage entnommen. Weitere Details sowie erste Simulationsergebnisse (Maxwell FEM-Modell + Simplorer Regelkreis), können in der ursprünglichen Projektanfrage[^fnAnfrageBrunner] eingesehen werden. 

><a name="refProjectDesc"/> Ziel des Projektes ist </a> der Aufbau eines funktionsfähigen XY-Galvanometer-Scanners mit selbstentworfenen Galvanometer-Motoren + Leistungstreiber und eines in C implementierten Software-Reglers (...). Als Galvanometer-Motor-Typ ist ein "Moving magnet motor" geplant. Um die Motorkonstruktion einfach zu halten, ist ein Stator Design mit nur einem Polpaar angedacht.
<a name="refExplainFEMSol"/> </a>
>Unter Zuhilfenahme der FEM-Simulationsumgebung "Maxwell" und "Simplorer", sollen Reglerparameter anhand eines nichtlinearen Modells des Galvanometer-Motors optimiert werden. Die Sollwert-Vorgaben für die XY-Winkelpositionen werden vorerst als einfache Lookup-Tabellen direkt auf dem Mikrocontroller erzeugt, welcher auch die diskreten Reglerfunktionen übernehmen soll. 

>Sollte das geplante System soweit funktionieren, dass mit dem Scanner einfache geometrische Figuren erzeugt werden können (Kreise, Quadrate, Achter, ...), könnte eine PC-Software zur Erzeugung von Pixelkoordinaten inkl. Dunkeltastung des Lasers als Erweiterung angedacht werden.
    
![GalvosXY](./pics/galvanometerMaxwell.png "Anordnung der Aktoren in XY-Scanner Konfiguration")

Statische sowie dynamische Eigenschaften der in ANSYS Maxwell konstruierten Aktoren werden auf Basis finiter Elemente modelliert und in einem Multi-Domain-Modell[^fnMultiDomain] abgebildet. 
    
## Fertigungsproblematik ##
Die Motorkonstruktion konnte nie vollständig an einem funktionsfähigen Prototypen getestet werden. Hierzu werden folgende Begründungen genannt:

1. Unzureichende dynamische Eigenschaften (Rotormasse, Stabmagnet)
2. Kostenintensive / nicht vor Ort durchführbare mechanische Fertigungsschritte
3. Bearbeitung des Neodym Materials (Rotormagnet) nicht umsetzbar 
4. Bearbeitung des aus Ferrit Pulver gepressten Statorkerns schwer umsetzbar 
5. Verfügbarkeit ungenutzter, professioneller Galvanometer-Motoren

Das "unzureichend" bezieht sich auf das in Abschnitt Error: Reference source not found (Zitat, letzter Abschnitt) formulierte Projektziel. Um die dynamischen Eigenschaften zu verbessern, wäre die mechanische Bearbeitung von Zukaufteilen notwendig gewesen. Nach einigen gemeinsamen Recherchen mit den Werkzeug-Spezialisten des ansässigen Instituts für Materialien und Prozesse (IMP), wurde von einer maschinellen Bearbeitung abgeraten.[^fnArnoldMagn]

## Industriell gefertigte Aktoren ##
Für die weitere Umsetzung des Projekts kamen gebrauchte Spiegel-Galvanometer der Firma "Cambridge Technology Inc." zum Einsatz. Da keine herstellerspezifischen Informationen über den mechanischen Aufbau der Cambridge Galvanometer zur Verfügung standen, konnte die in Abschnitt [Ursprünglich Motivation](#ursprungliche-motivation) sowie die in [brun1] beschriebene Multi-Domain-Softwarelösung im weiteren Projektverlauf nicht mehr eingesetzt werden.  
Eine zerstörungsfreie Demontage der vorhanden Aktoren konnte nicht gewährleistet werden. Außerdem ließe der innere mechanische Aufbau keine Rückschlüsse auf die wichtigen Materialeigenschaften des Rotors bzw. Statorkerns zu.   

Durch eine sorgfältige Strukturierung des Projektablaufs hätte u. U. Zeit gespart werden können. Die erarbeiteten Kenntnisse im Bereich "Multiphysik und Systemsimulation" sind keines falls umsonst gewesen. Hinsichtlich der produktiven Bearbeitung von Projekten, lässt der bisherige Ablauf jedoch viel Kritik zu. Fertigungsprozesse unterliegen grundsätzlich irgend welchen Einschränkungen. Bereits während der Recherche zum Thema Permanentmagnet, wäre eine Anfrage über die Bearbeitbarkeit notwendig gewesen!

# Projektziel #
Als übergeordnetes Projektziel soll ein optisches Ablenksystem (2-Achsen → XY-Koordinaten) für eine Laserquelle (Laserpointer, sichtbares Spektrum) auf Basis industriell gefertigter Spiegelgalvanometer geplant, simuliert, entworfen, aufgebaut und verifiziert werden. Die Aktoren (Spiegelgalvanometer der Firma Cambridge) sind als gegeben zu betrachten (Zukaufteil). <img src="./pics/galvoMirrorsXY_2.svg" title="Funktionsprinzip XY-Scanner" align="top" height="190px" style="float:right; margin: 1em 0em 0em 1em;"/>Die Positionierung des Laserpunktes soll hinreichend "schnell" und "präzise" sein so dass zumindest einfache geometrische Figuren auf einen hellen Hintergrund projiziert werden können. Die Regelung der Aktoren soll diskret realisiert und auf einem Mikrocontroller STM32F429i implementiert werden. Die Pixel-Koordinaten (Sollwerte) werden im Speicher des STM32 abgelegt und sollen über eine PC-Schnittstelle aktualisiert werden können. 

Zu Begin des Kapitels [Modellbildungsprozess](#modellbildungsprozess) folgt eine erste Aufteilung des Projekts "XY-Galvanometer-Scanner":

# Terminologie #
Auf häufig wiederkehrende Begriffe wie z. B. Modell, Modellbildung oder System, soll hier kurz eingegangen werden da sie als Überbegriffe sehr universell definiert sein können. 

## Galvanometer* ##
>Ein Galvanometer-Scanner ist ein hochdynamisches elektro-optisches Bauteil, bei dem <a style="color: #ddd ">ein</a> drehbare Spiegel von geringer Trägheit verwendet werden, um einen Laserstrahl mit hoher Genauigkeit und Wiederholbarkeit zu positionieren. Der Name Galvanometer bezieht sich auf den Motor-Typ.[^fnGalvoScanlab]

## System ##
Es gibt sehr abstrakte Definitionen des System-Begriffs. Auch in der soziologischen Systemtheorie werden System-Begriffe formuliert so dass z.B. durch menschliche Handlungen ein abstraktes Modell eines sozialen Systems angeregt bzw. dessen Systemantwort beschrieben werden kann. Eine sehr universelle Definition lautet z. B.:

> "__System:__ a set of physical entities that interact and are observable, where the entities can be a specified quantity of matter or a volume in space." [^fnChRoy]
><p style="color: #707070 "> Eine Menge von physikalischen Einheiten die interagieren und beobachtbar sind, wobei sie eine definierte Menge Materie (bzw. eine bestimmte Anzahl an Teilchen) oder ein physischer Körper im Raum sein können. </p>

Im folgenden "beschränken" wir uns auf den System-Begriff im Sinne der Systemtheorie als elementare Disziplin der Ingenieurswissenschaften. Systeme und Signale sind die beiden wichtigsten Konzepte der Systemtheorie. In der Praxis werden Gebilde oder Konstrukte als System bezeichnet, die bei Anregung mit einem Eingangssignal *x(t)* mit einem Ausgangssignal *y(t)* reagieren.[^fnRUnb] 

Ein Gesamtsystem fügt sich aus Teilsystemen zusammen. Je nach Komplexität der übergeordneten Aufgabe (Wie "dick" sind Pflichten- und Lasten- Heft?) entstehen zahlreiche Abstraktionsebenen die es zu *dokumentieren* und meist auch zu warten gilt. 

Hinsichtlich eines _Software-Systems_ wird der Begriff _System_ in der [IEEE 1471][ieee1471] wie folgt definiert:
>Ein System ist ein aus Teilen zusammengesetztes und strukturiertes Ganzes. Es hat eine Funktion, erfüllt einen Zweck und verfügt über eine Architektur. [[MDA:2006, p.57]][@MDA:2006]

<!-- Der Begriff System ist hier und im Folgenden als Abkürzung für Teilsystem zu verstehen. -->

## Modell ##
Um ein Modell beschreiben zu können, muss zuvor das System *gewählt* werden, dessen tatsächliche Eigenschaften über den *__Prozess__ der Modellbildung* abstrahiert werden soll. Auch für den Begriff *Modell* finden sich zahlreiche Definitionen in der Literatur. Einige eignen sich sehr gut zur Definition im Sinne technischer Zusammenhänge und Computersimulationen Einige werden im folgenden zitiert: 
Die Grundlagen der Modellierung schuf Herbert Stachowiak 1973 mit der Veröffentlichung der "Allgemeinen Modelltheorie". Demnach ist ein Modell durch __Abbildung__, __Verkürzung__ und __Pragmatismus__ gekennzeichnet.[^fnStachowiak]

>__*Abbildung*__
Ein Modell ist stets ein Modell von etwas – nämlich Abbildung oder Repräsentation eines natürlichen oder eines künstlichen Originals, wobei dieses Original selbst auch wiederum ein Modell sein kann.

>__*Verkürzung*__
Ein Modell erfasst im Allgemeinen nicht alle Attribute des Originals, sondern nur diejenigen, die dem Modellschaffer bzw. Modellnutzer relevant erscheinen.

>__*Pragmatismus*__
Modelle sind ihren Originalen nicht eindeutig zugeordnet. Sie erfüllen ihre Ersetzungsfunktion für

> 1.   bestimmte Subjekte (für wen?)
> 2.   innerhalb bestimmter Zeitintervalle (wann?)
> 3.   unter Einschränkung auf bestimmte gedankliche oder tätliche Operationen (wozu?).

Eine kompaktere Definition wurde einem Lehrbuch _"Grund- und Leistungskurs Informatik"_ von _Karl-Hermann Rollke_ und _Klaus Sennholz_ entnommen: 

>Ein *Modell* ist ein durch Abstraktion (__Reduzierung__ und Verallgemeinerung) gewonnenes __Abbild__ eines bestimmten Ausschnitts der Realität. Das Modell wird zu dem Zweck entworfen, den für die Lösung eines *bestimmten* Problems relevanten Teil der Wirklichkeit für den Menschen oder eine Maschine (Computer) überschaubar und *operationalisierbar* zu machen.[^fnRoSe]

<a style="background-color: yellow;"> ...ist es wichtig, den Systemgrad minimal zu halten.
Die folgende Beispielaufgabe soll diesen Zusammenhang etwas greifbarer darstellen: </a>

### Beispiel ###
Für eine analoge Filterschaltung wird ein mathematisches Modell gefordert. Die Schaltung soll zur Tiefpassfilterung in einer __Highend-HiFi__ Stereoanlage eingesetzt werden. Für den Übergang vom Durchlass- in den Sperrbereich ist eine Dämpfung von 20dB/Dekade vorgegeben. Anhand des Modells soll das Dämpfungsverhalten mittels einiger harmonischer Testsignale untersucht werden können. 

__Möglichkeit 1__
<img src="./pics/elko_ersatz_hf_reload.svg" title="Realitätsgetreues Ersatzschaltbild eines RC-Tiefpassfilters" align="top" height="190px" style="float:right; margin: .4em 0em 0em 1em;"/>Man leitet aus den Anforderungen ab, dass ein Standard Filter mit Tiefpasscharakter 1. Ordnung gefordert ist. Da es sich beim Endprodukt um eine Highend-Anlage handelt, sollte ein möglichst präzises Modell formuliert werden. Unter Berücksichtigung aller tatsächlich parasitärer Größen von passiven Bauelementen[^fnElektrBauelem] wie Serieninduktivität (ESL) und Serienwiderstände (ESR) der Anschlussdrähte/Anordnung der Elektroden, der Isolationswiderstände und der dielektrischen Absorption (Nachladeeffekt, Rda, Cda), ergibt sich für einen einfachen RC-Tiefpass mit einer Dämpfungsflanke von 20dB/Dekade, das nebenstehende Schaltbild. Da die Ordnung eines Systems direkt aus der Anzahl seiner unabhängigen Energiespeicher abgeleitet werden kann, muss dem geforderten mathematischen Modell eine __Differentialgleichung 5. Ordnung__!!! zugrunde gelegt werden. 

__Möglichkeit 2__
... dgl der Ordnung 1....

Ein formuliertes Modell unterliegt also der Anforderung, möglichst alle __*relevanten*__ Charakteristika eines Systems abzubilden wobei der _Systemgrad_ minimal gehalten werden soll. So gelingt es, komplexe Zusammenhänge aufzuspalten und eine Problemstellung zu partitionieren.

## Modellbildung ##
<a style="background-color: yellow;"> Top-Down- und Bottom-Up-Design
In der Informatik bezeichnet man einen Entwicklungsprozess für Software als Top-down, wenn der Entwurf mit abstrahierten Objekten beginnt, die dann konkretisiert werden; der Prozess ist Bottom-up, wenn von einzelnen Detail-Aufgaben ausgegangen wird, die zur Erledigung übergeordneter Prozesse benötigt werden. Zudem wird im Zusammenhang mit Compilerbau von Top-down- und Bottom-up-Parsern gesprochen (genauere Informationen unter Top-Down- und Bottom-Up-Design). </a>

Modellbildung
Klassifikation von Modellen hinsichtlich ihrer Repräsentation:
...
Modell
mentales Modell physikal. Modell
analoges Modell
Darstellungsmodell
symbol. Modell
mathemat. Modell
grafisches Modell
verbales Modell
...


Unter Modellbildung (Modellierung) versteht man den Prozess, von einem System
ein Modell zu erstellen. Hierzu gehören folgende Schritte:
1. Identifizierung der Systemgrenzen     Black-Box-Modell
2. Identifizierung der Untersysteme und ihrer Beziehungen     Strukturmodell
3. Definition von Relationen zwischen Variablen     Verhaltensmodell
MK:III-21 Modeling Concepts © STEIN 2000-2015
Modellbildung
Ablauf der Top-Down-Modellbildung: Abstrakte Modelle werden auf weniger
abstrakte Modelle abgebildet.
mentales Modell
Strukturmodell
algorithm. Modell
Computermodell
Verhaltensmodell
System + Frage
Interpretation des
konkreteren Modells
Basis des abstrakteren.
hohe Abstraktion
niedrige Abstra

---

Prozesse der Modellbildung: wiki
Ablauf einer Modellbildung
Bei der Modellbildung lassen sich folgende Prozesse differenzieren:

Abgrenzung: Nichtberücksichtigung irrelevanter Objekte
Reduktion: Weglassen von Objektdetails
Dekomposition: Zerlegung, Auflösung in einzelne Segmente
Aggregation: Vereinigung, Zusammenfassen von Segmenten zu einem Ganzen
Abstraktion: Begriffs- bzw. Klassenbildung

---

Die enormen Anforderungen, die aus Anwendersicht an Hard- und Softwarekomponenten gestellt werden, in Verbindung mit dem Aspekt der Wirtschaftlichkeit, machen sich bereits in der Projektierungsphase eines Auftrags bemerkbar. *"Reusability"* ist ein Begriff aus der Softwarearchitektur und charakterisiert Software (Quellcode, Dokumentation, Testumgebungen, ...) bezüglich ihrer *Wiederverwertbarkeit* in Folgeprojekten oder Folgeschritten des selben Projektes.[^fnReuseCode] Um einen Schritt weiter in Richtung _modellgetriebene Architektur_ (_engl. Model Driven Architecture_, __*MDA*__) zu gehen, soll an dieser Stelle ein Unterpunkt aus [[MDA:2006, p.17]][@MDA:2006], Kapitel _"Akute Probleme bei der Software-Erstellung"_, zitiert werden:

>__Äußere und innere Gleichförmigkeit von Projekten__ 
Zwar impliziert ein Projekt immer einen neuartigen und einmaligen Charakter, oftmals werden aber mehrere Projekte in der gleichen Fach- und/oder Technikdomäne durchgeführt. Genau so oft ähneln oder gleichen sich daher die (architekturellen) Konzepte der realisierten Anwendungen. Diese Gleichförmigkeit wird häufig übersehen oder schlicht ignoriert und anstatt diese domänen-spezifischen Konzepte wiederverwendbar zu machen, wird die gleiche Arbeit unnötigerweise mehrfach verrichtet.

Natürlich ist der Begriff der *Wiederverwertbarkeit* nicht nur auf Komponenten einer Softwarearchitektur beschränkt. Auch im Hardwarebereich kann ein Unternehmen durch frühzeitig eingeleitete Abstraktionsprozesse, u. U. eine _Gleichförmigkeit_ zu geplanten Folgeprojekten erkennen und das Teilsystem _"von Heute"_ bereits zugunsten eines Teilsystems _"von Morgen"_ optimieren.

# Formelzeichen und Einheiten #

## Zeitabhängige Größen ##

| Bezeichnung           | Symbol               | Einheit            | <span style="color: #bbb">engl. Bezeichnung</span>               |
| --------------------- | :------------------: | :----------------: | ---------------------------------------------------------------- |
| Spulenstrom           | $i_L$                | $\si A$            | <span style="color: #bbb"> Coil current              </span>     |
| Elek. Drehmoment      | $M_\{EL\}$           | $\si\{N.m\}$       | <span style="color: #bbb"> Electrical torque         </span>     |
| Reibungsmoment        | $M_\{FR\}$           | $\si\{N.m\}$       | <span style="color: #bbb"> Rotor dynamic friction torque </span> |
| Torsionsfedermoment   | $M_\{TB\}$           | $\si\{N.m\}$       | <span style="color: #bbb"> Torsion bar torque        </span>     |
| Drehimpuls            | $L_\omega$           | $\si\{N.m.s\}$     | <span style="color: #bbb"> Angular momentum          </span>     |
| Winkelposition        | $\varphi_\{rad\}$    | $\si\{rad\}$       | <span style="color: #bbb"> Angular position          </span>     |
|                       | $\varphi_\{deg\}$    | $\si\{°\}$         | <span style="color: #bbb">                           </span>     |
| Winkelgeschwindigkeit | $\omega$             | $\Si\{rad\per s\}$ | <span style="color: #bbb"> Angular velocity          </span>     |
| Stromregler Eingang   | $U_\{ccI\}$          | $\si V$            | <span style="color: #bbb"> Current controller input  </span>     |
| Stromregler Ausgang   | $U_\{ccO\}$          | $\si V$            | <span style="color: #bbb"> Current controller output </span>     |
| Spannung Messshunt    | $U_\{sh\}$           | $\si V$            | <span style="color: #bbb"> Shunt voltage             </span>     |

## Konstanten ##

| Bezeichnung              | Symbol                | Einheit                | <span style="color: #bbb">engl. Bezeichnung</span>          |
| ------------------------ | :-------------------: | :--------------------: | ----------------------------------------------------------- |
| Wicklungsinduktivität    | $L$                   | $\si H$                | <span style="color: #bbb">Coil inductance</span>            |
| Wicklungswiderstand      | $R_L$                 | $\si\{\Omega\}$        | <span style="color: #bbb">Coil resistance</span>            |
| Messwiderstand           | $R_\{SH\}$            | $\si\{\Omega\}$        | <span style="color: #bbb">Current shunt resistance</span>   |
| Massenträgheit d. Rotors | $J_R$                 | $\si\{kg.m^2\}$        | <span style="color: #bbb">Rotor inertia</span>              |
| EMF-Konstante            | $K_\{EMF\}$           | $\Si\{V.s\per rad\}$   | <span style="color: #bbb">Back EMF const.</span>            |
| Torsionsfederkonstante   | $K_\{TB\}$            | $\Si\{N.m\per rad\}$   | <span style="color: #bbb">Torsion bar torque const.</span>  |
| Reibungskonstante        | $K_\{FR\}$            | $\Si\{N.m.s\per rad\}$ | <span style="color: #bbb">Friction torque const.</span>     |
| El. Drehmomentkonstante  | $K_\{EL\}$            | $\Si\{N.m\per A\}$     | <span style="color: #bbb">El. magnetic torque const.</span> |

# Modellbildungsprozess #
>"It's a bunch of shapes connected by lines." Dilbert 
[[MDA:2006, p.73]][@MDA:2006]

Dieser Aussage entsprechend soll hier aus dem formellen Anforderungskatalog (vergl. Pflichtenheft) ein erstes abstraktes Modell abgeleitet werden. 

* Aktoren 
* Sensoren
* Leistungselektronik
* Steuer- und Reglerelektronik
    * Mikrocontrollerplatine 
    * Signalkonditionierung
        - Pegelwandlung 
        - Anti-Aliasing (ADC)
        - Rekonstruktionsfilter (DAC)
* Software 
    * Implementierung der Regelalgorithmen

![abstractSystemC](./pics/abstractSystemC.svg "Erste Unterteilung") 

## Generisches Modell ##
In der Informatik sind _generische Typen_ Datentypen mit der Möglichkeit zur Angabe von Typparametern. Man spricht auch von _parametrischer Polymorphie_.[^fnwikiGenericTypes] Überträgt man den Begriff _generisch_ auf die hier genutzte Modell-Art, so muss ein Modell entstehen dass in der Lage ist, eine ganze Menge von vergleichbaren Aktoren (Drehmoment-Motoren) zu beschreiben. Übergibt man dem generischen Typ _"Aktor"_ oder _"Galvanometer"_ die für das zu erzeugende Modell spezifischen Parameter wie Drehmomentkonstante, Wicklungsinduktivität oder das Massenträgheitsmoment der Rotorwelle, soll ein entsprechendes Modell erzeugt werden. Dieses Modell wird als _Subsystem_ __*Aktor*__ auf einer höheren Abstraktionsebene in ein weiteres Modell eingebunden und anschließend simuliert. 

Die Analogie zu _generic types_ in objektorientierten Programmiersprachen ist nur teilweise zulässig. Vergleicht man diese Methode jedoch mit der in [Vorarbeit](#vorarbeit) aufgezeigten, nämlich einem Computermodell, abhängig von Geometrie und Materialparametern, so finden sich doch einige Eigenschaften, die analog verwendet werden können.

### Mathematische Zusammenhänge ###
Die Grundlage eines generischen Modells ist seine Mathematik. Die Gesetze der Physik müssen bei der mathematischen Modellierung eingehalten werden. Der Verlauf der Geschwindigkeit $v(t)$ eines Körpers lässt sich z. B. durch Differentiation seiner Streckenfunktion $s(t)$ oder durch Integration seiner Beschleunigung $a(t)$ über der Zeit formulieren. Diese Gesetzmäßigkeiten gelten gleichermaßen für translatorische sowie rotatorische Bewegung. Daraus folgt, dass z. B. die Integralbildung der Winkelgeschwindigkeit $\omega(t)$ eines rotierenden Körpers unmittelbar auf seine Winkelposition $\varphi(t)$ führt. Diese grundlegenden Gesetze müssen später anhand des Modells verifiziert werden können. 

##### Translation und Rotation #####
Die _Grundgleichungen für Translation und Rotation_  sollen einerseits zur einheitlichen Notation im Rahmen dieser Arbeit beitragen, zum anderen dient die Tabelle (vergl. [[Iser:2008, 123]][@Iser:2008]) der Überprüfung von <span style="background-color: yellow; color: red">physikalischen Einheiten </span>.

| Translation                          | in eine Richtung         | Rotation                                  | um eine Achse             |
|:-------------------------------------|:------------------------:|:------------------------------------------|:-------------------------:|
| $s$                                  | Weg                      | $\varphi$                                 | Winkel                    |
| $v=\dot s$                           | Geschwindigkeit          | $\omega = \dot\varphi$                    | Winkelgeschwindigkeit     |
| $a=\dot v = \ddot s$                 | Beschleunigung           | $\dot\omega = \ddot\varphi$               | Winkelbeschleunigung      |
| $m$                                  | Masse                    | $J, \theta$                               | Trägheitsmoment           |
| $\vec F$                             | Kraft in Wegrichtung     | $\vec M$                                  | Moment um Drehachse       |
| $\vec I = m \cdot \vec v$            | Impuls                   | $\vec L = J \cdot \vec\omega$             | Drehimpuls                |
| $\vec F = m \cdot \vec a$            | Kraeftesatz              | $\vec M = J \cdot \dot\omega$             | Momentensatz              |
| $E_k = \frac 1 2\; m \cdot v^2$      | kinetische Energie       | $E_k = \frac 1 2\; J \cdot \omega^2$      | kinetische Energie        |
| $W = \int F ds$                      | Arbeit                   | $W = \int M d\varphi$                     | Arbeit                    |
| $P = F \cdot v$                      | Leistung                 | $P = M \cdot \omega$                      | Leistung                  |

Das aufstellen von *Bilanzgleichungen* ist ein essenzieller Bestandteil bei der Modellbildung von technischen System und Prozessen. Zum Beispiel gilt für jedes energetisch abgeschlossene System (Bsp.: idealer Feder-Masse-Schwingkreis, idealer LC-Schwingkreis) stehts, dass die Momentanenergie zu jedem Zeitpunkt $t \ge 0$ identisch mit der Energie zum Zeitpunkt $t=0$ übereinstimmt. 

#### Energiebilanz in allgemeiner Form ####
<img src="./pics/energiebilanzConst.svg" title="Energiebilanz eines beliebigen, abgeschlossenen Gebildes" align="left" height="154px" style="float:left; margin: .4em .8em 0em 0em;"/> Verläuft über die Grenzen eines geschlossenen Gebildes (System, Prozess, ...) kein Energiestrom, so unterliegt das Gebilde dem *Energieerhaltungssatz* wobei innerhalb der Grenenzen $N$ _verschiedene Energiearten_ $E_i$ vorhanden sein _können_ (siehe Abbildung links). Es ist z.B. unproblematisch, Analogie-Beziehungen zwischen translatorischer und rotatorischer Bewegung anhand des Energieerhaltungssatzes nachzuweisen. Die theoretische _Umformung der mechanischen Größen_ $m, \vec{v}, \vec{J}$ und $\vec{\omega}$ entspricht hier dem Gebilde im Sinne eines energetisch abgeschlossenen Prozesses.

$$ \frac{1}{2} \cdot m \cdot v^2 = E_{kin}
\;\;\;\widehat{=}\;\;\;
E_{rot} = \frac{1}{2} \cdot J_x \cdot \omega^2 $$

Aus dem Energieerhaltungssatz kann das *Kräftegleichgewicht* abgeleitet werden. Wegen den analogen Gesetzmäßigkeiten zwischen translatorischer und rotatorischer Bewegung, kann vom Kräftegleichgewicht eines bewegten Körpers auf ein Drehmomentgleichgewicht geschlossen werden.

#### Impulsbilanzgleichung ####
Wirkt auf einen Körper der Masse $m$ und dem Impuls $\vec I = m \cdot \vec v$ eine äußere Kraft $\vec F$, so gilt bei translatorischer Bewegung und $m=const$ entsprechend dem [Impulserhaltungssatz][@Impulserhaltung][^fnImpulserhaltung] folgende Bilanzgleichung: 

\begin{equation}
\frac{\partial}{\partial\,t}\,\vec I = m \cdot \frac{\partial}{\partial\,t}\,\vec v(t) = \vec F(t) \label{eqImpulsbil}\end{equation}

Die Beziehung in \eqref{eqImpulsbil} wird als Impulsbilanzgleichung bezeichnet. Analog wird die Impulsbilanz für rotiernde Körper mit der als skalar betrachteten Massenträgheit $J$ und bestehendem Drehimpuls $\vec L_s = J \cdot \vec \omega$ aufgestellt. Gleichung \eqref{eqDrehimpulsbil} wird folgerichtig als __Drehimpulsbilanzgleichung__ bezeichnet.

\begin{equation}{\frac{\partial}{\partial\,t}\,\vec L_s = J \cdot \frac{\partial}{\partial\,t}\,\vec \omega(t) = \vec M(t)} \label{eqDrehimpulsbil}\end{equation}

## Aktoren ##
Wie bereits in Abschnitt [Industriell gefertigte Aktoren](#industriell-gefertigte-aktoren) erwähnt, wurden Galvoscanner als Aktor-Baugruppen eingesetzt. Um die physikalischen Zusammenhänge eines Drehmoment-Motors nach dem Galvanometer-Prinzip in ein Computermodell überführen zu können, gibt es mehrere Ansätze. Die Möglichkeit, ein Multiphysik-Modell zu erstellen und einzusetzen, wurde im Abschnitt [Vorarbeit](#vorarbeit) angesprochen. Ein anderer, hier genutzter Ansatz, wird im Abschnitt [generisches Modell](#generisches-modell) beschrieben. 

### Klassifizierung ###
Galvanometer-Motoren lassen sich nicht so ohne weiteres in eine Unterklasse der Elektromotoren einordnen. Als Messinstrument in Drehspulmesswerken erzeugt das Galvanometer eine mechanische Drehbewegung proportional zum gemessenen Strom. DC-Motoren hingegen sind elektromechanische Baugruppen die eine elektrische Gleichleistung in eine mechanische Leistung umsetzen können. Im dynamischen Betrieb verhält sich ein Spiegelgalvanometer ähnlich einem DC-Motor. Das Momentanmoment, multipliziert mit der Drehzahl ergibt eine mechanische Leistung in $\si{N.m/s}$. Im Galvanometer Betrieb (Messinstrument) gleicht der Galvomotor einem elektrischen Drehmagneten welcher ein mechanisches Drehmoment erzeugt. 

Bei der Modellierung von DC-Motoren wird der Zusammenhang zwischen Motorstrom und Drehmoment oft soweit linearisiert, dass zur Beschreibung ein konstanter Faktor, die Drehmomentkonstante, ausreichend ist. Zulässig wird diese Annäherung, wenn man die magnetische Flussdichte des Erreger-Magnetfeldes als konstant betrachten kann ([siehe Abbildung][motorModeling]).<img src="./pics/motorBconst.png" title="DC-Motor mit konstantem Erregerfeld" align="top" height="250px" style="float:right; margin: 1em 0em 0em 1em;"/> Da das elektromechanische Wirkprinzip der hier verwendeten _"Moving Magnet Galvanometer"_ auf einem permanent erregten Magnetfeld basiert, ist die Annahme _B=const_ gerechtfertigt. Wenn die Intensität des Erregerfeldes für beide Betriebsarten (Motor, Drehmagnet) gleich und als konstant angenommen wird, entsteht durch die variable Position des Rotormagnetfelds gegenüber dem des Statorfeldes ein Fehler. Tabelle [_Mechanical Specifications_](#refTableMechanic) kann eine maximale Auslenkung der Rotorwelle von $\pm 20\si{°}$ entnommen werden. Das Momentanmoment ändert sich in diesem Bereich entsprechend dem Kosinus des Rotorwinkels was im schlimmsten Fall zu einem Fehlerfaktor von $cos(20° \pi/180°) \approx 0.94$ führt. Obwohl es sich bei Galvanometer-Motoren also nicht um DC-Motoren im klassischen Sinn handelt, kann eine Drehmomentkonstante zur approximation angegeben werden. Wie in Abschnitt [Industriell gefertigte Aktoren](#industriell-gefertigte-aktoren) erwähnt, muss das Modell anhand von Herstellerspezifikationen konkretisiert werden können. In Tabelle [_Mechanical Specifications_](#refTableMechanic "Goto Table Mechanical Specifications") ist die entsprechende Drehmomentkonstante unter _Torque Constant_ angegeben.

Der Vollständigkeit halber sollen an dieser Stelle einige Parallelen zur Unterklasse der _elektronisch kommutierten_ Elektromotoren gezogen werden. Das Rotormaterial der unter dem Begriff _"Brushless <a style="color: #aaa ">DC-</a>Motor"_ bekannten Antriebe besteht i.d.R. ebenfalls aus permanent magnetisierten Werkstoffen. Durch eine elektronische Ansteuerung wird über mehrere Statorwicklungen ein Drehfeld erzeugt.

### Herstellerspezifikation ###
Bei den hier eingesetzten, industriell gefertigten Motoren der Firma [_Cambridge Technology_][cambridgeTech] handelt es sich um optische Scannereinheiten (Serie 6860) vom Typ _"Moving Magnet"_ mit integriertem Positionssensor, welcher auf Basis variabler Kapazitäten arbeitet. Die vom Hersteller liebevoll unter [__Veteran Galvo Motors__][veteranGalvo] kategorisierten Aktoren gehören zwar nicht mehr zu den aktuellen Produkten von _Cambridge Technology_, sind jedoch hervorragend geeignet für das hier dokumentierte Projektvorhaben. 

Nachfolgend werden die [Herstellerspezifikationen][typ6860spec] der __6860__ Serie aufgelistet.<br>
<a name="refTableElectric"> </a>

| Electrical Specifications | Symbol         | Value                          |                                   |                      |
|---------------------------|----------------|--------------------------------|:---------------------------------:|:--------------------:|
| Coil Inductance           | $L$            | $\SI\{160\}\{\micro\henry\}$   |                                   | $\pm\SI\{10\}\{\%\}$ |
| Coil Resistance           | $R_L$          | $\SI\{1.5\}\{\ohm\}$           |                                   | $\pm\SI\{10\}\{\%\}$ |
| Back-EMF const.           | $K_\{EMF\}$    | $\SI\{0.17\}\{mV s /\degree\}$ | $\SI\{9.74\}\{mV s /\radian\}$    | $\pm\SI\{10\}\{\%\}$ |
| RMS Current               | $I_\{L-RMS\}$  | $\SI\{4.6\}\{A\}$              | at $\ T_\{case\}=\SI\{50\}\{°C\}$ | Max.                 |
| Peak Current              | $I_\{L-PEAK\}$ | $\SI\{25\}\{A\}$               |                                   | Max.                 |
| Step Response Time        | Small Angle    | $\SI\{0.5\}\{ms\}$             | inertia matched load              |                      |

<a name="refTableMechanic"> </a>

| Mechanical Specifications           | Symbol                  | Value                        |                           |                      |
| ---                                 | ---                     | ---                          | ---                       | ...                  |
| Angular Excursion                   | $\Delta\varphi_\{Max\}$ | \SI\{40\}\{\degree\}         | \SI\{0.698\}\{\radian/s\} |                      |
| Rotor Inertia                       | $J_R$                   | \SI\{0.6\}\{gm.cm^2\}        | \SI\{6e-8\}\{kg.m^2\}     | $\pm\SI\{10\}\{\%\}$ |
| Torque Constant                     | $K_\{EL\}$              | \SI\{9.3*10^4\}\{dyne.cm/A\} | \SI\{9.3e-3\}\{N.m/A\}    | $\pm\SI\{10\}\{\%\}$ |
| Maximum Coil Temperature            |                         | \SI\{110\}\{°C\}             |                           |                      |
| Thermal Resistance<br>(Coil - Case) |                         | \SI\{1.5\}\{°C/\watt\}, Max  |                           |                      |

<a name="refTablePositionDetect"> </a>

| Position Detector                | Value                                   |      |
| ---                              | ---                                     |      |
| Linearity                        | 99.9%, Minimum, over 40 degrees         |      |
| Scale Drift                      | 50PPM/°C, Maximum                       |      |
| Zero Drift                       | 15 microradians/°C, Maximum             |      |
| Repeatability, Short Term        | 8 microradians                          |      |
| Output Signal, Common Mode       | 585µA @ AGC voltage=10VDC               | $\pm\SI\{20\}\{\%\}$ |
| Output Signal, Differential Mode | 14.5µA/° @ common mode current of 585µA | $\pm\SI\{20\}\{\%\}$ |

<span style="font-size: 80%">$\;\;\;1\;dyne.cm \;\;\;\Leftrightarrow\;\;\; 1\times 10^{-7} Nm$
$\;\;\;1\;gm.cm^2 \;\;\;\Leftrightarrow\;\;\; 1\times 10^{-7} kg.m^2$</span>
<br>

### Elektrisches Teilsystemen ###
Das fertige Modell des Galvomotors setzt sich aus elektrischen und mechanischen Teilsystemen zusammen. Als Stellgröße der Regelstrecke bzw. der Aktoren wurde beim ersten Modellierungsversuch die __Eingangsspannung__ der Statorinduktivität verwendet. In differentieller Form ist die Zweipolbeziehung einer idealen Induktivität gegeben durch:
$$ u(t)=L \cdot \frac{\partial~i_L}{\partial~t} $$
Bezeichnet $u_M(t)$ die Eingangsspannung der Statorwicklung und $R_L$ den reellen Wicklungswiderstand, so gilt für eine reale Motorinduktivität 
$$ u_M(t)=L \cdot \frac{\partial~i_L}{\partial~t} + R_L \cdot i_L(t) 
\;\;\;\Leftrightarrow\;\;\;
\frac{u_M(t)}{L} = \frac{\partial~i_L}{\partial~t} + \frac{R_L}{L} \cdot i_L(t) $$ 
Wird diese Differentialgleichung Laplace-transformiert, ergibt sich im Bildbereich die Funktionsgleichung:
$$\mathscr{L}\Bigg(\frac{u_M(t)}{L}\Bigg) = \frac{U_M(s)}{L} = s \cdot I_L(s) - i_{L0} + \frac{R_L}{L} \cdot I_L(s)$$ 
Bei verschwindenden Anfangsbedingungen $i_{L0}=0$ gilt für die Übertragungsfunktion (transfer function, TF) zwischen Motorspannung und Motorstrom: 
$$ \begin{equation}
G_{EL^*}(s) = \frac{I_L(s)}{U_M(s)} = \frac{1}{L} \cdot \frac{1}{s+\frac{R_L}{L}} \label{eqGsAusg} \end{equation} $$
Die Zeitkonstante des ersten Energiespeichers im System kann durch Umformung des Nennerpolynoms von \eqref{eqGsAusg} bestimmt werden und beträgt $\; {\large\tau} = \frac{L}{R_L} = \frac{160\,\mu H}{1.5\,\Omega}\approx 107\,\mu s$. 

Mit dem Ziel, das System als Blockschaltbild darzustellen, wird die Übertragungsfunktion nach der Regel für PT1-Glieder umgeformt. Es gilt darauf zu achten dass bei der Umformung keine freien $s$-Faktoren entstehen da Systeme mit Nullstellenüberschuss keine Bandbegrenzung besitzen. Ein ideales Differenzierglied mit $G(s)=s$ ist aus Kausalitätsgründen technisch nicht realisierbar. \begin{equation} \mathrm{Übertragungsfunktion = \frac{Vorwärtspfad}{1 + Vorwärtspfad \times Rückwärtspfad}} \label{eqForwardPath} \\\\ \phantom{.} \\\\ G_{EL}(s) = \frac{I_L(s)}{U_M(s)} \cdot \frac{1/s}{1/s} = \frac{1}{s} \frac{1}{L} \cdot \frac{1}{1 + \frac{1}{s} \frac{R_L}{L}} \end{equation} <center>![realInductor](./pics/simulExport/realInductor.svg "Motorinduktivität")</center> 

#### Back-EMF ####
Die Änderung der magnetischen Flussdichte innerhalb einer Leiterschleife erzeugt nach Faraday und Maxwell ein elektrisches Feld zwischen den Leiteranschlüssen. Die _elektromagnetische Induktion_ führt bei Elektromotoren zu einer elektrischen Spannung, die der Quellenspannung des Motorantriebs entgegen wirkt. Aus diesem Grund wird diese elektromotorische Kraft (EMK, engl. "Electromotive Force", EMF) auch als Back-EMF oder Counter-EMF bezeichnet. Die Intensität der Back-EMF steigt proportional mit der Geschwindigkeit der bewegten Leiterschleife bzw. des bewegten Magnetfeldes, was im Modell durch die Produktbildung von Winkelgeschwindigkeit und einem konstanten Faktor $K_{EMF}$ berücksichtigt werden muss. Wenn die mechanischen Reibungsverluste eines elektrischen Antriebs zu 0 gesetzt werden, sind Drehmomentkonstante $K_{EL}$ und $K_{EMF}$ identisch.

In den Herstellerspezifikationen ([Electrical Specifications](#refTableElectric)) ist der EMF-Faktor mit $0.17\si{mV/degree/sec}\;\;±10\%$ angegeben. In si-Einheiten umgerechnet ergibt sich daraus 

$\Si{24}{\degree\per\second}$
$\Si[number-unit-product={}]{24}{\degree\per\s}$
$\num{24}\si{\degree\per\second}$

$$\begin{aligned} 
0.17,mV/degree/sec &= 9.74\times 10^{-3} V/rad/s \nonumber \\\
&= 9.74\times 10^{-3} Nm/A \nonumber
\end{aligned}$$

was, bis auf die Reibungsverluste, ziemlich genau der Drehmomentkonstante entspricht. Für die elektromotorische Kraft des bewegten Magnetfeldes gilt somit 
\begin{equation} u_{EMF}(t) = K_{EMF} \cdot \omega(t) \label{eqVemf} \end{equation} 
Die Spannung $u_{EMF}(t)$ wird mit negativem Vorzeichen in den Signalpfad vor $G_{EL^*}(s)$ Rückgekoppelt um ihren Einfluss auf die Dynamik des Aktors korregt zu modellieren.
\begin{equation} 
G_{EL}(s) = \frac{I_L(s)}{U_M(s)-U_{EMF}(s)} = \frac{1}{L} \frac{1}{s} \cdot \frac{1}{1 + \frac{1}{s} \frac{R_L}{L}} \label{eqGel} \end{equation} <center>![mechSubA](./pics/simulExport/mechSubA.svg "Mechanisches Subsystem")</center>

#### Elektrisch generiertes Drehmoment ####
Das elektrische Drehmoment $M_{EL}$ zum Zeitpunkt $t=t0$ entspricht dem Produkt aus Spulenstrom $i_L(t0)$ und Drehmomentkonstante $K_{EL}$, somit gilt $M_{EL}(t) = i_L(t) \cdot K_{EL}$ was einfach durch einen weiteren _Gain-Block_ im Blockschaltbild berücksichtigt wird. 

### Mechanik ###
Eine bewegte Masse speichert _kinetische Energie_ $E_{kin}$. Diese steigt dabei quadratisch zur Geschwindigkeit der bewegten Masse an. Rotiert eine Körper um eine feste Achse, so spricht man von _Rotationsenergie_ $E_{rot}$. Sie steigt in Abhängigkeit des [Trägheitsmoments][@Jx][^fnInertialmoment] $J_R$ des Körpers und dem Quadrat seiner Winkelgeschwindigkeit $\omega(t)$.
 
Das mechanische Teilsystem kann also ebenfalls durch ein entsprechend dimensioniertes PT1-Glied beschrieben werden (Ein einzelner, linear unabhängiger Energiespeicher). Um den systemtheoretischen Zusammenhang der einzelnen mechanischen Größen mathematisch abbilden zu können, wurde folgende Liste erstellt. Sie beinhaltet zusätzlich Näherungen und Annahmen die bisher getroffen wurden

- elektrisches Drehmoment $\bf{M_{EL}}$
    + Erregerfeld gilt als konstant bezüglich Intensität ($\vec{B}, \vec{H}$) und Winkelpos. (siehe [Klassifizierung](#klassifizierung)) 
    + $M_{EL}$ ist im Bereich $\pm \frac{1}{2}\cdot \Delta\varphi_{Max} = \pm 20°$ proportional zum Spulenstrom $i_L(t)$
    + Herstellerangaben zum Proportionalitätsfaktor $K_{EL}$ vorhanden 
- Trägheitsmoment $\bf{J_R}$ (alt. Inertialmoment) des rotierenden Körpers setzt sich zusammen aus 
    + Rotorwelle, Rotormagnet, Sensorscheibe und Spiegel
    + Die Drehachse wird als fest und die Rotormasse als homogen verteilt, angenommen 
        * Trägheitstensor darf in die skalare Größe des Trägheitsmoments überführt werden
    + Herstellerangabe zum skalaren Trägheitsmoment $J_R$ vorhanden 
- mechanische Reibung $\bf{M_{FR}}$, verursacht durch Reibungsverluste in
    + Kugellager, Positionssensor, keine Herstellerangaben
- äußeres Lastmoment / Rückstellmoment $\bf{M_{TB}}$  
    + siehe [Lastmoment](#lastmoment)
    + keine Herstellerangaben

#### Lastmoment ####
Für den konkreten mechanischen Aufbau des Scannermodells _6860_ konnten keine zuverlässigen Quellen gefunden werden. Die Vermutung, dass die Rotorwelle einem statischen Lastmoment ausgesetzt ist, soll im folgenden kurz begründet werden:

1. Rückstellung der Rotorwelle bis auf ±4° um die Mittelstellung wenn Spannungsfrei geschaltet
    - Die Rotorwelle wird automatisch in Mittelstellung zurück gedreht wenn das elektrische Moment zu 0 wird.
    - Dieser Effekt könnte, abhängig von Aufbau und Geometrie des magnetischen Statorkreises, auch darauf zurück zu führen sein, dass sich bei Mittelstellung der geringste magnetische Widerstand einstellt. Anders formuliert, könnte die Rückstellbewegung auch auf die [Reluktanzkraft](https://de.wikipedia.org/wiki/Reluktanzkraft "https://de.wikipedia.org/wiki/Reluktanzkraft") zurückzuführen sein.  
3. Kräftegleichgewicht bei sehr geringen Statorströmen (wenige mA)
    - Wird ein minimaler Gleichstrom in die Motorspule eingeprägt, so stellt sich im Bereich $\Delta\varphi_\{Max\}$ ein Gleichgewichtszustand des Drehwinkels ein. 
2. Quelle: Mechanisches Funktionsprinzip von Effektlasern auf [www.laserfx.com][laserfx]
4. Elektrische "Erdung" des Rotorkörpers um elektrostatischen Effekten vorzubeugen

In der Produktspezifikation des Herstellers sind keinerlei Angaben bezüglich eines statischen Lastmoments zu finden. Da dieses jedoch experimentell nachgewiesen werden kann und sich der Einfluss nur schwer abschätzen lässt, wurde bei der Modellbildung ein entsprechendes Lastmoment in Form einer Torsionsfederkonstante (lineares Verhalten) mit einbezogen.

#### Mechanisches Teilsystem ####
Entsprechend des Abschnitts [Mathematische Zusammenhänge](#mathematische-zusammenhänge) dient die Drehimpulsbilanzgleichung \eqref{eqDrehimpulsbil} als Ausgangspunkt für die konkrete Formulierung des mechanischen Teilsystems. Um das dynamische Verhalten der Aktoren weitestgehend korrekt abzubilden, müssen die zeitabhängigen Drehmomente $M_{EL},\,M_{FR},\,M_{TB}$ und das Massenträgheitsmoment $J_R$, bei der Bilanzbildung mit entsprechendem Vorzeichen berücksichtigt werden.
\begin{equation} 
J_R\,\frac{\partial}{\partial\,t} \, \omega(t) = M_{EL}(t) - \big[M_{FR}(t) + M_{TB}(t) \big] \label{eqDrehimpulsbilBase}\end{equation}
Das mechanische Reibmoment $\vec M_{FR}(t)$ und das Lastmoment $\vec M_{TB}(t)$ der Torsionsfeder wirken dem elektrisch generierten Drehmoment $\vec M_{EL}(t)$ entgegen. 
\begin{equation}    
J_R \; \dot\omega = M_{EL} - M_{Mech} \label{eqDrehimpulsbilKon} \end{equation} Werden die i.A. gerichteten Größen auf skalare reduziert, ergeben sich folgende, einfache Beziehungen 
\begin{equation}    
M_{TB} \;\propto\; \varphi \;\;\;\Leftrightarrow\;\;\; M_{TB} = K_{TB}\cdot\boldsymbol{\varphi} \label{eqLinearTorsin}    
\end{equation} Das Torsionsmoment (statisches Lastmoment) steigt an, je weiter der Rotor aus seiner Ruhelage heraus bewegt wird. Die Gleit-Reibung ist hingegen nur von der Geschwindigkeitsdifferenz zweier Körper abhängig, geht man von einem konstanten Gleitreibungskoeffizienten im Bereich $\pm 1/2\cdot\Delta\varphi_{Max}$ aus. Bei entsprechend "schwer" anlaufenden Antrieben sollte die Haftreibung (oft durch verzögerte Signum-Funktion modelliert) nicht außer Acht gelassen werden. Glücklicherweise kann hier auf die Klasse der hochgradig nicht-lineare Übertragungsfunktionen verzichtet werden. Für die Gleitreibung gillt jedoch: 
$$ \begin{align}
M_{FR} \;\propto\; \omega &\;\;\;\Leftrightarrow\;\;\; M_{FR} = K_{FR} \cdot\boldsymbol{\dot\varphi} \label{eqLinearFriction} \\\
M_{EL} \;\propto\; i_L &\;\;\;\Leftrightarrow\;\;\; M_{EL} = K_{EL}\cdot i_L \label{eqLinearElTorque}
\end{align} $$ Der lineare Zusammenhang zwischen Ankerstrom und Drehmoment wurde bereits erwähnt. Nach einsetzen von \eqref{eqLinearTorsin}, \eqref{eqLinearFriction} und \eqref{eqLinearElTorque} in die Drehimpulsbilanzgleichung aus \eqref{eqDrehimpulsbilKon} erhät man dann eine lineare DGL 2. Ordnung mit konstanten Koeffizienten:

\begin{equation}
J_R~\ddot\varphi + K_{FR}~\dot\varphi + K_{TB}~\varphi = K_{EL}\cdot i_L(t) \label{eqDglSecond} \\\\ \phantom{.} \\\\
\small{\left[kg\,s^2\right]\left[\frac{rad}{s^2}\right] + \left[\frac{Nm\,s}{rad}\right]\left[\frac{rad}{s}\right] + \left[\frac{Nm}{rad}\right]\left[rad\right] = \left[\frac{Nm}{A}\right]\left[A\right]} \\\\ \phantom{.} \end{equation}

Es gibt nun mehrere Ansätze wie die DGL in den Bildbereich transformiert werden kann. Mit Gleichung \eqref{eqDglSecond} als Ausgangspunkt, wäre eine direkte Transformation problemlos umsetzbar. Durch Anwendung des Differentiationstzes der Laplace-Theorie, lässt sich die Bildfunktion schnell aufstellen.
\begin{equation} 
\mathscr{ L }\bigg\lbrace\frac{\mathrm{d}^n x}{\mathrm{d} t^n}\bigg\rbrace = s^n \cdot X\left(s\right)-s^{n-1} \cdot x(0_{\small-})- \,\dots\left.\frac{\mathrm{d}^{n-1}x}{\mathrm{d}t^{n-1}} \right\bracevert\_{t=0_{\small-}} \;\;\;\;\;\;\;\;\;{\small{und\ mit}\;\;} \mathscr{L}\lbrace\varphi(t)\rbrace = {\large\Phi}(s) \nonumber
\\\\ \phantom{.} \\\\ \Downarrow \\\\ \phantom{.} \\\\
\frac{K_{EL}}{J_R} \cdot\mathscr{ L }\,\Big\lbrace\ i_L(t) {\Big\rbrace} = s^2 \,{\large\Phi}(s) - s\,\varphi(0)-\dot\varphi(0) + \frac{K_{FR}}{J_R}\cdot s \,{\large\Phi}(s) - \frac{K_{FR}}{J_R}\, \varphi(0) + \frac{K_{EL}}{J_R} \cdot {\large\Phi}(s) \nonumber
\end{equation}
Setzt man die Anfangsbedingungen in beiden Ableitungen wieder zu null, entseht zwar ein übersichtlicher Ausdruck, jedoch lässt sich von diesem nicht so ohne weiters auf die Struktur der Blockschaltung schließen. 
Andere wichtige Systemeigenschaften wie z.B. die stationäre Verstärkung oder die Zeitkonstanten des Streckenteils $\Phi{\small(s)/}I_L{\small(s)}$, können der Übertragungsfunktion ${\mathrm G_{{\small \mathrm M_1}}}$ jedoch entnommen werden.

\begin{equation}
\frac{K_{EL}}{J_R} \cdot I_L(s) = s^2 \,{\large\Phi}(s) + \frac{K_{FR}}{J_R}\cdot s \,{\large\Phi}(s) + \frac{K_{EL}}{J_R} \cdot {\large\Phi}(s) \nonumber \\\\ \phantom{.} \\\\ \Updownarrow \\\\ \phantom{.} \\\\
{\mathrm G_{{\small \mathrm M_1}}}(s)=\frac{{\large\Phi}(s)}{I_L(s)} = \frac{K_{EL}}{J_R} \cdot \frac{1}{s^2+s\cdot\frac{K_{FR}}{J_R}\+ \frac{K_{TB}}{J_R}\} \label{equDglWI}
\end{equation}

<span style="background-color: yellow"> Mit dem Übergang in den Bildbereich wurden die physikalischen Zusammenhänge beim ersten Ansatz untransparent. Aufgrund der Forderung nach einer , die Laplace Transformation auf eine DGL 1. Ordnung anwenden zu können, muss einer der kinetischen Energiespeicher aus \eqref{eqLinearFriction} "wegfallen". Wieder ausgehend von der Drehimpulsbilanzgleichung \eqref{eqDrehimpulsbilBase}, wird dieses mal nach dem "nächsten Verwandten" von $J_R\cdot\omega$ innerhalb der Inhomogenität der DGL gesucht:</span>

Werden in der Ausgangsgleichung nur Terme eingesetzt, die höchstens eine Integration über $\boldsymbol{\dot\omega}$ liegen, bleibt auch die Ordnung der resultierenden DGL erhalten. In \eqref{eqDrehimpulsbilBase} wird also nur das Reibmoment $M_{FR}$ durch $K_{FR} \cdot{\dot\varphi}=K_{FR} \cdot{\omega}\,$ und das elektrische Moment $M_{EL}$ entsprechend substituiert. Anschließend folgt wieder die Laplace-Transformation wobei $\Omega(s)$ als $\mathscr{ L } \big\lbrace\,\omega(t)\big\rbrace$ zu verstehen ist.
\begin{align} 
J_R\,\frac{\partial}{\partial\,t} \, \omega(t) &= \boldsymbol{K_{EL}\cdot i_L(t)} - \boldsymbol{K_{FR} \cdot \omega (t)} - M_{TB}(t) \;\;&&\Leftrightarrow \nonumber \\\
J_R\,\dot\omega + K_{FR} \cdot \omega  &= K_{EL}\cdot i_L - M_{TB}  &&\Big|\;\mathscr{ L } \lbrace\,\dots\rbrace \nonumber \\\
\Omega(s)\cdot \big(s\cdot J_R+K_{FR}\big) &= K_{EL}\cdot I_L(s) - M_{TB}(s) &&wenn\ \omega(0)=0 \label{eqBeforeLapMech} 
\end{align} 
Um an die Übertragungsfunktion des elektrischen Teilsystems $G_{EL}(s)$ aus \eqref{eqGel} anknüpfen zu können, muss Gleichung \eqref{eqBeforeLapMech} in eine Form gebracht werden, in der $I_L(s)$ im Nenner auftaucht:
\begin{align} 
\frac{ \Omega(s) }{K_{EL}\cdot I_L(s) - M_{TB}(s)}  &= \frac 1 {s\cdot J_R+K_{FR}} \nonumber \\\
&= \color{red}{\frac{1}{s} \frac{1}{J_R}} \cdot \frac{1}{1 + \color{red}{\frac{1}{s} \frac{\color{blue}{K_{FR}}}{J_R}}} \nonumber
\end{align}
Diese Übertragungsfunktion lässt sich nach einer Umformung entsprechend Regel \eqref{eqForwardPath} wieder direkt in einem Blockdiagramm darstellen:
<center>![mechSubInklTb](./pics/simulExport/mechSubInklTb.svg "Mechanisches Subsystem inkl. Torsionsmoment")</center>

#### Positionssensor ####
Die verwendeten Galvoscanner sind mit einem integrierten Positionsdetektor ausgestattet. Die Winkelposition der Rotorwelle wird anhand variabler Kapazitäten gemessen ([siehe Abb. in _Modellbildungsprozess_](#modellbildungsprozess)). Die Größenordnung der Kapazitätsdifferenz liegt bei nur wenigen Picofarad. Um auch kleine Positionsänderungen präzise messen zu können, sind entsprechend hohe Anforderungen an die Mess- und Auswerteelektronik zu stellen. Die vom Hersteller bereitgestellte Winkelposition ist einer Trägerschwingung von $f_0 = 1.6~MHz$ aufmodulliert und steht als Differenzstromsignal zur Verfügung. Mit einer entsprechend präzise ausgelegten Operationsverstärkerschaltung wurde das Differenzstromsignal zu einer proportionalen Gleichtaktspannung demoduliert. Der Proportionalitätsfaktor wird im Folgenden als $K_{PD}$ bezeichnet und besitzt die Einheit $V/rad$.
Um den eingebauten Positionssensor der _6860_ Galvoscanner zu modellieren, wird die Winkelgeschwindigkeit $\omega(t)$ durch einen einfachen Integrationsblock in die Winkelposition $\varphi(t)$ überführt (siehe [Mathematische Zusammenhänge](#mathematische-zusammenhänge)). 

#### Verbindung der Teilsysteme ####
Nachfolgende Abbildung zeigt das zusammengesetzte Modell. Der in Abschnitt [Positionssensor](#positionssensor) erwähnte Proportionalitätsfaktor $K_{PD}$ muss erst in der Rückführung von $\varphi(t)$ auf den ADC des diskreten Reglers beachtet werden.
<center>![systemSubCmpl](./pics/simulExport/systemSubCmpl.svg "Zusammengesetztes Teilsysteme")</center>
Die in den Teilsystem-Blockschaltbildern noch offenen Signaleingänge $M_{TB}$ sowie $V_{EMF}$, müssen entsprechend den linearisierten Beziehungen aus \eqref{eqVemf} bzw. \eqref{eqLinearTorsin} erzeugt werden. Das resultierende, __lineare__ Modellist in folgender Abbildung gegeben:
<center>![systemLinCmpl](./pics/simulExport/systemLinCmpl.svg "Lineares Aktor Modell")</center>


$$ G(s)=\frac{K_{EL}} { \color{green}{J_R~L}\cdot s^3 + (\color{blue}{ K_{FR}~L+J_R~R_L+J_R~R_{sh} }) \cdot s^2 + (\color{red}{K_{EMF}~K_{EL}+K_{FR}~R_L+K_{FR}~R_{sh}}) \cdot s } $$

#### Aktor Gesamtmodell ####
Das Gesamtmodell der Galvoscanner entspricht im Wesentlichen dem aus Abschnitt [Verbindung der Teilsysteme](#verbindung-der-teilsysteme). Die Winkelposition wird im Bereich $|\,\varphi\,| > 1/2\cdot\Delta\varphi_\{Max\}$ nichtlinear da der Aussteuerbereich des Rotors durch mechanische Endanschläge blockiert wird. Weiterhin wird auch der vom Hersteller angegebene Wicklungsspitzenstrom als Grenzwert für den linearen Bereich des Ankerstromkreises interpretiert sodass die Übertragungsfunktion des elektrischen Teilsystems für $|\,i_L\,| > 25\,A$ ungültig wird. Beide Bereiche werden im Blockdiagramm durch Sättigungsblöcke modelliert.   

##### Regelungsnormalform #####
> Systeme, die über eine lineare Differentialgleichung N-ter Ordnung beschrieben werden, sind linear und zeitinvariant. [^fnMesystoDglSys]

Eine universelle Methode zur Ableitung grafischer Blockdiagramm aus mathematischen Vorschriften, führt über die __Zustandsraumbeschreibung__ von LTIs. Jedes Zustandsraummodell kann _direkt_ auf einen als __Regeleungsnormalform__ bekannten Signalflussplan abgebildet werden! Die Regelungsnormalform stützt sich dabei auf der _Transformierbarkeit_ von linearen Differentialgleichungssystemen N-ter Ordnung in N lineare Differentialgleichungen 1. Ordnung. Nachfolgende Abbildung zeigt ein Blockdiagramm der Regelungsnormalform für alle LTI DGL-Systeme der Ordnung 3. 

<center>![Regeleungsnormalform](./pics/regelNormalform.svg "Signalflussplan der Regeleungsnormalform für Systeme 3. Ordnung")</center>



### Testsignale ###
#### Problematik der Sättigung ####
## Stellglied / Leistungsteil ##
## Signalkonditionierung ##
# Angaben zur Systemdynamik #
## Spezifikationen des Gesamtsystems ##
# Gesamtsystem
## Warum ARM? ##
# Software
## DOXYGEN!!! ##
## CMSIS ##
# Regelungstechnik
## Diskretisierungsverfahren ##
# Geschlossene Simulationsumgebung #
## Umsetzung in MATLAB / Simulink ##
## "frequency response model estimation" ##
## copy ltspice conform laplace function of the estimated system  ##
## Aktoren -> Simulink Modelle  ##
## Endstufe -> LTspice -> MATLAB ##
## Levelshifter -> LTspice -> MATLAB ##
## Antialias / Rekonstruktionsfilter -> MATLAB ##
# Simulationen und Verifizierung
## Step-by-Step ##
## Spice: Geht die Simulation nicht ... ##
###  ... geht auch der Testaufbau nicht! ###
## Regelalgorithmen testen: ##
### RC-Glied direkt an gepufferten DAC ###
### Testsignale im uC erzeugen ###
### Oszibilder mit MATLAB-Simulation vergl. ###
# Modellparameter testen
# Hardware
# Resumee
# Quellenangaben

<!-- # geschlosseneModell #
# Simulation #
# SpezifikationedeGesamtsystem #
# ModellierununSimulation #
# Gesamtsystem #
# Modellbildung #
# ModellbildundeTeilsysteme #
# Hardware #
# Software #
# UmsetzuniMATLAB/Simulink #
# VerifizierundeModellmöglich? #
# Modellparametebestimmeuntesten #
# Schwerpunkt #
# Quellenangaben # -->

[^fnWikiAnsys]: __*ANSYS*__ ["*(Kurzform für **AN**alysis **SYS**tem) ist eine Finite-Elemente-Software der Firma Ansys Inc., ehemals SASI (Swanson Analysis Systems Inc.).*"][wikiAnsys]

[^fnMaxwell]: *ANSYS* __*Maxwell*__ ["*is the premier low frequency electromagnetic field simulation software for engineers tasked with designing and analyzing 2-D and 3-D electromagnetic devices.*"][AnsMaxwell]

[^fnSimplorer]: *ANSYS* __*Simplorer*__ ["*is a powerful platform for modeling, simulating and analyzing virtual system prototypes.(…) broad support for assembling system-level physical models and helping product development organizations connect conceptual design, analysis and system verification.*"][AnsSymplor]

[^fnArnoldMagn]: __*Arnold Magnetics*__ [*"The magnet material is both brittle and very hard (Rockwell C 57 to 61) and requires diamond wheels for slicing and diamond or special abrasive wheels for grinding."*][MagnetManu]

[^fnChRoy]: __*C. Roy, W. Oberkampf, 2010*__ [*Verification and Validation in Scientific Computing*][RoyGooglebook] 

[^fnRUnb]: __*Rolf Unbehauen, 2002*__ [*Systemtheorie 1: Allg. Grundlagen, Signale und lineare Systeme im Zeit- und Frequenzbereich*][SystemUnbehauen]

[^fnAnfrageBrunner]: __*Projektanfrage HsKA*__ [*Projektanfrage_Galvanometer-Scanner_Prof_Brunner.pdf*][AnfragePdf]

[^fnMultiDomain]: __*Multi-Domain-Modelle*__ *oder auch* __*Multiphysik-Modelle*__ *sind Simulationsmodelle, die Systeme über mehrere physikalische Domänen hinweg, in ihren Eigenschaften beschreiben und ihre Wechselwirkungen simulieren können. Hier wurden Statik/Kinematik (Mechanik-Domäne), Magnetostatik/Magnetodynamik (allg. Elektrodynamik, Elektrik-Domäne) sowie thermodynamische Vorgänge in einem planar- oder 3-dimensionalen FEM-Modell simuliert.*

[^fnWikiSys]: __*Systemtheorie*__ [*Wikipedia: Systemtheorie (Ing.)*][wikiSysth]

[^fnCapSens]: __*Differential-Drehkondensator*__ [*Wikipedia: Differential-Drehkondensator*][wikiVarCap]

[^fnNoBrainChip]: __*Chip without text*__ http://www.clker.com/cliparts/e/5/2/J/G/G/chip-without-text.svg/ 

[^fnBrain]: __*Brain*__ http://troy-halverson.appspot.com/IsmProv/brain.svg 

[^fnReuseCode]: __*Reusability*__ [*Wikipedia: Reusability*][wikiReuse]

[^fnRoSe]: __*K. H. Rollke, K. Sennholz*__ *Grund und Leistungskurs Informatik; Cornelsen Verlag, Berlin, 1994*

[^fnHarms09]: __*Eike Harms*__ [*Konfigurationsmanagement unter Berücksichtigung von Verwendungsinstanzen*][harms] 

[^fnStachowiak]: __*Herbert Stachowiak*__ [*Allgemeine Modelltheorie*][StachowiakBooks] 1973, Kap. 2.1.1.1, S. 131 ... 133

[^fnPapula2]: __*Lothar Papula*__ [*Mathematik für Ingenieure und Naturwissenschaftler Band 2*][Papula2] 2009, Kap. 1.4 S. 348

[^fnElektrBauelem]: __*R. Großmann, A. Frey*__ [*Elektronische Bauelemente*][GroFrey]

[^fnwikiGenericTypes]: __*Generischer Typ*__ [*Wikipedia: Generischer Typ*][wikiGenericTypes] 

[^fnGalvoScanlab]: __*Galvanometer-Scanner*__ http://www.scanlab.de/service/glossary/g#Galvanometer-Scanner

[^fnInertialmoment]: __*Trägheitsmoment*__ https://de.wikipedia.org/wiki/Tr%C3%A4gheitsmoment   <a name="citeInertialmoment"/> </a>

[^fnAngularMomentum]: __*Drehimpuls und Drehmoment*__ https://www.lernhelfer.de/schuelerlexikon/physik-abitur/artikel/drehimpuls

[^fnImpulserhaltung]: __*Impulserhaltungssatz*__ https://de.wikipedia.org/wiki/Impulserhaltungssatz   <a name="citeImpulserhaltung"/> </a>

[^fnMesystoDglSys]: __*Interpretation der Übertragungsfunktion*__ http://www.eit.hs-karlsruhe.de/mesysto/teil-a-zeitkontinuierliche-signale-und-systeme/systeme-im-laplace-bereich/interpretation-der-uebertragungsfunktion.html

[@MDA:2006]: #citeMDA "V. Gruhn, D. Pieper, C. Röttgers; MDA® Effektives Software-Engineering mit UML 2® und Eclipse TM. Springer-Verlag Berlin Heidelberg; 2006;"

[@Probst:2011]: #citeProbst "Uwe Probst; Servoantriebe in der Automatisierungstechnik - Komponenten, Aufbau und Regelverfahren; 2011;"

[@Iser:2008]: #citeIserm "Rolf Isermann; Mechatronische Systeme - Grundlagen; 2008;"

[@Jx]: #citeInertialmoment "Das Trägheitsmoment, auch Massenträgheitsmoment oder Inertialmoment, gibt den Widerstand eines starren Körpers gegenüber einer Änderung seiner Rotationsbewegung um eine gegebene Achse an (Drehmoment geteilt durch Winkelbeschleunigung). Damit spielt es die gleiche Rolle wie im Verhältnis von Kraft und Beschleunigung die Masse;" 

[@Impulserhaltung]: #citeImpulserhaltung "Der Impulserhaltungssatz (manchmal auch kurz Impulssatz genannt) ist einer der wichtigsten Erhaltungssätze der Physik und besagt, dass der Gesamtimpuls in einem abgeschlossenen System konstant ist. „Abgeschlossenes System“ bedeutet, dass das System keine Wechselwirkungen mit seiner Umgebung hat."

<a name="citeMDA"/> </a>
__[MDA:2006]__ _V. Gruhn, D. Pieper, C. Röttgers;_ __*MDA® Effektives Software-Engineering mit UML 2® und Eclipse TM. Springer-Verlag Berlin Heidelberg; 2006;*__

<a name="citeProbst"/> </a>
__[Probst:2011]__ _Uwe Probst;_ __*Servoantriebe in der Automatisierungstechnik - Komponenten, Aufbau und Regelverfahren; 2011;*__

<a name="citeIserm"/> </a>
__[Iser:2008]__ _Rolf Isermann;_ __*Mechatronische Systeme - Grundlagen; 2008;*__



---

[wikiAnsys]: https://de.wikipedia.org/wiki/ANSYS_(Software) "ANSYS (Software)"
[wikiSysth]: https://de.wikipedia.org/wiki/Systemtheorie_(Ingenieurwissenschaften) "Systemtheorie (Ingenieurwissenschaften)"
[wikiVarCap]: https://de.wikipedia.org/wiki/Datei:Differential-Varko.svg "Variabler Drehkondensator (differentiell)"
[wikiReuse]: https://en.wikipedia.org/wiki/Reusability "Reusability (Computer science and software engineering)"
[AnsMaxwell]: http://www.ansys.com/Products/Electronics/ANSYS-Maxwell "Products/Electronics: "Maxwell""
[AnsSymplor]: http://www.ansys.com/it-IT/Products/Systems/ANSYS-Simplorer "Products/Systems: "Simplorer""
[RoyGooglebook]: https://books.google.de/books/about/Verification_and_Validation_in_Scientifi.html?id=7d26zLEJ1FUC&redir_esc=y "Online book resource"
[MagnetManu]: http://www.arnoldmagnetics.com/en-us/Technical-Library/Magnet-Manufacturing-Process "Magnet manufacturing process"
[AnfragePdf]: ./Projektanfrage_Galvanometer-Scanner_Prof_Brunner.pdf "Dokument mit Projektanfrage" 
[SystemUnbehauen]: https://books.google.de/books?id=zcbnBQAAQBAJ&pg=PA1&lpg=PA1&dq=Systeme+und+Signale+sind+die+beiden+wichtigsten+Konzepte+der+Systemtheorie&source=bl&ots=je6qEA32bz&sig=UagREGj3tQWfEyX9y_OzGwfVWH0&hl=de&sa=X&ved=0ahUKEwjo_MDMjKPQAhXEPhQKHfVBBz0Q6AEIIzAC#v=onepage&q=Systeme%20und%20Signale%20sind%20die%20beiden%20wichtigsten%20Konzepte%20der%20Systemtheorie&f=false "Online book resource"
[WillertUML]: http://www.embeddedcomputingconference.ch/pdf_2011/4c1-vanderheiden.pdf "UML statt „C“ Vorurteile gegenüber der UML?"
[StachowiakBooks]: https://books.google.de/books?hl=de&id=DK-EAAAAIAAJ&focus=searchwithinvolume&q=Ein+Modell+ist+stets+ein+Modell+von+etwas "Online book resource"
[Papula2]: https://www.pdf-archive.com/2015/03/28/papula-mathematik-fuer-ingenieure-2/papula-mathematik-fuer-ingenieure-2.pdf "Volltext: Mathematik für Ingenieure und Naturwissenschaftler Band 2"
[GroFrey]: http://www.hs-augsburg.de/~ragr/Topics/SCHT2/Common/Skript_EB_V3.3.pdf "Elektronische Bauelemente"
[harms]: http://docplayer.org/16028346-Zur-erlangung-des-akademischen-grades-eines-doktors-der-ingenieurwissenschaften.html "Dissertation - Universität Karlsruhe"
[ieee1471]: https://de.wikipedia.org/wiki/IEEE_1471 "IEEE Recommended Practice for Architectural Description of Software-Intensive Systems"
[wikiGenericTypes]: https://de.wikipedia.org/wiki/Generischer_Typ "Generischer Typ"
[veteranGalvo]: https://www.google.de/#q=cambridge%20technology%206860 "Veteran Galvo Motors"
[cambridgeTech]: www.cambridgetechnology.com "www.cambridgetechnology.com"
[typ6860spec]: <https://www.google.de/url?sa=t&rct=j&q=&esrc=s&source=web&cd=10&cad=rja&uact=8&ved=0ahUKEwjZ5bLLuLXQAhWBuRQKHfd3Bc4QIAhgMAk&url=http%3A%2F%2Fwebcache.googleusercontent.com%2Fsearch%3Fq%3Dcache%3A1O6mSJqn6noJ%3Acambridgetechnology.net%2Findex.php%253Foption%253Dcom_docman%2526task%253Ddoc_download%2526gid%253D322%2B%26cd%3D10%26hl%3Dde%26ct%3Dclnk%26gl%3Dde&usg=AFQjCNFCsAo8tjp7P4odi0Yv0yQupg3JAw&sig2=KDaq0vZeNkkPfkigxltuPg> "google cache, letzter Aufruf: 19.11.2016"
[motorModeling]: http://ctms.engin.umich.edu/CTMS/index.php?example=MotorPosition&section=SystemModeling "http://ctms.engin.umich.edu/CTMS/index.php?example=MotorPosition&section=SystemModeling"
[laserfx]: http://www.laserfx.com/Works/Works3S.html "How Laser Shows Work - Scanning System"
[leifiDrehbewegung]: http://www.leifiphysik.de/mechanik/drehbewegungen "Drehbewegungen"

# Important Notes #
- MathJax:
    + Math Settings:
        * Zoom Trigger: No Zoom
        * Zoom Factor: 200%
        * Math Renderer: 
            - Common HTML
            - Fast Preview
        * Scale all Math: 90%
    + Accessibillity

# Trash #
<a name="refTableElectric"> </a>

| Elektrische Spezifikationen    |                              |                |                      |
| ---                            | ---                          | ---            | ...                  |
| Coil Resistance                | 1.5 Ohm                      |                | $\pm\SI\{10\}\{\%\}$ |
| Coil Inductance                | 160µH                        |                | $\pm\SI\{10\}\{\%\}$ |
| Back EMF Voltage               | 0.17mV/degree/sec            | 9.74mV/rad/sec | $\pm\SI\{10\}\{\%\}$ |
| RMS Current                    | 4.6A @ T_case=50°C, Max      |                |                      |
| Peak Current                   | 25A, Max                     |                |                      |
| Small Angle Step Response Time | 0.5ms (inertia matched load) |                |                      |


<a name="refTableMechanic"> </a>

| Mechanical Specifications        |                    |             |                      |
| ---                              | ---                | ---         | ...                  |
| Rated Angular Excursion          | 40°                |             |                      |
| Rotor Inertia                    | 0.6 gm.cm^2        | 6e-8 kg.m^2 | $\pm\SI\{10\}\{\%\}$ |
| Torque Constant                  | 9.3 10^4 dyne.cm/A | 9.3e-3 Nm/A | $\pm\SI\{10\}\{\%\}$ |
| Maximum Coil Temperature         | 110°C              |             |                      |
| Thermal Resistance (Coil - Case) | 1.5°C/Watt, Max    |             |                      |

<span style="font-size: 80%">$\;\;\;1\;dyne.cm \;\;\;\Leftrightarrow\;\;\; 1\times 10^{-7} Nm$
$\;\;\;1\;gm.cm^2 \;\;\;\Leftrightarrow\;\;\; 1\times 10^{-7} kg.m^2$</span>

| Position Detector                |                                         |                      |
| ---                              | ---                                     |                      |
| Linearity                        | 99.9%, Minimum, over 40 degrees         |                      |
| Scale Drift                      | 50PPM/°C, Maximum                       |                      |
| Zero Drift                       | 15 microradians/°C, Maximum             |                      |
| Repeatability, Short Term        | 8 microradians                          |                      |
| Output Signal, Common Mode       | 585µA @ AGC voltage=10VDC               | $\pm\SI\{20\}\{\%\}$ |
| Output Signal, Differential Mode | 14.5µA/° @ common mode current of 585µA | $\pm\SI\{20\}\{\%\}$ |

<p style="margin: 0em 18em 0em 9em; background: -webkit-linear-gradient(top left, #ccc 20%, #ccc 40%, rgba(250, 250, 250, 0) 100%);"> 
</p>

kann nach Newton's 3. Axiom [_"Actio et Reactio"_](https://de.wikipedia.org/wiki/Actio_und_Reactio) $\Rightarrow \vec{F_{A\rightarrow B}} = -\vec{F_{B\rightarrow A}} $ folgende Bestimmungsgleichung aufgestellt werden: 

$$ \omega(t)=L \cdot \frac{\partial~\varphi}{\partial~t} $$


$$ \vec{L} = \vec{r} \times \vec{p} = \vec{r} \times \left( m\cdot\vec{v}\right) \label{eqRmv} $$

Durch die zeitliche Ableitung $\dot{\vec{L}}$ erhält man den Drehmomentvektor $\vec{M}$. Da sowohl Ortsvektor $\vec{r}(t)$ wie auch der Geschwindigkeitsvektor $\vec{v}(t)$ des Impulses $\vec{p}(t)$ Funktionen in _t_  darstellen, muss Gleichung \eqref{eqRmv} über die Produktregel differenziert werden:  

\begin{align}
\frac{\partial}{\partial\,t} \vec{L} &= \dot{\vec{r}} \times \left( m \cdot \vec{v} \right) \nonumber \\\ 
\dot{\vec{L}} &= \dot{\vec{r}} \times \left( m \cdot \vec{v} \right) + \vec{r} \times \left( m \cdot \dot{\vec{v}} \right) \nonumber
\end{align}

<!-- > Bei der Translation charakterisiert der Impuls den Bewegungszustand eines Körpers. In analoger Weise lässt sich bei der Rotation der Bewegungszustand eines rotierenden starren Körpers durch die physikalische Größe Drehimpuls kennzeichnen.[^fnAngularMomentum]  -->

---
__Parameterableitung eines Vektors mit konstanter Länge__ 
Ist der Betrag eines Vektors $\vec{r}(x)$ als konstant zu betrachten, so steht dieser stehts senkrecht zu seiner Ableitung:    

\begin{align}
\vec{r} = const \;\;\;&\Rightarrow\;\;\; \left| \vec{r} \right| = const \;\;\;\Rightarrow\;\;\; \sqrt{\vec{r} \cdot \vec{r}} = const \nonumber \\\ &\Rightarrow\;\;\; \vec{r} \cdot \vec{r} = const \label{eqrr}
\end{align}

Unter Anwendung der Produktregel wird die erste Ableitung von \eqref{eqrr} nach $x$ gebildet:

$$ \frac{\partial\,\vec{r}}{\partial\,x} \cdot \vec{r} \;+\; \vec{r} \cdot \frac{\partial\,\vec{r}}{\partial\,x} = 2 \cdot \left( \vec{r} \cdot \frac{\partial}{\partial\,x}\vec{r} \right) = 0 $$

Hieraus folgt, dass der Vektor senkrecht zu seiner Ableitung stehen muss.
$$ \vec{L} = J \cdot \vec{\omega} $$



<img src="./pics/energiebilanzDeriv.svg" title="Energiebilanz eines beliebigen Energiespeichers" align="rigth" height="138x" style="float:right; margin: 0em 0em 0em .5em;"/>
Die im Rahmen dieser Arbeit relevanten,  Erhaltungssätze 
Für den Fall 
Der Drehimpulsvektor $\vec{L}$ eines starren Körpers wird definirt als Kreuzprodukt aus Ortsvektor und Impulsvektor. 

Auch in der technischen Mechanik stützen sich viele mathematische Ansätze der Dynamik auf Bilanzgleichungen diverser physikalischer Größen. Zum Beispiel gilt für jedes energetisch abgeschlossene System (Bsp.: idealer Feder-Masse-Schwingkreis, idealer LC-Schwingkreis) stehts, dass die Momentanenergie zu jedem Zeitpunkt $t \ge 0$ identisch mit der Energie zum Zeitpunkt $t=0$ übereinstimmt. In diesem Fall bestimmt die _Anfangsbedingung_ das Energieniveau des Systems. 
<p style="margin-top: 2em; background-color: yellow; padding: 1em"> Die Gesetze zur __*Erhaltung*__ der _Masse_, der _Energie_ und des _Impulses_ sind fundamental. Aus diesen Erhaltungssätzen lassen sich domänenübergreifende, aber auch vollkommen unspezifische Bilanzgleichungen formulieren, d.h. unabhängig von der "Bauform" der Prozesse. </p><p style="text-align: right; margin-top: -1em; margin-bottom: 2.5em"> vergl. [[Iser:2008, 61]][@Iser:2008]</p>

<!-- M_{FR} \;\propto\; \omega &\;\;\;\Leftrightarrow\;\;\; M_{FR} = K_{FR} \cdot\boldsymbol{\dot\varphi} \label{eqLinearFriction} \\\
M_{EL} \;\propto\; i_L &\;\;\;\Leftrightarrow\;\;\; M_{EL} = K_{EL}\cdot i_L \label{eqLinearElTorque} -->
<!-- $$ \mathsf{G(s)=  \frac{\small{Y}(s)}{\small{U}(s)} = \frac{z_3\cdot s^2+z_2\cdot s+z_1}{s^3+n_3\cdot s^2+n_2\cdot s+n_1} }$$ --> 

$\pm 20°\,s^{-1}$
$\pm 20\si{°/s}$
$\pm 20°\si{\per s}$
$\pm 20\si[per-mode=symbol]{°/s}$
$\pm 20\Si{°/s}$
$\Si{\ang{\pm 20} \per s}$
$\pm 20 \Si{\degree \per s}$
$\ang{100}$
$100°$