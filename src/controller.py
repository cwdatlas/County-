from csvrepo import CsvRepo


class controller:
    # The controller, states as simply as it's the only controller, provides the cli front end to the program.
    # it contains all commands and print statements for operation a cli environment.
    # Programmed by Aidan Scott with help from Nate Anderson (Tester)
    def __init__(self):
        # Make sure that main_loop's while loop runs
        self.running = True

        # initialize command array and repo
        self.commands = {"add": self.add, "get": self.get, "quit": self.quit, "help": self.help}
        self.repo = CsvRepo()  # Inits database (in this case a CSV file)

        # start the program
        self.main_loop()

    def main_loop(self):
        print("County Database. Type 'help' for help and 'quit' to quit")
        print("This database is used to search Montana Counties by county name, city name and licence plate prefix")
        print("Adding cities is also available, make sure to exclude all spaces in county names or city names.")
        while self.running:
            # split incoming string by spaces
            command = input("-> ").split(' ')
            if command[0] in self.commands:
                # Pass all but the first section of the command
                self.commands[command[0]](command[1:])  # Use commands dictionary to call matching command.
            else:
                print(f"command '{command[0]}' not recognized, try 'help' to see available commands")

    # Commands:
    def add(self, command):
        # The add command adds a city to the database with two arguments, city and county.
        # County code is added to the row in the repo (but as its abstracted I wouldn't need to know that)
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
        # The get command gets all rows which contain the city, county or code in them.
        # Counties with more than one city provide the best feedback as they have more than one line.
        # incoming command should have a length of 2, no more or less
        if len(command) != 2:
            print("Invalid arguments, you must use 'get' 'city/county/code' 'name'")
            # This allows me to have a print statement at the end of the function which prints all gathered data
            return None
        elif command[0] == "city":
            # look up all rows with stated city name
            data = self.repo.get_by_city(command[1])
            self.list(data)
        elif command[0] == "county":
            # look up all rows with stated county name
            data = self.repo.get_by_county(command[1])
            self.list(data)
        elif command[0] == "code":
            # look up all rows with stated county code
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
            # Visualize data
            data = self.repo.get_by_code(int(command[1]))
            self.list(data)

    def quit(self, command):
        # Quit turns off the main_loop while loop, shutting down the program
        self.running = False
        print("Goodbye")

    def help(self, command):
        # Help provides guidance to the user
        print("You have access to 4 commands, 'get', 'add', 'quit' and 'help'")
        print("'get' has two arguments, city/county/code and then the 'name'")
        print("Please note that city/county/code are your arguments, so you would not state city name. Check example")
        print("example: 'get county broadwater'")
        print("'add' has two arguments, 'city' 'county'. Make sure the county exists before use")
        print("Please note that the 'add' command does not need specification on if you are adding city/county/code")
        print("example: 'add toston broadwater'")
        print("'quit' exits the program")
        print("'help' shows this page")

    def list(self, data):
        # List lists out data from returned data. it works with all three return types
        if len(data) == 0:
            print("No data found with specified parameters, try 'help' for more information or add data with 'add'")
            return None
        # Prints out all data from returned lists
        # First print out basic county and city
        for i in data[0]:
            print(i + "   " + str(data[0][i]))
        # Second add all extra datapoints, specifically all other cities than first stated.
        for i in range(1, len(data)):
            for j in data[i]:
                if j == "City":
                    print("Other Cities: " + str(data[i][j]))
