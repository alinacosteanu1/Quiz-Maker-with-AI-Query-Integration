from backend import quizuri, adauga_in_leaderboard, citeste_leaderboard

print("🧠 Bine ai venit la QUIZ!\n")
nume = input("Introdu numele tău: ").strip()

print("\nCategorii disponibile:")
for c in quizuri.keys():
    print(" -", c)

categorie = input("\nAlege categoria: ").lower().strip()
if categorie not in quizuri:
    print("❌ Categoria nu există.")
    exit()

intrebari = quizuri[categorie]
scor = 0

for i, q in enumerate(intrebari, 1):
    print(f"\n{i}. {q['intrebare']}")
    for litera, text in q["variante"].items():
        print(f"  {litera}) {text}")
    raspuns = input("Răspunsul tău (a/b/c/d): ").lower().strip()
    if raspuns == q["corect"]:
        print("✅ Corect!")
        scor += 1
    else:
        print(f"❌ Greșit! Răspunsul corect era: {q['corect']}) {q['variante'][q['corect']]}")

print(f"\n📊 Scor final: {scor}/{len(intrebari)}")
adauga_in_leaderboard(nume, scor, len(intrebari))
print("\n🏆 LEADERBOARD:")
print(citeste_leaderboard())