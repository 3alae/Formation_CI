def get_fixed_prov_name(celda_name):
    suffix = celda_name[0:3]
    data = {'AND':'AND',
            'ARA':'ARG',
            'AST':'AST',
            'CAN':'CAN',
            'CLM':'CAM',
            'CYL':'CAL',
            'CAT':'CAT',
            'VAL':'CVA',
            'EXT':'EXT',
            'GAL':'GAL',
            'BAL':'IBA',
            'CAN':'ICA',
            'MAD':'MAD',
            'MUR':'MUR',
            'NAV':'NAV',
            'PVA':'PVA',
            'RIO':'RIO'
           }
    try: 
        return data[suffix]
    except:
        return None





