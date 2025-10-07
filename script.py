# -*- coding: utf-8 -*-

#Andrei

import tkinter
from tkinter import ttk
import random
import sqlite3

def centrer_fenetre():
    """Cette fonction calculera la position a la quelle il faut placer la fenetre pour quelle soit au centrede l'écran"""
    # Obtient la largeur de l'écran
    largeur_ecran = fenetre.winfo_screenwidth()
    # Obtient la hauteur de l'écran
    hauteur_ecran = fenetre.winfo_screenheight()
    largeur_fenetre = 700  # Largeur de la fenêtre
    hauteur_fenetre = 500  # Hauteur de la fenêtre
    # Calcule la position X pour centrer la fenêtre horizontalement
    x_position = (largeur_ecran - largeur_fenetre) // 2
    # Calcule la position Y pour centrer la fenêtre verticalement
    y_position = (hauteur_ecran - hauteur_fenetre) // 2
    
    # Configure la géométrie de la fenêtre pour la centrer en fonction de son angfle supérieur gauche
    fenetre.geometry(f"{largeur_fenetre}x{hauteur_fenetre}+{x_position}+{y_position}")
    
    
    
    
def menu():
    """cette fonctioin permet de configurer le bouton "MENU" qui va me permettre de retourner au menu"""
    #i=on detruit l'application comme pour la fermer 
    fenetre.destroy()
    #puis on la reconstruit en appelant la fonction de base qui contient toute la structure de la premiere page
    start_application()
    
    
    
    
def page_ajouter():
    """Cette fonction va creer la premiere page lorsque l'on va clicker sur le bouton ajouter"""
    #tout d'abord on va détruire tout ce que la page principale possede 
    for widget in fenetre.winfo_children():
        widget.destroy()
        
    #on cree ensuite un label qui va contenir tout ce que la page aura besoin    
    page_ajouter = tkinter.Label(fenetre, background=couleur_principale)
    #on applique et on utilise expand pour le centrer au milieu de la page
    page_ajouter.pack(expand=True)
        
    #on va creer un label pour du texte, qui va se trouver dans le label page_ajouter qu'on a cree precedement
    texte = tkinter.Label(page_ajouter, text = "Entrez le nom du site :", background=couleur_principale)
    #on va le cetrer et au fur et a mesure que on ajoutera des nouveaux widget au label page_ajouter en utilisant
    #expand ils vont se superposer automatiquement
    texte.pack(expand=True)
    
    #on va creer un bouton menu qui va se trouver en dehors du Label page_ajouter on va retirer les effets de style pour l'héstétique
    bouton_menu = tkinter.Button(fenetre, text="MENU", command=menu, bg=couleur_principale,relief="solid", bd=0, activebackground=couleur_principale, highlightthickness=0 ,borderwidth=1)
    #on va appliquer puis on va le mettre en bas a droite de la page avec une separation de la bordure,sw s'est pour spécifier quel
    #point doit etre centré popur notre cas s'est le coté sud ouest (pour sud west) 
    bouton_menu.pack(side=tkinter.BOTTOM,anchor='sw',padx=10, pady = 10)
    
    #on cree un champ de texte dans lequel on va entrer l'indormation que l'on va recuprere par la suite
    global champ_texte
    #on utilise donc la méthode Entry, et ce champ de texte va se retrouver en dessous du texte que l'onn a creer precedement 
    #dans le label page_ajouter
    champ_texte = tkinter.Entry(page_ajouter)
    #on applique et on utilise expand pour le centrer automatiquement en dessous du text
    champ_texte.pack(expand = True)
    #cette commande va nous permettre de directement ecrire sur notre clavier sans avoir a clicker sur le champ de texte pour écrire
    champ_texte.focus_set()
    
    #on utilise cette focntion qui lorsque l'onva clicker sur entrer elle va lancer la fonction enter_pressed
    champ_texte.bind("<Return>", enter_pressed)
    
def enter_pressed(event):
    """cette fonction va se lancer lorsque l'evenement entrer va se produire d'ou l'existance de "event" en argument"""
    #on va globaliser la variable pour la recuperer plus tard 
    global site_entre
    #on y met dans cette variable ce qui existe dans le champ_texte en utilisant une fonction .get()
    site_entre = champ_texte.get()
    #puis on lance la fonction suivante qui va permettre de l'ajouter a la base de données
    ajout_site()

def ajout_site():
    """cette fonction va verifier si une variable existe dans la base de donnees et recuperer son id si oui et 
    l'ajouter si non et recuperer son id aussi"""
    #on cree la variable nouveau_site qui va stocker l'id du site qu'il soit eistant ou non
    global nouveau_site
    #on se connecte a la base de donne situé dans le dossier
    connexion = sqlite3.connect("password_database.db")
    #on compte le nombre de fois que le site entré existe dans la base de donnes il renvoie soit 0 soit un car on ne
    #pourra pas entrer plusieures fois le meme site
    request = connexion.execute("SELECT Count(*) FROM Sites WHERE nom = '"+ site_entre +"'") 
    #onn utilise fetchone et  [0] pour recuperer le premier resultat de la premiere ligne de ce qu'il nous a renvoyé
    count = request.fetchone()[0]
    #si count = 0 alors le site n'est pas dans la base de données
    if count == 0:
        #il faut donc l'ajouter en utilisant une requete INSERT
        connexion.execute("INSERT INTO Sites (nom) VALUES ('"+ site_entre +"')")
        #aprés l'avoir inserer on va recuperer l'id du site pour l'utiliser plus tard avec une requete select
        request2 = connexion.execute("SELECT id_site FROM Sites WHERE nom = '"+site_entre+"'")
        #on reutilise fetchone pôur recuperer le premier resultat de la premiere ligne qu'il va nous renvoyer
        nouveau_site = request2.fetchone()[0]
    #si count n'est pas egal a 0 alors le site existe déjà
    else:
        #dans ce cas on va juste recuperer l'id du site pour le reutiliser plus tardavec une requete select
        request2 = connexion.execute("SELECT id_site FROM Sites WHERE nom = '"+site_entre+"'")
        #on reutilise fetchone pôur recuperer le premier resultat de la premiere ligne qu'il va nous renvoyer
        nouveau_site = request2.fetchone()[0]
    #on applique ce qu'on a fait dans le cas ou on aura inseré le site
    connexion.commit()
    #on coupe la connexion
    connexion.close()
    #puis on lance la prochaine page avec la fonction page_ajouter2()
    page_ajouter2()
    
    
    
    
def page_ajouter2():
    """Cette focntion ressemble a la precedente mais cette fois ci elle va nous permettre de recuperer
    le nom d'utilisateur"""
    for widget in fenetre.winfo_children():
        widget.destroy()
        
    page_ajouter2 = tkinter.Label(fenetre, background=couleur_principale)
    page_ajouter2.pack(expand=True)
    
    texte = tkinter.Label(page_ajouter2, text = "Entrez le nom d'utilisateur :", background=couleur_principale)
    texte.pack(expand=True)
    
    bouton_menu = tkinter.Button(fenetre, text="MENU", command=menu, bg=couleur_principale,relief="solid", bd=0, activebackground=couleur_principale, highlightthickness=0 ,borderwidth=1)
    bouton_menu.pack(side=tkinter.BOTTOM,anchor='sw',padx=10, pady = 10)
    
    global champ_texte
    champ_texte = tkinter.Entry(page_ajouter2)
    champ_texte.pack(expand = True)
    champ_texte.focus_set()
    
    champ_texte.bind("<Return>", enter_pressed2)
    
def page_ajouter_secondaire():
    """Cette focntion est la meme que la precedente mais elle va se lancer si jamais le compte existe déjà
    pour prevenir l'utilisateur que il existe déjà"""
    for widget in fenetre.winfo_children():
        widget.destroy()
        
    page_ajouter2 = tkinter.Label(fenetre, background=couleur_principale)
    page_ajouter2.pack(expand=True)
    
    
    #S'est la seule difference entre l'ancienne fonction et celle la on averti l'utilisateur avec du texte en ROUGE
    texte = tkinter.Label(page_ajouter2, text = "Ce compte existe déjà !", background=couleur_principale, fg="red")
    texte.pack(expand=True)
    
    texte1 = tkinter.Label(page_ajouter2, text = "Entrez le nom d'utilisateur :", background=couleur_principale)
    texte1.pack(expand=True)
    
    bouton_menu = tkinter.Button(fenetre, text="MENU", command=menu, bg=couleur_principale,relief="solid", bd=0, activebackground=couleur_principale, highlightthickness=0 ,borderwidth=1)
    bouton_menu.pack(side=tkinter.BOTTOM,anchor='sw',padx=10, pady = 10)
    
    global champ_texte
    champ_texte = tkinter.Entry(page_ajouter2)
    champ_texte.pack(expand = True)
    champ_texte.focus_set()
    
    champ_texte.bind("<Return>", enter_pressed2)
    
