
# DATEN EINLESEN

df_clean <- read_delim("/Users/ausleihe/Desktop/daten/14.10.2024/df_cleaned.csv", delim = ";")
tracking_data_clean <- read_delim("/Users/ausleihe/Desktop/daten/14.10.2024/df_tracking_cleaned.csv", delim = ";")

# Überprüfung auf fehlende Werte 
anyNA(df_clean)
df_clean %>% summarise_all(~sum(is.na(.))) %>% print()

#################################################################################################################################

# Anzahl der gemeinsamen Probanden in den beiden Datensätzen zählen
gemeinsame_probanden <- intersect(df_clean$participant.code, tracking_data_clean$participant.code)
anzahl_gemeinsame_probanden <- length(gemeinsame_probanden)
cat("Anzahl der gemeinsamen Probanden in beiden Datensätzen:", anzahl_gemeinsame_probanden, "\n")
gemeinsame_probanden <- intersect(df_clean$participant.code, tracking_data_clean$participant.code)

# Filtern df_clean und tracking_data_clean
df <- df_clean %>%
  filter(participant.code %in% gemeinsame_probanden)
tracking_data<- tracking_seperate %>%
  filter(participant.code %in% gemeinsame_probanden)

# Überprüfe die Anzahl der verbleibenden Probanden in beiden Datensätzen
anzahl_probanden_df <- n_distinct(df$participant.code)
anzahl_probanden_tracking <- n_distinct(tracking_data$participant.code)

# Ausgabe der Anzahl der verbleibenden Probanden
cat("Anzahl der Probanden in df_cleaned nach dem Filtern:", anzahl_probanden_df, "\n")
cat("Anzahl der Probanden in tracking_seperate nach dem Filtern:", anzahl_probanden_tracking, "\n")

#################################################################################################################################

# DESKRIPTIVE STATISTIK

psych::describe(df)

# Deskriptive Statistik für Alter
summary(df$alter) 
sd_age <- sd(df$alter, na.rm = TRUE)
sd_age

# Histogramm der Altersverteilung
ggplot(df, aes(x = alter)) +
  geom_histogram(binwidth = 1, fill = "blue", color = "black") +
  labs(title = "Altersverteilung", x = "Alter", y = "Häufigkeit") +
  theme_minimal()

# Boxplot der Altersverteilung
ggplot(df, aes(y = alter)) +
  geom_boxplot(fill = "blue", color = "black") +
  labs(title = "Boxplot der Altersverteilung", y = "Alter") +
  theme_minimal()

# Häufigkeiten und Prozente für Geschlecht
gender_freq <- table(df$geschlecht)
gender_perc <- prop.table(gender_freq) * 100
print(gender_freq)
print(gender_perc)

# Häufigkeiten und Prozente für Ernährungsgewohnheiten
diet_freq <- table(df$ernährung)
diet_perc <- prop.table(diet_freq) * 100
print(diet_freq)
print(diet_perc)

# Häufigkeiten und Prozentsätze für Ernährungsgewohnheiten pro Behandlungsgruppe
diet_summary <- df %>%
  group_by(treatment.group, ernährung) %>%
  summarise(count = n(), .groups = 'drop') %>% 
  group_by(treatment.group) %>%
  mutate(percentage = (count / sum(count)) * 100) %>%
  arrange(treatment.group, ernährung)
print(diet_summary)

# Häufigkeiten und Prozente für Politische Orientierung
politics_freq <- table(df$politische.O)
politics_perc <- prop.table(politics_freq) * 100
print(politics_freq)
print(politics_perc)

# Häufigkeiten und Prozente für Studierende
studis_freq <- table(df$studierende)
studis_perc <- prop.table(studis_freq) * 100
print(studis_freq)
print(studis_perc)

# Häufigkeiten und Prozente für Haushaltseinkauf
einkauf_freq <- table(df$einkauf)
einkauf_perc <- prop.table(einkauf_freq) * 100
print(einkauf_freq)
print(einkauf_perc)

