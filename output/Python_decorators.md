## Explication
Les décorateurs en Python sont une forme d'extension de fonctionnalités qui permettent de modifier ou d'ajouter des comportements à une fonction ou une méthode existante sans avoir besoin de les réécrire. Ils sont utilisés pour ajouter des fonctionnalités comme le journalisation, la validation, le cache et bien plus encore.

## Concepts clés
- **Décorateur** : Une fonction qui prend une autre fonction en argument et renvoie une fonction modifiée.
- **@decorator_name** : Syntaxe糖 pour appliquer un décorateur à une fonction.
- **wrapper function** : Fonction interne qui est utilisée dans le décorateur pour ajouter le comportement supplémentaire.

## Exemple
```python
# Définition d'un simple décorateur
def my_decorator(func):
    def wrapper():
        print("Avant l'exécution de la fonction")
        func()
        print("Après l'exécution de la fonction")
    return wrapper

# Utilisation du décorateur avec la syntaxe @decorator_name
@my_decorator
def say_hello():
    print("Hello!")

# Appel de la fonction décorée
say_hello()

# Sortie :
# Avant l'exécution de la fonction
# Hello!
# Après l'exécution de la fonction
```