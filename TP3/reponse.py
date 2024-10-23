# Créez une classe abstraite Shape avec une méthode abstraite area().
# Implémentez deux classes dérivées : Circle et Rectangle.
# Chaque classe devra implémenter sa propre version de la méthode area().

from abc import ABC, abstractmethod
from statistics import mean, median, variance

class Shape(ABC):
    def __init__(self, name):
        self.name = name
    @abstractmethod
    def area(self):
        pass
class Circle(Shape):
    def __init__(self, radius, name="Circle"):
        super().__init__(name)
        self.radius = radius

    def area(self):
        return 3.14 * (self.radius ** 2)

class Rectangle(Shape):
    def __init__(self, width, height, name="Rectangle"):
        super().__init__(name)
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height



# Créez une classe BankAccount avec un solde initial.
# Surchargez les opérateurs + et - pour permettre d’ajouter ou 
# retirer de l’argent du
# compte bancaire en utilisant ces opérateurs

class BankAccount:
    def __init__(self, initial_balance=0):
        self.balance = initial_balance

    def __add__(self, montant):
        if isinstance(montant, (int, float)):
            self.balance += montant
        return self

    def __sub__(self, montant):
        if isinstance(montant, (int, float)):
            self.balance -= montant
        return self

    def __str__(self):
        return f"BankAccount balance: {self.balance}"


# Créez un décorateur @check_positive qui vérifie si le nombre passé en argument à une
# fonction est positif. Si le nombre est négatif, levez une exception ValueError.

def check_positive(func):
    def wrapper(x):
        if x < 0:
            raise ValueError("The number must be positive")
        return func(x)
    return wrapper

@check_positive
def example_function(x):
    return x * 2

# Créez une classe Car avec un attribut privé speed.
# Utilisez le décorateur @property pour lire la vitesse et un setter pour la modifier.
# La vitesse ne peut pas dépasser 200 km/h (et doit être > 0), sinon une exception
# ValueError est levée

class Car:
    def __init__(self, speed=50):
        self._speed = None
        self.speed = speed

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        if value <= 0 or value > 200:
            raise ValueError("la vitesse doit être entre 1 et 200 km/h")
        self._speed = value


# Créez une classe Person qui prend un nom et un âge en entrée.
# Utilisez une exception personnalisée InvalidAgeError pour lever une erreur si l’âge est
# négatif ou supérieur à 150 ans

class AgeError(Exception):
    pass

class Person:
    def __init__(self, name, age):
        self.name = name
        if age < 0 or age > 150:
            raise AgeError("L'âge doit être entre 0 et 150 ans")
        self.age = age


# Implémentez un pattern Singleton pour une classe DatabaseConnection qui garantit
# qu’il n’existe qu’une seule instance de connexion à la base de données.
# L’instance de cette classe doit permettre de créer un context (qui, lui, n’est pas unique),
# et qui permet d’ajouter une entrée (id, data), de la supprimer par id, ou de drop toutes
# les lignes.
# Les opérations doivent être exécutées (flush) une fois le context fermé

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class DbContext:
    def __init__(self, connection=None):
        self.connection = connection if connection else DatabaseConnection()

    def __enter__(self):
        return self.connection.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.connection.__exit__(exc_type, exc_val, exc_tb)

class DatabaseConnection(metaclass=SingletonMeta):
    def __init__(self):
        self.entries = []  # List to store the data

    def __enter__(self):
        self._temp_entries = []
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:  # Commit changes if no exception occurred
            self.entries.extend(self._temp_entries)
        self._temp_entries = []  # Clear temporary entries regardless

    def add_entry(self, entry):
        """Add an entry in the form of a dictionary"""
        self._temp_entries.append(entry)

    def remove_by_id(self, id):
        """Remove an entry by its ID"""
        self.entries = [entry for entry in self.entries if entry["id"] != id]

    def drop_all(self):
        """Remove all entries"""
        self.entries.clear()


# Créez une factory pour générer des objets Circle ou Rectangle (héritant d’une classe
# abstraite Shape) en fonction d’un paramètre passé à une méthode create. Vous devez
# pouvoir choisir quelle forme créer en fonction des paramètres fournis.

class ShapeFactory:
    @staticmethod
    def create(shape, **kwargs):
        if shape.lower() == "circle":
            return Circle(kwargs.get("radius"))
        elif shape.lower() == "rectangle":
            return Rectangle(kwargs.get("width"), kwargs.get("height"))
        else:
            raise ValueError("Unknown shape type")

# Créez une classe Matrix et surchargez les opérateurs + et * pour permettre l’addition et
# la multiplication de matrices.
# Gérez les exceptions si les matrices ne sont pas de tailles compatibles