# Häufigkeiten und Prozente für Einkommen
income_freq <- table(df$einkommen)
income_perc <- prop.table(income_freq) * 100
print(income_freq)
print(income_perc)

# Häufigkeitstabellen 
table(df$geschlecht, df$ernährung)
table(df$geschlecht, df$politische.O)
table(df$geschlecht, df$sustainable.choice)
table(df$politische.O, df$sustainable.choice)

# Boxplot erstellen tracking_data
boxplot(tracking_data$duration)
# Hier die drei Ausreisser rausschmeissen oder drinnen lassen?

# Q-Q-Plot erstellen tracking_data
qqnorm(tracking_data$duration, main = "Q-Q-Plot der Dauer")
qqline(tracking_data$duration, col = "red")

# Wahl nachhaltiger vs. nicht-nachhaltiger Optionen
choice_counts <- df %>%
  group_by(sustainable.choice) %>%
  summarise(count = n())
print(choice_counts)

# Nicht-Nachhaltig: 1652
# Nachhaltig: 3883

# Anzahl nachhaltiger und nicht nachhaltiger Entscheidungen pro Gruppe
choice_counts_by_group <- df %>%
  group_by(treatment.group, sustainable.choice) %>%
  summarise(count = n()) %>%
  mutate(choice_type = ifelse(sustainable.choice == 1, "Nachhaltig", "Nicht Nachhaltig"))
print(choice_counts_by_group)

# Prozentsätze nachhaltiger und nicht nachhaltiger Entscheidungen pro Gruppe
choice_percentages_by_group <- df %>%
  group_by(treatment.group) %>%
  summarise(
    count_sustainable = sum(sustainable.choice == 1),
    count_unsustainable = sum(sustainable.choice == 0),
    total_count = n(),
    nachhaltig = (count_sustainable / total_count) * 100,
    nicht_nachhaltig = (count_unsustainable / total_count) * 100,
    .groups = 'drop'
  ) %>%
  select(treatment.group, nachhaltig,  nicht_nachhaltig)
print(choice_percentages_by_group)
#                                 Nachhaltig            Nicht-Nachhaltig
# control                           68.9                     31.1
# label                             69.5                     30.5
# norm                              71.0                     29.0

# Mittelwerte und Standardabweichungen
df %>% 
  group_by(treatment.group) %>%
  summarise(
    mean_sustainable_choice = mean(sustainable.choice, na.rm = TRUE),
    sd_sustainable_choice = sd(sustainable.choice, na.rm = TRUE),
    mean_recall_accuracy = mean(absolut_diff, na.rm = TRUE),
    sd_recall_accuracy = sd(absolut_diff, na.rm = TRUE)
  )

# Häufigkeiten
table(df$treatment.group)
table(df$sustainable.choice)


#################################################################################################################################


# GRAFISCHE DARSTELLUNG 

# Balkendiagramm für Einkommen
income_freq <- df %>%
  count(einkommen) %>%
  mutate(percentage = n / sum(n) * 100)

ggplot(income_freq, aes(x = einkommen, y = n, fill = einkommen)) + 
  geom_bar(stat = "identity") + 
  labs(title = "Häufigkeit des monatlichen Einkommens", x = "Monatliches Einkommen", y = "Häufigkeit") + 
  theme_minimal() + 
  scale_fill_brewer(palette = "Set6") + 
  theme(axis.text.x = element_text(angle = 45, hjust = 1)) +
  scale_y_continuous(limits = c(0, 200))

# Boxplot für Einkommen nach Geschlecht
ggplot(df, aes(x = factor(num_geschlecht), y = num_einkommen)) +
  geom_boxplot() +
  labs(title = "Einkommen nach Geschlecht", x = "Geschlecht", y = "Einkommen")

