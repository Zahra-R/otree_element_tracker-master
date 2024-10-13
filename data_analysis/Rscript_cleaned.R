install.packages('tidyverse')
install.packages("psych")       
install.packages("corrplot")    
install.packages("lme4")  
install.packages('emmeans')
library(tidyverse)              
library(psych)
library(corrplot)
library(lme4)
library(readr)
library(magrittr)
library(tidyr)
library(dplyr)
library(ggplot2)
library(emmeans)


#################################################################################################################################


# Bereinigter Datensatz
# Daten einlesen 

df_cleaned <- read_delim("/Users/ausleihe/Desktop/daten/14.10.2024/all_apps_wide_2024-10-13.csv", delim = ",")

# Umwandlung in Long-Format
df_cleaned <- df_cleaned %>%
  pivot_longer(
    cols = starts_with("tracking_demo.") | 
      starts_with("memory_task.") | 
      starts_with("NEPR_scale.") | 
      starts_with("demographics.") | 
      starts_with("num_"),  
    names_to = c("round", ".value"),
    names_pattern = "(\\d+)\\.(.*)",
    values_transform = list(.value = as.character)
  )

# Umwandlung von 'round' in numerisch
df_cleaned <- df_cleaned %>%
  mutate(round = as.numeric(round))

# Entfernen von Duplikaten bei nicht-wiederholten Variablen
non_repeating_vars <- df_cleaned %>%
  select(participant.code, 
         participant.orderStimuli, 
         participant.comprehensionCheck, 
         participant.comprehensionCheck2) %>%
  distinct()

# Zusammenführen der nicht-wiederholenden Variablen
df_cleaned <- df_cleaned %>%
  left_join(non_repeating_vars, by = "participant.code")

# Entfernen von NA-Werten in 'player.treatment'
df_cleaned <- df_cleaned %>%
  filter(!is.na(player.treatment))

# Unnötige Variablen entfernen
df_cleaned <- df_cleaned %>%
  select(-participant._current_app_name, -participant._current_page_name, -participant.time_started_utc, -player.role, -player.payoff, -group.id_in_subsession, -subsession.round_number, -session.config.name, -introduction.1.player.comprehension1, -introduction.1.player.comprehension2, -participant.comprehensionCheck.y, -participant.comprehensionCheck2.y, -participant.orderStimuli.y, -introduction.1.player.id_in_group, -player.id_in_group, -session.label, -session.mturk_HITId, -session.mturk_HITGroupId, -session.comment, -session.is_demo, -session.config.participation_fee, -session.config.real_world_currency_per_point, -introduction.1.player.role, -introduction.1.player.payoff, -introduction.1.player.consent, -participant._is_bot, -participant.mturk_assignment_id, -participant.label, -participant.visited, -participant.mturk_worker_id, -participant.payoff, -introduction.1.group.id_in_subsession, introduction.1.subsession.round_number, -participant._max_page_index, -introduction.1.subsession.round_number, -session.code)

# Nur die ProbandInnen beibehalten, die bis page 90 gekommen sind
participants_reached_90_or_more <- df_cleaned %>%
  filter(participant._index_in_pages >= 90) %>%
  pull(participant.code) 

# Jetzt die Probanden, die weniger als Seite 90 erreicht haben, ausschließen
df_cleaned <- df_cleaned %>%
  filter(participant.code %in% participants_reached_90_or_more)

# Variable participant._index_in_pages entfernen
df_cleaned <- df_cleaned %>%
  select(-participant._index_in_pages)

# Anzahl der Probanden
anzahl_probanden <- df_cleaned %>% 
  pull(participant.code) %>% 
  n_distinct()
print(anzahl_probanden)

# Anzahl der Probanden: 415
# Nach Zufallsprinzip Probanden entfernen?


#################################################################################################################################


# Umwandlung der Stimuli-Reihenfolge und Erstellen neuer Variablen
df_cleaned <- df_cleaned %>%
  mutate(participant.orderStimuli.x = gsub("\\[|\\]", "", participant.orderStimuli.x)) %>%
  mutate(stimuli_order = strsplit(participant.orderStimuli.x, ", ")) %>%
  mutate(stimuli_order = lapply(stimuli_order, function(x) as.numeric(trimws(x)))) %>%
  group_by(participant.code) %>%
  mutate(
    round = round - 1,  # Reduziere die Rundenanzahl um 1
    roundstimuliID = sapply(round, function(i) {
      order_list <- stimuli_order[[1]]
      round_index <- i  # i ist bereits angepasst durch die obige Zeile
      if (round_index >= 0 && round_index < length(order_list)) {
        return(order_list[round_index + 1])
      } else {
        return(NA)
      }
    })
  ) %>%
  ungroup() %>%
  select(-stimuli_order)