def enter_pressed2(event):
    #on va recuperer le nom que l'utilisateur a entré
    global nom_entre
    #on utilise .get() pour cela 
    nom_entre = champ_texte.get()
    #on lance la prochaine fonction
    verification_compte()
    
def verification_compte():
    """Cette focntion va nous permettre de verifier si le compte assigné au site entré par l'utilisateur existe déjà
    car si oui, bah on peut pas avoir deux comptes avec les memes identifiants sur des sites donc ce n'est pas possible"""
    #on se connecte a la base de données
    connexion = sqlite3.connect("password_database.db")
    #on utilise la meme requete Select Count(*) pour verifier si sa existe déjà
    request = connexion.execute("SELECT Count(*) FROM utilisateur WHERE id_site = "+ str(nouveau_site) +" AND identifiant = '"+ nom_entre +"'")
    #on réutilise fetchone pour recuperer la premiere valeur 
    count = request.fetchone()[0]
    #si count est different de 0 alors le compte existe déjà
    if count != 0:
        #donc on le renvoi a la page secondaire qui va l'en avertir
        page_ajouter_secondaire()
    #sinon sa veut dire qu'il n'existe pas 
    else:
        #on lance donc la fonction pour la suite
        page_ajouter3()
    
    
    
    
def page_ajouter3():
    """Cette fonction va nous permettre de savoir si l'utilisateur souhaite un mot de passe généré aléatoirement
    ou si il veut le choisur lui meme"""
    for widget in fenetre.winfo_children():
        widget.destroy()
        
    page_ajouter3 = tkinter.Label(fenetre, background=couleur_principale)
    page_ajouter3.pack(expand=True)
    
    texte = tkinter.Label(page_ajouter3, text = "Voulez vous un mot de passe aléatoire ou en saisir un ?", background=couleur_principale)
    texte.pack(expand=True)
    
    #on crée le cadre pour les boutons comme a la page principale
    cadre_boutons2 = tkinter.Frame(page_ajouter3, bg=couleur_principale)
    cadre_boutons2.pack(pady = 10)
    #le bouton Aléatoire va nous permettre de lancer la fonction page_aleatoire 
    bouton_aleatoire = tkinter.Button(cadre_boutons2, text="Aléatoire", command=page_aleatoire, bg=couleur_principale,bd=0, relief="solid", activebackground=couleur_principale,highlightthickness=0, borderwidth=1)
    bouton_aleatoire.pack(side = tkinter.LEFT, padx=40)
    #le bouton Saisir va nous permettre de lancer la fonction page_saisir 
    bouton_saisir = tkinter.Button(cadre_boutons2, text="Saisir", command=page_saisir, bg=couleur_principale, bd=0, relief="solid", activebackground=couleur_principale, highlightthickness=0,borderwidth=1)
    bouton_saisir.pack(side = tkinter.LEFT, padx=40)
    
    bouton_menu = tkinter.Button(fenetre, text="MENU", command=menu, bg=couleur_principale,relief="solid", bd=0, activebackground=couleur_principale, highlightthickness=0 ,borderwidth=1)
    bouton_menu.pack(side=tkinter.BOTTOM,anchor='sw',padx=10, pady = 10)




def verification_mdp(password):
    """Cette fonction va nous permetre de savoir si le mot de passe est sécurisée"""
    #on crée 4 variables dans lesquelles on va separer les characteres de la variable characteres de la fonction en dessous
    #sa va nous permettre de faire une verification séparée pour l'existance de chaque charactere different dans le mot de 
    #passe qui va se generer dans la fonction en dessous
    lettre_min = "azertyuiopqsdfghjklmwxcvbn"
    lettre_maj = "AZERTYUIOPQSDFGHJKLMWXCVBN"
    chiffres = "0123456789"
    symboles = "&-_@=+%*!:/;.,?"
    #on cree donc des variables de verification qui sont initialisées a False
    a = False; b = False; c = False; d = False
    #on va faire chque verification pour voir si il y a au moins un charactere de chque variable dans la variable password
    #si oui alors on les met a True
    for char in lettre_min:
        if char in password:
            a = True
    for char in lettre_maj:
        if char in password:
            b = True
    for char in chiffres:
        if char in password:
            c = True  
    for char in symboles:
        if char in password:
            d = True
    #pour finir on fait le dernier test qui est de savoir si tout est bon
    if a == True and b == True and c == True and d == True:
        #alors on renvoi true ce qui va nous permetre de debloquer la boucle while dans la fonction generateur()
        return True
    
def generateur():
    """Cette fonction va nous permettre de créer un mot de passe super sécurisé"""
    #on crée la variable password en global pour la reutiliser plus tard
    global password
    #le password est vide pour l'instant
    password = ""
    mini = 8#le minimum s'est le minimum de de la taille du mot de passe
    maxi = 32#le macimum pour le maximum de la taille du mot de passe
    #on crée une variable qui va contenir tout les characteres Majuscules minuscules chiffres et certains symboles
    #que l'on va utiliser pour la génération du mot de passe
    characteres = "azertyuiopqsdfghjklmwxcvbnAZERTYUIOPQSDFGHJKLMWXCVBN0123456789&-_@=+%*!:/;.,?"
    #on va créer une boucle qui va s'arreter seulement si le mot de passe est sécurisé selon la fonction verification_mdp
    while verification_mdp(password) != True:
        #on va y mettre un boucle qui va se repeter au hasard entre mini et maxi fois 
        for i in range(random.randint(mini,maxi)):
            #puis a chque fois un charactere au hasard depuis la variable characteres va s'ajouter a la variable password
            password += random.choice(characteres)
    #si sa s'arrete alors on renvoi le resultat donc le mot de passe
    return password

def page_aleatoire():
    """Cette focntion va afficher a l'utilisateur le mot de passe qui a ete généré automatiquement et grace a laquelle il
    va pourvoir aussi le copier"""
    for widget in fenetre.winfo_children():
        widget.destroy()
    #on va appeler la fonction generateur() qui va generer le mot de passe
    generateur()
    #vu que on la declaré en global on peut donc le recuperer
    global password
    
    page_aleatoire = tkinter.Label(fenetre, background=couleur_principale)
    page_aleatoire.pack(expand=True)

    
    texte = tkinter.Label(page_aleatoire, text = "Voici votre mot de passe :", background=couleur_principale)
    texte.pack(expand=True)
    #C'est ici que l'on va l'afficher, on y met un fond blanc pour que ce soit plus joli
    texte2 = tkinter.Label(page_aleatoire, text = password, background="white")
    texte2.pack(expand=True)
    #Ici on va créer le bouton Copier qui va permettre de copier le mot de passe dans le press papier si l'utilisateur le souhaite
    #il va lancer la fonction copier_mot_de_passe pour cela
    bouton_copier = tkinter.Button(page_aleatoire, text="Copier", command=copier_mot_de_passe, bg=couleur_principale, bd=0, relief="solid", activebackground=couleur_principale, highlightthickness=0,borderwidth=1)
    bouton_copier.pack(expand = True,pady=3)
    
    bouton_menu = tkinter.Button(fenetre, text="MENU", command=menu, bg=couleur_principale,relief="solid", bd=0, activebackground=couleur_principale, highlightthickness=0 ,borderwidth=1)
    bouton_menu.pack(side=tkinter.BOTTOM,anchor='sw',padx=10, pady = 10)
    #on lance la prochaine fonction pour l'ajouter dans la base de donnée le mot de passe et l'utilisateur
    ajout_mot_de_passe2()
    
def ajout_mot_de_passe2():
    """cette fonction va se lancer apres avoir affiché le mot de passe a l'utilisateur elle va nous permettre de l'insérer dans 
    la base de données"""
    #on recuperer d'abord toutes les variables dont on aura besoin
    global nouveau_site
    global nom_entre
    global password
    #on se connecte a la base de données
    connexion = sqlite3.connect("password_database.db")
    #on insert le nom d'utilisateur le mot de passe au id_site correspondant
    connexion.execute("INSERT INTO utilisateur (id_site,identifiant,mdp) VALUES ('"+ str(nouveau_site) +"','"+ nom_entre +"','"+ password +"')")
    #on applique la modification
    connexion.commit()
    #puis on coupe la connexion
    connexion.close()
    
