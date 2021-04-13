files=./assets/phrases/*
mkdir -p ./assets/recognitions/kraken/

for f in $files
do
  strings=(${f//// })
  uuid_png=(${strings[3]//./ })
  uuid=${uuid_png[0]}
  output=./assets/recognitions/kraken/$uuid.txt
  echo "Recognising file $f"
  kraken -i $f $output binarize segment ocr -m ./assets/en_best.mlmodel
done