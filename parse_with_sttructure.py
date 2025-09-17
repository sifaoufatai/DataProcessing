import re
import json

def extract_san_sequences(file_path):
    """
    Extrait les SAN et leurs séquences depuis un fichier Markdown.
    Garde le texte, les images et les formules LaTeX.
    """
    sequences = []
    current_sa = ""
    current_sequence_name = ""
    current_sequence_content = ""
    sequences_in_sa = []

    # Regex pour détecter un SAN
    san_pattern = re.compile(r"^##\s*SAN", re.IGNORECASE)
    # Regex pour détecter une séquence avec LaTeX possible
    sequence_pattern = re.compile(r"^##?\s*Séquence\s*(.*?)\s*\d+\s*:\s*(.*)", re.IGNORECASE)

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if not line:
            continue



        # Détecter un nouveau SAN
        if san_pattern.match(line):
            current_sa = line.replace("SAN", "SITUATION D'APPRENTISSAGE")
            current_sequence_name = ""
            current_sequence_content = ""
            sequences_in_sa = []
            continue

        # Détecter une séquence
        match_seq = sequence_pattern.match(line)
        if match_seq:
            # Sauvegarder la séquence précédente
            if current_sequence_name:
                sequences.append({
                    "sequence_name": current_sequence_name,
                    "sequence_content": current_sequence_content.strip(),
                    "sa": current_sa,
                    "sequences_in_sa": sequences_in_sa.copy()
                })
            current_sequence_name = line
            current_sequence_content = ""
            sequences_in_sa.append(current_sequence_name)
            continue

        # Ajouter le contenu intermédiaire (texte, images, LaTeX)
        if current_sequence_name:
            current_sequence_content += line + "\n"

    # Ajouter la dernière séquence
    if current_sequence_name:
        sequences.append({
            "sequence_name": current_sequence_name,
            "sequence_content": current_sequence_content.strip(),
            "sa": current_sa,
            "sequences_in_sa": sequences_in_sa.copy()
        })

    # Écrire le JSON final
    with open("output_san.json", "w", encoding="utf-8") as f:
        json.dump(sequences, f, ensure_ascii=False, indent=2)

    print("✅ Extraction terminée. Fichier 'output_san.json' généré.")


# Exemple d'utilisation
extract_san_sequences("6e-azo-judicael.md")
