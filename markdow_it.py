import re
import json

def extract_san_sequences_latex(file):
    list_sequence = []
    sa = ""
    sequence_name = ""
    sequence_content = ""
    list_sequence_in_sa = []

    # Détecte les SAN
    san_pattern = re.compile(r"^##\s*SAN")

    # Détecte les séquences du type :
    # ## Séquence $n^{\circ}$ 2 : Cône de révolution
    sequence_pattern = re.compile(r"^##\s*Séquence\s*(\$\S+\$|\S+)?\s*\d+\s*:\s*(.*)")

    with open(file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if not line:
            continue


        # Détecter un nouveau SAN
        if san_pattern.match(line):
            sa = line.replace("SAN", "SITUATION D'APPRENTISSAGE")
            sequence_name = ""
            sequence_content = ""
            list_sequence_in_sa = []
            continue

        # Détecter une séquence
        match_seq = sequence_pattern.match(line)
        if match_seq:
            # Sauvegarder la séquence précédente
            if sequence_name:
                list_sequence.append({
                    "sequence_name": sequence_name,
                    "sequence_content": sequence_content.strip(),
                    "sa": sa,
                    "list_sequence_in_sa": list_sequence_in_sa.copy()
                })
            # Nouvelle séquence
            sequence_name = line
            sequence_content = ""
            list_sequence_in_sa.append(sequence_name)
            continue

        # Ajouter le contenu intermédiaire (texte, images, LaTeX)
        if sequence_name:
            sequence_content += line + "\n"
        print(sequence_content)
        
    # Ajouter la dernière séquence
    if sequence_name:
        list_sequence.append({
            "sequence_name": sequence_name,
            "sequence_content": sequence_content.strip(),
            "sa": sa,
            "list_sequence_in_sa": list_sequence_in_sa.copy()
        })

    # Écriture JSON final
    with open("output_san_latex.json", "w", encoding="utf-8") as f:
        json.dump(list_sequence, f, ensure_ascii=False, indent=2)

    print("✅ Extraction terminée. Fichier 'output_san_latex.json' généré.")


# Exemple d'utilisation
extract_san_sequences_latex("6e-azo-judicael.md")
