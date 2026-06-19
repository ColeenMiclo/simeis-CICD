import requests
import pytest
import uuid




BASE_URL = "http://78.123.114.124:42666"

def generate_unique_name():
    return f"testuser{uuid.uuid4().hex[:12]}"

def testScenario1():
    #On crée un nouveau joueur
    response = requests.post(f"{BASE_URL}/player/new/{generate_unique_name()}").json()
    playerId = response.get("playerId")

    #Préparation du header pour les requêtes suivantes
    headers = {"Content-Type": "application/json", "Simeis-Key": response.get("key")}

    #On récupère les informations du joueur (money et station)
    playerInfo = requests.get(f"{BASE_URL}/player/{playerId}", headers=headers).json()

    playerInitMoney = playerInfo.get("money")
    playerStation = playerInfo.get("stations")[0]

    #On récupère la liste des vaisseaux disponibles à l'achat
    shipPrices = requests.get(f"{BASE_URL}/station/{playerStation}/shipyard/list", headers=headers).json()
    shipToBuy = shipPrices.get("ships")[0].get("id")

    #On achète le vaisseau
    shipBuy = requests.post(f"{BASE_URL}/station/{playerStation}/shipyard/buy/{shipToBuy}", headers=headers).json()

    assert shipBuy.get("error") == "ok", "Ship buy should be successful"

    #On vérifie que l'argent du joueur a diminué après l'achat du vaisseau
    playerMoneyAfterShipBuy = requests.get(f"{BASE_URL}/player/{playerId}", headers=headers).json().get("money")
    
    assert playerInitMoney > playerMoneyAfterShipBuy, "Player money should have decreased after buying a ship"

    #On achète un module de Miner
    buyModule = requests.post(f"{BASE_URL}/station/{playerStation}/shop/modules/{shipToBuy}/buy/Miner", headers=headers).json()
    assert buyModule.get("error") == "ok", "Module buy should be successful"

    #On vérifie que l'argent du joueur a diminué après l'achat du module
    playerMoneyAfterModuleBuy = requests.get(f"{BASE_URL}/player/{playerId}", headers=headers).json().get("money")

    assert playerMoneyAfterShipBuy > playerMoneyAfterModuleBuy, "Player money should have decreased after buying a module"

    print("Test scenario 1 completed successfully")


def testScenario2():
    ''' - On créer un nouveau joueur
        - On récupère la liste des factories disponibles à l'achat
        - On achète une factory
        - La transaction est validée
        - On démarre la production d'un module
-       - On vérifie que la production est bien en cours
        - On stoppe la production
        - On vérifie que la production est bien stoppée
    '''
    
    #On crée un nouveau joueur
    response = requests.post(f"{BASE_URL}/player/new/{generate_unique_name()}").json()
    playerId = response.get("playerId")

    headers = {"Content-Type": "application/json", "Simeis-Key": response.get("key")}

    # On récupère les informations du joueur
    playerInfo = requests.get(f"{BASE_URL}/player/{playerId}", headers=headers).json()
    playerStation = playerInfo.get("stations")[0]

    # On récupère la liste des industries disponibles à l'achat
    industryToBuy = requests.get(f"{BASE_URL}/station/{playerStation}/industry/buy", headers=headers).json()

    assert industryToBuy.get("error") == "ok", "Industry should be successful"

    industryName = list(industryToBuy.keys())[2]

    # On achète une industry
    industryBuy = requests.post(f"{BASE_URL}/station/{playerStation}/industry/buy/{industryName}", headers=headers).json()
    industryId = industryBuy.get("id")

    assert industryBuy.get("error") == "ok", "Industry buy should be successful"

    # On démarre la production d'un module
    industryStart = requests.post(f"{BASE_URL}/station/{playerStation}/industry/start/{industryId}", headers=headers).json()

    assert industryStart.get("error") == "ok", "Industry start should be successful"

    # On vérifie que la production est bien en cours
    industryStatus = requests.post(f"{BASE_URL}/station/{playerStation}/industry/stop/{industryId}", headers=headers).json()
    assert industryStatus.get("error") == "ok", "Industry stop should be successful"

    print("Test scenario 2 completed successfully")


def testScenario3():
    ''' - On créer un nouveau joueur
        - On achète un vaisseau
        - La transaction est validée
        - On recrute un crew member
        - Le recrutement est validé
        - On le place sur un ship
        - On vérifie que le crew member est bien promu
        - On recrute un deuxième idle
        - On le vire
        - On vérifie que le crew member est bien viré
    '''

    #On crée un nouveau joueur
    response = requests.post(f"{BASE_URL}/player/new/{generate_unique_name()}").json()
    playerId = response.get("playerId")

    headers = {"Content-Type": "application/json", "Simeis-Key": response.get("key")}

    playerInfo = requests.get(f"{BASE_URL}/player/{playerId}", headers=headers).json()
    playerStation = playerInfo.get("stations")[0]

    #On récupère la liste des vaisseaux disponibles à l'achat
    shipPrices = requests.get(f"{BASE_URL}/station/{playerStation}/shipyard/list", headers=headers).json()
    shipToBuy = shipPrices.get("ships")[0].get("id")

    #On achète le vaisseau
    shipBuy = requests.post(f"{BASE_URL}/station/{playerStation}/shipyard/buy/{shipToBuy}", headers=headers).json()

    assert shipBuy.get("error") == "ok", "Ship buy should be successful"

    #   On recrute un crew member
    hire = requests.post(f"{BASE_URL}/station/{playerStation}/crew/hire/Pilot", headers=headers).json()

    assert hire.get("error") == "ok", "Crew member hire should be successful"

    #  On le place sur un ship
    assignement = requests.post(f"{BASE_URL}/station/{playerStation}/crew/assign/{hire.get('id')}/ship/{shipToBuy}/pilot", headers=headers).json()
    assert assignement.get("error") == "ok", "Crew member assignment should be successful"

    # On recrute un deuxième crew member
    hireAgain = requests.post(f"{BASE_URL}/station/{playerStation}/crew/hire/Operator", headers=headers).json()

    # On le vire
    fire = requests.post(f"{BASE_URL}/station/{playerStation}/crew/fire/{hireAgain.get('id')}", headers=headers).json()
    assert fire.get("error") == "ok", "Crew member fire should be successful"

    print("Test scenario 3 completed successfully")



testScenario1()
testScenario2()
testScenario3()