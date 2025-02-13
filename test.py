import random

def assegna_goal(tiro, parata):
        goal = None

        gap = tiro - parata 
        probabilita_goal = 50 + gap

        numero_casuale = random.randint(1, 100)

        if -50 < gap < 50:
            print(f"C'è una possibilita di segnare di: {probabilita_goal}%")
            if numero_casuale <= probabilita_goal:
                goal = True
            else: 
                goal = False
        
        if gap >= 50:
            goal = True
        
        if gap <= - 50:
            goal = False

        return goal

print(assegna_goal(93, 78))