import json
import xlsxwriter
import pandas as pd

with open("/workspaces/RocketStats/refactorreplayfile/exampleReplays/ex1.json") as f:  # automatisieren
    re = json.load(f)


# Folgender Plan

# erstmal auf boost scheißen damit n bissl progress zu sehen ist :)


# für den Anfang: Player und Controller Id
def initialise_json_to_string(replay_json):
    temp_replay = json.dumps(replay_json)
    found_Frames = temp_replay.find('"frames"')
    first_replay = temp_replay[found_Frames:]
    return first_replay


class Replay:
    def __init__(self, whole_replay_json):
        self.rr = initialise_json_to_string(whole_replay_json)

    def set_remaining_replay(self, remaining_replay):
        self.rr = remaining_replay

    def cut(self, token, shift=None):  # token = part to get searched
        if shift is None:
            shift = 0
        index_of_token = self.rr.find(token)  # abcde überspringe token
        # print(index_of_token)
        test = index_of_token + len(token) + 1 + shift
        temp = self.rr[test:]  # +1 für whitespace cuts

        self.rr = temp
        # print(temp)  # debug         1. test bestanden :)


class Vectors:

    def __init__(self, start_vector_tupel):
        self.x = start_vector_tupel[0]
        self.y = start_vector_tupel[1]
        self.z = start_vector_tupel[2]

    def set_update_pos(self, new_vector_tupel):
        self.x = new_vector_tupel[0]
        self.y = new_vector_tupel[1]
        self.z = new_vector_tupel[2]

    def get_list(self):
        return [self.x, self.y, self.z]


class Player:

    def __init__(self, player_id, player_name, player_team, vector: Vectors):
        self.id = player_id
        self.name = player_name
        self.team = player_team
        self.controller_id = None
        self.player_pos = vector
        self.index_in_file = None

    def set_id(self, new_id):
        self.id = new_id

    def set_team(self, new_team):
        self.team = new_team

    def set_current_car_controller_id(self, new_car_controller_id):
        self.controller_id = new_car_controller_id

    def set_index_in_file(self, new_index):
        self.index_in_file = new_index

    def get_player(self):
        return self

    def get_name(self):
        return self.name


class Ball:
    index_in_file = 0

    def __init__(self, first_ball_id, vector: Vectors):
        self.ball_id = first_ball_id
        self.ball_pos = vector

    def set_ball_id(self, new_ball_id):
        self.ball_id = new_ball_id


