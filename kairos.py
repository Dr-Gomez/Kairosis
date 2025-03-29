import os
import datetime

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
    return [{'title': q[0], 'description': q[1], 'exp': int(q[2]), 'level': q[3], 'days': q[4].split(','), 'start_time': q[5], 'end_time': q[6]} for q in quests]

# Save quests to file
def save_quests(quests):
    with open(QUESTS_FILE, 'w') as file:
        for quest in quests:
            file.write(f"{quest['title']}|{quest['description']}|{quest['exp']}|{quest['level']}|{','.join(quest['days'])}|{quest['start_time']}|{quest['end_time']}\n")

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

# Get current day and time
def get_current_day_time():
    now = datetime.datetime.now()
    return now.strftime('%A'), now.strftime('%H:%M')

# Check if a quest is available
def is_quest_available(quest):
    current_day, current_time = get_current_day_time()
    start_time, end_time = quest['start_time'], quest['end_time']
    
    if current_day not in quest['days']:
        return False
    return start_time <= current_time <= end_time

# Display the UI
def display_ui(quests, user_level):
    os.system('clear')
    length = os.get_terminal_size().columns
    print("\033[36m" + "╭"+"=" * (length - 2)+"╮")
    print("┃"+"Kairosis".center(length - 2, ' ') + "┃")
    print("╰"+"=" * (length - 2)+"╯" + "\033[37m")
    
    exp_for_next_level = EXP_PER_LEVEL - user_level['exp']
    
    print("\033[31m" + "╭"+"=" * (length // 3 - 2)+ "╮" + "\033[35m"+ " " * (length // 3) + "\033[35m" + "╭" + "=" * (length // 3 - 2 + length % 3) + "╮")
    print("\033[31m" + "┃"+"User Level: " + str(user_level['level']) + " " * (length // 3 - 2 - len(str(user_level['level'])) - 12) +"┃" + " " * (length // 3) + "\033[35m" + "┃" + " " * (length // 3 - 2 - 13 + length % 3) + "Welcome Back," + "┃")
    print("\033[31m" + "┃"+"EXP to next level: "+ str(exp_for_next_level) + " " * (length //3 - 2 - len(str(exp_for_next_level)) - 19)  +"┃" + " " * (length // 3) + "\033[35m" + "┃"+ " " * (length // 3 - 2 - 7 + + length % 3) + "Player." "┃")
    print("\033[31m" + "╰"+"=" * (length // 3 - 2)+"╯" + "\033[35m"+ " " * (length // 3) + "\033[35m" + "╰" + "=" * (length // 3 - 2 + length % 3) + "╯")
    print("\033[37m")

    print("QUESTS:".center(length, " ") + "\n")
    print('-' * length)
    
    for i, quest in enumerate(quests):
        if (is_quest_available(quest)):
            title, description, exp, level, days, start_time, end_time = quest.values()
            print(f"\033[32mName: {title} \033[37m")
            print(f"\033[33mDescription: {description} \033[37m")
            print(f"\033[34mEXP: {exp} \033[37m")
            print(f"\033[35mLevel: {level} \033[37m")
            print(f"\033[36mAvailable: {', '.join(days)} from {start_time} to {end_time} \033[37m")
            print(f"ID: {i} \033[37m")
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
            level = input("Enter quest level (DEFCON): ").upper()
            exp = int(input("Enter quest EXP (1- 100): "))
            days = input("Enter valid days (comma-separated, e.g., Monday,Tuesday): ").split(',')
            start_time = input("Enter start time (HH:MM format): ")
            end_time = input("Enter end time (HH:MM format): ")
            quests.append({'title': title, 'description': description, 'exp': exp, 'level': level, 'days': days, 'start_time': start_time, 'end_time': end_time})
            save_quests(quests)

        elif choice == 'd':
            quest_num = int(input("Enter quest number to delete: "))
            if 0 <= quest_num < len(quests):
                del quests[quest_num]
                save_quests(quests)

        elif choice == 'm':
            quest_num = int(input("Enter quest number to mark as done: "))
            if 0 <= quest_num < len(quests):
                if is_quest_available(quests[quest_num]):
                    user_level['exp'] += quests[quest_num]['exp']
                    if user_level['exp'] >= EXP_PER_LEVEL:
                        user_level['level'] += 1
                        user_level['exp'] -= EXP_PER_LEVEL
                    save_user_level(user_level)
                    print("\033[32mQUEST COMPLETED!\033[37m")
                    input("Press Enter to continue...")
                else:
                    print("\033[31mThis quest is not available at this time.\033[37m")
                    input("Press Enter to continue...")
        

        elif choice == 'e':
            print("\033[0m")
            os.system("clear")
            break

if __name__ == "__main__":
    main()
