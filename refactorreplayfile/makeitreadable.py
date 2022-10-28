# "ActorUpdates":[{"Id":1,"TAGame.GameEvent_Soccar_TA:bBallHasBeenHit":true}]},{"Time":14.6434307,"Delta":0.034722697,"DeletedActorIds":[],"ActorUpdates":[{"Id":6,"Engine.PlayerReplicationInfo:Ping":53}]},{"Time":15.26967,"Delta":0.035942,"DeletedActorIds":[],"ActorUpdates":[{"Id":1,"TAGame.GameEvent_Soccar_TA:SecondsRemaining":299}]},{"Time":16.1725063,"Delta":0.0347226,"DeletedActorIds":[],"ActorUpdates":[{"Id":6,"Engine.PlayerReplicationInfo:Ping":52}]},{"Time":16.20723,"Delta":0.0347228,"DeletedActorIds":[],"ActorUpdates":[{"Id":6,"Engine.PlayerReplicationInfo:Ping":53}]},{"Time":16.2419529,"Delta":0.034722697,"DeletedActorIds":[],"ActorUpdates":[{"Id":6,"Engine.PlayerReplicationInfo:Ping":52}]},{"Time":16.2766762,"Delta":0.0347226,"DeletedActorIds":[],"ActorUpdates":[{"Id":1,"TAGame.GameEvent_Soccar_TA:SecondsRemaining":298}]},{"Time":16.4502926,"Delta":0.0347236,"DeletedActorIds":[],
# USE CAREFULLY !!!!!!!!!!!!!!  GLOBAL WAS USED mybe
import json

with open("7F9346474A7AF3D2367450B5744BCFD9.json") as f:
    everything = json.load(f)

right_cut = json.dumps(everything)
left_cut = ""
next_enter = 0
dif_deleted_ids = 0
rows = []
i = 0

# print(right_cut)  # debug


# "Goals": [                                                                     Sampel
# {"Time": 47.296936, "PlayerName": "L3NN1", "PlayerTeam": 0},
# {"Time": 135.323242, "PlayerName": "L3NN1", "PlayerTeam": 0},
# {"Time": 261.6303, "PlayerName": "L3NN1", "PlayerTeam": 0},
# {"Time": 330.804474, "PlayerName": "L3NN1", "PlayerTeam": 0},
# {"Time": 359.558167, "PlayerName": "L3NN1", "PlayerTeam": 0}],



def get_identifier_char():
    next_index = right_cut.find('": ')
    identifier_char = right_cut[next_index + 3]
    # print(identifier_char)   #debug
    return identifier_char


def get_index_of_identifier_char():
    next_index = right_cut.find('": ')
    return next_index


def cut_case1(remaining_right_cut):  # case 1 = x oder "x"   Bsp; "Part1Length":3427,  oder; "Part1Crc":"D444417C",
    cut_index = remaining_right_cut.find(",", get_index_of_identifier_char()) + 1           # find next , +1 for ,
    # print(cut_index)                          # debug
    rows.append(remaining_right_cut[:cut_index])  # das schnipsel an die liste hängen
#    print(remaining_right_cut[:cut_index])              #debug
    return remaining_right_cut[cut_index:]                          # first test bestanden                              #


def cut_case2(remaining_right_cut):                     # zweite TODSÜNDE DER CODE WIRD KOPIERT IN CASE 3
    cut_index = remaining_right_cut.find("}", get_index_of_identifier_char()) + 2           # find next }  +2 for ,
    rows.append(remaining_right_cut[:cut_index])
#    print(remaining_right_cut[:cut_index])              #debug
    return remaining_right_cut[cut_index:]                      # first test bestanden                                  #


def cut_case3(remaining_right_cut ):

    while "]" != remaining_right_cut[remaining_right_cut.find("}")]:     # bis das ] nach dem } gefunden worden ist
        print(remaining_right_cut[remaining_right_cut.find("}")+3])       # debug
        cut_index = remaining_right_cut.find("}", get_index_of_identifier_char()) + 2           # find next } +2 for ,
        rows.append(remaining_right_cut[:cut_index])
        print(rows)                          # debug

    print(remaining_right_cut[:cut_index])                              # debug
    return remaining_right_cut[cut_index:]  # first test bestanden







# j = 0

# for i in rows:                                             # debug
# print(str(j) + i + "\n")
# j += 1

# with open("ex1formatted.TXT", "w") as asuwish:  # saving
# for i in positions:
#    asuwish.write(i + "\n")
