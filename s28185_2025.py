import matplotlib.pyplot as plt  # import biblioteki do rysowania wykresów
import random # import biblioteki do generowania liczb losowych


def generate_dna_sequence(length):
    return ''.join(random.choices('ACGT', k=length)) # zwraca ciąg składający się z liter A, T, C lub G o podanej długości


def insert_name(sequence, name):
    pos = random.randint(0, len(sequence)) # generuje losowy indeks 
    return sequence[:pos] + name + sequence[pos:] # wstawia podane imię w podaną sekwencję od wygenerowanego indeksu


def calculate_statistics(sequence):
    total = len(sequence) # długość sekwencji
    stats = {nt: (sequence.count(nt) / total) * 100 for nt in 'ACGT'} # procentowy udział nukleotydów w sekwencji
    cg = stats['C'] + stats['G'] # suma procentowych udziałów nukleotydów C i G
    return stats, cg # zwraca statystyki


def save_fasta(id_seq, description, sequence_with_name):
    filename = f"{id_seq}.fasta" # nazwa pliku
    with open(filename, 'w') as f:
        f.write(f">{id_seq} {description}\n") # zapisuje id sekwencji i opis do pliku
        # ORIGINAL:
        # f.write(sequence_with_name + '\n')
        # MODIFIED formatowanie FASTA — linie po 60 znaków
        for i in range(0, len(sequence_with_name), 60): # dzielenie sekwencji na linie po 60 znaków
            f.write(sequence_with_name[i:i+60] + '\n') # zapisuje sekwencje do pliku
        
    return filename # zwraca nazwę pliku


# ORIGINAL:
# length = int(input("Podaj długość sekwencji: "))
# MODIFIED (obsługa błędów wejściowych — zabezpiecza przed podaniem nieprawidłowych danych):
while True:
    try:
        length = int(input("Podaj długość sekwencji: ")) # długość sekwencji wczytywana od użytkownika
        if length <= 0: # sprawdzenie czy długość jest większa od zera
            print("Długość musi być większa od zera.") # informacja o błędzie
            continue # ponowna próba
        break # poprawna wartość wychodzi z pętli
    except ValueError: # jeśli użytkownik poda coś, co nie jest liczbą
        print("Proszę podać liczbę całkowitą.") # informacja o błędzie

id_seq = input("Podaj ID sekwencji: ") # ID sekwencji wczytywane od uzytkownika
description = input("Podaj opis sekwencji: ") # opis sekwencji wczytywany od użytkownika
name = input("Podaj imię: ") # imię wczytywane od uzytkownika

dna_sequence = generate_dna_sequence(length) # generowanie sekwencji
sequence_with_name = insert_name(dna_sequence, name) # dodanie imienia do sekwencji w losownym miejscu

file_name = save_fasta(id_seq, description, sequence_with_name) # zapis do pliku i otrzymanie nazwy pliku
print(f"Sekwencja została zapisana do pliku {file_name}") # informacja o zapisaniu sekwencji do pliku

stats, cg_ratio = calculate_statistics(dna_sequence) # otrzymanie statystyk

print("Statystyki sekwencji:")
for nt in 'ACGT': # iterowanie po nukleotydach
    print(f"{nt}: {stats[nt]:.1f}%") # wyświetlenie statystyk dla danego nukleotydu
print(f"%CG: {cg_ratio:.1f}") # wyświetlenie sattystyk dla udziału nukleotydów CG

# MODIFIED dodano wykres słupkowy:

labels = list(stats.keys())
values = [stats[nt] for nt in labels]

plt.figure(figsize=(6, 4)) # etykiety słupków (nukleotydy)
plt.bar(labels, values, color=['blue', 'green', 'orange', 'red']) # wykres słupkowy z kolorami
plt.title('Zawartość nukleotydów (%)') # tytuł wykresu
plt.ylabel('Procent') # nazwa osi y
plt.ylim(0, 100) # zakres osi y
plt.grid(axis='y', linestyle='--', alpha=0.7) # dodanie siatki poziomej

# Dodanie wartości nad słupkami
for i, v in enumerate(values):
    plt.text(i, v + 1, f"{v:.1f}%", ha='center') # wartości nad słupkami

plt.tight_layout() # automatyczne dopasowanie układu
plt.show() # wyświetlenie wykresu
