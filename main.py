import random
import time

class Giocatore:
    def __init__(self, nome, ruolo):
        self.nome = nome 
        self.ruolo = ruolo 

class GiocatoreMovimento(Giocatore):
    def __init__(self, nome, ruolo, tiro):
        if ruolo not in {"difensore", "centrocampista", "attaccante"}:
            raise ValueError("Ruolo non valido per un giocatore di movimento")
        
        if tiro not in range(1, 100):
            raise ValueError(f"Valore dell'abilità tiro non valido: '{tiro}'. Il valore deve essere nel range 1 e 100.")
        super().__init__(nome, ruolo)
        self.tiro = tiro
    
    def tira(self):
        print(f"{self.nome} tira in porta!")

class Portiere(Giocatore):
    def __init__(self, nome, parata):
        if parata not in range(1, 100):
            raise ValueError(f"Valore dell'abilità tiro non valido: '{parata}'. Il valore deve essere nel range 1 e 100.")
        super().__init__(nome, "portiere")
        self.parata = parata

    def para(self):
        print(f"{self.nome} prova a parare il tiro!")

class Squadra:
    def __init__(self, nome, giocatori):
        if len(giocatori) != 11:
            raise ValueError("La squadra deve avere esattamente 11 giocatori.")
        
        portieri = [g for g in giocatori if isinstance(g, Portiere)]
        if len(portieri) != 1:
            raise ValueError(f"La squadra deve avere esattamente 1 portiere, trovati: {len(portieri)}")

        self.nome = nome
        self.giocatori = giocatori
        self.portiere = portieri[0]
        self.punteggio = 0

        self.attaccanti = [g for g in self.giocatori if isinstance(g, GiocatoreMovimento) and g.ruolo == "attaccante"]
        self.centrocampisti = [g for g in self.giocatori if isinstance(g, GiocatoreMovimento) and g.ruolo == "centrocampista"]
        self.difensori = [g for g in self.giocatori if isinstance(g, GiocatoreMovimento) and g.ruolo == "difensore"]

    def formazione(self):
        print("\n--------------------------\n")
        print(f"Ecco la formazione della squadra {self.nome} \n")

        n_difensori = len(self.difensori)
        n_centrocampisti = len(self.centrocampisti)
        n_attaccanti = len(self.attaccanti)

        print(f"Il modulo scelto dall'allenatore è il {n_difensori}-{n_centrocampisti}-{n_attaccanti}\n")
        print(f"In porta: {self.portiere.nome.upper()}\n")

        stringa_base_difesa = "Linea difensiva formata da: "
        stringa_finale_difesa = stringa_base_difesa + ", ".join([d.nome.upper() for d in self.difensori])
        print(stringa_finale_difesa + '\n')

        stringa_base_centrocampo = "A centrocampo: "
        stringa_finale_centrocampo = stringa_base_centrocampo + ", ".join([c.nome.upper() for c in self.centrocampisti])
        print(stringa_finale_centrocampo + '\n')

        stringa_base_attacco = "Attacco composto da: "
        stringa_finale_attacco = stringa_base_attacco + ", ".join([a.nome.upper() for a in self.attaccanti])
        print(stringa_finale_attacco + '\n')

    
    def attacca(self):
        opzioni = (
            (self.attaccanti, 0.6),
            (self.centrocampisti, 0.3),
            (self.difensori, 0.1),
        )

        giocatori_pesati = []
        for gruppo, peso in opzioni:
            giocatori_pesati.extend(gruppo * int(peso * 10)) 
        
        tiratore = random.choice(giocatori_pesati)
        time.sleep(2)
        print(f"{tiratore.nome} ({tiratore.ruolo}, con un tiro di {tiratore.tiro}) della squadra {self.nome} sta tirando in porta!")
        return tiratore

    def difende(self):
        time.sleep(2)
        print(f"{self.portiere.nome} con una parata di {self.portiere.parata} sta provando a parare il tiro!")
        return self.portiere

