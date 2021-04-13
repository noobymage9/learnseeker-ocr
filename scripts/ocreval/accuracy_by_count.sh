correct_files=./assets/recognitions/truth/*
ngram $correct_files > ngram
ngram=./ngram

tesseract_character_accuracy_average=./reports/tesseract/character_accuracy/average.txt
tesseract_output=./reports/tesseract/accuracy_by_frequency.txt
groupacc $ngram $tesseract_character_accuracy_average temp
(head -n +1 temp && tail -n+2 temp | sort -n -r -k 1 temp) | head -n -2 > $tesseract_output
rm temp

calamari_0_character_accuracy_average=./reports/calamari_0/character_accuracy/average.txt
calamari_0_output=./reports/calamari_0/accuracy_by_frequency.txt
groupacc $ngram $calamari_0_character_accuracy_average temp
(head -n +1 temp && tail -n+2 temp | sort -n -r -k 1 temp) | head -n -2 > $calamari_0_output
rm temp

calamari_1_character_accuracy_average=./reports/calamari_1/character_accuracy/average.txt
calamari_1_output=./reports/calamari_1/accuracy_by_frequency.txt
groupacc $ngram $calamari_1_character_accuracy_average temp
(head -n +1 temp && tail -n+2 temp | sort -n -r -k 1 temp) | head -n -2 > $calamari_1_output
rm temp

calamari_2_character_accuracy_average=./reports/calamari_2/character_accuracy/average.txt
calamari_2_output=./reports/calamari_2/accuracy_by_frequency.txt
groupacc $ngram $calamari_2_character_accuracy_average temp
(head -n +1 temp && tail -n+2 temp | sort -n -r -k 1 temp) | head -n -2 > $calamari_2_output
rm temp

calamari_3_character_accuracy_average=./reports/calamari_3/character_accuracy/average.txt
calamari_3_output=./reports/calamari_3/accuracy_by_frequency.txt
groupacc $ngram $calamari_3_character_accuracy_average temp
(head -n +1 temp && tail -n+2 temp | sort -n -r -k 1 temp) | head -n -2 > $calamari_3_output
rm temp

calamari_4_character_accuracy_average=./reports/calamari_4/character_accuracy/average.txt
calamari_4_output=./reports/calamari_4/accuracy_by_frequency.txt
groupacc $ngram $calamari_4_character_accuracy_average temp
(head -n +1 temp && tail -n+2 temp | sort -n -r -k 1 temp) | head -n -2 > $calamari_4_output
rm temp

kraken_character_accuracy_average=./reports/kraken/character_accuracy/average.txt
kraken_output=./reports/kraken/accuracy_by_frequency.txt
groupacc $ngram $kraken_character_accuracy_average temp
(head -n +1 temp && tail -n+2 temp | sort -n -r -k 1 temp) | head -n -2 > $kraken_output
rm temp

rm ngram