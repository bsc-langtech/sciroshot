# coding=utf-8

import csv
import datasets

PATH_TO_TEST_CSV = "testSet/scidoc_allenai_mesh.csv"

class ScidocMesh(datasets.GeneratorBasedBuilder):
    def _info(self):
        return datasets.DatasetInfo(
            description="",
            features=datasets.Features(
                {
                    "id":                datasets.Value("string"),
                    "title":             datasets.Value("string"),
                    "abstract":          datasets.Value("string"),
                    "full_text":         datasets.Value("string"),
                    "label":             datasets.Value("string"),
                    "label_description": datasets.Value("string"),
                }
            ),
            homepage="",
            citation="",
        )

    def _split_generators(self, dl_manager):
        test_path = dl_manager.download_and_extract(PATH_TO_TEST_CSV)
        return [datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": test_path})]

    def _generate_examples(self, filepath):
        with open(filepath, encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file, quotechar='"', delimiter=",", quoting=csv.QUOTE_ALL, skipinitialspace=True)
            next(csv_reader) # skip header row
            for id_, row in enumerate(csv_reader):
                uid, title, abstract, label, label_description = row
                title     = title.replace("\n", " ")     # remove EOL characters
                abstract  = abstract.replace("\n", " ")  # remove EOL characters
                full_text = ": ".join((title, abstract)) # concatenate title and abstract
                yield id_, {"id": uid,
                			"title": title,
                			"abstract": abstract,
                			"full_text": full_text, 
                			"label": label,
                			"label_description": label_description,
                			}
