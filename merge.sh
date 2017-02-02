#!/bin/bash
[[ -e "out.mmd" ]] && mv out.mmd /media/data/Trash

CH=( $(ls chapters/*.mmd | sort -n) )

for k in "${CH[@]}"; do
    cat $k >> out.mmd
done

#find ./chapters/ -type f -exec sh -c "cat {} >> out.mmd" \;

