
# Normalization constants (from your MATLAB output)
MU_X = [
        230.9398217557887846851372160017490386962891, 
        19.5920039980010329827564419247210025787354, 
        4194.1321546404205946600995957851409912109375
    ]
SIG_X = [
        305.4770190790853234830137807875871658325195 , 
        5.9114260306857273619129955477546900510788, 
        5602.8786687436795546091161668300628662109375
    ]
MU_T = 4194.1321546404205946600995957851409912109375
SIG_T = 5602.8786687436795546091161668300628662109375


def denormalize_pred(num):
    return num * SIG_T + MU_T

def normalize_pred(num):
    return (num - MU_X[2]) / SIG_X[2]

def normalize_list(ls):

    return [normalize_datapoint(entry) for entry in ls]

def normalize_datapoint(raw):
    """raw: dict or list-like with 6 un-normalized values in order
    [irradiance, temperature, true_power, hour, day_of_week, month]


    returns: normalized features as Python list of 6 floats (same order)
    """
    irr, temp, p, hour, day_of_week, month = raw


    # MATLAB normalized first 3 via normalize (x - mu)/sigma
    irr_n = (irr - MU_X[0]) / SIG_X[0]
    temp_n = (temp - MU_X[1]) / SIG_X[1]
    p_n = (p - MU_X[2]) / SIG_X[2]


    # date features normalized as in MATLAB:
    hour_n = hour / 23.0
    dow_n = (day_of_week - 1) / 6.0
    month_n = (month - 1) / 11.0


    return [irr_n, temp_n, p_n, hour_n, dow_n, month_n]