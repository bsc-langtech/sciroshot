import csv
import datasets

logger = datasets.logging.get_logger(__name__)

_PATH = "/data/"
_TRAIN_FILE = "01-12-2021_train_mini.csv"
_DEV_FILE   = "01-12-2021_dev_mini.csv"
_TEST_FILE  = "01-12-2021_test_mini.csv"

class magConfig(datasets.BuilderConfig):
    def __init__(self, **kwargs):
        super(magConfig, self).__init__(**kwargs)


class mag(datasets.GeneratorBasedBuilder):
    BUILDER_CONFIGS = [
        magConfig(
            name="MAG",
            version=datasets.Version("1.0.1"),
            description="MAG entailment dataset",
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description="",
            features=datasets.Features(
                {
                    "PaperId":    datasets.Value("string"), #
                    "FieldOfStudy":  datasets.Value("string"),
                    "WikiFieldOfStudy":  datasets.Value("string"),
                    "Abstract": datasets.Value("string"),
                    "labels":   datasets.features.ClassLabel(names=["ENTAILMENT","NEUTRAL"]),
                    "Score": datasets.Value("float32"), #
                }
            ),
            homepage="",
            citation="",
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        urls_to_download = {
            "train": f"{_PATH}{_TRAIN_FILE}",
            "dev": f"{_PATH}{_DEV_FILE}",
            "test": f"{_PATH}{_TEST_FILE}",
        }
        downloaded_files = dl_manager.download_and_extract(urls_to_download)

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": downloaded_files["train"]}),
            datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"filepath": downloaded_files["dev"]}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": downloaded_files["test"]}),
        ]

    def _generate_examples(self, filepath):
        """This function returns the examples in the raw (text) form."""
        logger.info("generating examples from = %s", filepath)
        with open(filepath, encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter="\t", skipinitialspace=True)
            next(csv_reader, None)
            for id_, row in enumerate(csv_reader):
                if len(row) != 6:
                    print(len(row), row)
                    print("filepath:", filepath, "ID:", id_)
                else:
                    PaperId, FieldOfStudy, Abstract, Label, Score, WikiFieldOfStudy = row
                    yield id_, {
                                "PaperId": PaperId, 
                                "FieldOfStudy": FieldOfStudy, 
                                "WikiFieldOfStudy": WikiFieldOfStudy, 
                                "Abstract": Abstract, 
                                "labels": Label, 
                                "Score": Score
                                }

# ValueError: could not convert string to float: 'Score'
