# Paper: Evaluating OpenAI’s Whisper and Human Transcription Accuracy on Low-Pass Filtered Speech at 2 kHz
# Linda Mazzone, Fortesa Zeqiri
# Levenstein Distance and Error Rate Human Transcription

import numpy as np
import string
import re



def levenshtein_dynamic(S1: list, S2: list) -> str:
    """Return the Levenshtein distance between two sentences using dynamic-programming."""
    # Initialize table
    Lenght_S1 = len(S1)
    Lenght_S2 = len(S2)

    # Initializing the cost matrix
    cost_matrix = np.zeros((Lenght_S1 + 1, Lenght_S2 + 1), dtype=int)

    # Initializing the first row and column of the cost matrix
    for i in range(Lenght_S1 + 1):
        cost_matrix[i, 0] = i
    for j in range(Lenght_S2 + 1):
        cost_matrix[0, j] = j
    # Fill table
    for i in range(1, Lenght_S1 + 1):
        for j in range(1, Lenght_S2 + 1):
            if S2[j - 1] == S1[i - 1]:
                cost_matrix[i][j] = cost_matrix[i - 1][j - 1]  # Keep
            else:
                cost_matrix[i][j] = 1 + min(
                    cost_matrix[i - 1][j],  # Delete
                    cost_matrix[i][j - 1],  # Insert
                    cost_matrix[i - 1][j - 1],  # Replace
                )
    wer = cost_matrix[-1][-1]/Lenght_S2
    # Solution in the bottom right corner

    return f"Cost Matrix:\n {cost_matrix[1:][1:]} \n Global cost: {cost_matrix[-1][-1]} \n Word Error Rate (normalized Levenshtein distance): {wer} "

def remove_punctuation(text):
    translator = str.maketrans('', '', string.punctuation)
    return text.translate(translator)


def process_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        # Read the file's content
        content = file.read()
        stripped_content_old = remove_punctuation(content)
        x = re.sub(r'[ßẞ]', "ss", stripped_content_old)
        stripped_content = re.sub(r'[^a-zA-ZÄÖÜäöü\s]', "", x)


        # Split the content into words
        words_list = stripped_content.upper().split()
        return words_list


def process_golden(filename_golden):
    with open(filename_golden, 'r', encoding='utf-8') as file:
        # Read the file's content
        content = file.read()
        stripped_content_old = remove_punctuation(content)
        x = re.sub(r'[ßẞ]', "ss", stripped_content_old)
        stripped_content = re.sub(r'[^a-zA-ZÄÖÜäöü\s]', "", x)

        # Split the content into words
        words_list_golden = stripped_content.upper().split()
        return words_list_golden


paragraph1_human = process_file("paragraph1_human.txt")
paragraph2_human = process_file("paragraph2_human.txt")
paragraph3_human = process_file("paragraph3_human.txt")

paragraph1_golden = process_golden("golden_standard_paragraph_1.txt")
paragraph2_golden = process_golden("golden_standard_paragraph_2.txt")
paragraph3_golden = process_golden("golden_standard_paragraph_3.txt")

leven_1 = levenshtein_dynamic(paragraph1_golden, paragraph1_human)
leven_2 = levenshtein_dynamic(paragraph2_golden, paragraph2_human)
leven_3 = levenshtein_dynamic(paragraph3_golden, paragraph3_human)

print("\n", "Paragraph 1:", "\n", leven_1)
print("\n", "Paragraph 2:", "\n", leven_2)
print("\n", "Paragraph 3:", "\n", leven_3)


print(paragraph1_human)
print(paragraph2_human)
print(paragraph3_human)



