[![BCH compliance](https://bettercodehub.com/edge/badge/NMarkgraf/typography-latex.py?branch=master)](https://bettercodehub.com/)
[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](http://www.repostatus.org/badges/latest/active.svg)](http://www.repostatus.org/#active)
[![Minimal Python needed: 3.5+](https://img.shields.io/badge/Python-3.5%2B-brightgreen.svg)](https://www.python.org)
[![CodeFactor](https://www.codefactor.io/repository/github/nmarkgraf/typography-latex.py/badge)](https://www.codefactor.io/repository/github/nmarkgraf/typography-latex.py)
[![ORCiD](https://img.shields.io/badge/ORCiD-0000--0003--2007--9695-green.svg)](https://orcid.org/0000-0003-2007-9695)

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


