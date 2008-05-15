#!/bin/bash

for item in `ls in/*.tar.bz2`; do
	cp $item . && \

	item=${item#"in/"} && \
	tar -xjvf $item && \

	item=${item%".tar.bz2"} && \

	ifo=`ls $item/*.ifo` && \
	dict_dz=`ls $item/*.dict.dz` && \
	dict_gz=${dict_dz%".dz"}".gz" && \

	mv $dict_dz $dict_gz && \

	gunzip -v $dict_gz && \

	makedict -o dummy -i stardict $ifo | ./dummy2lightlang.pl -s en --info $ifo > $item"."result && \

	echo "$item: --- processed ---"
done