# Korrelation abhängig von der Ernährung
model <- lm(num_ernährung ~ num_geschlecht + num_studierende + num_einkauf + num_politische_orientierung + num_einkommen, data = df)
summary(model)
# Insbesondere zeigen Frauen und Menschen mit linker politischer Orientierung umweltfreundlichere Ernährungsgewohnheiten im Vergleich zu Männern und Menschen mit rechter politischer Orientierung. 
# Ein höheres Einkommen ist ebenfalls mit weniger umweltfreundlichen Ernährungsgewohnheiten assoziiert.

# Korrelationsmatrix für alle Daten (numerisch)
cor_matrix <- cor(df %>% select(num_ernährung, num_einkommen, num_geschlecht, num_studierende, num_einkauf, num_politische_orientierung), use = "complete.obs")
print(cor_matrix)

# Korrelation-Plot erstellen für alle Daten (numerisch)
corrplot(cor_matrix, method = "circle", type = "upper", tl.col = "black", tl.cex = 0.7)


#################################################################################################################################


# LOGISTISCHE MULTILEVEL-REGRESSION

# Umwandlung in numerische Variablen/ Faktoren
df <- df %>%
  mutate(price.chosen = as.numeric(gsub(",", ".", price.chosen)),
         protein.chosen = as.numeric(gsub(",", ".", protein.chosen)),
         sustainability_score = as.numeric(gsub(",", ".", sustainability_score)))

df$participant.id <- as.factor(df$participant.id)
df$treatment.group <- as.factor(df$treatment.group)

# Skalierung der Prädiktorvariablen
df <- df %>%
  mutate(
    sustainability_score = scale(sustainability_score),
    price.chosen = scale(price.chosen),
    CO2.chosen = scale(CO2.chosen),
    protein.chosen = scale(protein.chosen)
  )

# Modell 1: Logistische Regression, um die Wahrscheinlichkeit nachhaltiger Entscheidungen über die Zeit zu untersuchen (mit "round" als Prädiktor und random intercept für "participant")
mod1 <- glmer(sustainable.choice ~ round.number + (1 | participant.id), 
              data = df, family = binomial)
summary(mod1)

# Modell 2: Erweiterung von Modell 1 um die Gruppenzugehörigkeit (Control, Label, Norm) als festen Effekt.
mod2 <- glmer(sustainable.choice ~ round.number + treatment.group + (1 | participant.id), 
              data = df, family = binomial)
summary(mod2)

# Modell 3: Hinzufügen der Pro-Environmental Attitudes und CO2-Emissionen als Kontrollvariablen.
# Hohe Korrelation zwischen sustainability_score und CO2.chosen
mod3 <- glmer(sustainable.choice ~ round.number + treatment.group + 
                sustainability_score + CO2.chosen + 
                (1 | participant.id), 
              data = df, family = binomial)
summary(mod3)

# Korrelationen zwischen Variablen
cor_matrix <- cor(df %>% select(price.chosen, CO2.chosen, protein.chosen, sustainability_score), use = "complete.obs")
print(cor_matrix)

# Modell 4: Interaktion zwischen Gruppenzugehörigkeit und Pro-Environmental Attitudes.
# Error: pwrssUpdate did not converge in (maxit) iterations

mod4 <- glmer(sustainable.choice ~ treatment.group * sustainability_score + 
                price.chosen + CO2.chosen + protein.chosen + 
                (1 | participant.id), 
              data = df, 
              family = binomial, 
              control = glmerControl(optimizer = "bobyqa", optCtrl = list(maxfun = 100000)))

summary(mod4)

# Modell 5: Kontraste
emm <- emmeans(mod4, ~ treatment.group | sustainability_score)
contrast(emm, method = "pairwise")

#################################################################################################################################

# RECALL ACCURACY

# Hinzufügen der Variable, ob die Kohlenstoffattribute, die beim Memory test abgefragt werden, angesehen wurden
# Nur von den relevanten round.stimuliID, die im memory_task abgefragt werden: 7, 8, 14, 9, 11
interested_stimuli <- c(7, 8, 14, 9, 11)