def copier_mot_de_passe():
    """cette fonction nous permet de copier le mot de passe dans le press papier si l'utilisatueur va cliquer sur le bouton
    copier"""
    #on recupere le mot de passe
    global password
    #on efface ce qu'il y a dans le press papier d'abord
    fenetre.clipboard_clear()
    #et on ajoute au press papier le password
    fenetre.clipboard_append(password)

    
    
    
def page_saisir():
    """Cette focntion va permettre a l'utilisateur de saisir son propre mot de passe elle sera active seulement si 
    l'utilisateur decide de clicker sur le bouton saisir"""
    for widget in fenetre.winfo_children():
        widget.destroy()
        
    page_saisir = tkinter.Label(fenetre, background=couleur_principale)
    page_saisir.pack(expand=True)
    
    texte = tkinter.Label(page_saisir, text = "Entrez votre mot de passe :", background=couleur_principale)
    texte.pack(expand=True)
    
    bouton_menu = tkinter.Button(fenetre, text="MENU", command=menu, bg=couleur_principale,relief="solid", bd=0, activebackground=couleur_principale, highlightthickness=0 ,borderwidth=1)
    bouton_menu.pack(side=tkinter.BOTTOM,anchor='sw',padx=10, pady = 10)
    
    #On cree donc le champ de texte pour saisir le mot de passe
    global champ_texte
    champ_texte = tkinter.Entry(page_saisir)
    champ_texte.pack(expand = True)
    champ_texte.focus_set()
    
    champ_texte.bind("<Return>", enter_pressed3)
    
def page_saisir2():
    """Cette fonction est la meme que la precedente mais la seule difference est que elle averti l'utilisateur dans le cas 
    ou le mot de passe ne correspond pas aux caractéristiques permettant de verifier si le mot de passe est sécurisé
    elle se lance seulement si le mot de passe entré n'est pas sécurisé"""
    for widget in fenetre.winfo_children():
        widget.destroy()
        
    page_saisir = tkinter.Label(fenetre, background=couleur_principale)
    page_saisir.pack(expand=True)
    
    #Voici l'avertissement en ROUGE
    texte_attention = tkinter.Label(page_saisir, text = "Attention le mot de passe doit etre entre 8 et 32 characteres.", background=couleur_principale, fg="red")
    texte_attention.pack(expand=True)
    #Voici la suite de l'avertissement 
    texte_attention2 = tkinter.Label(page_saisir, text = "Il doit comporter des majuscules des minuscules des chiffres et des symboles !", background=couleur_principale, fg="red")
    texte_attention2.pack(expand=True)
    
    texte = tkinter.Label(page_saisir, text = "Entrez votre mot de passe :", background=couleur_principale)
    texte.pack(expand=True)
    
    bouton_menu = tkinter.Button(fenetre, text="MENU", command=menu, bg=couleur_principale,relief="solid", bd=0, activebackground=couleur_principale, highlightthickness=0 ,borderwidth=1)
    bouton_menu.pack(side=tkinter.BOTTOM,anchor='sw',padx=10, pady = 10)
    #Ici s'est le meme champ de texte qui va lancer la meme fonction que precedement si l'utilisateur appuie sur la touche entrer
    global champ_texte
    champ_texte = tkinter.Entry(page_saisir)
    champ_texte.pack(expand = True)
    champ_texte.focus_set()
    
    champ_texte.bind("<Return>", enter_pressed3)
    
def enter_pressed3(event):
    global password
    global nouveau_site
    global nom_entre
    password = champ_texte.get()
    #On va tester pour voir si le mot de passe est sécurisé 
    if verification_mdp(password) == True:
        #si oui alors on va l'ajouter en lansant la focntion ajout_mot_de_passe
        ajout_mot_de_passe()
    #et si il ne l'est pas
    else:
        #on lance la fonction page_saisir2() qui va prévenir l'utilisateur que le mot de passe n'est pas sécurisé et 
        #que il y a donc certains criteres a respecter
        page_saisir2()
        
def ajout_mot_de_passe():
    """Cette focntion va nous permettre d'ajouter le mot de passe dans la base de données"""
    global nouveau_site
    global nom_entre
    global password
    #on ouvre la connexion
    connexion = sqlite3.connect("password_database.db")
    #on insert le mot de passe l'identifiant au siote correspondant 
    connexion.execute("INSERT INTO utilisateur (id_site,identifiant,mdp) VALUES ('"+ str(nouveau_site) +"','"+ nom_entre +"','"+ password +"')")
    #on applique les modifications
    connexion.commit()
    #on ferme la connexion
    connexion.close()
    #puis on retourne directement eu menu en lancant la fonction menut()
    menu()
        
        
        
        
def page_rechercher():
    """cette focntion est la fonction qui va se lancer si l'utilisateur va appuier sur le bouton rechercher, elle 
    contient 3 options différentes"""
    for widget in fenetre.winfo_children():
        widget.destroy()
        
    page_rechercher = tkinter.Label(fenetre, background=couleur_principale)
    page_rechercher.pack(expand=True)
    
    texte = tkinter.Label(page_rechercher, text = "Que souhaitez vous faire: Afficher, Modifier ou Supprimer ?", background=couleur_principale)
    texte.pack(expand=True)
    #creation d'un cadre pour les boutons 
    cadre_boutons = tkinter.Frame(page_rechercher, bg=couleur_principale)
    cadre_boutons.pack(expand=True)
    
    #le bouton afficher va permettre de d'afficher tout les comptes et mot de passes pour un site choisit ce bouton lance
    #la fonction page_afficher
    bouton_afficher = tkinter.Button(cadre_boutons, text="AFFICHER", command=page_afficher,bg=couleur_principale,relief="solid", bd=0, activebackground=couleur_principale, highlightthickness=0 ,borderwidth=1)
    bouton_afficher.pack(side = tkinter.LEFT, padx=10)
    
    #le bouton modifier va permettre de modifier les infirmations d'un compte sur un site soit le mot de passe
    #soit le nom d'utilisateur ou les deux, il lancera la fonction page_modifier
    bouton_modifier = tkinter.Button(cadre_boutons, text="MODIFIER", command=page_modifier,bg=couleur_principale,relief="solid", bd=0, activebackground=couleur_principale, highlightthickness=0 ,borderwidth=1)
    bouton_modifier.pack(side = tkinter.LEFT, padx=10)
    
    #le bouton supprimer va permettre de supprimer un compte en fonction du site et de l'identifiant pas besoin du
    #mot de passe, il lancera la fonction page_supprimer
    bouton_supprimer = tkinter.Button(cadre_boutons, text="SUPPRIMER", command=page_supprimer,bg=couleur_principale,relief="solid", bd=0, activebackground=couleur_principale, highlightthickness=0 ,borderwidth=1)
    bouton_supprimer.pack(side = tkinter.LEFT, padx=10)
    
    bouton_menu = tkinter.Button(fenetre, text="MENU", command=menu, bg=couleur_principale,relief="solid", bd=0, activebackground=couleur_principale, highlightthickness=0 ,borderwidth=1)
    bouton_menu.pack(side=tkinter.BOTTOM,anchor='sw',padx=10, pady = 10)
    
    
    
    
def page_afficher():
    """Cette fonction va se lancer si l'utilisateur click sur le bouton afficher , elle va afficher un page lui demandant 
    le site pour lequel il veut voir les comptes, et elle va notamment afficher les sites déjà existants"""
    for widget in fenetre.winfo_children():
        widget.destroy()
        
    page_afficher = tkinter.Label(fenetre, background=couleur_principale)
    page_afficher.pack(expand=True)
    
    #on se connecte a la base de données
    connexion = sqlite3.connect("password_database.db")
    #puis on va recuperer tous les sites existants 
    request = connexion.execute("SELECT nom FROM Sites")
    #on va recuperer ces noms sous forme de tuple qui contient seulement un seul element (un site)   
    liste_noms = request.fetchall()
    #on ferme la connexion
    connexion.close()
    
    # On crée une nouvelle liste pour stocker les noms des sites
    noms = []
    
    # On parcourt chaque tuple dans liste_noms
    for nom in liste_noms:
        # On ajoute le premier élément de chaque tuple à la liste noms
        noms.append(nom[0])
    
    #on va transformer sa en chaine de characteres en y mettant des espaces entre chaque valeur de la liste
    noms_espaces = ' '.join(noms)
    
    #Ici on va donc afficher tous les sites existants avec une option en plus qui va eviter a ce que la chaine de characteres 
    #noms_espaces ne séetende et sorte des bordures de l'application, on y met wraplength qui va definir la taille,
    #jusqua laquelle elle peut s'étendre s'est a dire 600
    texte = tkinter.Label(page_afficher, text = noms_espaces, background=couleur_principale, wraplength=600)
    texte.pack(expand=True)
        
    texte2 = tkinter.Label(page_afficher, text = "Pour lequel des sites suivants souhaitez vous voir les comptes ?", background=couleur_principale)
    texte2.pack(expand=True)
    
    bouton_menu = tkinter.Button(fenetre, text="MENU", command=menu, bg=couleur_principale,relief="solid", bd=0, activebackground=couleur_principale, highlightthickness=0 ,borderwidth=1)
    bouton_menu.pack(side=tkinter.BOTTOM,anchor='sw',padx=10, pady = 10)
    
    global champ_texte
    champ_texte = tkinter.Entry(page_afficher)
    champ_texte.pack(expand = True)
    champ_texte.focus_set()
    
    champ_texte.bind("<Return>", enter_pressed4)
    
