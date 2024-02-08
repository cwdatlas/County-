from csvrepo import CsvRepo


class controller:
    def __init__(self):
        self.running = True

        # initialize command array and repo
        self.commands = {"add": self.add, "get": self.get, "quit": self.quit, "help": self.help}
        self.repo = CsvRepo()  # Inits database (in this case a CSV file)

        # start the program
        self.main_loop()

    def main_loop(self):
        print("County Database. Type help for help")
        while self.running:
            command = input("-> ").split(' ')
            if command[0] in self.commands:
                self.commands[command[0]](command[1:])
            else:
                print(f"command {command[0]} not recognized, try 'help' to see avaliable commands")

    # Commands:
    def add(self, command):
        # incoming command should have a length of 2, no more or less
        if len(command) != 2:
            print("Invalid arguments, you must use 'add' 'city name' 'county name'")
            return None
        else:
            # I cant check if the city or county is in the repo without asking it if it exists.
            # if the repo returns false, then it could not add the city
            add_status = self.repo.add_city(command[0], command[1])
            if add_status:
                print(f"City '{command[0].capitalize()}' added in county '{command[1].capitalize()}'")
            else:
                print("Your city already exists or your county does not exist. Search by county to see all counties")

    def get(self, command):
        # incoming command should have a length of 2, no more or less
        if len(command) != 2:
            print("Invalid arguments, you must use 'get' 'city/county/code' 'name'")
            # This allows me to have a print statement at the end of the function which prints all gathered data
            return None
        elif command[0] == "city":
            data = self.repo.get_by_city(command[1])
            self.list(data)
        elif command[0] == "county":
            data = self.repo.get_by_county(command[1])
            self.list(data)
        elif command[0] == "code":
            try:
                # validates if str can be turned into int. exits if it cant
                int(command[1])
            except ValueError:
                print("Entered code must be an number")
                return None
            # validates that int is within bounds. exits if not
            if int(command[1]) > 55 or int(command[1]) < 1:
                print("Entered code must be an number from 1 to 55")
                return None

            data = self.repo.get_by_code(int(command[1]))
            self.list(data)

    def quit(self, command):
        # incoming command should have a length of 1, no more or less
        self.running = False
        print("Goodbye")

    def help(self, command):
        # incoming command should have a length of 0, no more or less
        print("You have access to 4 commands, 'get', 'add', 'quit' and 'help'")
        print("'get' has two arguments, city/county/code and then the 'name'")
        print("example: 'get county broadwater'")
        print("'add' has two arguments, 'city' 'county'. Make sure the county exists before use")
        print("example: 'add toston broadwater'")
        print("'quit' exits the program")
        print("'help' shows this page")

    def list(self, data):
        if len(data) == 0:
            print("No data found with specified parameters, try 'help' for more information or add data with 'add'")
            return None
        # Prints out all data from returned lists
        for i in data[0]:
            print(i + "   " + str(data[0][i]))
        for i in range(1, len(data)):
            for j in data[i]:
                if j == "City":
                    print("Other Cities: " + str(data[i][j]))


