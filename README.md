![Logo of the project](https://cdn.discordapp.com/attachments/545544110086291456/608344452439867402/OC_PIZZA.png)

# Concevez la solutins technique OC Pizza

Imulations compléte d'un systéme de gestion de données.

### Installation / Mise en route :

# Installation [Python 3.7]
https://www.python.org/ftp/python/3.7.2/python-3.7.2.exe

# Packages Python nécessaires :
- Request

```shell
https://github.com/Lyss74/P6_solution_technique_Oc_Pizza/archive/master.zip
cd P6_solution_technique_Oc_Pizza
pipenv install
pipenv shell
```
Cela va installè les packages nécessaires et lancer l'environnement virtuel en quelques secondes.

## Lancez un serveur Mysql afin d'interagir avec la base de donnèes:

## La connexion à la base se fera sous ces identifiants: 
```shell
DATABASE = 'Oc_Pizza'
USER = 'OCP6' 
PASSWORD = 'OC_STUDENT' 
```

# Ensuite lancez l'application :
```shell
python main.py 

```
Pour une premiéres utilisation séléctionnez 'A', afin de proceder à l'alimentation de la base de données.

## Liens :

- Page d'accueil du projet : https://openclassrooms.com/fr/projects/126/assignment
- Dépôt Git: https://github.com/Lyss74/P6_solution_technique_Oc_Pizza

## Fonctionnalités de l'application :

* Alimenter la base de données sans modifié les configurations
* S'inscrire dans la base de données OC Pizza
* Consultez la liste des employes par restaurant
* Consultez les recettes des pizzas
* Réaliser une commande de pizza

Énnoncé
-------

« OC Pizza » est un jeune groupe de pizzeria en plein essor et spécialisé dans les pizzas livrées ou à emporter. Il compte déjà 5 points de vente et prévoit d’en ouvrir au moins 3 de plus d’ici la fin de l’année. Un des responsables du groupe a pris contact avec vous afin de mettre en place un système informatique, déployé dans toutes ses pizzerias et qui lui permettrait notamment :

* d’être plus efficace dans la gestion des commandes, de leur réception à leur livraison en passant par leur préparation
* de suivre en temps réel les commandes passées et en préparation
* de suivre en temps réel le stock d’ingrédients restants pour savoir quelles pizzas sont encore réalisables
* de proposer un site Internet pour que les clients puissent :
    * passer leurs commandes, en plus de la prise de commande par téléphone ou sur place
    * payer en ligne leur commande s’ils le souhaitent – sinon, ils paieront directement à la livraison
    * modifier ou annuler leur commande tant que celle-ci n’a pas été préparée
* de proposer un aide mémoire aux pizzaiolos indiquant la recette de chaque pizza
* d’informer ou notifier les clients sur l’état de leur commande

Le client a déjà fait une petite prospection et les logiciels existants qu’il a pu trouver ne lui conviennent pas.

Dans votre proposition de solution, vous partirez du principe que vous disposez dans votre société de toutes les ressources et compétences nécessaires à la réalisation du projet.

Travail demandé
---------------

En tant qu’analyste-programmeur, votre travail consiste, à ce stade, à définir le domaine fonctionnel et à concevoir l’architecture technique de la solution répondant aux besoins du client, c’est-à-dire :

* modéliser les objets du domaine fonctionnel
* identifier les différents éléments composant le système à mettre en place et leurs interactions
* décrire le déploiement des différents composants que vous envisagez
* élaborer le schéma de la ou des bases de données que vous comptez créer