def page_afficher2():
    """Cette focntion est la meme fonction que la precedente masi elle contient une chose en plus, un avertissement pour
    dire a l'utilisateur que le Site qu'il a entré n'existe pas dans la base de donnnées"""
    for widget in fenetre.winfo_children():
        widget.destroy()
        
    page_afficher = tkinter.Label(fenetre, background=couleur_principale)
    page_afficher.pack(expand=True)
    
    connexion = sqlite3.connect("password_database.db")
    request = connexion.execute("SELECT nom FROM Sites")
    liste_noms = request.fetchall()
    connexion.close()
    
    noms = []
    for nom in liste_noms:
        noms.append(nom[0])
        
    noms_espaces = ' '.join(noms)
    
    texte = tkinter.Label(page_afficher, text = "Ce site n'existe pas dans la base de données !", background=couleur_principale, fg="red")
    texte.pack(expand=True)
    
    texte1 = tkinter.Label(page_afficher, text = noms_espaces, background=couleur_principale, wraplength=600)
    texte1.pack(expand=True)
        
    texte2 = tkinter.Label(page_afficher, text = "Pour lequel des sites suivants souhaitez vous voir les comptes ?", background=couleur_principale)
    texte2.pack(expand=True)
    
    bouton_menu = tkinter.Button(fenetre, text="MENU", command=menu, bg=couleur_principale,relief="solid", bd=0, activebackground=couleur_principale, highlightthickness=0 ,borderwidth=1)
    bouton_menu.pack(side=tkinter.BOTTOM,anchor='sw',padx=10, pady = 10)
    
    global champ_texte
    champ_texte = tkinter.Entry(page_afficher)
    champ_texte.pack(expand = True)
    champ_texte.focus_set()
    
    champ_texte.bind("<Return>", enter_pressed4)
    
def enter_pressed4(event):
    global site_entre
    site_entre = champ_texte.get()
    verification_site()
    
def verification_site():
    """cette focntion va permettre de verifier l'existence du site"""
    global site_entre
    global nouveau_site
    connexion = sqlite3.connect("password_database.db")
    #avec la requete Select count(*) on voit si site_entre existe déjà
    request = connexion.execute("SELECT Count(*) FROM Sites WHERE nom = '"+ site_entre +"'") 
    #on recupere l'information de la premiere ligne
    count = request.fetchone()[0]
    #si count est different de 0 sa veut dire que le site existe
    if count != 0:
        #on recupere donc l'id du site auquel il correspond pour l'utiliser plus tard
        request2 = connexion.execute("SELECT id_site FROM Sites WHERE nom = '"+ site_entre +"'")
        #on recupere l'information
        nouveau_site = request2.fetchone()[0]
        #puis on lance la page qui va aficher la liste des comptes correspondant a ce site
        affiche_comptes_du_site()
    #si le site n'existe pas
    else:
        #on va atterir sur page_afficher2() qui va avvertir l'utilisateur que le site qu'il a entré n'existe pas
        page_afficher2()
    connexion.commit()
    connexion.close()
    
def affiche_comptes_du_site():
    """Cette fonction va afficher une page qui va afficher sous forme de tableau les identifiants puis les mot de passes 
    pour le site qu'il a entré"""
    global nouveau_site
    
    for widget in fenetre.winfo_children():
        widget.destroy()
        
    # Création du Treeview pour afficher les données, avec deux colonnes identifiant et Mot de passe
    tree = ttk.Treeview(fenetre, columns=("Identifiant", "Mot de Passe"), show="headings")
    #configuration des entetes et colonnes
    tree.heading("Identifiant", text="Identifiant")
    tree.heading("Mot de Passe", text="Mot de Passe")
    #on applique et on y met fill... pour remplir toute la page de l'application avec le tableau
    tree.pack(fill=tkinter.BOTH, expand=True)
    
    #on se connecte a la base de données
    connexion = sqlite3.connect("password_database.db")
    #on y recuperer l'identifiant et le mot de passe de l'id_site
    request = connexion.execute("SELECT identifiant, mdp FROM utilisateur WHERE id_site = '"+ str(nouveau_site) +"'")
    #le resultat sera sous forme de liste de tuple
    data = request.fetchall()
    #on ferme la connexion
    connexion.close()
    
    #on va recuperer l'identifiant et le mot_de_passe a l'aide d'une boucle for pour chaque tuple dans la liste data
    for i, (identifiant, mot_de_passe) in enumerate(data):
        #on va ensuite inserer ces deux valeurs dans le Treeview, on spécifie avec "" que la nouvelle ligne doit etre inséré
        #au niveau le plus haut du tableau, et end pour dire que la nouvelle ligne doit etre inséré a la suite des lignes
        #déjà existentes
        tree.insert("", "end", values=(identifiant, mot_de_passe))
        
    #On y place le bouton pour retourner au menu
    bouton_menu = tkinter.Button(fenetre, text="MENU", command=menu, bg=couleur_principale,relief="solid", bd=0, activebackground=couleur_principale, highlightthickness=0 ,borderwidth=1)
    bouton_menu.pack(side=tkinter.BOTTOM,anchor='sw',padx=10, pady = 10)
    
    
    
    
def page_modifier():
    """Cette focntion va etre lancé si l'utilisateur clique sur le bouton modifier elle va demander a l'utilisateur 
    sur quel site sougaite t'il apporter des modifications a ses comptes"""
    for widget in fenetre.winfo_children():
        widget.destroy()
        
    page_modifier = tkinter.Label(fenetre, background=couleur_principale)
    page_modifier.pack(expand=True)
     
    connexion = sqlite3.connect("password_database.db")
    request = connexion.execute("SELECT nom FROM Sites")
    liste_noms = request.fetchall()
    connexion.close()
     
    noms = []
    for nom in liste_noms:
        noms.append(nom[0])
         
    noms_espaces = ' '.join(noms)
     
    texte = tkinter.Label(page_modifier, text=noms_espaces, background=couleur_principale, wraplength=600)
    texte.pack(expand=True)

    texte1 = tkinter.Label(page_modifier, text = "Pour quel site souhaitez vous modifier une information des comptes ?", background=couleur_principale)
    texte1.pack(expand=True)
     
    bouton_menu = tkinter.Button(fenetre, text="MENU", command=menu, bg=couleur_principale,relief="solid", bd=0, activebackground=couleur_principale, highlightthickness=0 ,borderwidth=1)
    bouton_menu.pack(side=tkinter.BOTTOM,anchor='sw',padx=10, pady = 10)
     
    global champ_texte
    champ_texte = tkinter.Entry(page_modifier)
    champ_texte.pack(expand = True)
    champ_texte.focus_set()
     
    champ_texte.bind("<Return>", enter_pressed7)
    
