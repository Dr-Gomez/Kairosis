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
    print("\033[36m") # Cyan text
    print("╭"+"=" * (length - 2)+"╮")
    print("┃"+"Kairosis".center(length - 2, ' ')+"┃")
    print("╰"+"=" * (length - 2)+"╯")
    print("\033[37m") # White Text
    print("\nQUESTS:\n")

    for i, quest in enumerate(quests):
        #print(f"{i+1}. {quest['title']}".ljust(40) + f"EXP: {quest['exp']}")

        title = quest['title']
        description = quest['description']
        exp = quest['exp']


        print(f"Name: {quest['title']}")
        print(f"Description: {quest['description']}")
        print(f"EXP: {quest['exp']}")
        print(f"Level: {quest['level']}")
        print('-' * 80)
    
    print("\nUser Level: ", user_level['level'])
    exp_for_next_level = EXP_PER_LEVEL - user_level['exp']
    print(f"EXP to next level: {exp_for_next_level}")
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
