import os

# Constants
QUESTS_FILE = 'quests.txt'
USER_LEVEL_FILE = 'user_level.txt'
EXP_PER_LEVEL = 100

# Load quests from file
def load_quests():
    if not os.path.exists(QUESTS_FILE):
        return []
    with open(QUESTS_FILE, 'r') as file:
        quests = [line.strip().split('|') for line in file]
    return [{'title': q[0], 'description': q[1], 'exp': int(q[2]), 'level': q[2]} for q in quests]

# Save quests to file
def save_quests(quests):
    with open(QUESTS_FILE, 'w') as file:
        for quest in quests:
            file.write(f"{quest['title']}|{quest['description']}|{quest['exp']}|{quest['level']}\n")

# Load user level and EXP
def load_user_level():
    if not os.path.exists(USER_LEVEL_FILE):
        return {'level': 1, 'exp': 0}
    with open(USER_LEVEL_FILE, 'r') as file:
        level, exp = map(int, file.readline().strip().split('|'))
    return {'level': level, 'exp': exp}

# Save user level and EXP
def save_user_level(user_level):
    with open(USER_LEVEL_FILE, 'w') as file:
        file.write(f"{user_level['level']}|{user_level['exp']}\n")

# Display the UI
def display_ui(quests, user_level):
    os.system('clear')
    length = os.get_terminal_size().columns
    print("\033[36m" + "╭"+"=" * (length - 2)+"╮")
    print("┃"+"Kairosis".center(length - 2, ' ')+"┃")
    print("╰"+"=" * (length - 2)+"╯" + "\033[37m")
    
    exp_for_next_level = EXP_PER_LEVEL - user_level['exp']
    
    print("\033[31m" + "╭"+"=" * (length // 3 - 2)+ "╮" + "\033[35m"+ " " * (length // 3) + "\033[35m" + "╭" + "=" * (length // 3 - 2) + "╮")
    print("\033[31m" + "┃"+"User Level: " + str(user_level['level']) + " " * (length // 3 - 2 - len(str(user_level['level'])) - 12) +"┃" + " " * (length // 3) + "\033[35m" + "┃" + " " * (length // 3 - 2 - 13) + "Welcome Back," + "┃")
    print("\033[31m" + "┃"+"EXP to next level: "+ str(exp_for_next_level) + " " * (length //3 - 2 - len(str(exp_for_next_level)) - 19)  +"┃" + " " * (length // 3) + "\033[35m" + "┃"+ " " * (length // 3 - 2 - 7) + "Player." "┃")
    print("\033[31m" + "╰"+"=" * (length // 3 - 2)+"╯" + "\033[35m"+ " " * (length // 3) + "\033[35m" + "╰" + "=" * (length // 3 - 2) + "╯")
    print("\033[37m")

    print("\n"+"QUESTS:".center(length, " ")+"\n")
    print('-' * length)

    for i, quest in enumerate(quests):
        title = quest['title']
        description = quest['description']
        exp = quest['exp']
        level = quest['level']

        print(f"Name: {title}")
        print(f"Description: {description}")
        print(f"EXP: {exp}")
        print(f"Level: {level}")
        print(f"ID: {i}")
        print('-' * length)
    
    print("\nOptions: [C]reate Quest, [D]elete Quest, [M]ark Quest Done, [E]xit")

# Main loop
def main():
    print("\033[40m") # Black background
    print("\033[37m") # White Text
    quests = load_quests()
    user_level = load_user_level()

    while True:
        display_ui(quests, user_level)
        choice = input("Choose an option: ").strip().lower()

        if choice == 'c':
            title = input("Enter quest title: ")
            description = input("Enter quest description: ")
            exp = int(input("Enter quest EXP: "))
            level = input("Enter quest level: ").upper()
            quests.append({'title': title, 'description': description, 'exp': exp, 'level': level})
            save_quests(quests)

        elif choice == 'd':
            quest_num = int(input("Enter quest number to delete: ")) - 1
            if 0 <= quest_num < len(quests):
                del quests[quest_num]
                save_quests(quests)

        elif choice == 'm':
            quest_num = int(input("Enter quest number to mark as done: ")) - 1
            if 0 <= quest_num < len(quests):
                user_level['exp'] += quests[quest_num]['exp']
                if user_level['exp'] >= EXP_PER_LEVEL:
                    user_level['level'] += 1
                    user_level['exp'] -= EXP_PER_LEVEL
                save_user_level(user_level)
                del quests[quest_num]
                save_quests(quests)

        elif choice == 'e':
            print("\033[0m")
            os.system("clear")
            break

if __name__ == "__main__":
    main()