def create_table(replay):

    current_word_for_id = '"actor_id": '

    def get_actor_by_id(put_player_list_in_here: [Player], id_of_searched_actor):
        for i in put_player_list_in_here:
            if i.id == id_of_searched_actor:
                return i

        if ball.ball_id == id_of_searched_actor:
            return ball

        # print("Player not found")

    def mustSave():
        dont_save = 0  # zu faul für enum
        player_save = 1
        car_save = 2
        ball_save = 3
        if replay.rr.find(
                'TAGame.Default__PRI_TA') < 100:  # 100 ist grobe Abschätzung = {"Id": 0, "NameId": 0, "TypeName": "TAGame.Default__PRI_TA", "ClassName": "TAGame.PRI_TA", "Initial + ...
            return player_save
        elif replay.rr.find('Archetypes.Car.Car_Default') < 100:
            return car_save
        elif replay.rr.find('Archetypes.Ball.Ball_Default') < 100:
            return ball_save

        return dont_save

    def get_int_after(token):
        # kann bis zu 3 ziffern lang sein. STRING BIS ZUM LETZTEN LEERZEICHEN VOR ZAHL EINGEBEN

        
        number_string = ""
        j = 0

        while True:
            try:
                number_string = number_string + replay.rr[replay.rr.find(token) + len(token) + j]  # get next ziffer
            except IndexError:
                print("erzähl mir mehr")

            not_number = replay.rr[replay.rr.find(token) + len(token) + j + 1]


            if not_number == "," or not_number == "}":
                break
            j += 1

            if j > 10:
                print("J ist zu groß lol")
                number_string = "-1337"
                break

        # checken, ob es auch wirklich ne zahl is
        try:
            number = int(number_string)
            return number
        except ValueError:
            # print("wroooooooooooong")
            return -1

        # print(number)       # debug

    def get_float_after(token):
        # kann bis zu 3 ziffern lang sein. STRING BIS ZUM LETZTEN LEERZEICHEN VOR ZAHL EINGEBEN

        number_string = ""
        j = 0

        while True:
            number_string = number_string + replay.rr[replay.rr.find(token) + len(token) + j]  # get next ziffer
            not_number = replay.rr[replay.rr.find(token) + len(token) + j + 1]
            if not_number == "," or not_number == "}":
                break
            j += 1

            if j > 10:
                print("J ist zu groß lol")

        try:
            number = float(number_string)
            return number
        except ValueError:
            # print("wroooooooooooong")
            return -1

    def read_vector():
        temp_x = get_float_after('"X": ')
        temp_y = get_float_after('"Y": ')
        temp_z = get_float_after('"Z": ')
        return [temp_x, temp_y, temp_z]

    # Macht ne schöne sortierte erste Liste, und ab dem zweiten mal speichert es nur die neuen variablen
    def get_player_list():

        unsorted_controllers = []
        nonlocal first_time

        while True:

            # cut vor "Id" : sobald es mehr als nur controller sind braucht das n rework
            replay.cut(current_word_for_id, - (len(current_word_for_id)+3))     # +3 für die bis zu 3 ziffern.

            temp_index = get_int_after(current_word_for_id)  # temp = String
            #print remaining lenght of rr
            print(replay.rr.__len__())

            needToSave = mustSave()
            if 0 != needToSave:  # = dont save

                if 1 == needToSave:  # = save player
                    temp_name = replay.rr[replay.rr.find('PlayerName": "') + 14: replay.rr.find('", "Engine.Player')]
                    temp_team = get_int_after('"ActorId": ')
                    current_player_list.append(Player(temp_index, temp_name, temp_team, Vectors(read_vector())))

                elif 2 == needToSave:  # = save CarId
                    found_player_id = get_int_after('"ActorId": ')
                    seT = True

                    if not first_time:
                        get_actor_by_id(current_player_list, found_player_id).set_current_car_controller_id(temp_index)
                    else:
                        for x in current_player_list:
                            if x.id == found_player_id:
                                seT = False
                                x.set_current_car_controller_id(temp_index)
                            elif seT:
                                # = [9,15]  ; 15 ist Ziel Id 9 is car controller
                                unsorted_controllers.append([temp_index, found_player_id])

                elif 3 == needToSave:  # save Ball
                    ball.set_ball_id(temp_index)
                    ball.ball_pos.set_update_pos(read_vector())
                # print("New Ball Index = " + str(ball.ball_id))

            replay.rr = replay.rr[len(current_word_for_id)+3:]

            # ABBRUCH: wenn keyword "Time" vor der nächsten "Id" zu finden ist
            next_time = replay.rr.find('"Time"')
            next_id = replay.rr.find('{"Id":')
            if next_time < next_id:
                print("Players Updated")
                break

        if first_time:

            # die noch nicht zugewiesen car_controller fixen
            for i in range(unsorted_controllers.__len__()):
                temp_player = get_actor_by_id(current_player_list, unsorted_controllers[i][1])
                if temp_player is not None:
                    temp_player.set_current_car_controller_id(unsorted_controllers[i][0])

            # finde größten Team Index
            temp_team_bigger = - 1
            for x in current_player_list:
                if x.team > temp_team_bigger:
                    temp_team_bigger = x.team

            # team umbenennen zu 0 und 1 und richtig zuweisen
            for x in current_player_list:
                if x.team < temp_team_bigger:
                    x.set_team(0)
                else:
                    x.set_team(1)

            # Liste nach Team sortieren
            current_player_list.sort(key=lambda p: p.team)

            # Alle Player mit ihrem Table index versehen
            next_index = 4
            for x in current_player_list:
                x.set_index_in_file(next_index)
                next_index += 4

            first_time = False
            print("First list created")

    def write_header(player_list: [Player]):
        worksheet_pos.write(0, 0, "Ball")
        i = 4
        for x in player_list:
            temp_name = x.name
            worksheet_pos.write(0, i, temp_name)
            i += 4

    def write_line(input_to_print):

        nonlocal frame

        # Ball Pos Printen
        ball_coordinates = ball.ball_pos.get_list()
        for i in range(3):
            worksheet_pos.write(frame, i + 1, ball_coordinates[i])

        # Player Pos Printen
        for x in input_to_print:
            for i in range(3):
                worksheet_pos.write(frame, x[0][0] + i + 1, x[1][i])  # an der richtigen stelle schreiben !!!

    def collect_data_til_next_goal_or_end():
        nonlocal frame
        list_to_print = []  # [[id],[x,y,z]],[id,...

        while True:

            next_occ_time = replay.rr.find('"Time": ')
            next_occ_id = replay.rr.find(current_word_for_id)
            if next_occ_time < next_occ_id:
                write_line(list_to_print)
                list_to_print = []
                frame += 1

            replay.cut(current_word_for_id, - (len(current_word_for_id)+3))
            next_id = get_int_after(current_word_for_id)

            if next_id == ball.ball_id:
                ball.ball_pos.set_update_pos(read_vector())
            else:
                for x in current_player_list:
                    temp_id = x.controller_id
                    if next_id == temp_id:
                        x.player_pos.set_update_pos(read_vector())
                        list_to_print.append([[x.index_in_file], read_vector()])

            # auf break testen: bis was in DeletedActorIds":[] was drinnen steht oder TickMarks auftaucht
            test = replay.rr[replay.rr.find('"DeletedActorIds": [') + len('"DeletedActorIds": ['):].find(']')

            if 0 < test:
                print("GOL / Del nicht leer!")
                replay.cut('"ActorUpdates": [{')
                break

            # Sobald "TickMarks" vor dem Nächsten "Time" kommt
            next_tick = replay.rr.find('"TickMarks"')
            next_time = replay.rr.find('"Time"')
            if next_tick < next_time:
                replay.rr = replay.rr[len(current_word_for_id)+3:]
                break

            replay.rr = replay.rr[len(current_word_for_id)+3:]


    #####################################


    workbook = xlsxwriter.Workbook('better_table.xlsx')
    worksheet_pos = workbook.add_worksheet("Positions")
    frame = 1
    ball = Ball(0, Vectors([0, 0, 0]))
    first_time = True
    current_player_list = []
    get_player_list()
    write_header(current_player_list)

    # von tor zu tor die tabelle füllen:
    while True:

        collect_data_til_next_goal_or_end()

        # Sobald "TickMarks" vor dem Nächsten "Time" kommt
        next_tick = replay.rr.find('"TickMarks"')
        next_time = replay.rr.find('"Time"')
        if next_tick < next_time:
            break

        if frame == 2488:
            print("debug")
        print(frame)

        get_player_list()


    workbook.close()

    print("fertig")

    return workbook