#################################################################################################################################


# Umbenennung der Variablennamen
df_cleaned <- df_cleaned %>%
  rename(
    participant.id = participant.id_in_session,
    stimuli.order = participant.orderStimuli.x,
    comp.check1 = participant.comprehensionCheck.x,
    comp.check2 = participant.comprehensionCheck2.x,
    round.number = round,
    choice = player.choice,
    sustainable.left = player.sustainableLeft,
    treatment.group = player.treatment,
    sustainable.choice = player.choice_sustainable,
    name.nonSustainable = player.AName,
    name.Sustainable = player.BName,
    estimate.nonSustainable = player.AEstimate,
    estimate.Sustainable = player.BEstimate,
    correct.nonSustainable = player.ACorrect,
    correct.Sustainable = player.BCorrect,
    frage_1 = player.frage_1,
    frage_2 = player.frage_2,
    frage_3 = player.frage_3,
    frage_4 = player.frage_4,
    frage_5 = player.frage_5,
    frage_6 = player.frage_6,
    frage_7 = player.frage_7,
    frage_8 = player.frage_8,
    alter = player.alter,
    geschlecht = player.geschlecht,
    studierende = player.studierende,
    einkommen = player.monatliches_einkommen,
    einkauf = player.haushalts_einkauf,
    politische.O = player.politische_orientierung,
    ernährung = player.ernaehrungsgewohnheiten,
    ernährung_other= player.ernaehrungsgewohnheiten_other,
    email = player.email,
    round.stimuliID= roundstimuliID
  )

################################################################################################################################# 


## Ordinaldaten numerisch umwandeln

# Geschlecht
df_cleaned$num_geschlecht <- (df_cleaned$geschlecht == "Weiblich") * 1 + 
  (df_cleaned$geschlecht == "Männlich") * 2 +
  (df_cleaned$geschlecht == "Divers") * 3 +
  (df_cleaned$geschlecht == "Sonstige") * 4

# Studierende
df_cleaned$num_studierende <- (df_cleaned$studierende == "Ja") * 1 + 
  (df_cleaned$studierende == "Nein") * 2

# Haushaltseinkauf
df_cleaned$num_einkauf <- (df_cleaned$einkauf == "Ja") * 1 + 
  (df_cleaned$einkauf == "Nein") * 2

# Einkommen
df_cleaned$num_einkommen <- (df_cleaned$einkommen == "0-1000") * 1 + 
  (df_cleaned$einkommen == "1001-3000") * 2 +
  (df_cleaned$einkommen == "3001-5000") * 3 +
  (df_cleaned$einkommen == "5001-7000") * 4 +
  (df_cleaned$einkommen == "Mehr als 7000") * 5 +
  (df_cleaned$einkommen == "Ich möchte keine Angabe machen") * 6
df_cleaned$num_einkommen

# Politische Orientierung
df_cleaned$num_politische_orientierung <- (df_cleaned$politische.O == "Links") * 1 + 
  (df_cleaned$politische.O == "Mitte-links") * 2 +
  (df_cleaned$politische.O == "Mitte") * 3 +
  (df_cleaned$politische.O == "Mitte-rechts") * 4 +
  (df_cleaned$politische.O == "Rechts") * 5 +
  (df_cleaned$politische.O == "Ich möchte keine Angabe machen") * 6

# Ernährungsgewohnheiten
df_cleaned$num_ernährung <- (df_cleaned$ernährung == "AllesesserIn") * 1 + 
  (df_cleaned$ernährung == "Vegetarisch") * 2 +
  (df_cleaned$ernährung == "Vegan") * 3

# Comprehension Check 
df_cleaned <- df_cleaned %>% 
  mutate(
    comp.check1 = case_when(
      comp.check1 == "correct" ~ 1,
      comp.check1 %in% c("a_false", "b_false", "c_false") ~ 0,
      TRUE ~ NA_real_
    ),
    comp.check2 = case_when(
      comp.check2 == "correct" ~ 1,
      comp.check2 %in% c("a_false", "b_false", "c_false") ~ 0,
      TRUE ~ NA_real_
    )
  )


################################################################################################################################# 


# DataFrame aus der Liste der Stimuli mit Preis, Emissionen und Proteine