class Partita:
    def __init__(self, squadra1, squadra2):
        self.squadra1 = squadra1
        self.squadra2 = squadra2
        print(f"Benvenuti alla partita {squadra1.nome} - {squadra2.nome}")

        self.punteggio_squadra1 = 0
        self.punteggio_squadra2 = 0

        self.squadra1.formazione()
        self.squadra2.formazione()

        self.minuti_partita = range(1, 91)

        self.azioni_salienti = []
        self.seleziona_azioni_salienti()

        self.avvia_timer()
        
    def seleziona_azioni_salienti(self):
        minuti = [i for i in range(1, 91)]
        for _ in range(6):
            azione = random.choice(minuti)
            minuti.remove(azione)
            self.azioni_salienti.append(azione)

    def avvia_timer(self):
        for i in self.minuti_partita:
            print(f"Minuto: {i}")
            if i in self.azioni_salienti:
                self.genera_azione()

            if i == 90:
                print("Partita finita!")
                self.fine_partita()
            
            time.sleep(1)

    def genera_azione(self):
        squadra_off = random.choice([self.squadra1, self.squadra2])
        squadra_dif = self.squadra1 if squadra_off == self.squadra2 else self.squadra2

        print(f"Attacca la squadra {squadra_off.nome}")

        tiratore = squadra_off.attacca()
        portiere = squadra_dif.difende()

        goal = self.assegna_goal(tiratore.tiro, portiere.parata)

        if goal:
            time.sleep(2)
            print("GOOOOOOL!!!!")

            if squadra_off == self.squadra1:
                self.punteggio_squadra1 += 1
            else:
                self.punteggio_squadra2 += 1
            
            self.stampa_punteggio(goal)

        else:
            time.sleep(2)
            print(f"Tiro parato da {portiere.nome}")
            self.stampa_punteggio(goal)

    def assegna_goal(self, tiro, parata):
        goal = None

        gap = tiro - parata 
        probabilita_goal = 50 + gap

        numero_casuale = random.randint(1, 100)

        if -50 < gap < 50:
            if numero_casuale <= probabilita_goal:
                goal = True
            else: 
                goal = False
        
        if gap >= 50:
            goal = True
        
        if gap <= - 50:
            goal = False

        return goal

    def stampa_punteggio(self, goal):
        if goal is True: 
            time.sleep(1)
            print(f"Il punteggio è ora di: {self.punteggio_squadra1}-{self.punteggio_squadra2}")
        else:
            time.sleep(1)
            print(f"Si rimane sul punteggio di: {self.punteggio_squadra1}-{self.punteggio_squadra2}")

    def fine_partita(self):
        if self.punteggio_squadra1 > self.punteggio_squadra2:
            print(f"Ha vinto {self.squadra1.nome} per {self.punteggio_squadra1}-{self.punteggio_squadra2}")
        elif self.punteggio_squadra1 < self.punteggio_squadra2:
            print(f"Ha vinto {self.squadra2.nome} per {self.punteggio_squadra1}-{self.punteggio_squadra2}")
        else:
            print(f"Pareggio: {self.punteggio_squadra1}-{self.punteggio_squadra2}")

# -----------------------------------------------------REAL MADRID------------------------------------------------------------
giocatore1 = GiocatoreMovimento("Dani Carvajal", "difensore", 85)
giocatore2 = GiocatoreMovimento("Sergio Ramos", "difensore", 89)
giocatore3 = GiocatoreMovimento("Raphaël Varane", "difensore", 87)
giocatore4 = GiocatoreMovimento("Marcelo", "difensore", 88)
giocatore5 = GiocatoreMovimento("Luka Modrić", "centrocampista", 92)
giocatore6 = GiocatoreMovimento("Casemiro", "centrocampista", 86)
giocatore7 = GiocatoreMovimento("Toni Kroos", "centrocampista", 90)
giocatore8 = GiocatoreMovimento("Gareth Bale", "attaccante", 89)
giocatore9 = GiocatoreMovimento("Karim Benzema", "attaccante", 88)
giocatore10 = GiocatoreMovimento("Cristiano Ronaldo", "attaccante", 94)
giocatore11 = Portiere("Keylor Navas", 85)

squadra_real_madrid = Squadra("Real Madrid", [giocatore1, giocatore2, giocatore3, giocatore4, giocatore5, giocatore6, giocatore7, giocatore8, giocatore9, giocatore10, giocatore11])

# -----------------------------------------------------BARCELLONA------------------------------------------------------------
giocatore12 = GiocatoreMovimento("Sergi Roberto", "difensore", 82)
giocatore13 = GiocatoreMovimento("Gerard Piqué", "difensore", 88)
giocatore14 = GiocatoreMovimento("Samuel Umtiti", "difensore", 85)
giocatore15 = GiocatoreMovimento("Jordi Alba", "difensore", 86)
giocatore16 = GiocatoreMovimento("Sergio Busquets", "centrocampista", 89)
giocatore17 = GiocatoreMovimento("Andrés Iniesta", "centrocampista", 90)
giocatore18 = GiocatoreMovimento("Ivan Rakitić", "centrocampista", 87)
giocatore19 = GiocatoreMovimento("Lionel Messi", "attaccante", 95)
giocatore20 = GiocatoreMovimento("Luis Suárez", "attaccante", 92)
giocatore21 = GiocatoreMovimento("Neymar Jr.", "attaccante", 94)
giocatore22 = Portiere("Marc-André ter Stegen", 86)

squadra_barcellona = Squadra("Barcellona", [giocatore12, giocatore13, giocatore14, giocatore15, giocatore16, giocatore17, giocatore18, giocatore19, giocatore20, giocatore21, giocatore22])

partita = Partita(squadra_real_madrid, squadra_barcellona)