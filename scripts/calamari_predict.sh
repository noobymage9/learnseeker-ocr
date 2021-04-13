mkdir -p ./assets/recognitions/calamari_0/
mkdir -p ./assets/recognitions/calamari_1/
mkdir -p ./assets/recognitions/calamari_2/
mkdir -p ./assets/recognitions/calamari_3/
mkdir -p ./assets/recognitions/calamari_4/

calamari-predict --checkpoint ./assets/calamari_models/0.ckpt --files ./assets/phrases/* --output_dir ./assets/recognitions/calamari_0/
calamari-predict --checkpoint ./assets/calamari_models/1.ckpt --files ./assets/phrases/* --output_dir ./assets/recognitions/calamari_1/
calamari-predict --checkpoint ./assets/calamari_models/2.ckpt --files ./assets/phrases/* --output_dir ./assets/recognitions/calamari_2/
calamari-predict --checkpoint ./assets/calamari_models/3.ckpt --files ./assets/phrases/* --output_dir ./assets/recognitions/calamari_3/
calamari-predict --checkpoint ./assets/calamari_models/4.ckpt --files ./assets/phrases/* --output_dir ./assets/recognitions/calamari_4/