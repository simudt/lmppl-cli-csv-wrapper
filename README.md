# LMPPL CLI CSV Wrapper

A tiny CLI wrapper around [lmppl](https://github.com/asahi417/lmppl) for Pre-Trained Language Models Perplexity Calculation for CSV files. Please edit your config.ini file according to your needs.

For larger CSV files, it's highly recommended to have a NVIDIA GPU hardware unless processing going to be significantly slower due to the increased computational requirements.

Prompt examples are taken from [fka/awesome-chatgpt-prompts](https://huggingface.co/datasets/fka/awesome-chatgpt-prompts)

## Google Colab Usage

Clone the repository:

```bash
git clone https://github.com/simuark/lmppl-cli-csv-wrapper
```

Modify the _config.ini_ file according to your needs:

```yaml
[Config]
csv_file = /content/data/prompts.csv
csv_sentence_header = sentence
model_name = gpt2
batch_size = 8
delimiter = ,
```
