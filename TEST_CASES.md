# Test Cases – Kalkulator Wynagrodzenia Netto

> Przypadki testowe dla testera manualnego.  

---

## TC001 – Obliczenie netto dla umowy o pracę – wartości domyślne

| Pole | Opis |
|------|------|
| **ID** | TC001 |
| **Tytuł** | Obliczenie netto dla umowy o pracę – wartości domyślne |
| **Warunki początkowe** | Aplikacja jest otwarta w przeglądarce |
| **Kroki testowe** | 1. Wpisz kwotę brutto: **8000** <br> 2. Wybierz rodzaj umowy: **Umowa o pracę** <br> 3. Pozostaw wiek: **30** <br> 4. Kliknij przycisk **Oblicz** |
| **Oczekiwany rezultat** | Składki społeczne: 1096,80 PLN, Składka zdrowotna: 621,29 PLN, KUP: 250,00 PLN, Kwota netto: ~5483,53 PLN |

---

## TC002 – Obliczenie netto dla umowy zlecenie ze składkami ZUS

| Pole | Opis |
|------|------|
| **ID** | TC002 |
| **Tytuł** | Obliczenie netto dla umowy zlecenie ze składkami ZUS |
| **Warunki początkowe** | Aplikacja jest otwarta w przeglądarce |
| **Kroki testowe** | 1. Wpisz kwotę brutto: **5000** <br> 2. Wybierz rodzaj umowy: **Umowa zlecenie** <br> 3. Wpisz wiek: **35** <br> 4. Kliknij przycisk **Oblicz** |
| **Oczekiwany rezultat** | Składki społeczne > 0, Składka zdrowotna > 0, KUP = 20% od (brutto - składki społeczne), Kwota netto < 5000 PLN |

---

## TC003 – Umowa zlecenie dla studenta poniżej 26 lat – brak składek ZUS

| Pole | Opis |
|------|------|
| **ID** | TC003 |
| **Tytuł** | Umowa zlecenie dla studenta poniżej 26 lat – brak składek ZUS |
| **Warunki początkowe** | Aplikacja jest otwarta w przeglądarce |
| **Kroki testowe** | 1. Wpisz kwotę brutto: **4000** <br> 2. Wybierz rodzaj umowy: **Umowa zlecenie** <br> 3. Wpisz wiek: **22** <br> 4. Zaznacz checkbox **Jestem studentem** <br> 5. Kliknij przycisk **Oblicz** |
| **Oczekiwany rezultat** | Składki społeczne: **0,00 PLN**, Składka zdrowotna: **0,00 PLN** |

---

## TC004 – Ulga dla młodych (poniżej 26 lat) – PIT = 0

| Pole | Opis |
|------|------|
| **ID** | TC004 |
| **Tytuł** | Ulga dla młodych (poniżej 26 lat) – PIT = 0 |
| **Warunki początkowe** | Aplikacja jest otwarta w przeglądarce |
| **Kroki testowe** | 1. Wpisz kwotę brutto: **6000** <br> 2. Wybierz rodzaj umowy: **Umowa o pracę** <br> 3. Wpisz wiek: **24** <br> 4. Zaznacz checkbox **Ulga dla młodych** <br> 5. Kliknij przycisk **Oblicz** |
| **Oczekiwany rezultat** | Podatek PIT: **0,00 PLN** |

---

## TC005 – Umowa o dzieło – brak składek ZUS i zdrowotnej

| Pole | Opis |
|------|------|
| **ID** | TC005 |
| **Tytuł** | Umowa o dzieło – brak składek ZUS i zdrowotnej |
| **Warunki początkowe** | Aplikacja jest otwarta w przeglądarce |
| **Kroki testowe** | 1. Wpisz kwotę brutto: **7000** <br> 2. Wybierz rodzaj umowy: **Umowa o dzieło** <br> 3. Kliknij przycisk **Oblicz** |
| **Oczekiwany rezultat** | Składki społeczne: **0,00 PLN**, Składka zdrowotna: **0,00 PLN**, KUP: **1400,00 PLN** (20% z 7000) |

---

## TC006 – Umowa o dzieło z 50% KUP 

| Pole | Opis |
|------|------|
| **ID** | TC006 |
| **Tytuł** | Umowa o dzieło z 50% KUP |
| **Warunki początkowe** | Aplikacja jest otwarta w przeglądarce |
| **Kroki testowe** | 1. Wpisz kwotę brutto: **10000** <br> 2. Wybierz rodzaj umowy: **Umowa o dzieło** <br> 3. Zaznacz checkbox **50% KUP** <br> 4. Kliknij przycisk **Oblicz** |
| **Oczekiwany rezultat** | KUP: **5000,00 PLN** (50% z 10000), Podstawa PIT: **5000,00 PLN** |

---

## TC007 – Własna wartość KUP dla umowy o pracę

| Pole | Opis |
|------|------|
| **ID** | TC007 |
| **Tytuł** | Własna wartość KUP dla umowy o pracę |
| **Warunki początkowe** | Aplikacja jest otwarta w przeglądarce |
| **Kroki testowe** | 1. Wpisz kwotę brutto: **9000** <br> 2. Wybierz rodzaj umowy: **Umowa o pracę** <br> 3. Wpisz w polu KUP (stała kwota): **300** <br> 4. Kliknij przycisk **Oblicz** |
| **Oczekiwany rezultat** | KUP: **300,00 PLN** (zamiast domyślnych 250 PLN) |

---

## TC008 – Walidacja – ujemna kwota brutto

| Pole | Opis |
|------|------|
| **ID** | TC008 |
| **Tytuł** | Walidacja – ujemna kwota brutto |
| **Warunki początkowe** | Aplikacja jest otwarta w przeglądarce |
| **Kroki testowe** | 1. Wpisz kwotę brutto: **-1000** <br> 2. Wybierz rodzaj umowy: **Umowa o pracę** <br> 3. Kliknij przycisk **Oblicz** |
| **Oczekiwany rezultat** | Aplikacja wyświetla komunikat o błędzie, obliczenia nie są wykonywane |

---

## TC009 – Walidacja – wiek powyżej 120 lat

| Pole | Opis |
|------|------|
| **ID** | TC009 |
| **Tytuł** | Walidacja – wiek powyżej 120 lat |
| **Warunki początkowe** | Aplikacja jest otwarta w przeglądarce |
| **Kroki testowe** | 1. Wpisz kwotę brutto: **5000** <br> 2. Wybierz rodzaj umowy: **Umowa o pracę** <br> 3. Wpisz wiek: **150** <br> 4. Kliknij przycisk **Oblicz** |
| **Oczekiwany rezultat** | Aplikacja wyświetla komunikat o błędzie walidacji |

---

## TC010 – Sprawdzenie endpointu health check

| Pole | Opis |
|------|------|
| **ID** | TC010 |
| **Tytuł** | Sprawdzenie endpointu health check |
| **Warunki początkowe** | Aplikacja jest uruchomiona na serwerze |
| **Kroki testowe** | 1. Otwórz w przeglądarce adres: **/health** |
| **Oczekiwany rezultat** | Strona wyświetla JSON: `{"status": "ok"}` |

---
