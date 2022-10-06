import sys, math, json, re, random, os, operator

helpMessage = (
        'Usage: movieELO <command>\n',
        'Commands:',
        '  help, h:      \tSends this help message.',
        '  startup, s:   \tInitiates the startup.',
        '  add, a:       \tAllows you to add movie(s).',
        '  output-elo, o:\tSends the elo ratings.',
        ''
        )

if (len(sys.argv) == 1):
    exit('\n'.join(helpMessage) + "\nUnknown command!\n")
else:
    sys.argv.pop(0)

try:
    movies = json.load(open('movies.json', "r"))

except FileNotFoundError:
    movies = {}

os.system("color")

class movie:
    def __init__(self, name, elo):
        self.name = name
        self.elo = elo

class myColors:
    MOVIE1 = '\033[32m'
    MOVIE2 = '\033[36m'
    OPTION = '\033[33m'
    RESET = '\033[0m'

def addMovie():
    if (len(movies) < 10):
        exit("Please use the statrtup command!\n")
    moviesList = []
    while True:
        movieInput = input("Please enter a movie or quit (q).\t")

        if (movieInput in movies):
            userInput = input("You already have this movie added. Are you sure you want to continue? {myColors.OPTION}(y/n){myColors.RESET}\t")
            match userInput:
                case 'n':
                    print("Excited sucessfully.")
                    break

                case _:
                    exit('\n'.join(helpMessage) + "\nUnknown command!\n")

        if (movieInput == 'q'):
            print("Excited sucessfully.")
            break

        else:
            movieInput = movie(movieInput, 1000)
            for x in range(1, 11):
                while True:
                    randomMovie = random.choice(list(movies.keys()))
                    if (randomMovie not in moviesList):
                        break
                moviesList.append(randomMovie)
                userInput = input(f"{x}. Do you like {myColors.MOVIE1}{randomMovie}{myColors.RESET} more than {myColors.MOVIE2}{movieInput.name}{myColors.RESET}? {myColors.OPTION}(y/n){myColors.RESET}\t")
                match userInput:
                    case "y":
                        movies[randomMovie], movieInput.elo = eloFun(movies[randomMovie], movieInput.elo)
                
                    case "n":
                        movieInput.elo, movies[randomMovie] = eloFun(movieInput.elo, movies[randomMovie])

                    case _:
                        exit('\n'.join(helpMessage) + "\nUnknown command!\n")

            movies[movieInput.name] = movieInput.elo
        moviesList.clear()
    json.dump(dict(sorted(movies.items(), key=operator.itemgetter(1),reverse=True)), open('movies.json', "w"), indent=4)

# just loads the first 10 movies into the json file, after that this program is useless
def startup():
    moviesList = []
    # takes 10 movies in and puts them into the list | least favorite movie first
    for x in range(1, 11):
        movieInput = input(f"Input the {x}th movie:\t")
        moviesList.append(movie(movieInput, 1000))

    # going through list and setting the elo of each movie
    # this should happen n(n - 1) / 2 times where n is the amount of movies
    for x in range(1, 10):
        for y in range(0, x):
            moviesList[x].elo, moviesList[y].elo = eloFun(moviesList[x].elo, moviesList[y].elo)

    # finally adding the movies into the dict after reversing it
    moviesList.reverse()
    for x in moviesList:
        movies[x.name] = x.elo

    # save the movies into the json file
    json.dump(movies, open('movies.json', "w"), indent=4)

# Contains util functions used in the program

def eloFun(winner, loser):
    if (winner >= loser):
        amount = math.floor((min(loser, winner) / max(winner, loser)) * elo(winner, loser))

    else:
        amount = math.ceil(elo(winner, loser))

    # checking to see if the elo is invalid
    if (loser - amount <= 0):
        return winner, loser
    return (winner + amount), (loser - amount)

# the elo formula
def elo(num1, num2):
    return (pow(abs(num1 - num2), 0.9) * 0.3) + 5 # the 5 is the range between the values

for x in sys.argv:
    match (re.search("(?!-).", x, re.I|re.A).group()):
        case "h":
            exit('\n'.join(helpMessage))

        case "s":
            startup() 

        case "a":
            addMovie()

        case "o":
            # formats and prints the movies, after making sure that the file exists
            if (len(movies) == 0):
                exit("Please use the startup command!\n")
            else:
                for i, x in enumerate(movies.keys()):
                    print(f"{i + 1}. {myColors.MOVIE1}{x}{myColors.RESET}: {myColors.MOVIE2}{movies[x]}{myColors.RESET}")

        case _:
            exit('\n'.join(helpMessage) + "\nUnknown command!\n")