# Hinzufügen der Variable, ob das Kohlenstoffattribut in den interessierenden Runden angesehen wurde
tracking_data <- tracking_data %>%
  group_by(participant.id) %>%
  summarise(
    carbon_viewed = ifelse(any(attributeType == "CO2e/ kg" & stimulusID %in% interested_stimuli), 1, 0),
    .groups = 'drop'
  )

# Variable carbon_viewed in den Datensatz df einfügen
tracking_data <- tracking_data %>%
  mutate(participant.id = as.factor(participant.id))
df <- df %>%
  left_join(tracking_data, by = "participant.id")
df$carbon_viewed <- as.factor(df$carbon_viewed)
# Es kann nicht sein, dass sich niemand der CO2 Attribut von diesen 5 Stimuli angeschaut hat???

# Multilevel-Regression für Recall Accuracy abhängig davon, ob das Carbon Attribut gesehen wurde
# Kann nicht durchgeführt werden, da sich niemand das Carbon Attribut angeschaut hat
model_recall <- lmer(absolut_diff ~ treatment.group + carbon_viewed +
                     (1 | participant.id), 
                   data = df)
summary(model_recall)

# Multilevel-Regression für Recall Accuracy abhängig von den Umwelt-Werten 
mod_recall <- lmer(absolut_diff ~ treatment.group + sustainability_score + 
                     (1 | participant.id), 
                   data = df)
summary(mod_recall)
# Hier Schwierigkeiten mit participant.id

# Interaktioneffekte: Gruppenzugehörigkeit und Umwelt-Einstellungen auf Recall Accuracy 
mod_interaction_recall <- lmer(absolut_diff ~ treatment.group * sustainability_score + 
                                 (1 | participant.id), 
                               data = df)
summary(mod_interaction_recall)
# Hier Schwierigkeiten mit participant.id

# Interaktioneffekte: Gruppenzugehörigkeit und Ansehen des Carbon Attributs auf Recall Accuracy 
mod_recall_interaction <- lmer(absolut_diff ~ treatment.group * carbon_viewed + (1 | participant.id), data = df)
summary(mod_recall_interaction)

# Kontraste zur Untersuchung der Gruppenunterschiede
emm <- emmeans(mod_recall_interaction, ~ treatment.group | sustainability_score)
contrast(emm)

# Visualisierung der Recall-Accuracy
ggplot(df, aes(x = sustainability_score, y = absolut_diff, color = treatment.group)) +
  geom_point() +
  geom_smooth(method = "lm", se = FALSE) +
  labs(title = "Recall-Accuracy vs. Umwelt-Einstellungen", x = "Pro-Umwelt-Einstellungen", y = "Recall-Genauigkeit") +
  theme_minimal()


#################################################################################################################################


# Weitere Plots zur Visualisierung der Daten
ggcol3 <- scale_color_manual(values = c("red", "blue", "green"))  

ggplot(df, aes(round.number, sustainable.choice, na.rm = TRUE)) + 
  stat_smooth(aes(group = participant.id, color = treatment.group), method = "lm", formula = y ~ x, se = FALSE, na.rm = TRUE, size = 0.1) + 
  stat_smooth(aes(group = treatment.group, color = treatment.group), method = "lm", formula = y ~ x, se = FALSE, na.rm = TRUE, size = 1.5, linetype = "solid") + 
  ggcol3 + ylab("choice") + xlab("rounds")

ggplot(df, aes(round.number, sustainable.choice, na.rm = TRUE)) + 
  stat_smooth(aes(group = participant.id, color = treatment.group), method = "loess", formula = y ~ x, se = FALSE, span = 1, na.rm = TRUE, size = 0.1) + 
  stat_smooth(aes(group = treatment.group, color = treatment.group), method = "loess", formula = y ~ x, span = 1, se = FALSE, na.rm = TRUE, size = 1.5, linetype = "solid") + 
  ggcol3 + facet_wrap(~treatment.group) + ylab("choice") + xlab("rounds") 

