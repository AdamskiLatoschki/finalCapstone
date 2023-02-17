from datetime import date


def task_overview():
    # Calculating the following:
    # total number of tasks
    # total number of completed tasks
    # total number of uncompleted tasks
    # Total number of uncompleted and overdue tasks
    # The percentage of tasks that are incomplete
    # The percentage of tasks that are overdue

    with open("tasks.txt", "r") as file:
        task_data = file.readlines()

    total_tasks = len(task_data)
    completed_task = 0
    uncompleted_task = 0
    overdue_task = 0
    not_completed_and_overdue = 0
    today = date.today().strftime("%d %b %Y")

    for task in task_data:
        task_split = task.split(", ")
        if task_split[5].strip("\n") == "Yes":
            completed_task += 1
        else:
            uncompleted_task += 1
        if today < task_split[4]:
            overdue_task += 1
        if task_split[5].strip("\n") == "No" and today < task_split[4]:
            not_completed_and_overdue += 1

    incomplete_perc = (uncompleted_task / total_tasks) * 100
    overdue_perc = (overdue_task / total_tasks) * 100

    with open("task_overview.txt", "w+") as file:
        file.write(f'Total number of tasks:\t\t\t\t\t\t\t{total_tasks}\n'
                   f'Total number of completed tasks:\t\t\t\t{completed_task}\n'
                   f'Total number of uncompleted tasks:\t\t\t\t{uncompleted_task}\n'
                   f'Uncompleted and overdue tasks:\t\t\t\t\t{not_completed_and_overdue}\n'
                   f'The percentage of tasks that are incomplete:    {round(incomplete_perc)}%\n'
                   f'The percentage of tasks that are overdue:\t   {round(overdue_perc)}%\n')


def user_overview():
    # Calculating the following:
    # Number of registered users
    # Number of tasks registered
    # Following statistics for each user:
    # Total tasks assigned
    # Percentage of tasks assigned
    # Percentage of tasks completed
    # Percentage of tasks incomplete
    # Percentage of tasks incomplete & overdue

    with open("user.txt", "r") as file:
        user_data = file.readlines()

    with open("tasks.txt", "r") as file:
        task_data = file.readlines()

    total_users = len(user_data)
    total_tasks = len(task_data)
    tasks_per_user = 0
    completed_tasks = 0
    uncompleted_tasks = 0
    tasks_per_user_dict = {}
    tasks_perc_dict = {}
    tasks_completed_perc_dict = {}
    tasks_uncompleted_perc_dict = {}
    today = date.today().strftime("%d %b %Y")
    not_completed_and_overdue = 0
    not_completed_and_overdue_dict = {}
    string_to_write = f"Number or users registered: {total_users}\nNumber of tasks registered: {total_tasks}\n"

    for user_entry in user_data:
        user_has_tasks = False
        user_split = user_entry.strip("\n").split(", ")
        user = user_split[0]
        for task in task_data:
            task_split = task.strip("\n").split(", ")

            if user == task_split[0]:
                user_has_tasks = True
                tasks_per_user += 1
                if task_split[-1] == 'Yes':
                    completed_tasks += 1
                else:
                    uncompleted_tasks += 1

                if task_split[5].strip("\n") == "No" and today < task_split[4]:
                    not_completed_and_overdue += 1

        if user_has_tasks:
            # Tasks assigned to each user
            tasks_per_user_dict[user] = tasks_per_user
            # Percentage of the total number of tasks assigned to the user
            tasks_per_user_perc = (tasks_per_user / total_tasks) * 100
            tasks_perc_dict[user] = tasks_per_user_perc
            # Percentage of the total number of completed tasks assigned to the user
            tasks_completed_perc = (completed_tasks / tasks_per_user) * 100
            tasks_completed_perc_dict[user] = tasks_completed_perc
            # Percentage of the total number of uncompleted tasks assigned to the user
            tasks_uncompleted_perc = (uncompleted_tasks / tasks_per_user) * 100
            tasks_uncompleted_perc_dict[user] = tasks_uncompleted_perc
            # Percentage of the tasks that have not been completed yet and are overdue for the user
            not_completed_and_overdue_perc = (not_completed_and_overdue / tasks_per_user) * 100
            not_completed_and_overdue_dict[user] = not_completed_and_overdue_perc
        else:
            tasks_per_user_dict[user] = 0
            tasks_perc_dict[user] = 0.0
            tasks_completed_perc_dict[user] = 0.0
            tasks_uncompleted_perc_dict[user] = 0.0
            not_completed_and_overdue_dict[user] = 0.0

        tasks_per_user = 0
        uncompleted_tasks = 0
        completed_tasks = 0
        not_completed_and_overdue = 0

        string_to_write += "============================================================================\n"
        string_to_write += f"Statistics for {user}\n"
        string_to_write += f"Total tasks assigned: {tasks_per_user_dict[user]}\n"
        string_to_write += f"Percentage of tasks assigned: {tasks_perc_dict[user]}\n"
        string_to_write += f"Percentage of tasks completed: {tasks_completed_perc_dict[user]}\n"
        string_to_write += f"Percentage of tasks incomplete: {tasks_uncompleted_perc_dict[user]}\n"
        string_to_write += f"Percentage of tasks incomplete & overdue: {not_completed_and_overdue_dict[user]}\n"
        string_to_write += "============================================================================\n"

    with open("user_overview.txt", "w") as file:
        file.write(string_to_write)


