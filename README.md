# projectGalvoDocu #
This repository contains all source files necessary for the documentation of project GalvoScanner.

# pandoc 2 pdf compatibility #
---
__Tex cannot handle svg's__
If all svg's exists also in png format:   
```bash
sed -ri.bak 's/\.svg/.png/g' <file.md>
```

Another way is to produce pdf-images via inkscape: 
```bash
arr=($(grep -oE '\.\/.*\.svg' <file.md>))

for k in "${arr[@]}"; 
  do inkscape -D -T -z --file="$k" --export-pdf="$(dirname $k)/$(basename $k .svg).pdf" --export-latex;
done

sed -ri.bak 's/\.svg/.pdf/g' <file.md>
```
---
__No leading/traiing spaces inside inline maths allowed__

# Run pandoc #
First try to convert directly from markdown to pdf: 
```bash
pandoc -sSf markdown -o<file>.pdf <file>.md
```
## Known issues ##
If there are errors to fix within the *.tex file, run: 
```bash
pandoc -sSf markdown -o<file>.tex <file>.md
```

## Fixing LaTex sources ##
```tex
(... packages)
\usepackage{siunitx}
\newcommand{\Si}{\large\si[per-mode=fraction]{1}}
```

replace:
\Si\{rad\per s\}            \Si\{rad\per sec\}
\Si\{V.s\per rad\}          \Si\{V.sec\per rad\}
\Si\{N.m\per rad\}          \Si\{\newton\meter\per rad\}
\Si\{\newton\meter\per A\}  \Si\{\newton\meter\per Amp\}
\(\si\{\newton\meter\}\)    \(\si{\newton\meter}\)