def page_modifier2():
    """Cette focntion est la meme que la precedente mais elle va avertir l'utilisateur que le site n'existe pas si il n'existe
    pas"""
    for widget in fenetre.winfo_children():
        widget.destroy()
        
    page_modifier = tkinter.Label(fenetre, background=couleur_principale)
    page_modifier.pack(expand=True)
     
    connexion = sqlite3.connect("password_database.db")
    request = connexion.execute("SELECT nom FROM Sites")
    liste_noms = request.fetchall()
    connexion.close()
     
    noms = []
    for nom in liste_noms:
        noms.append(nom[0])
         
    noms_espaces = ' '.join(noms)
    
    #Texte d'avertissement en rouge
    texte = tkinter.Label(page_modifier, text="Ce site n'est pas enregistré !", background=couleur_principale, fg="red")
    texte.pack(expand=True)
     
    texte1 = tkinter.Label(page_modifier, text=noms_espaces, background=couleur_principale, wraplength=600)
    texte1.pack(expand=True)

    texte2 = tkinter.Label(page_modifier, text = "Pour quel site souhaitez vous modifier une information des comptes ?", background=couleur_principale)
    texte2.pack(expand=True)
     
    bouton_menu = tkinter.Button(fenetre, text="MENU", command=menu, bg=couleur_principale,relief="solid", bd=0, activebackground=couleur_principale, highlightthickness=0 ,borderwidth=1)
    bouton_menu.pack(side=tkinter.BOTTOM,anchor='sw',padx=10, pady = 10)
     
    global champ_texte
    champ_texte = tkinter.Entry(page_modifier)
    champ_texte.pack(expand = True)
    champ_texte.focus_set()
     
    champ_texte.bind("<Return>", enter_pressed7)
    
def enter_pressed7(event):
    global site_entre
    site_entre = champ_texte.get()
    verification_site3()
    
def verification_site3():
    """Cette focntion va nous permettre de voir si le site entré par l'utilisateur existe, elle est lancé apres la fonction
    enter_pressed7 qui est lancé si l'utilisateur appuie sur entrer"""
    #on recupere les variables globales
    global site_entre
    global nouveau_site
    #on se connecte a la base de données
    connexion = sqlite3.connect("password_database.db")
    #on execute une requete select pour compter le nombre de fois que site_entre est present dans la base de donnees
    request = connexion.execute("SELECT Count(*) FROM Sites WHERE nom = '"+ site_entre +"'") 
    #on recupere la valeur 
    count = request.fetchone()[0]
    #si count different de 0 alors le site existe
    if count != 0:
        #donc on recupere l'id_site auquel il est relié
        request2 = connexion.execute("SELECT id_site FROM Sites WHERE nom = '"+ site_entre +"'")
        #on recupere la valeur dans la varibale nouveau_site globale
        nouveau_site = request2.fetchone()[0]
        #puis on lance la suite avec la fonction page_modifier3()
        page_modifier3()
    #sinon sa veut dire que le site n'existe pas
    else:
        #donc sa nous lance la fonction page_modifier2 qui est la copie de page_modifier() ùmùais avec un avertissement pour
        #dire que le site existe déjà
        page_modifier2()
    connexion.commit()
    connexion.close()
    
def page_modifier3():
    """Cette fonction va permettre a l'utilisateur de nous donner l'identifiant pour lequel il souahaite apporter
    des modifications"""
    for widget in fenetre.winfo_children():
        widget.destroy()
        
    page_modifier3 = tkinter.Label(fenetre, background=couleur_principale)
    page_modifier3.pack(expand=True)
    
    connexion = sqlite3.connect("password_database.db")
    #on va faire une requete sql pour voir les identifiants déjà existants pour les afficher par la suite
    request = connexion.execute("SELECT identifiant FROM utilisateur WHERE id_site ='"+ str(nouveau_site) +"'")
    #on les recupere dans une variable sous forme de liste de tuple 
    liste_noms = request.fetchall()
    #on ferme la connexion
    connexion.close()
    
    #on va utiliser la meme fonction que precedement pour mettre cette liste de tuple sous forme de chaine de charactere
    noms = []
    for nom in liste_noms:
        noms.append(nom[0])
        
    noms_espaces = ' '.join(noms)
    
    #on affiche la chaine de charactere de tous les identifiants existants
    texte = tkinter.Label(page_modifier3, text = noms_espaces, background=couleur_principale, wraplength=600)
    texte.pack(expand=True)
    
    texte1 = tkinter.Label(page_modifier3, text = "Pour quel identifiant souhaitez vous faire des modifications ?", background=couleur_principale)
    texte1.pack(expand=True)
    
    bouton_menu = tkinter.Button(fenetre, text="MENU", command=menu, bg=couleur_principale,relief="solid", bd=0, activebackground=couleur_principale, highlightthickness=0 ,borderwidth=1)
    bouton_menu.pack(side=tkinter.BOTTOM,anchor='sw',padx=10, pady = 10)
    
    global champ_texte
    champ_texte = tkinter.Entry(page_modifier3)
    champ_texte.pack(expand = True)
    champ_texte.focus_set()
    
    champ_texte.bind("<Return>", enter_pressed8)
    
def page_modifier4():
    """Cette focntion est la meme que la precedente la seule difference s'est qu'elle va avertir l'utilisateur que
    l'identifiant qu'il a entré n'existe pas dans la base de données elle sera lancé seulement si l'identifiant n'existe
    pas"""
    for widget in fenetre.winfo_children():
        widget.destroy()
        
    page_modifier4 = tkinter.Label(fenetre, background=couleur_principale)
    page_modifier4.pack(expand=True)
    
    connexion = sqlite3.connect("password_database.db")
    request = connexion.execute("SELECT identifiant FROM utilisateur WHERE id_site ='"+ str(nouveau_site) +"'")
    liste_noms = request.fetchall()
    connexion.close()
    
    noms = []
    for nom in liste_noms:
        noms.append(nom[0])
        
    noms_espaces = ' '.join(noms)
    
    texte = tkinter.Label(page_modifier4, text = "Cet identifiant n'existe pas !", background=couleur_principale, fg="red")
    texte.pack(expand=True)
    
    texte1 = tkinter.Label(page_modifier4, text = noms_espaces, background=couleur_principale, wraplength=600)
    texte1.pack(expand=True)
    
    texte2 = tkinter.Label(page_modifier4, text = "Pour quel identifiant souhaitez vous faire des modifications ?", background=couleur_principale)
    texte2.pack(expand=True)
    
    bouton_menu = tkinter.Button(fenetre, text="MENU", command=menu, bg=couleur_principale,relief="solid", bd=0, activebackground=couleur_principale, highlightthickness=0 ,borderwidth=1)
    bouton_menu.pack(side=tkinter.BOTTOM,anchor='sw',padx=10, pady = 10)
    
    global champ_texte
    champ_texte = tkinter.Entry(page_modifier4)
    champ_texte.pack(expand = True)
    champ_texte.focus_set()
    
    champ_texte.bind("<Return>", enter_pressed8)
    
def enter_pressed8(event):
    global nom_entre
    nom_entre = champ_texte.get()
    verification_identifiant()
    
def verification_identifiant():
    """cette fonction va nous permettre de savoir si l'identifiant existe dans la base de données"""
    global nouveau_site
    global nom_entre
    connexion = sqlite3.connect("password_database.db")
    #on compte le nombre de fois qu'il y a l'identifiant nom_entre à l'id_site qui se troive dans la variable globale nouveau_site
    request = connexion.execute("SELECT Count(*) FROM utilisateur WHERE id_site = '"+ str(nouveau_site) +"' AND identifiant = '"+ nom_entre +"'") 
    #on recupere cette information dans la variable count
    count = request.fetchone()[0]
    #si count est égal a 0 alors il n'existe pas  
    if count == 0:
        #on le renvoi donc  a la page_modifier4 qui contient l'avertissement 
        page_modifier4()
    #si count est donc different de 0
    else:
        #alors l'identifiant existe donc on continue avec la suite et on lance la prochaine fonction
        page_modifier5()
    
def page_modifier5():
    """Cette fonction va nous permettre de recuperer le nouvel identifiant que l'utilisateur souhaite mettre"""
    for widget in fenetre.winfo_children():
        widget.destroy()
        
    page_modifier5 = tkinter.Label(fenetre, background=couleur_principale)
    page_modifier5.pack(expand=True)
    
    connexion = sqlite3.connect("password_database.db")
    #on recupere les identifiants existants grace au SELECT
    request = connexion.execute("SELECT identifiant FROM utilisateur WHERE id_site ='"+ str(nouveau_site) +"'")
    #on recupere dans la variable liste_noms sous forme de liste de tuple
    liste_noms = request.fetchall()
    connexion.close()
    
    noms = []
    for nom in liste_noms:
        noms.append(nom[0])
        
    #on le transforme en chaine de characteres
    noms_espaces = ' '.join(noms)
    
    #on le previent des identifiants déjà existants
    texte = tkinter.Label(page_modifier5, text = "Les identifiants existants sont: "+noms_espaces, background=couleur_principale, wraplength=600)
    texte.pack(expand=True)
    
    texte1 = tkinter.Label(page_modifier5, text = "Quel est le nouvel identifiant que vous voulez mettre ?", background=couleur_principale)
    texte1.pack(expand=True)
    
    #On va lui demander de ne rien mettre si il ne vetut pas changer l'identifiant 
    texte2 = tkinter.Label(page_modifier5, text = "N'écrivez rien si vous ne voulez pas le changer", background=couleur_principale,fg="red")
    texte2.pack(expand=True)
    
    bouton_menu = tkinter.Button(fenetre, text="MENU", command=menu, bg=couleur_principale,relief="solid", bd=0, activebackground=couleur_principale, highlightthickness=0 ,borderwidth=1)
    bouton_menu.pack(side=tkinter.BOTTOM,anchor='sw',padx=10, pady = 10)
    
    global champ_texte
    champ_texte = tkinter.Entry(page_modifier5)
    champ_texte.pack(expand = True)
    champ_texte.focus_set()
    
    champ_texte.bind("<Return>", enter_pressed9)
    
