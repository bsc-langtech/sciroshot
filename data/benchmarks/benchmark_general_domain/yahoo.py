# coding=utf-8

import csv
import datasets

PATH_TO_DEV_CSV = "topic/dev.txt"

LABEL_NAMES = {
    0: "society or culture",
    1: "science or mathematics", 
    2: "health", 
    3: "education or reference",
    4: "computers or internet",
    5: "sports",
    6: "business or finance",
    7: "entertainment or music",
    8: "family or relationships",
    9: "politics or government",
}

class YahooAnswers(datasets.GeneratorBasedBuilder):
    def _info(self):
        return datasets.DatasetInfo(
            description="",
            features=datasets.Features(
                {
                    "text":  datasets.Value("string"),
                    "label": datasets.Value("string"),
                }
            ),
            homepage="",
            citation="",
        )

    def _split_generators(self, dl_manager):
        dev_path = dl_manager.download_and_extract(PATH_TO_DEV_CSV)
        return [
            datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"filepath": dev_path})
        ]

    def _generate_examples(self, filepath):
        with open(filepath, encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file, quotechar='"', delimiter="\t", quoting=csv.QUOTE_ALL, skipinitialspace=True)
            for id_, row in enumerate(csv_reader):
                label_id, text = row
                yield id_, {"text": text, "label": LABEL_NAMES[int(label_id)]}
