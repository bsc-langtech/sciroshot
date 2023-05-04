#t coding=utf-8

import csv
import datasets

PATH_TO_TEST_CSV = "situation/test.txt"

class SituationHF(datasets.GeneratorBasedBuilder):
    def _info(self):
        return datasets.DatasetInfo(
            description="",
            features=datasets.Features(
                {
                    "text":                             datasets.Value("string"),
                    "label":                            datasets.Value("string"),
                    "food supply":                      datasets.Value("bool"),
                    "infrastructure":                   datasets.Value("bool"),
                    "medical assistance":               datasets.Value("bool"),
                    "search or rescue":                 datasets.Value("bool"),
                    "shelter":                          datasets.Value("bool"),
                    "utilities, energy or sanitation": datasets.Value("bool"),
                    "water supply":                     datasets.Value("bool"),
                    "evacuation":                       datasets.Value("bool"),
                    "regime change":                    datasets.Value("bool"),
                    "terrorism":                        datasets.Value("bool"),
                    "crime violence":                   datasets.Value("bool"),
                    "none":                             datasets.Value("bool"),
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
                label, text = row
                yield id_, {
                        "text": text,
                        "label": label,
                        "food supply": "food" in label,
                        "infrastructure": "infra" in label,
                        "medical assistance": "med" in label,
                        "search or rescue": "search" in label,
                        "shelter": "shelter" in label,
                        "utilities, energy or sanitation": "utils" in label,
                        "water supply": "water" in label,
                        "evacuation": "evac" in label,
                        "regime change": "regimechange" in label,
                        "terrorism": "terrorism" in label,
                        "crime violence": "crimeviolence" in label,
                        "none": "out-of-domain" in label,
                    }