def add_task():
    # Function adding a new task
    with open('tasks.txt', 'a+') as tasks_file:
        # Taking inputs from the user
        task = input('Please enter the title of the task: ')
        assigning_user = input('Please enter a username of the person you want to assign the task to: ')
        task_description = input('Please enter description of the assigned task: ')
        date_due = input("Enter due date in dd Mon yyyy format: ")
        assigning_date = date.today().strftime("%d %b %Y")

        # Writing to file
        tasks_file.write("\n")
        tasks_file.write(f'{assigning_user}, {task}, {task_description}, {assigning_date}, {date_due}, No')


def view_mine():
    # Function displaying all tasks assigned to logged certain user
    with open('tasks.txt', 'r+') as tasks_file:
        file = tasks_file.readlines()

    tasks_dict = {}
    no_task = True

    # Looping over and filtering info
    for pos, lines in enumerate(file):
        split_data = lines.split(', ')

        tasks_dict[pos] = lines

        if username in split_data[0]:
            no_task = False
            print(f'--------[{pos + 1}]----------\n'
                  f'Task:\t\t\t\t{split_data[1]}\n'
                  f'Assigned to:\t\t{split_data[0]}\n'
                  f'Assigned date:\t\t{split_data[3]}\n'
                  f'Due date:\t\t\t{split_data[4]}\n'
                  f'Is completed:\t\t{split_data[5].rstrip()}\n'
                  f'Description:\t\t{split_data[2]}\n'
                  '--------------------\n')
    if no_task:
        print("You have no tasks")
    else:
        while True:
            # Asking user if it wants to edit any of the tasks
            task_choice = int(input('Please enter a number of the task for editing or "-1" to back to menu: '))

            if task_choice == 0 or task_choice < -1 or task_choice > len(file):
                print('Invalid number , try again!')
                continue
            elif task_choice == -1:
                break

            else:
                # Displaying menu to the user with options they can do with chosen task
                option_choice = int(input('\nSelect one of the following options below: \n'
                                          '1 - Edit due date\n'
                                          '2 - Mark as completed \n'
                                          '3 - Edit user assigned\n'
                                          ': '
                                          ))

                if option_choice <= 0 or option_choice > 3:
                    print('You have selected invalid option, try again')
                    continue

                chosen_task = tasks_dict[task_choice - 1]
                print(chosen_task)
                #  Asking user to input new due date
                if option_choice == 1:
                    new_due_date = input('Please enter a new due date for this task in (DD Mon YYYY) format: ')
                    split_data = chosen_task.split(', ')
                    del split_data[4]
                    split_data.insert(4, new_due_date)
                    new_data = ', '.join(split_data)
                    tasks_dict[task_choice - 1] = new_data
                    #  Replacing old due date with the new one
                    string_to_write = ""
                    for val in tasks_dict.values():
                        string_to_write += val

                    print('\nNew due date for your task has been registered!')

                    with open("tasks.txt", "w") as file:
                        file.write(string_to_write)

                    break
                # Option to change the status of the task
                if option_choice == 2:
                    split_data = chosen_task.split(', ')
                    del split_data[-1]
                    split_data.insert(5, "Yes\n")
                    new_data = ', '.join(split_data)
                    tasks_dict[task_choice - 1] = new_data

                    string_to_write = ""
                    for val in tasks_dict.values():
                        string_to_write += val

                    print('\nNew status for your task has been registered!')

                    with open("tasks.txt", "w") as file:
                        file.write(string_to_write)

                    break
                # Asking user for the input, assigning new user to the task
                if option_choice == 3:
                    new_username = input(' Enter a name of the new user you want to assign to this task: ')
                    split_data = chosen_task.split(', ')
                    del split_data[0]
                    split_data.insert(0, new_username)
                    new_data = ', '.join(split_data)
                    tasks_dict[task_choice - 1] = new_data

                    string_to_write = ""
                    for val in tasks_dict.values():
                        string_to_write += val

                    with open("tasks.txt", "w") as file:
                        file.write(string_to_write)

                    print('\nNew username for your task has been registered!')

                    break


