files=./assets/phrases/*
mkdir -p ./reports/tesseract/character_accuracy/raw/
mkdir -p ./reports/calamari_0/character_accuracy/raw/
mkdir -p ./reports/calamari_1/character_accuracy/raw/
mkdir -p ./reports/calamari_2/character_accuracy/raw/
mkdir -p ./reports/calamari_3/character_accuracy/raw/
mkdir -p ./reports/calamari_4/character_accuracy/raw/
mkdir -p ./reports/kraken/character_accuracy/raw/

# Character character_accuracy
for f in $files
do
  strings=(${f//// })
  uuid_png=(${strings[3]//./ })
  uuid=${uuid_png[0]}
  correct_file=./assets/recognitions/truth/$uuid.txt

  tesseract_acc_output=./reports/tesseract/character_accuracy/raw/$uuid.txt
  tesseract_generated_file=./assets/recognitions/tesseract/$uuid.txt
  accuracy $correct_file $tesseract_generated_file $tesseract_acc_output

  calamari_0_acc_output=./reports/calamari_0/character_accuracy/raw/$uuid.txt
  calamari_0_generated_file=./assets/recognitions/calamari_0/$uuid.pred.txt
  accuracy $correct_file $calamari_0_generated_file $calamari_0_acc_output

  calamari_1_acc_output=./reports/calamari_1/character_accuracy/raw/$uuid.txt
  calamari_1_generated_file=./assets/recognitions/calamari_1/$uuid.pred.txt
  accuracy $correct_file $calamari_1_generated_file $calamari_1_acc_output

  calamari_2_acc_output=./reports/calamari_2/character_accuracy/raw/$uuid.txt
  calamari_2_generated_file=./assets/recognitions/calamari_2/$uuid.pred.txt
  accuracy $correct_file $calamari_2_generated_file $calamari_2_acc_output

  calamari_3_acc_output=./reports/calamari_3/character_accuracy/raw/$uuid.txt
  calamari_3_generated_file=./assets/recognitions/calamari_3/$uuid.pred.txt
  accuracy $correct_file $calamari_3_generated_file $calamari_3_acc_output

  mkdir -p ./reports/calamari_4/character_accuracy/raw/
  calamari_4_acc_output=./reports/calamari_4/character_accuracy/raw/$uuid.txt
  calamari_4_generated_file=./assets/recognitions/calamari_4/$uuid.pred.txt
  accuracy $correct_file $calamari_4_generated_file $calamari_4_acc_output

  mkdir -p ./reports/kraken/character_accuracy/raw/
  kraken_acc_output=./reports/kraken/character_accuracy/raw/$uuid.txt
  kraken_generated_file=./assets/recognitions/kraken/$uuid.txt
  accuracy $correct_file $kraken_generated_file $kraken_acc_output
done

tesseract_acc_files=./reports/tesseract/character_accuracy/raw/*
tesseract_acc_avg_output=./reports/tesseract/character_accuracy/average.txt
accsum $tesseract_acc_files > $tesseract_acc_avg_output

calamari_0_acc_files=./reports/calamari_0/character_accuracy/raw/*
calamari_0_acc_avg_output=./reports/calamari_0/character_accuracy/average.txt
accsum $calamari_0_acc_files > $calamari_0_acc_avg_output

calamari_1_acc_files=./reports/calamari_1/character_accuracy/raw/*
calamari_1_acc_avg_output=./reports/calamari_1/character_accuracy/average.txt
accsum $calamari_1_acc_files > $calamari_1_acc_avg_output

calamari_2_acc_files=./reports/calamari_2/character_accuracy/raw/*
calamari_2_acc_avg_output=./reports/calamari_2/character_accuracy/average.txt
accsum $calamari_2_acc_files > $calamari_2_acc_avg_output

calamari_3_acc_files=./reports/calamari_3/character_accuracy/raw/*
calamari_3_acc_avg_output=./reports/calamari_3/character_accuracy/average.txt
accsum $calamari_3_acc_files > $calamari_3_acc_avg_output

calamari_4_acc_files=./reports/calamari_4/character_accuracy/raw/*
calamari_4_acc_avg_output=./reports/calamari_4/character_accuracy/average.txt
accsum $calamari_4_acc_files > $calamari_4_acc_avg_output

kraken_acc_files=./reports/kraken/character_accuracy/raw/*
kraken_acc_avg_output=./reports/kraken/character_accuracy/average.txt
accsum $kraken_acc_files > $kraken_acc_avg_output