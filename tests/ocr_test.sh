echo "Tesseract Predicting..."
python ./scripts/tesseract_predict.py

echo "Calamari Predicting..."
./scripts/calamari_predict.sh

echo "Kraken Predicting..."
./scripts/kraken_predict.sh

echo "Running character accuracy..."
./scripts/ocreval/character_accuracy.sh

echo "Running word accuracy..."
./scripts/ocreval/word_accuracy.sh

echo "Running accuracy by count..."
./scripts/ocreval/accuracy_by_count.sh