def page_modifier6():
    """Cette focntion est la meme que la precedente elle contient suelement un avertissement permettant de 
    prevenir l'utilisateur que l'identifiant qu'il a entré existe déjà dans la base de données"""
    for widget in fenetre.winfo_children():
        widget.destroy()
        
    page_modifier6 = tkinter.Label(fenetre, background=couleur_principale)
    page_modifier6.pack(expand=True)
    
    connexion = sqlite3.connect("password_database.db")
    request = connexion.execute("SELECT identifiant FROM utilisateur WHERE id_site ='"+ str(nouveau_site) +"'")
    liste_noms = request.fetchall()
    connexion.close()
    
    noms = []
    for nom in liste_noms:
        noms.append(nom[0])
        
    noms_espaces = ' '.join(noms)
    
    #Avertissement en rouge comme quoi l'identifiant existe déjà
    texte = tkinter.Label(page_modifier6, text = "Le nouvel identifiant saisit existe déjà veuillez en saisir un autre !" , background=couleur_principale, fg="red")
    texte.pack(expand=True)
    
    texte1 = tkinter.Label(page_modifier6, text = "Les identifiants existants sont: "+noms_espaces, background=couleur_principale, wraplength=600)
    texte1.pack(expand=True)
    
    texte2 = tkinter.Label(page_modifier6, text = "Quel est le nouvel identifiant que vous voulez mettre ?", background=couleur_principale)
    texte2.pack(expand=True)
    
    texte3 = tkinter.Label(page_modifier6, text = "N'écrivez rien si vous ne voulez pas le changer", background=couleur_principale,fg="red")
    texte3.pack(expand=True)
    
    bouton_menu = tkinter.Button(fenetre, text="MENU", command=menu, bg=couleur_principale,relief="solid", bd=0, activebackground=couleur_principale, highlightthickness=0 ,borderwidth=1)
    bouton_menu.pack(side=tkinter.BOTTOM,anchor='sw',padx=10, pady = 10)
    
    global champ_texte
    champ_texte = tkinter.Entry(page_modifier6)
    champ_texte.pack(expand = True)
    champ_texte.focus_set()
    
    champ_texte.bind("<Return>", enter_pressed9)
    
def enter_pressed9(event):
    """Cette fonction va nous permettre de recuperer le nouvel_identifiant si l'utilisateur appuie sur entrer"""
    global nouvel_identifiant
    nouvel_identifiant = champ_texte.get()
    #on verifie avec la fonction verification_nouveal_identifiant()
    verification_nouvel_identifiant()
    
def verification_nouvel_identifiant():
    """Cette focntion va nous permettre de déterminer si le nouveal identifiant n'existe pas déjà dans la base de données"""
    #on recupere les 3 variables dont on a besoion
    global nouvel_identifiant
    global nouveau_site
    #connexion a la base de données
    connexion = sqlite3.connect("password_database.db")
    #Requête SQL permettant de compter le nombre de fois que 
    # nouvel_identifiant existe dans la base de données.
    request = connexion.execute("SELECT Count(*) " \
    "FROM utilisateur WHERE id_site = "
    + str(nouveau_site) +" AND identifiant = '"+ nouvel_identifiant +"'") 
    #on met la reponse de la requete dans une varibale 
    count = request.fetchone()[0]
    #si count est different de 0 alors il existe déjà
    if count != 0:
        #donc on lance la fonction permettant de lui redemander d'en entrer un nouveau et qui l'avertis que il existe déjà
        page_modifier6()
    #sinon sa veut dire que il n'existe pas
    elif count == 0:
        #donc on peut passer à la suite
        page_modifier7()
    connexion.commit()
    connexion.close()
    
def page_modifier7():
    """Cette focntion va nous permettre d'obtenir le nouveau mot de passe que l'utilisateur veut changer si il le souhaite
    effectivement"""
    for widget in fenetre.winfo_children():
        widget.destroy()
        
    page_modifier7 = tkinter.Label(fenetre, background=couleur_principale)
    page_modifier7.pack(expand=True)
    
    texte = tkinter.Label(page_modifier7, text = "Quel est le nouveau mot de passe que vous voulez mettre ?", background=couleur_principale)
    texte.pack(expand=True)
    #On lui précise de ne rien écrire si il ne souhaite pas le changer
    texte1 = tkinter.Label(page_modifier7, text = "N'écrivez rien si vous ne voulez pas le changer", background=couleur_principale,fg="red")
    texte1.pack(expand=True)
    
    bouton_menu = tkinter.Button(fenetre, text="MENU", command=menu, bg=couleur_principale,relief="solid", bd=0, activebackground=couleur_principale, highlightthickness=0 ,borderwidth=1)
    bouton_menu.pack(side=tkinter.BOTTOM,anchor='sw',padx=10, pady = 10)
    
    global champ_texte
    champ_texte = tkinter.Entry(page_modifier7)
    champ_texte.pack(expand = True)
    champ_texte.focus_set()
    
    champ_texte.bind("<Return>", enter_pressed10)
    
def page_modifier8():
    """Cette fonction est la meme que la precedente avec un avertissement en plus permettant de lui dire que le mot de passe
    ne correspond pas aux critéres indiqués"""
    for widget in fenetre.winfo_children():
        widget.destroy()
        
    page_modifier8 = tkinter.Label(fenetre, background=couleur_principale)
    page_modifier8.pack(expand=True)
    #Avertissement en rouge pour le prévenir que ces critéres ne sont pas respéctés
    texte_attention = tkinter.Label(page_modifier8, text = "Attention le mot de passe doit etre entre 8 et 32 characteres.", background=couleur_principale, fg="red")
    texte_attention.pack(expand=True)
    
    texte_attention2 = tkinter.Label(page_modifier8, text = "Il doit comporter des majuscules des minuscules des chiffres et des symboles!", background=couleur_principale, fg="red")
    texte_attention2.pack(expand=True)
    
    texte = tkinter.Label(page_modifier8, text = "Quel est le nouveau mot de passe que vous voulez mettre ?", background=couleur_principale)
    texte.pack(expand=True)
    #On lui précise de ne rien écrire si il ne veut pas le changer
    texte1 = tkinter.Label(page_modifier8, text = "N'écrivez rien si vous ne voulez pas le changer", background=couleur_principale,fg="red")
    texte1.pack(expand=True)
    
    bouton_menu = tkinter.Button(fenetre, text="MENU", command=menu, bg=couleur_principale,relief="solid", bd=0, activebackground=couleur_principale, highlightthickness=0 ,borderwidth=1)
    bouton_menu.pack(side=tkinter.BOTTOM,anchor='sw',padx=10, pady = 10)
    
    global champ_texte
    champ_texte = tkinter.Entry(page_modifier8)
    champ_texte.pack(expand = True)
    champ_texte.focus_set()
    
    champ_texte.bind("<Return>", enter_pressed10)
    
def enter_pressed10(event):
    """On récupere le nouveau mot de passe qu'il a entré"""
    global nouveau_mot_de_passe
    nouveau_mot_de_passe = champ_texte.get()
    #on lance la suite
    verification_password()
    