def view_all():
    # Function displaying all tasks assigned
    with open('tasks.txt', 'r+') as task_file:
        file = task_file.readlines()

        # Looping over and filtering info, displaying all tasks
        for pos, lines in enumerate(file):
            assigned_user, title, description, assign_date, due_date, complete_task = lines.split(', ')

            print(f'--------[{pos + 1}]----------\n'
                  f'Task:\t\t\t\t{title}\n'
                  f'Assigned to:\t\t{assigned_user}\n'
                  f'Assigned date:\t\t{assigned_date}\n'
                  f'Due date:\t\t\t{due_date}\n'
                  f'Is completed:\t\t{complete_task.rstrip()}\n'
                  f'Description:\t\t{description}\n'
                  '--------------------\n')


def reg_user():
    # Function registering new users
    #  Asking user for the information to register a new user
    new_user = input('Please enter a new username: ')
    while new_user in usernames_list:
        print('This user already exists! Try again.\n')
        new_user = input('Please enter a new username: ')
    while new_user not in usernames_list:
        new_pass = input('Please enter a new password: ')
        confirm_pass = input('Please confirm your new password: ')
        # Validating if both entered passwords match.
        if new_pass == confirm_pass:
            usernames_list.append(new_user)
            print('New user has been registered!')
            user_file.write("\n")
            user_file.write(f'{new_user}, {new_pass}')
            break

        print('Incorrect details. Try again!')


assigned_date = date.today().strftime("%d %b %Y")
usernames_list = []
passwords = []

# Program login section
with open('user.txt', 'r') as user_file:
    for line in user_file:
        user, psw = line.strip('\n').split(', ')
        usernames_list.append(user)
        passwords.append(psw)

# Username
username = input('Please enter a username to login to your account: ')
while username not in usernames_list:
    print('Invalid details. Try again!')
    username = input('Please enter a username to login to your account: ')

# Password
password = input('Please enter your password: ')
post = usernames_list.index(username)
while password != passwords[post]:
    password = input('Invalid password, please try again: ')
print(f'\nWelcome {username.capitalize()} !')

# Main menu
while True:
    if username == 'admin':
        menu = input('\nSelect one of the following Options below: \n'
                     'r - Registering a user\n'
                     'a - Adding a task \n'
                     'va - View all tasks\n'
                     'vm - View my task\n'
                     'gr - Generate report\n'
                     'ds - Display stats\n'
                     'e - Exit\n:'
                     ).lower()
    else:
        menu = input('\nSelect one of the following Options below: \n'
                     'a - Adding a task \n'
                     'va - View all tasks\n'
                     'vm - view my task\n'
                     'e - Exit\n:'
                     ).lower()

    # Registering the user
    if menu == 'r':
        if username == 'admin':
            with open('user.txt', 'a+') as user_file:
                reg_user()
        else:
            print('\nYou are not allowed to use this option! Try again')
    # Creating a new task entry
    elif menu == 'a':
        add_task()
    # Displaying all tasks
    elif menu == 'va':
        view_all()
    # Displaying tasks for the logged user only.
    elif menu == 'vm':
        view_mine()
    # Generating reports
    elif menu == "gr":
        task_overview()
        user_overview()
    # Displaying statistics
    elif menu == 'ds':
        # Generating reports, read and displaying statistics from generated files
        if username == 'admin':
            task_overview()
            user_overview()

            with open("task_overview.txt", "r") as report:
                file_two = report.readlines()
            print("Task Overview:")
            for line in file_two:
                line = line.strip()
                print(line)

            with open("user_overview.txt", "r") as report:
                file_one = report.readlines()
            print("User Overview:")
            for line in file_one:
                line = line.strip()
                print(line)

    elif menu == 'e':
        print('\nGoodbye!!!')
        exit()
    else:
        print("You have made a wrong choice, Please Try again")