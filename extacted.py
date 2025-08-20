import json
from markitdown import MarkItDown


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

    json_file = pdf_file.replace('.pdf', '.json')
    json_file = os.path.join(output_dir, json_file)
    with open(json_file, 'w') as f:
        json.dump(sequences, f, indent=4)

    return sequences

import os
if __name__ == '__main__':
    dir ="/home/INT/idrissou.f/PycharmProjects/RagProject/Extractor/pdf"
    for file in os.listdir(dir):
        if file.endswith(".pdf"):
            extract_sequence(os.path.join(dir, file), "output_dir")