stimuli_list <- data.frame(
  StimulusID = 0:14,
  PriceA = c(3, 1.25, 7, 1.15, 0.36, 0.51, 16, 16.5, 25, 25.50, 20, 19.50, 17.50, 1.95, 29.50),
  CO2A = c(5718, 2187, 3802, 5763, 4400, 3780, 5351, 21693, 4419, 16363, 17914, 18357, 11094, 23019, 20825),
  ProteinA = c(20, 7, 4, 4, 1, 2, 32, 36, 33, 47, 35, 44, 32, 10, 35),
  PriceB = c(1.60, 1.18, 7, 1, 0.49, 0.81, 17.50, 14.50, 22, 12.50, 17.50, 17.50, 19, 0.70, 28),
  CO2B = c(1116, 622, 2334, 1498, 900, 1155, 1479, 1478, 1215, 1384, 2100, 1918, 1575, 2422, 895),
  ProteinB = c(9, 10, 0.8, 10, 1, 3, 18, 23, 29, 23, 20, 25, 24, 4, 27),
  NameA = c("Eier mit Speck", "Schoko-Cerealien mit Kuhmilch", "Schokoladeneis", "Vollmilchschokolade", 
            "Mango", "Joghurt-Müsliriegel", "Bacon Mac&Cheese", "Cheeseburger", "Salami-Pizza", 
            "Steak", "Spaghetti Meatballs", "Lasagne mit Hackfleisch", "Roastbeef-Sandwich", 
            "Beef Jerky", "Lammkotelett"),
  NameB = c("Hummus mit Brot", "Haferflocken mit pflanzlicher Milch und Früchten", "Früchtesorbet", 
            "Erdnussbutter-Marmeladen-Sandwich", "Apfel", "Cracker", "Kichererbsen-Curry", 
            "Falafel-Sandwich", "Chili sin Carne", "Gemüseauflauf", "Spaghetti Marinara", 
            "Vegetarische Spaghetti Bolognese", "Veganer Burrito", "Trail Mix", "Makrele")
)

df_cleaned <- df_cleaned %>%
  left_join(stimuli_list, by = c("round.stimuliID" = "StimulusID"))

# Erstellen neuer Variablen basierend auf der Wahl des Teilnehmers und der Stimulus Reihenfolge
df_cleaned <- df_cleaned %>%
  mutate(
    price.chosen = ifelse(sustainable.choice == 1, PriceB, PriceA),
    protein.chosen = ifelse(sustainable.choice == 1, ProteinB, ProteinA),
    food.chosen = ifelse(sustainable.choice == 1, NameB, NameA),
    CO2.chosen = ifelse(sustainable.choice == 1, CO2B, CO2A)
  )

# Differenzen zwischen tatsächlichen und geschätzten Memory Task Werten 
df_cleaned <- df_cleaned %>%
  mutate(
    diff_nonSustainable = correct.nonSustainable - estimate.nonSustainable,
    diff_Sustainable = correct.Sustainable - estimate.Sustainable
  )

df_cleaned <- df_cleaned %>%
  mutate(
    # Absolute Differenzen
    absolut_diff = abs(diff_nonSustainable) + abs(diff_Sustainable),
    
    # Differenzen mit Berücksichtigung der Über- und Unterschätzung
    real_diff = diff_nonSustainable + diff_Sustainable
  )

# Sustainability Score
df_cleaned <- df_cleaned %>%
  mutate(
    frage_1_scaled = (frage_1 - 1) / 5, 
    frage_2_scaled = (frage_2 - 1) / 5,
    frage_3_scaled = (frage_3 - 1) / 5,
    frage_4_scaled = (frage_4 - 1) / 5,
    frage_5_scaled = (frage_5 - 1) / 6, 
    frage_6_scaled = (frage_6 - 1) / 6,
    frage_7_scaled = (frage_7 - 1) / 4, 
    frage_8_scaled = (frage_8 - 1) / 4
  )

# Gesamtwert berechnen als Durchschnitt der skalierten Fragen
df_cleaned <- df_cleaned %>%
  rowwise() %>%
  mutate(
    sustainability_score = mean(c(
      frage_1_scaled, frage_2_scaled, frage_3_scaled, frage_4_scaled,
      frage_5_scaled, frage_6_scaled, frage_7_scaled, frage_8_scaled
    ), na.rm = TRUE)
  )

df_cleaned <- df_cleaned %>%
  mutate(sustainability_score = na_if(sustainability_score, NaN))


################################################################################################################################# 


# Ausgabe des Data Frames zur Überprüfung
print(df_cleaned)

# Daten exportieren
write.csv2(df_cleaned, "/Users/ausleihe/Desktop/daten/14.10.2024/df_cleaned.csv", row.names = FALSE)
