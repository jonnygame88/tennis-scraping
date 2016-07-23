import pandas as pd
input_file = 'atp-input.csv'
base_path = 'C:\\Users\\Jonathan\\Documents\\'
base_path += 'Projects\\tennis-modelling\\data\\elo-ratings\\'
elo_input = pd.read_csv(base_path + input_file)

## define elo probability
def p_elo(ediff):
    return(1/(1+10**(-ediff/400)))

## define reference vectors
players = list(range(55000)); N = len(players)
elos = N*[7*[0]]; defaults = [1500, 1750, 2000, 2000, 2000, 2000, 1750]
mcounts = N*[8*[0]]; mlast = N*[0]

## generate elo ratings
for i in range(len(elo_input)):
    # get match values
    surface = elo_input.surface_id.loc[i]
    level = elo_input.level_id.loc[i]
    p1 = elo_input.winner_id.loc[i]
    p2 = elo_input.loser_id.loc[i]
    dval = elo_input.date_val.loc[i]
    w = elo_input.wscore.loc[i]
    # fetch reference values
    last1, last2 = mlast[p1], mlast[p2]
    ntotal1, ntotal2 = mcounts[p1][0], mcounts[p2][0]
    nsurface1, nsurface2 = mcounts[p1][surface], mcounts[p2][surface]
    if dval > last1 + 0.5: ncycle1 = 0
    else: ncycle1 = mcounts[p1][7]
    if dval > last2 + 0.5: ncycle2 = 0
    else: ncycle2 = mcounts[p2][7]
    if ntotal1 == 0: elo1 = defaults[level]
    else: elo1 = elos[p1][0]
    if ntotal2 == 0: elo2 = defaults[level]
    else: elo2 = elos[p2][0]
    if nsurface1 == 0: s_elo1 = elo1
    else: s_elo1 = elos[p1][surface]
    if nsurface2 == 0: s_elo2 = elo2
    else: s_elo2 = elos[p2][surface]
    # calculate expected scores, differences
    exp_main = p_elo(elo1-elo2)
    exp_surface = p_elo(s_elo1-s_elo2)
    d_main = w-exp_main
    d_surface = w-exp_surface
    # update input table
    elo_input = elo_input.set_value(i, 'p1_ntotal', ntotal1)
    elo_input = elo_input.set_value(i, 'p1_ncycle', ncycle1)
    elo_input = elo_input.set_value(i, 'p1_nsurface', nsurface1)
    elo_input = elo_input.set_value(i, 'p2_ntotal', ntotal2)
    elo_input = elo_input.set_value(i, 'p2_ncycle', ncycle2)
    elo_input = elo_input.set_value(i, 'p2_nsurface', nsurface2)
    elo_input = elo_input.set_value(i, 'p1_elo', elo1)
    elo_input = elo_input.set_value(i, 'p1_s_elo', s_elo1)
    elo_input = elo_input.set_value(i, 'p1_d_elo', d_main)
    elo_input = elo_input.set_value(i, 'p1_d_s_elo', d_surface)
    elo_input = elo_input.set_value(i, 'p2_elo', elo2)
    elo_input = elo_input.set_value(i, 'p2_s_elo', s_elo2)
    elo_input = elo_input.set_value(i, 'p2_d_elo', -d_main)
    elo_input = elo_input.set_value(i, 'p2_d_s_elo', -d_surface)
    # calculate k_vals
    if ntotal1 < 50 or ncycle1 < 20: kmain1 = 32
    else: kmain1 = 16
    if ntotal1 < 50 or ncycle1 < 20 or nsurface1 < 20: ksurface1 = 32
    else: ksurface1 = 16
    if ntotal2 < 50 or ncycle2 < 20: kmain2 = 32
    else: kmain2 = 16
    if ntotal2 < 50 or ncycle2 < 20 or nsurface2 < 20: ksurface2 = 32
    else: ksurface2 = 16
    # update reference vectors
    if elo_input.completed.loc[1] == 1 and level <= 5:
        elos[p1][0] = elo1 + kmain1*d_main
        elos[p1][surface] = s_elo1 + ksurface1*d_surface
        mcounts[p1][0] = ntotal1 + 1
        mcounts[p1][surface] = nsurface1 + 1
        elos[p2][0] = elo2 - kmain2*d_main
        elos[p2][surface] = s_elo2 - ksurface2*d_surface
        mcounts[p2][0] = ntotal2 + 1
        mcounts[p2][surface] = nsurface2 + 1
    # track progress
    if i%1000 == 0: print('completed ' + str(i))

## save output
elo_input.to_csv(base_path + 'atp-output.csv', index = False)