def verification_password():
    """Cette fonction va permettre de modifier les informations du compte que l'utilisateur a voulu modifier, en fonction
    de ce qu'il a entré dans les fonctions préceédentes"""
    #On recupere toutes les variables nécessaires a cela 
    global nouveau_mot_de_passe
    global nouvel_identifiant
    global nouveau_site
    global nom_entre
    #on établit la connexion
    connexion = sqlite3.connect("password_database.db")
    #on verifie si l'utilisateur n'a rion entré 
    if nouveau_mot_de_passe == "" and nouvel_identifiant == "":
        #dans ce cas on fait rien 
        return
    #si par contre il souhaite modifier l'identifiant alors on fait:
    if nouvel_identifiant != "" and nouveau_mot_de_passe == "":
        # Requête SQL pour mettre à jour l'identifiant dans la table utilisateur
        connexion.execute("UPDATE utilisateur SET identifiant = '"+ nouvel_identifiant +"'WHERE id_site = '"+ str(nouveau_site) +"' AND identifiant = '"+ nom_entre +"'")
    #si par contre il souhaite modifier le mot de passe alors on fait:
    if nouvel_identifiant == "" and nouveau_mot_de_passe != "":
        #on regarde si le mot de passe correspond aux critéres de sécurité grace a la fonction verification_mdp()
        #si oui alors :
        if verification_mdp(nouveau_mot_de_passe) == True:
            #Requete SQL permettant de modifier le mot de passe et l'identifiant pour le site entré
            #Requete SQL pour mettre à jour seulement le mot de passe
            connexion.execute("UPDATE utilisateur SET mdp = '"+ nouveau_mot_de_passe +"'WHERE id_site = '"+ str(nouveau_site) +"' AND identifiant = '"+ nom_entre +"'")
            #Si le mot de passe ne correspond pas aux critéres
        else:
            #alors on l'envoi sur la page comportant l'avertissement pour qu'il en entre un nouveau
            page_modifier8()
    #Si par contre il souhaite modifier les deux alors on fait:
    if nouvel_identifiant != "" and nouveau_mot_de_passe != "":
        #on regarde si le mot de passe correspond aux critéres de sécurité grace a la fonction verification_mdp()
        #si oui alors :
        if verification_mdp(nouveau_mot_de_passe) == True:
            #Requete SQL permettant de modifier le mot de passe et l'identifiant pour le site entré
            connexion.execute("UPDATE utilisateur SET identifiant = '"+ nouvel_identifiant +"', mdp = '"+ nouveau_mot_de_passe +"'WHERE id_site = '"+ str(nouveau_site) +"' AND identifiant = '"+ nom_entre +"'")
        #Si le mot de passe ne correspond pas aux critéres
        else :
            #alors on l'envoi sur la page comportant l'avertissement pour qu'il en entre un nouveau
            page_modifier8()
    connexion.commit()
    connexion.close()
        
    
    
    
def page_supprimer():
    """Cette focntion va se lancer si l'utilisateur clickera sur le bouton supprimer elle va lui demander pour quel site 
    il souhiate supprier des comptes"""
    for widget in fenetre.winfo_children():
        widget.destroy()
        
    page_supprimer = tkinter.Label(fenetre, background=couleur_principale)
    page_supprimer.pack(expand=True)
    
    connexion = sqlite3.connect("password_database.db")
    #on recuperer les sites existants dans la base de donnees
    request = connexion.execute("SELECT nom FROM Sites")
    liste_noms = request.fetchall()
    connexion.close()
    
    #on les met sous forme de chaine de charactere espacés
    noms = []
    for nom in liste_noms:
        noms.append(nom[0])
        
    noms_espaces = ' '.join(noms)
    #on les affihce a l'utilisateur
    texte = tkinter.Label(page_supprimer, text=noms_espaces, background=couleur_principale, wraplength=600)
    texte.pack(expand=True)

    texte1 = tkinter.Label(page_supprimer, text = "Pour quel site souhaitez vous supprimer des comptes ?", background=couleur_principale)
    texte1.pack(expand=True)
    
    bouton_menu = tkinter.Button(fenetre, text="MENU", command=menu, bg=couleur_principale,relief="solid", bd=0, activebackground=couleur_principale, highlightthickness=0 ,borderwidth=1)
    bouton_menu.pack(side=tkinter.BOTTOM,anchor='sw',padx=10, pady = 10)
    
    global champ_texte
    champ_texte = tkinter.Entry(page_supprimer)
    champ_texte.pack(expand = True)
    champ_texte.focus_set()
    
    champ_texte.bind("<Return>", enter_pressed5)
    
def page_supprimer2():
    """Cette fonction est la meme que la precedente elle va etre appelé si le site n'existe pas dans la base de données 
    et elle contient unn avertissement permettant d'indiquer a l'utilisateur qu ele site n'existe pas"""
    for widget in fenetre.winfo_children():
        widget.destroy()
        
    page_supprimer2 = tkinter.Label(fenetre, background=couleur_principale)
    page_supprimer2.pack(expand=True)
    
    connexion = sqlite3.connect("password_database.db")
    request = connexion.execute("SELECT nom FROM Sites")
    liste_noms = request.fetchall()
    connexion.close()
    
    noms = []
    for nom in liste_noms:
        noms.append(nom[0])
        
    noms_espaces = ' '.join(noms)
    
    #Avertissement pour indiquer que le site n'existe pas en rouge
    texte = tkinter.Label(page_supprimer2, text = "Ce site n'est pas enregistré !", background=couleur_principale, fg="red")
    texte.pack(expand=True)
    
    texte1 = tkinter.Label(page_supprimer2, text = noms_espaces, background=couleur_principale, wraplength=600)
    texte1.pack(expand=True)

    texte2 = tkinter.Label(page_supprimer2, text = "Pour quel site souhaitez vous supprimer des comptes ?", background=couleur_principale)
    texte2.pack(expand=True)
    
    bouton_menu = tkinter.Button(fenetre, text="MENU", command=menu, bg=couleur_principale,relief="solid", bd=0, activebackground=couleur_principale, highlightthickness=0 ,borderwidth=1)
    bouton_menu.pack(side=tkinter.BOTTOM,anchor='sw',padx=10, pady = 10)
    
    global champ_texte
    champ_texte = tkinter.Entry(page_supprimer2)
    champ_texte.pack(expand = True)
    champ_texte.focus_set()
    
    champ_texte.bind("<Return>", enter_pressed5)
    
def enter_pressed5(event):
    global site_entre
    site_entre = champ_texte.get()
    verification_site2()
    
def verification_site2():
    """Cette focntion va nous permettre de veriier si le site existe dans la base de données, elle va se lancer
    aprés la fonction enter_pressed5() qui elle se lance apres que l'utilisateur ait appuyé sur la touche entrer"""
    global site_entre
    global nouveau_site
    #On se connecte a la base de données
    connexion = sqlite3.connect("password_database.db")
    #On compte le nombre de fois que site_entre existe dans la base de données
    request = connexion.execute("SELECT Count(*) FROM Sites WHERE nom = '"+ site_entre +"'") 
    #on met sa dans une variables 
    count = request.fetchone()[0]
    #si count est different de 0 alors le site existe 
    if count != 0:
        #donc on fait une requete SQL pour recuperer l'id_site que l'on va pouvoir utiliser plus tard
        request2 = connexion.execute("SELECT id_site FROM Sites WHERE nom = '"+ site_entre +"'")
        nouveau_site = request2.fetchone()[0]
        #puis on lance la focntion page_supprimer3 qui sera la suite
        page_supprimer3()
    #si le site n'existe pas
    else:
        #on lance la fonction page_supprimer2 qui va avertier l'utilisateur que le site n'existe pas
        page_supprimer2()
    connexion.commit()
    connexion.close()
    
def page_supprimer3():
    """Cette fonction va permettre de demander a l'utilisateur quel compte il souhaite supprimer en lui demandant
    l'identifiant du compte elle se lancera seulement si le site qu'il a entré precedement existe"""
    for widget in fenetre.winfo_children():
        widget.destroy()
        
    page_supprimer3 = tkinter.Label(fenetre, background=couleur_principale)
    page_supprimer3.pack(expand=True)
    
    connexion = sqlite3.connect("password_database.db")
    #oon va recuperer les identifiants existants a l'id_site dans la table Utilisateur
    request = connexion.execute("SELECT identifiant FROM utilisateur WHERE id_site ='"+ str(nouveau_site) +"'")
    #on le recupere dans une varibale sous forme de liste de tuple
    liste_noms = request.fetchall()
    connexion.close()
    
    
    #on le met sous forme de chaine de characteres
    noms = []
    for nom in liste_noms:
        noms.append(nom[0])
        
    noms_espaces = ' '.join(noms)
    
    #on affiche les identifiants existants
    texte = tkinter.Label(page_supprimer3, text = noms_espaces, background=couleur_principale, wraplength=600)
    texte.pack(expand=True)
    
    texte1 = tkinter.Label(page_supprimer3, text = "Saisissez l'identifiant du compte que vous voulez supprimer :", background=couleur_principale)
    texte1.pack(expand=True)
    
    bouton_menu = tkinter.Button(fenetre, text="MENU", command=menu, bg=couleur_principale,relief="solid", bd=0, activebackground=couleur_principale, highlightthickness=0 ,borderwidth=1)
    bouton_menu.pack(side=tkinter.BOTTOM,anchor='sw',padx=10, pady = 10)
    
    global champ_texte
    champ_texte = tkinter.Entry(page_supprimer3)
    champ_texte.pack(expand = True)
    champ_texte.focus_set()
    
    champ_texte.bind("<Return>", enter_pressed6)
    
