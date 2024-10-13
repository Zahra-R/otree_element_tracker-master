
# Bereinigter Datensatz
# Daten einlesen 
 
tracking_seperate <- read_delim("/Users/ausleihe/Desktop/daten/14.10.2024/tracking_demo_2024-10-13.csv", delim = ",") %>% na.omit()
dim(tracking_seperate)

# Variablen umbenennen
tracking_seperate <- tracking_seperate %>%
  rename(
    participant.code = participant_code,
    round.number = round_number,
    participant.id = id_in_group
  )

# Hinzufügen der Variable sustainable.choice
tracking_seperate <- tracking_seperate %>%
  left_join(df_cleaned %>% select(participant.code, round.number, sustainable.choice),
            by = c("participant.code", "round.number"))

# Hinzufügen einer neuen Variablen-Kombination aus element_id und attributeType
tracking_seperate <- tracking_seperate %>%
  mutate(
    # Extrahiere den Buchstaben (A oder B) aus element_id
    letter = case_when(
      str_detect(element_id, "A") ~ "A",
      str_detect(element_id, "B") ~ "B",
      TRUE ~ NA_character_
    ),
    # Ersetze attributeType durch kurze Namen und entferne Leerzeichen
    attribute_short = case_when(
      attributeType == "Preis" ~ "preis",
      attributeType == "CO2e/ kg" ~ "carbon",   
      attributeType == "Protein" ~ "protein",
      TRUE ~ str_replace_all(attributeType, " ", "") 
    )
  ) %>%
  # Kombiniere die beiden Variablen
  mutate(combined_var = paste0(letter, "_", attribute_short)) %>%
  # Entferne die nicht mehr benötigten Variablen
  select(-letter, -attribute_short)

# Anzahl Probanden
anzahl_probanden <- tracking_seperate %>% 
  pull(participant.code) %>% 
  n_distinct()
print(anzahl_probanden)
# 399

#################################################################################################################################

# Behalte nur Teilnehmer, die in beiden Datensätzen vorhanden sind
df_common <- df_cleaned %>%
  inner_join(tracking_seperate, by = "participant.code")
print(n_distinct(df_common$participant.code))
# 358

#################################################################################################################################

# Hinzufügen von treatment.group
df_cleaned_unique <- df_cleaned %>%
  select(participant.code, treatment.group) %>%
  distinct()

tracking_seperate <- tracking_seperate %>%
  left_join(df_cleaned_unique, by = "participant.code")

## Struktur des Datensatzes überprüfen
str(tracking_seperate)

# Daten exportieren
write.csv2(tracking_seperate, "/Users/ausleihe/Desktop/daten/14.10.2024/df_tracking_cleaned.csv", row.names = FALSE)

