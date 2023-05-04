# coding=utf-8

import csv
import datasets

PATH_TO_TEST_CSV = "emotion/test.txt"

LABEL_NAMES = {
    "joy"     : "joyful", 
    "fear"    : "afraid", 
    "anger"   : "angry",
    "sadness" : "sad",
    "surprise": "surprised", 
    "love"    : "love", 
    "disgust" : "disgusted", 
    "shame"   : "ashamed", 
    "guilt"   : "guilty", 
    "none"    : "nothing",
}

class EmotionHF(datasets.GeneratorBasedBuilder):

    def _info(self):
        return datasets.DatasetInfo(
            description="",
            features=datasets.Features(
                {
                    "text":  datasets.Value("string"),
                    "label": datasets.Value("string"),
                    "type":  datasets.Value("string"),
                }
            ),
            homepage="",
            citation="",
        )

    def _split_generators(self, dl_manager):
        test_path = dl_manager.download_and_extract(PATH_TO_TEST_CSV)
        return [
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": test_path}),
        ]

    def _generate_examples(self, filepath):
        with open(filepath, encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file, quotechar='"', delimiter="\t", quoting=csv.QUOTE_ALL, skipinitialspace=True)
            for id_, row in enumerate(csv_reader):
                label, type_, text = row
                if label =="noemo":
                    label = "none"
                yield id_, {"text": text, "label": label, "type": type_}
#                 yield id_, {"text": text, "label": LABEL_NAMES[label], "type": type_}
