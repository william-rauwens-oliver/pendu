import pygame
import random
import sys

pygame.init()

# Paramètres du jeu
largeur_fenetre = 800
hauteur_fenetre = 600
couleur_fond = (255, 255, 255)
couleur_texte = (255, 255, 255)
couleur_text_pendu = (50, 50, 50)
couleur_fond_rectangle = (50, 50, 50)
font_grande = pygame.font.Font(None, 36)
font_petite = pygame.font.Font(None, 24)

# Chargement des mots depuis le fichier "mots.txt"
with open("fichiers texte/mots.txt", "r") as fichier:
    mots = fichier.read().splitlines()

with open("fichiers texte/scores.txt", "a"):
    pass

score_joueur = 0

font_menu_principal = pygame.font.Font("polices/design.graffiti.comicsansmsgras.ttf", 36)
font_petite = pygame.font.Font(None, 24)

border_radius = 10

def saisir_nom_utilisateur():
    nom = ""
    saisie_active = True
    titre = "Choisissez un nom d'utilisateur !"

    while saisie_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    saisie_active = False
                elif event.key == pygame.K_BACKSPACE:
                    nom = nom[:-1]
                elif event.unicode.isalpha():
                    nom += event.unicode

        fenetre.fill(couleur_fond)
        fenetre.blit(fond_ecran_menu, (0, 0))

        # Affichage du titre avec la nouvelle police
        text_titre = font_menu_principal.render(titre, True, couleur_text_pendu)
        text_rect_titre = text_titre.get_rect(center=(largeur_fenetre // 2, hauteur_fenetre // 2 - 250))
        fenetre.blit(text_titre, text_rect_titre)

        # Affichage du champ de saisie avec le bouton
        text = font_grande.render("Entrez votre nom:", True, couleur_texte)
        text_rect = text.get_rect(center=(largeur_fenetre // 2, hauteur_fenetre // 2 - 50))
        fenetre.blit(text, text_rect)

        pygame.draw.rect(fenetre, couleur_fond_rectangle, input_rect, border_radius=border_radius)
        pygame.draw.rect(fenetre, couleur_texte, input_rect, 2, border_radius=border_radius)
        text_nom = font_grande.render(nom, True, couleur_texte)
        text_rect_nom = text_nom.get_rect(center=input_rect.center)
        fenetre.blit(text_nom, text_rect_nom)

        pygame.display.flip()

    return nom

def obtenir_nom_joueur():
    return saisir_nom_utilisateur()

def choisir_mot():
    return random.choice(mots)

def rendre_texte_avec_fond(texte, font, couleur_texte, couleur_fond, position, offset_ombre=(2, 2), marge=(10, 10)):
    texte_surface = font.render(texte, True, couleur_texte)
    texte_rect = texte_surface.get_rect(center=position)

    largeur_rect = texte_rect.width + 2 * marge[0]
    hauteur_rect = texte_rect.height + 2 * marge[1]

    rect_fond = pygame.Rect(texte_rect.left - marge[0], texte_rect.top - marge[1], largeur_rect, hauteur_rect)

    pygame.draw.rect(fenetre, couleur_fond, rect_fond)
    pygame.draw.rect(fenetre, couleur_texte, rect_fond, 2)

    texte_surface_ombre = font.render(texte, True, (0, 0, 0))
    texte_rect_ombre = texte_surface_ombre.get_rect(center=(texte_rect.center[0] + offset_ombre[0], texte_rect.center[1] + offset_ombre[1]))

    return texte_surface_ombre, texte_rect_ombre, texte_surface, texte_rect

def jouer_pendu():
    global score_joueur

    nom_joueur = obtenir_nom_joueur()

    mot_a_trouver = choisir_mot().upper()
    lettres_trouvees = set()
    erreurs_max = 6
    erreurs = 0
    victoire = False
    defaite = False

    pygame.display.set_caption("Jeu du Pendu")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.unicode.isalpha():
                    lettre = event.unicode.upper()
                    if lettre not in lettres_trouvees:
                        lettres_trouvees.add(lettre)
                        if lettre not in mot_a_trouver:
                            erreurs += 1

        fenetre.fill(couleur_fond)
        fenetre.blit(fond_ecran_jeu, (0, 0))

        mot_affiche = ""
        for lettre in mot_a_trouver:
            if lettre in lettres_trouvees:
                mot_affiche += lettre + " "
            else:
                mot_affiche += "_ "

        couleur_bois = (139, 69, 19)
        couleur_ombre = (100, 50, 10)
        offset_x = 30
        offset_y = 150

        text = font_grande.render(mot_affiche, True, couleur_text_pendu)
        text_rect = text.get_rect(center=(largeur_fenetre // 2, 50 + offset_y))
        fenetre.blit(text, text_rect)

        if erreurs > 0:
            pygame.draw.line(fenetre, couleur_ombre, (largeur_fenetre // 2 - 150 + offset_x + 1, 300 + offset_y + 1), (largeur_fenetre // 2 - 150 + offset_x + 1, 100 + offset_y + 1), 5)
            pygame.draw.line(fenetre, couleur_bois, (largeur_fenetre // 2 - 150 + offset_x, 300 + offset_y), (largeur_fenetre // 2 - 150 + offset_x, 100 + offset_y), 5)
        if erreurs > 1:
            pygame.draw.line(fenetre, couleur_ombre, (largeur_fenetre // 2 - 150 + offset_x + 1, 300 + offset_y + 1), (largeur_fenetre // 2 - 150 + offset_x + 1, 100 + offset_y + 1), 5)
            pygame.draw.line(fenetre, couleur_bois, (largeur_fenetre // 2 - 150 + offset_x, 100 + offset_y), (largeur_fenetre // 2 + offset_x, 100 + offset_y), 5)
        if erreurs > 2:
            pygame.draw.line(fenetre, couleur_ombre, (largeur_fenetre // 2 - 150 + offset_x + 1, 300 + offset_y + 1), (largeur_fenetre // 2 - 150 + offset_x + 1, 100 + offset_y + 1), 5)
            pygame.draw.circle(fenetre, couleur_bois, (largeur_fenetre // 2 + offset_x, 150 + offset_y), 30, 5)
        if erreurs > 3:
            pygame.draw.line(fenetre, couleur_ombre, (largeur_fenetre // 2 - 150 + offset_x + 1, 300 + offset_y + 1), (largeur_fenetre // 2 - 150 + offset_x + 1, 100 + offset_y + 1), 5)
            pygame.draw.line(fenetre, couleur_bois, (largeur_fenetre // 2 + offset_x, 180 + offset_y), (largeur_fenetre // 2 + offset_x, 250 + offset_y), 5)
        if erreurs > 4:
            pygame.draw.line(fenetre, couleur_ombre, (largeur_fenetre // 2 - 150 + offset_x + 1, 300 + offset_y + 1), (largeur_fenetre // 2 - 150 + offset_x + 1, 100 + offset_y + 1), 5)
            pygame.draw.line(fenetre, couleur_bois, (largeur_fenetre // 2 + offset_x, 250 + offset_y), (largeur_fenetre // 2 - 30 + offset_x, 300 + offset_y), 5)
        if erreurs > 5:
            pygame.draw.line(fenetre, couleur_ombre, (largeur_fenetre // 2 - 150 + offset_x + 1, 300 + offset_y + 1), (largeur_fenetre // 2 - 150 + offset_x + 1, 100 + offset_y + 1), 5)
            pygame.draw.line(fenetre, couleur_bois, (largeur_fenetre // 2 + offset_x, 250 + offset_y), (largeur_fenetre // 2 + 30 + offset_x, 300 + offset_y), 5)

        pygame.display.flip()

        if set(mot_a_trouver) <= lettres_trouvees:
            victoire = True
            score_joueur += 10 * (erreurs_max - erreurs)
            print("Score:", score_joueur)

            with open("fichiers texte/scores.txt", "a") as fichier_scores:
                fichier_scores.write(f"{nom_joueur.upper()} : {score_joueur}\n")

            break
        elif erreurs == erreurs_max:
            defaite = True
            break

    # Déplacement de l'affichage du score à l'extérieur de la boucle
    if victoire:
        message_victoire_ombre, rect_victoire_ombre, message_victoire, rect_victoire = rendre_texte_avec_fond(f"Félicitations ! Vous avez trouvé le mot: {mot_a_trouver}", font_grande, (255, 255, 255), couleur_fond_rectangle, (largeur_fenetre // 2, hauteur_fenetre // 1.2))
        fenetre.blit(message_victoire_ombre, rect_victoire_ombre)
        fenetre.blit(message_victoire, rect_victoire)

    elif defaite:
        score_joueur = 0  # Réinitialisation du score à 0 sur défaite
        message_defaite_ombre, rect_defaite_ombre, message_defaite, rect_defaite = rendre_texte_avec_fond(f"Désolé, vous avez atteint le nombre maximum d'erreurs. Le mot était: {mot_a_trouver}", font_petite, (255, 255, 255), couleur_fond_rectangle, (largeur_fenetre // 2, hauteur_fenetre // 1.2))
        fenetre.blit(message_defaite_ombre, rect_defaite_ombre)
        fenetre.blit(message_defaite, rect_defaite)

    pygame.display.flip()

    pygame.time.delay(10000)
    pygame.quit()
    sys.exit()
    
# Création de la fenêtre
fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre), pygame.HWSURFACE | pygame.DOUBLEBUF)
pygame.display.set_caption("Menu Principal")

# Chargement de l'image du fond d'écran du menu
fond_ecran_menu = pygame.image.load("images/image-fond.jpg")
fond_ecran_menu = pygame.transform.scale(fond_ecran_menu, (largeur_fenetre, hauteur_fenetre))

# Chargement de l'image du fond d'écran de la fenêtre de jeu
fond_ecran_jeu = pygame.image.load("images/jeu-fond.jpg")
fond_ecran_jeu = pygame.transform.scale(fond_ecran_jeu, (largeur_fenetre, hauteur_fenetre))

# Position des boutons
rect_jouer = pygame.Rect((largeur_fenetre // 2 - 100, 120, 200, 50))
rect_inserer = pygame.Rect((largeur_fenetre // 2 - 150, 180, 300, 50))
input_rect = pygame.Rect((largeur_fenetre // 2 - 150, 240, 300, 50))
rect_scores = pygame.Rect((largeur_fenetre // 2 - 150, 500, 300, 60))
couleur_fond_bouton = (80, 80, 80)
border_radius = 10

insert_mode = False
nouveau_mot = ""

# Boucle principale du menu
while True:
    fenetre.blit(fond_ecran_menu, (0, 0))

    text_menu_principal = font_menu_principal.render("Menu Principal", True, (50, 50, 50))
    text_rect_menu_principal = text_menu_principal.get_rect(center=(largeur_fenetre // 2, 50))
    fenetre.blit(text_menu_principal, text_rect_menu_principal)

    pygame.draw.rect(fenetre, couleur_fond_bouton, rect_jouer, border_radius=border_radius)
    pygame.draw.rect(fenetre, couleur_texte, rect_jouer, 2, border_radius=border_radius)
    text_jouer = font_grande.render("Jouer", True, couleur_texte)
    text_rect_jouer = text_jouer.get_rect(center=rect_jouer.center)
    fenetre.blit(text_jouer, text_rect_jouer)

    pygame.draw.rect(fenetre, couleur_fond_bouton, rect_inserer, border_radius=border_radius)
    pygame.draw.rect(fenetre, couleur_texte, rect_inserer, 2, border_radius=border_radius)
    text_inserer = font_grande.render("Insérer un mot", True, couleur_texte)
    text_rect_inserer = text_inserer.get_rect(center=rect_inserer.center)
    fenetre.blit(text_inserer, text_rect_inserer)

    pygame.draw.rect(fenetre, couleur_fond_bouton, rect_scores, border_radius=border_radius)
    pygame.draw.rect(fenetre, couleur_texte, rect_scores, 2, border_radius=border_radius)
    text_scores = font_grande.render("Tableau Des Scores", True, couleur_texte)
    text_rect_scores = text_scores.get_rect(center=rect_scores.center)
    fenetre.blit(text_scores, text_rect_scores)

    if insert_mode:
        pygame.draw.rect(fenetre, couleur_fond_bouton, input_rect, border_radius=border_radius)
        pygame.draw.rect(fenetre, couleur_texte, input_rect, 2, border_radius=border_radius)
        text_annuler = font_grande.render("Annuler", True, couleur_texte)
        text_rect_annuler = text_annuler.get_rect(center=input_rect.center)
        fenetre.blit(text_annuler, text_rect_annuler)

        text_saisie = font_petite.render(nouveau_mot, True, couleur_text_pendu)
        text_rect_saisie = text_saisie.get_rect(center=(largeur_fenetre // 2, 300))
        fenetre.blit(text_saisie, text_rect_saisie)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if rect_jouer.collidepoint(event.pos):
                jouer_pendu()
            elif rect_inserer.collidepoint(event.pos):
                insert_mode = True
            elif rect_scores.collidepoint(event.pos):
                afficher_tableau_scores()
            elif insert_mode and input_rect.collidepoint(event.pos):
                insert_mode = False
                nouveau_mot = ""

        if insert_mode and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                with open("fichiers texte/mots.txt", "a") as fichier:
                    fichier.write(nouveau_mot + "\n" if not nouveau_mot.endswith("\n") else nouveau_mot)
                insert_mode = False
                nouveau_mot = ""
            elif event.key == pygame.K_BACKSPACE:
                nouveau_mot = nouveau_mot[:-1]
            else:
                nouveau_mot += event.unicode

    def afficher_tableau_scores():
        fond_ecran_scores = pygame.image.load("images/image-scores.jpg")
        fond_ecran_scores = pygame.transform.scale(fond_ecran_scores, (largeur_fenetre, hauteur_fenetre))

        fenetre.blit(fond_ecran_scores, (0, 0))
        pygame.display.set_caption("Tableau Des Scores")

        with open("fichiers texte/scores.txt", "r") as fichier_scores:
            scores = fichier_scores.readlines()

        y_position = 100
        font_petite = pygame.font.Font("polices/Courier New.ttf", 20)

        for score in scores:
            text_score = font_petite.render(score.strip(), True, couleur_text_pendu)
            text_rect_score = text_score.get_rect(center=(largeur_fenetre // 2, y_position))
            fenetre.blit(text_score, text_rect_score)
            y_position += 30

        font_petite = pygame.font.Font("polices/Courier New.ttf", 10)

        text_retour = font_petite.render("Cliquez n'importe où sur la page pour revenir au Menu Principal", True, couleur_text_pendu)
        text_rect_retour = text_retour.get_rect(center=(largeur_fenetre // 2, hauteur_fenetre - 100))
        fenetre.blit(text_retour, text_rect_retour)

        pygame.display.flip()

        attendre_clic()

    def attendre_clic():
        attente = True
        while attente:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    attente = False