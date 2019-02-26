# *typography-latex.py* der typographische Vor-Filter für LaTeX-Dateien

Dieser Vor-Filter wandelt z.B. in z.\\thinspace{}B. um, und setzt damit deutsche Typographie Emfehlungen um.

So wird aus der Datei `demo.tex`

```
\documentclass{minimal}
\begin{document}
Das ist z.B. ein Test in wie weit u.s.w. das m.a.W. umgewandelt wird.
\end{document}
```

mit Hilfe des Befehls

```
> typography-latex.py demo.tex
```

die Datei 

```
\documentclass{minimal}
\begin{document}
Das ist z.\thinspace{}B. ein Test in wie weit u.\thinspace{}s.\thinspace{}w. das m.\thinspace{}a.\thinspace{}W. umgewandelt wird.
\end{document}
```

Die Orginaldatei wir dabei in `demo.tex.bak` gesichert.

Viel Spaß damit
N.Markgraf