ggplot(data = df[as.numeric(substr(df$participant.id, 1, 5)) %% 10 == 0,], aes(x = round.number, y = sustainable.choice, group = participant.id)) + 
  stat_summary(aes(color = treatment.group), fun.y = mean, geom = "point", size = 0.5) + 
  stat_smooth(aes(color = treatment.group), method = "loess", formula = y ~ x, span = 1, se = FALSE, na.rm = TRUE, size = 0.3, linetype = "dashed") + 
  stat_smooth(aes(color = treatment.group), method = "lm", formula = y ~ x, se = FALSE, na.rm = TRUE, size = 0.3) + 
  facet_wrap(~participant.id) + ggcol3 + ylab("choice") + xlab("rounds") + ylim(0, 1)


#################################################################################################################################


# T-TESTS /ANOVA

# Vergleich der Anzahl nachhaltiger Entscheidungen zwischen den beiden experimentellen Gruppen und der Kontrollgruppe
# Daten korrekt bereinigen und vorbereiten
control <- df %>% filter(treatment.group == "control")
label <- df %>% filter(treatment.group == "label")
norm <- df %>% filter(treatment.group == "norm")

# Anzahl der nachhaltigen Entscheidungen pro Gruppe
sustainable_counts <- df %>%
  group_by(treatment.group) %>%
  summarise(sustainable_choices = sum(sustainable.choice))
print(sustainable_counts)

# Boxplot zur Visualisierung der Verteilung nachhaltiger Entscheidungen in den drei Gruppen
ggplot(df, aes(x = treatment.group, y = sustainable.choice, fill = treatment.group)) +
  geom_bar(stat = "identity") +
  labs(title = "Anzahl nachhaltiger Entscheidungen pro Gruppe",
       x = "Gruppe",
       y = "Anzahl nachhaltiger Entscheidungen") 

# T-Test zwischen control und label
controllabel <- t.test(control$sustainable.choice, label$sustainable.choice)
print(controllabel)
# Kein signifikanter Unterschied 

# T-Test zwischen control und norm
controlnorm <- t.test(control$sustainable.choice, norm$sustainable.choice)
print(controlnorm)
# Kein signifikanter Unterschied

# ANOVA für nachhaltige Entscheidungen zwischen den Gruppen
anova_model <- aov(sustainable.choice ~ treatment.group, data = df)
anova_summary <- summary(anova_model)
print(anova_summary)
# Kein signifikanter Unterschied 

# ANOVA für Recall Accuracy
anova_recall_accuracy <- aov(absolut_diff ~ treatment.group, data = df)
summary(anova_recall_accuracy)
# Signifikanter Unterschied (p-Wert von 0.0211) in der Recall Accuracy zwischen den Behandlungsgruppen

# ANOVA für Pro-Environmental Attitudes
anova_pro_env <- aov(sustainability_score ~ treatment.group, data = df)
summary(anova_pro_env)
# Kein signifikanter Unterschied (p-Wert von 0,335) im sustainability score zwischen den Behandlungsgruppen
 
#################################################################################################################################

# PRÜFUNG DER VORAUSSETZUNGEN FÜR DIE MODELLE - noch nicht fertig

install.packages(c("car", "lme4", "aod", "lmtest", "ResourceSelection", "corrplot"))
library(car)
library(lme4)
library(aod)
library(lmtest)
library(ResourceSelection)
library(corrplot)

#############################

# Multikollinearität (VIF) für alle Prädiktoren im Modell
vif(mod3)
print(vif_results)

#############################

# Hierarchische Struktur und Intraklassenkorrelation (ICC mit einem Nullmodell)

# Nullmodell erstellen
null_model <- glmer(sustainable.choice ~ 1 + (1 | participant.id), data = df, family = binomial)

