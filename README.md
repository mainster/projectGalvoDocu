# projectGalvoDocu
This repository contains all source files necessary for the documentation of project GalvoScanner.

# pandoc 2 pdf compatibility

- Tex cannot handle svg's
- No leading/traiing spaces inside inline maths allowed

```bash
arr=($(grep -oE '\.\/.*\.svg' projektGalvoDoku.md))

for k in "${arr[@]}"; 
  do inkscape -D -T -z --file="$k" --export-pdf="svg2pdf/$(basename $k .svg).pdf" --export-latex;
done

sed -r -i 's/(\.\/.*\.)svg/\1pdf/g' projektGalvoDoku_anrechnPandoc.md
```
pandoc -sSf markdown -o\<file\>.pdf \<file\>.md