# Strat für smoothing:
# Spalte für Spalte entlang gehen und auffüllen
# dif zwischen werten durch entsprechende serie von leeren zellen teilen und gib ihm
# Interessant:
# - hab nur 1000 zeilen gecheckt, aber maximal 2 leer hintereinander, -> ich mach mal 3
# - bei kickoffs gibts Rießen abstände/ und falsche ball positionen in den player reihen
# aber statt das im code zu fixen, würd ichs im Nachhinein bearbeiten :D

# wichtige lines: 123 567 91011...  ??
# header zählt nicht und excel zählt ab 1. also daher die -2


def smoothing_table(excel_workbook):

    old_df = excel_workbook

    new_df = pd.ExcelWriter("smooth_table.xlsx")

    # copy the head of the table
    old_df.iloc[:0].to_excel(new_df, sheet_name="Positions", index=False)
    # copy the first four columns starting in the second row
    old_df.iloc[:, :4].to_excel(new_df, sheet_name="Positions", startrow=0, index=False)

    # interpolate the rest of the table
    old_df.iloc[:, 4:].interpolate().to_excel(new_df, sheet_name="Positions", startrow=0, startcol=4, index=False)

    new_df.close()


################################################
# ACTUAL CODE:

replay = Replay(re)
temp_table = create_table(replay)


temp_table = pd.read_excel("better_table.xlsx")

smoothing_table(temp_table)



#################################################
# Goals for next Time:

# basically noch alles was das smoothen angeht


#################################################
# Sometime?!:

# git einrichten (git_bash)

#################################################

# potenzielle fehlerquelle frame auf 1 gesetzt
