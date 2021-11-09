
import fitz

def gather_pay_data(LES_PATH, LES_FILES, data):

    for file in LES_FILES:  # Now we loop through each PDF and access the text
        with fitz.open(LES_PATH + '\\' + file) as doc:
            text = ""
            for page in doc:
                text += page.get_text()

        # Text data comes to us as one long string with \n as delimeter
        # We just need to make a list of strings split on \n
        text = text.split('\n')
        # Here is where we determine what string item coordesponds to what key
        # and we append to the main data, bearing in mind that after the main
        # info, the order will change and we need to go hunting
        data_dict = {
            'pp_end_date': text[40], 'pp_pay_date': text[41], 'base_pay': float(text[46]), 
            'ot_rate': float(text[65]), 'gross_pay': float(text[66]), 'tsp_pct' : text[79],
            'ytd_gross': float(text[67]), 'net_pay': float(text[76]), 'ytd_net': float(text[77]), 
            }
        
        # This is the main loop to go through all the remaining list items and find the critical info
        i = 78
        while i < 150:
            if text[i] == 'OVERTIME':
                try:
                    data_dict['ot_hrs']
                    i += 1
                except KeyError:
                    data_dict['ot_hrs'] = float(text[i + 1])
                    i += 3
            elif text[i] == 'MEDICARE':
                try:
                    data_dict['medicare']
                    i += 1
                except KeyError:
                    data_dict['medicare'] = float(text[i + 1])
                    i += 3
            elif text[i] == 'ORG/UNION':
                data_dict['union'] = float(text[i + 2])
                i += 4
            elif text[i] == 'TAX, FEDERAL':
                try:
                    data_dict['fed_tax']
                    i += 1
                except KeyError:
                    data_dict['fed_tax'] = float(text[i + 1])
                    i += 3
            elif text[i] == 'TSP SAVINGS':
                try:
                    data_dict['tsp']
                    i += 1
                except KeyError:
                    data_dict['tsp'] = float(text[i + 1])
                    i += 3
            elif text[i] == 'FEHB':
                try:
                    data_dict['fehb']
                    i += 1
                except KeyError:    
                    data_dict['fehb'] = float(text[i + 1])
                    i += 4
            elif text[i] == 'OASDI':
                try:
                    data_dict['oasdi']
                    i += 1
                except KeyError:
                    if float(text[i + 1]) > 2000:
                        i += 2
                        pass
                    else:
                        data_dict['oasdi'] = float(text[i + 1])
                        i += 3
            elif text[i] == 'RETIRE, FERS':
                try:
                    data_dict['fers']
                    i += 1
                except KeyError:
                    data_dict['fers'] = float(text[i + 2])
                    i += 4
            elif text[i] == 'TAX, STATE':
                try:
                    data_dict['state_tax']
                    i += 1
                except KeyError:    
                    data_dict['state_tax'] = float(text[i + 2])
                    i += 4
            else:
                i += 1
        # Now we deterimine if there was any extra pay by comparing the last FY gross pay
        # to this FY gross pay along with regular pay and PP gross pay
        regular_pay = float(text[88])  # used later to determine pay differences below
        try: 
            extra_pay = data_dict['gross_pay'] - regular_pay - (data_dict['ot_hrs'] * data_dict['ot_rate'])
        except KeyError:
            extra_pay = data_dict['gross_pay'] - regular_pay
        if extra_pay > 1:
            data_dict['extra_pay'] = extra_pay
        
        # Main append to the DataFrame
        data = data.append(data_dict, 
            ignore_index=True)
    return data