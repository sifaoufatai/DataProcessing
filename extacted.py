import json
from markitdown import MarkItDown
import os

from argparse import ArgumentParser
def extract_sequence(pdf_file, output_dir):
    md = MarkItDown()
    result = md.convert(pdf_file)
    text = result.text_content
    lines = text.split('\n')

    sequences = []
    sequence_name = None
    sequence = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.lower().startswith('séquence n°'):
            if sequence_name:
                sequences.append(
                    {'name': sequence_name, 'content': '\n'.join(sequence)})
                sequence = []
            sequence_name = line.strip()
            continue
        if sequence_name:
            sequence.append(line)
    if sequence_name and sequence:
        sequences.append(
            {'name': sequence_name, 'content': '\n'.join(sequence)})

    json_file = os.path.splitext(os.path.basename(pdf_file))[0] + '.json'
    json_file = os.path.join(output_dir, json_file)
    with open(json_file, 'w') as f:
        json.dump(sequences, f, indent=4)
        print(f"Sequences extraites et enregistrées dans {json_file}")

    return sequences


if __name__ == '__main__':
    parser = ArgumentParser(description="Extraction des séquences depuis des fichiers PDF")
    parser.add_argument('--pdf_dir', type=str, required=True, help="Répertoire contenant les fichiers PDF")
    parser.add_argument('--output_dir', type=str, required=True, help="Répertoire de sortie pour les fichiers JSON")
    args = parser.parse_args()

    for file in os.listdir(args.pdf_dir):
        if file.endswith(".pdf"):
             extract_sequence(os.path.join(args.pdf_dir, file), args.output_dir)
