

### Klassifizierung ###
Galvanometer-Motoren lassen sich nicht so ohne weiteres in eine Unterklasse der Elektromotoren einordnen. Als Messinstrument in Drehspulmesswerken, erzeugt das Galvanometer eine mechanische Drehbewegung proportional zum gemessenen Strom. DC-Motoren hingegen sind elektromechanische Baugruppen die eine elektrische Gleichleistung in eine mechanische Leistung umsetzen können. Im dynamischen Betrieb verhält sich ein Spiegelgalvanometer ähnlich einem DC-Motor. Das Momentanmoment, multipliziert mit der Drehzahl ergibt eine mechanische Leistung in Nm/s. Im statischen Betrieb gleicht der Galvomotor einem elektrischen Drehmagneten welcher ein mechanisches Drehmoment erzeugt. 

Bei der Modellierung von DC-Motoren wird der Zusammenhang zwischen Motorstrom und Drehmoment oft soweit linearisiert, dass zur Beschreibung ein konstanter Faktor, die Drehmomentkonstante, ausreichend ist. Zulässig wird diese Annäherung, wenn man die magnetische Flußdichte des Erregermagnetfeldes als konstant betrachten kann ([siehe Abbildung][motorModeling]). 

![Bild](./motorMatlab"Der")

Da das elektromechanische Wirkprinzip der hier verwendeten "_Moving Magnet Galvanometer_" auf einem permanent erregten Magnetfeld basiert, ist die Annahme _B=const_ gerechtfertigt. Wenn die Intensität des Erregerfeldes für beide Betriebsarten (Motor, Drehmagnet) gleich und als konstant angenommen wird, entsteht durch die variable Position des Rotormagnetfelds gegenüber dem des Statorfelds ein Fehler. Tabelle [_Mechanical Specifications_](#refTableMechanic) kann eine maximale Auslenkung der Rotorwelle von +-20° entnommen werden. Das Momentanmoment ändert sich in diesem Bereich entsprechend dem Kosinus des Rotorwinkels was im schlimmsten Fall zu einem Fehlerfaktor von 

$$ cos(20°\frac{\pi}{180°})\approx 0.94 $$ 

führt. Obwohl es sich bei Galvanometer-Motoren also nicht um DC-Motoren im klassischen Sinn handelt, kann eine Drehmomentkonstante zur approximation angegeben werden. Wie in Abschnitt [Industriell gefertigte Aktoren](#industriell-gefertigte-aktoren), letzter Absatz, erwähnt, muss das Modell anhand von Herstellerspezifikationen konkretisiert werden können. In Tabelle [_Mechanical Specifications_](#refTableMechanic) ist die entsprechende Drehmomentkonstante unter _Torque Constant_ angegeben.

Der vollständigkeit halber sollen an dieser Stelle einige paralleln zur Unterklasse der _elektronisch kommutierten_ Elektromotoren gezogen werden. Das Rotormaterial der unter dem Begriff "_Brushless <a style="color: #ddd ">DC-</a>Motor_" bekannten Antriebe besteht i. d. R. ebenfalls aus permanent magnetisierten Werkstoffen. Durch eine elektronische Ansteuerung wird über mehrere Statorwicklungen ein Drehfeld erzeugt.

#### Mathematische Zusammenhänge ####
Grundlage eines generischen Modells ist seine Mathematik. Die Gesetze der Physik müssen bei der mathematischen Modellierung eingehalten werden. Der Verlauf der Geschwindigkeit _v(t)_ eines Körpers lässt sich z. B. durch Differentiation seiner Streckenfunktion _s(t)_ oder durch Integration seiner Beschleunigung _a(t)_ über der Zeit formulieren. Diese Gesetzmäßigkeiten gelten gleichermaßen für translatorische sowie rotatorische Bewegung. Daraus folgt, dass z. B. die Integralbildung der Winkelgeschwindigkeit _ω(t)_ eines rotierenden Körpers unmittelbar auf seine Winkelposition _φ(t)_ führt. Diese grundlegenden Gesetze müssen später anhand des Modells verifiziert werden können. 