# Vollständiges Modell erstellen
full_model <- glmer(sustainable.choice ~ round.number + treatment.group + (1 | participant.id), data = df, family = binomial)

# Extrahiere Varianz der Zufallseffekte aus dem Nullmodell
var_null_model <- as.data.frame(VarCorr(null_model))$vcov[1]

# Extrahiere Varianz der Zufallseffekte und Residuenvarianz aus dem vollständigen Modell
var_full_model_random <- as.data.frame(VarCorr(full_model))$vcov[1]  
var_full_model_residual <- sigma(full_model)^2 

# Berechne ICC
icc <- var_full_model_random / (var_full_model_random + var_full_model_residual)
print(icc)  # 0.4788337
cat("48% der Gesamtvarianz in der abhängigen Variablen wird durch Unterschiede zwischen den Teilnehmern erklärt.\n")

#############################

# Residuen des Nullmodells extrahieren
residuals_null <- residuals(null_model)

# Standardisierte Residuen berechnen
standardized_residuals <- residuals_null / sqrt(summary(null_model)$dispersion)

# Ausgabe der standardisierten Residuen
print(standardized_residuals)

# Residuen visualisieren
hist(standardized_residuals, breaks = 20, main = "Standardisierte Residuen", xlab = "Standardisierte Residuen")

# Streudiagramm der standardisierten Residuen gegen die Vorhersagen
predicted_values <- predict(null_model, type = "response")
plot(predicted_values, standardized_residuals, xlab = "Vorhergesagte Werte", ylab = "Standardisierte Residuen")
abline(h = 0, col = "red")

# Q-Q-Plot erstellen
qqnorm(standardized_residuals, main = "Q-Q-Plot der standardisierten Residuen")
qqline(standardized_residuals, col = "red")

# Shapiro-Wilk-Test durchführen
set.seed(123)  
sampled_residuals <- sample(standardized_residuals, size = min(5000, length(standardized_residuals)))
shapiro_test_result <- shapiro.test(sampled_residuals)
print(shapiro_test_result)

# Hinweis: Residuen folgen möglicherweise nicht der Normalverteilung

#############################

# Homoskedastizität (Residuenplot)
standardized_residuals_full <- residuals(full_model, type = "pearson")

# Residuenplot erstellen
plot(fitted(full_model), standardized_residuals_full, 
     xlab = "Fitted Values", ylab = "Standardized Residuals",
     main = "Residuals vs Fitted (Full Model)")
abline(h = 0, col = "red") 

#############################

# Lineare Beziehung auf der Logit-Skala (Box-Tidwell-Test)
boxTidwell(sustainable.choice ~ round.number + treatment.group + 
             num_geschlecht + num_studierende + num_einkauf + 
             num_politische_orientierung + num_einkommen,  
           data = df)

#############################

# Unabhängigkeit der Residuen (Durbin-Watson-Test)
# Berechne die Residuen des vollständigen Modells
residuals_full_model <- residuals(full_model, type = "pearson")

# Fitted values (vorhergesagte Werte) des vollständigen Modells
fitted_values_full_model <- fitted(full_model)

# Durbin-Watson-Test durchführen
dw_test <- dwtest(lm(residuals_full_model ~ fitted_values_full_model))
print(dw_test)

# DW = 2.1393: keine starke Autokorrelation in den Residuen
# p-value = 1
# Annahme der Unabhängigkeit der Residuen ist erfüllt

#############################

install.packages("ResourceSelection") 
library(ResourceSelection)

# Vorhersagen des Nullmodells erhalten
predicted_probs <- predict(null_model, type = "response")

# Hosmer-Lemeshow-Test durchführen
hoslem_test <- hoslem.test(df$sustainable.choice, predicted_probs, g = 10)  # g = Anzahl der Gruppen
print(hoslem_test)
# p-value < 2.2e-16: Modell passt nicht gut zu den Daten, deutet darauf hin, ass die Vorhersagen des Modells signifikant von den beobachteten Werten abweichen
