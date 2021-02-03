"# ET_Lesen_Py38_Dual" 

Das hier ist das angefangene Bastelprojekt entstanden aus dem oculib-Sandmann-Projekt (Python 2.7).
Ich habe es unter WinPy32Bit Python 3.6 und 3.8 getestet - im Single PC Mode kann ich den Eyetracker öffnen, kalibrieren usw. (über Kommandozeile) - PsychoPy GUI läuft, aber kein pyglet Window.

Die Klassen/Skripte aus oculib habe ich der Einfachheit halber z.T. rauskopiert ins Hauptverzeichnis, um mich erstmal nicht mit relativen imports auseinandersetzen zu müssen. In /smi/et_smi.py habe ich in der Methode "open" den mode="single" ergänzt.. Das müsste man natürlich eleganter machen und die beiden IP-Adressen per API direkt setzen können.

Hier der Fehler, den pyglet zu produzieren scheint: (getestet mit pyglet 1.4 und pyglet 1.5).

![OpenGl/pyglet Error](opengl_error.png)