def page_supprimer4():
    """Cette fonction est semblable a la précedente mais elle contient un avertissement dans le cas ou l'utilisateur
    aurait entré un identifiant inexistant dans la base de données"""
    for widget in fenetre.winfo_children():
        widget.destroy()
        
    page_supprimer4 = tkinter.Label(fenetre, background=couleur_principale)
    page_supprimer4.pack(expand=True)
    
    connexion = sqlite3.connect("password_database.db")
    request = connexion.execute("SELECT identifiant FROM utilisateur WHERE id_site ='"+ str(nouveau_site) +"'")
    liste_noms = request.fetchall()
    connexion.close()
    
    noms = []
    for nom in liste_noms:
        noms.append(nom[0])
        
    noms_espaces = ' '.join(noms)
    
    texte = tkinter.Label(page_supprimer4, text = noms_espaces, background=couleur_principale, wraplength=600)
    texte.pack(expand=True)
    #avertissement pour avertir l'utilisateur que l'identifiant n'existe pas dans la base de données
    texte1 = tkinter.Label(page_supprimer4, text = "L'identifiant n'existe pas !", background=couleur_principale, fg="red")
    texte1.pack(expand=True)
    
    texte2 = tkinter.Label(page_supprimer4, text = "Saisissez l'identifiant :", background=couleur_principale)
    texte2.pack(expand=True)
    
    bouton_menu = tkinter.Button(fenetre, text="MENU", command=menu, bg=couleur_principale,relief="solid", bd=0, activebackground=couleur_principale, highlightthickness=0 ,borderwidth=1)
    bouton_menu.pack(side=tkinter.BOTTOM,anchor='sw',padx=10, pady = 10)
    
    global champ_texte
    champ_texte = tkinter.Entry(page_supprimer4)
    champ_texte.pack(expand = True)
    champ_texte.focus_set()
    
    champ_texte.bind("<Return>", enter_pressed6)
    
def enter_pressed6(event):
    """Cette focntion va se lancer si l'utilisateur clique sur entrer elle nous permet de récuperer ce que l'utilisateur 
    a entré dans le champ de texte"""
    global nom_entre
    nom_entre = champ_texte.get()
    #on lance la fonction qui va nous permettre de supprimer le compte
    suppression_compte()
    
def suppression_compte():
    """Cette focntion va nous permettre de supprimer le compte du site et de l'identifiant que l'utilisateur a 
    saisit précèdement"""
    global nouveau_site
    global nom_entre
    #on se connecte a la base de données 
    connexion = sqlite3.connect("password_database.db")
    #On vérifie tout d'abord si l'identifiant existe a l'id_site qui se trouve dans la variable globale nouveau_site
    request = connexion.execute("SELECT Count(*) FROM utilisateur WHERE id_site = '"+ str(nouveau_site) +"' AND identifiant = '"+ nom_entre +"'")
    #on recupere l'information dans un varibale 
    count = request.fetchone()[0]
    #Si count est different de 0 alors l'identifiant existe
    if count != 0:
        #Donc on peut le supprimer en faisant une requete SQL DELETE
        connexion.execute("DELETE FROM utilisateur WHERE id_site = '"+ str(nouveau_site) +"' AND identifiant = '"+ nom_entre +"'")
        #puis on relance la fonction dans le cas ou l'utilisateur souhaiteriat supprimer plusieurs comptes a ce site
        page_supprimer3()
    #Sinon on lance la fonction page_supprimer4() pour avertir l'utilisateur que l'identifiant entré n'existe pas dans la 
    #base de données    
    else:
        page_supprimer4()
    connexion.commit()
    connexion.close()




def start_application():
    """cette fonction détient toute la structure de la premiere page de l'application
    elle va nous permettre de la reappeler a chaque fois pour relancer l'application pour revenir au MENU"""
    #on définis la couleuur principale pour tout ce que l'on va faire dans une variable global pour la reutiliser plus tard
    global couleur_principale
    couleur_principale = "#e6f9ff"
     # Création de la fenêtre principale
    global fenetre
    fenetre = tkinter.Tk()
    #titre de la fenetre
    fenetre.title("PassVault")
    #on definis la taille minimum
    fenetre.minsize(699,499)
    #on définis la taille maximum
    fenetre.maxsize(700,500)
    #on y met la couleur de fond
    fenetre.config(background=couleur_principale)
        
    #Création d'image
    width = 300#taille du canvas en largeur
    height = 300#taille du canvas en hauteur
    global image#je globalise la variable image pour qu'elle apparaisse lorsque je lance la fonction car sinon sa ne l'affiche pas
    #on définis ce que va contenir la variable image
    image = tkinter.PhotoImage(file="password.png").subsample(2,2)#on y met le fichier dans le dossier de l'image que
                                                                    #l'on souhaite utiliser et subsample pour réduire l'image
    #On crée un canvas qu'on va globaliser pour que sa marche qui va contenir l'image                                                                
    global canvas
    #on va y preciser ou il se situe donc dans la fenetre sa taille sa couleur de fond on retire ses bordures pour l'héstétique
    canvas = tkinter.Canvas(fenetre, width=width, height=height, bg=couleur_principale, bd=0, highlightthickness=0)
    #On l'utilise pour placer l'image sur une toile(Canvas) on va diviser pour la placer au centre de celui ci
    canvas.create_image(width/2, height/2, image=image)
    #il faut faire .pack pour appliquer cela et on utilise pady pour une petite séparation
    canvas.pack(pady = 5)
    
    #on va créer un cadre pour les boutons 
    global cadre_boutons
    #il va se situer dans fenetre principale et le fond sera de la couleur principale 
    cadre_boutons = tkinter.Frame(fenetre, bg=couleur_principale)
    #on applique et on ajoute une separation pour creer un espace entre le cadre et le canvas
    cadre_boutons.pack(pady = 10)
    
    #on va ajouter une image pour un bouton 
    global image_ajouter
    #méthode pour inserer l'image que l'on va recuperer dans la dossier et que l'on va reduire avec subsimple
    image_ajouter = tkinter.PhotoImage(file="ajouter.png").subsample(8,8)
    #on crée un image pour un premier bouton
    global bouton_ajouter
    #on va y mettre l'image il va se situer dans le cadre_boutons on y retire plusieurs effets de style et il lancera la fonction page_ajouter au click
    bouton_ajouter = tkinter.Button(cadre_boutons ,command=page_ajouter, image=image_ajouter, bg=couleur_principale,relief=tkinter.FLAT, bd=0, activebackground=couleur_principale, highlightthickness=0 ,borderwidth=0)
    #on applique la modification et on va le placer sur la gauche avec un espacement
    bouton_ajouter.pack(side = tkinter.LEFT, padx=70)
    #on crée un autre image pour un autre bouton
    global image_loupe
    #méthode pour inserer l'image que l'on va recuperer dans la dossier et que l'on va reduire avec subsimple 
    image_loupe = tkinter.PhotoImage(file="rechercher.png").subsample(8,8)
    #on y cree le bouton
    global bouton_loupe
    #on va y mettre l'image il va se situer dans le cadre_boutons on y retire plusieurs effets de style et il lancera la fonction page_rechercher au click
    bouton_loupe = tkinter.Button(cadre_boutons ,command=page_rechercher, image=image_loupe, bg=couleur_principale,relief=tkinter.FLAT, bd=0, activebackground=couleur_principale, highlightthickness=0 ,borderwidth=0)
    #on applique la modification et on va le placer sur la gauche avec un espacement
    bouton_loupe.pack(side = tkinter.LEFT, padx=70)
    
    #On apelle la fonction pour centrer la fenetre
    centrer_fenetre()
    
#On lance l'application
start_application()
#On place la boucle de l'application qui est extremement importante
fenetre.mainloop()

