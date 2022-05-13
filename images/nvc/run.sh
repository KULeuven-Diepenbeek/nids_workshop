#/bin/bash

bash /home/jvliegen/bin/extractImages.sh NIDSworkshop_images.drawio.pdf 01_network.png 01_encaps.png 11_flow.png 11_outline.png 11_outline_backwards.png 21_hashtable.png NN_network.png

for i in *.png.pdf
do
    NEWNAME=$(echo $i | cut -f 1 -d '.')
    convert $i $NEWNAME.png
    rm $i
    mv $NEWNAME.png ..
done