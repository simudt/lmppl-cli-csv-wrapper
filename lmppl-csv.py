import csv
import lmppl
import argparse
import urllib.request

from typing import List
from configparser import ConfigParser


def load_text_from_csv(csv_file: str, csv_sentence_header: str, delimiter: str = ",") -> List[str]:
    """
    Load text from a CSV file.

    Args:
        csv_file (str): Path to the CSV file.
        csv_sentence_header (str): Name of the column containing the sentences in the CSV file.
        delimiter (str, optional): Delimiter used in the CSV file. Defaults to ",".

    Returns:
        list: A list of sentences loaded from the CSV file.
    """
    text: List[str] = []
    with open(csv_file, "r", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=delimiter)
        header = next(reader)
        if csv_sentence_header not in header:
            raise ValueError(
                f"The '{csv_sentence_header}' column does not exist in the CSV file. Please refactor your {csv_file} to calculate PPL. '{csv_sentence_header}' header needed."
            )
        csv_requested_header_index = header.index(csv_sentence_header)
        for row in reader:
            text.append(row[csv_requested_header_index])
    return text


def initialize_language_model(model_name: str) -> lmppl.LM:
    """
    Initialize the language model.

    Args:
        model_name (str): Name of the language model.

    Returns:
        lmppl.LM: An instance of the language model.

    Raises:
        ImportError: If the LM class import fails.
        Exception: If there is an error initializing the language model.
    """
    try:
        scorer = lmppl.LM(model_name)
        return scorer
    except ImportError:
        raise ImportError("Failed to import the LM class. Make sure 'lmppl' is correctly installed.")
    except Exception as e:
        raise Exception(f"Failed to initialize the language model: {str(e)}")


def calculate_perplexity(scorer: lmppl.LM, text: List[str], batch_size: int) -> List[float]:
    """
    Calculate perplexity for a list of sentences.

    Args:
        scorer (lmppl.LM): The language model scorer.
        text (list): A list of sentences.
        batch_size (int): Batch size for calculating perplexity.

    Returns:
        list: A list of perplexities for the input sentences.
    """
    ppl: List[float] = []
    for i in range(0, len(text), batch_size):
        batch_text = text[i : i + batch_size]
        batch_ppl = scorer.get_perplexity(batch_text)
        ppl.extend(batch_ppl)
    return ppl


def append_perplexity_to_csv(csv_file: str, text: List[str], perplexities: List[float]) -> None:
    """
    Append perplexities to a CSV file.

    Args:
        csv_file (str): Path to the CSV file.
        text (list): A list of sentences.
        perplexities (list): A list of perplexities corresponding to the sentences.
    """
    with open(csv_file, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    with open(csv_file, "w", encoding="utf-8", newline="") as file:
        fieldnames = reader.fieldnames + ["Perplexity"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        print("\nStarting to calculate perplexity by row...")
        for index, (row, sentence, perplexity) in enumerate(zip(rows, text, perplexities)):
            row["Perplexity"] = perplexity
            writer.writerow(row)
            print(f"\nIndex ID: {index}\nSentence: {sentence}\nPerplexity: {perplexity}")


def calculate_average_perplexity(perplexities: List[float]) -> float:
    """
    Calculate the average perplexity.

    Args:
        perplexities (list): A list of perplexities.

    Returns:
        float: The average perplexity.
    """
    return sum(perplexities) / len(perplexities)


def main(config_file: str) -> None:
    """
    Main entry point of the script.

    Args:
        config_file (str): Path to the config INI file.
    """
    config = ConfigParser()
    config.read(config_file)

    csv_file = config.get("Config", "csv_file")
    csv_header = config.get("Config", "csv_sentence_header")
    model_name = config.get("Config", "model_name")
    batch_size = config.getint("Config", "batch_size")
    delimiter = config.get("Config", "delimiter", fallback=",")

    text = load_text_from_csv(csv_file, csv_sentence_header=csv_header, delimiter=delimiter)

    scorer = initialize_language_model(model_name)
    perplexities = calculate_perplexity(scorer, text, batch_size)
    append_perplexity_to_csv(csv_file, text, perplexities)
    average_perplexity = calculate_average_perplexity(perplexities)
    print("\n\nAverage Perplexity of the data input:", average_perplexity)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("config_file", help="Path to the config INI file")
    parser.add_argument("--delimiter", help="Delimiter used in the CSV file", default=",")
    args = parser.parse_args()

    main(args.config_file)