class Matrix:
    def __init__(self, values):
        self.values = values
        self.rows = len(values)
        self.cols = len(values[0]) if self.rows > 0 else 0

    def __add__(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Les matrices doivent avoir les mêmes dimensions pour ajouter")
        result = [
            [self.values[i][j] + other.values[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ]
        return Matrix(result)

    def __mul__(self, other):
        if self.cols != other.rows:
            raise ValueError("Les matrices doivent avoir des dimensions compatibles pour se multiplier")
        result = [
            [
                sum(self.values[i][k] * other.values[k][j] for k in range(self.cols))
                for j in range(other.cols)
            ]
            for i in range(self.rows)
        ]
        return Matrix(result)

    def __str__(self):
        return "\n".join(["\t".join(map(str, row)) for row in self.values])


# Créez une classe abstraite Animal avec une méthode abstraite speak().
# Implémentez des classes dérivées Dog et Cat.
# Ensuite, implémentez une factory AnimalFactory qui génère une instance de Dog ou
# Cat en fonction des paramètres d’entrée.
# Les paramètres sont :
# •animal_type : une chaîne de caractères contenant soit “dog” soit “cat” (ou autre).
# •name : une chaîne de caractères contenant le nom de l’animal.

class Animal(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        return f"Woof"

class Cat(Animal):
    def speak(self):
        return f"Meow"

class AnimalFactory:
    @staticmethod
    def create(animal_type, name):
        if animal_type.lower() == "dog":
            return Dog(name)
        elif animal_type.lower() == "cat":
            return Cat(name)
        else:
            raise ValueError("Animal inconnu")


# Créez une classe Product avec des attributs name et price.
# Surchargez les opérateurs de comparaison (==, <, >, etc.) pour comparer des objets
# Product en fonction de leur prix

class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __eq__(self, other):
        if isinstance(other, Product):
            return self.price == other.price
        return False

    def __lt__(self, other):
        if isinstance(other, Product):
            return self.price < other.price
        return False

    def __le__(self, other):
        if isinstance(other, Product):
            return self.price <= other.price
        return False

    def __gt__(self, other):
        if isinstance(other, Product):
            return self.price > other.price
        return False

    def __ge__(self, other):
        if isinstance(other, Product):
            return self.price >= other.price
        return False

    def __ne__(self, other):
        if isinstance(other, Product):
            return self.price != other.price
        return False


# Créez une fonction top_products(products, k) qui prend en paramètre une liste de
# produits et un entier k, et qui retourne les k produits les plus chers.

def top_product(products, k):
    if not all(isinstance(product, Product) for product in products):
        raise ValueError("Tous les éléments de la liste doivent être des instances de produit")
    return sorted(products, key=lambda product: product.price, reverse=True)[:k]

# Créez une classe Account avec une propriété balance.
# Si un dépôt est inférieur à 0 ou si un retrait rend le solde négatif, une exception
# ValueError doit être levée.
# Utilisez le décorateur @property pour gérer les accès et modifications du solde

class Account:
    def __init__(self, initial_balance=0):
        self._balance = initial_balance

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, amount):
        if amount < 0:
            raise ValueError("Le dépôt ne peut pas être inférieur à 0")
        self._balance = amount

    def deposit(self, amount):
        if amount < 0:
            raise ValueError("Le dépôt ne peut pas être inférieur à 0")
        self._balance += amount

    def withdraw(self, amount):
        if amount < 0:
            raise ValueError("Le retrait ne peut pas être inférieur à 0")
        if self._balance - amount < 0:
            raise ValueError("Le solde ne peut pas être négatif")
        self._balance -= amount


# Créez une classe Vector représentant un vecteur mathématique à deux dimensions.
# Implémentez les opérations de +, -, et *.

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        raise ValueError("Les deux opérandes doivent être des vecteurs")

    def __sub__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x - other.x, self.y - other.y)
        raise ValueError("Les deux opérandes doivent être des vecteurs")

    def __mul__(self, scalar):
        if isinstance(scalar, (int, float)):
            return Vector(self.x * scalar, self.y * scalar)
        raise ValueError("Le multiplicateur doit être un nombre")

    def __str__(self):
        return f"Vector({self.x}, {self.y})"


# Créez une classe générique Statistics qui accepte une liste de nombres et fournit des
# méthodes pour calculer la moyenne, la médiane et la variance des données.
# Utilisez le module statistics pour vous aider

class Statistics:
    def __init__(self, stats):
        if not all(isinstance(x, (int, float)) for x in stats):
            raise ValueError("All elements must be numbers")
        self.stats = stats

    def mean(self):
        return mean(self.stats)

    def median(self):
        return median(self.stats)

    def variance(self):
        return variance(self.stats)


