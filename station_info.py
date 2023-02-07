# Line full name
line = {'AEL':'Airport Express',\
        'TCL':'Tung Chung Line',\
        'TML':'Tuen Ma Line',\
        'TKL':'Tseung Kwan O Line',\
        'EAL':'East Rail Line'}

# Station Full name
sta = {\
    # AEL Airport Express
    'HOK' : 'Hong Kong',\
    'KOW' :'Kowloon',\
    'TSY' :'Tsing Yi',\
    'AIR' :'Airport',\
    'AWE' :'AsiaWorld Expo',\
    # TCL Tung Chung Line
    'HOK' : 'Hong Kong',\
    'KOW' : 'Kowloon',\
    'OLY' : 'Olympic',\
    'NAC' : 'Nam Cheong',\
    'LAK' : 'Lai King',\
    'TSY' : 'Tsing Yi',\
    'SUN' : 'Sunny Bay',\
    'TUC' : 'Tung Chung',\
    # TML Tuen Ma Line
    'WKS' : 'Wu Kai Sha',\
    'MOS' : 'Ma On Shan',\
    'HEO' : 'Heng On',\
    'TSH' : 'Tai Shui Hang',\
    'SHM' : 'Shek Mun',\
    'CIO' : 'City One',\
    'STW' : 'Sha Tin Wai',\
    'CKT' : 'Che Kung Temple',\
    'TAW' : 'Tai Wai',\
    'HIK' : 'Hin Keng',\
    'DIH' : 'Diamond Hill',\
    'KAT' : 'Kai Tak',\
    'SUW' : 'Sung Wong Toi',\
    'TKW' : 'To Kwa Wan',\
    'HOM' : 'Ho Man Tin',\
    'HUH' : 'Hung Hom',\
    'ETS' : 'East Tsim Sha Tsui',\
    'AUS' : 'Austin',\
    'NAC' : 'Nam Cheong',\
    'MEF' : 'Mei Foo',\
    'TWW' : 'Tsuen Wan West',\
    'KSR' : 'Kam Sheung Road',\
    'YUL' : 'Yuen Long',\
    'LOP' : 'Long Ping',\
    'TIS' : 'Tin Shui Wai',\
    'SIH' : 'Siu Hong',\
    'TUM' : 'Tuen Mun',\
    # TKL Tseung Kwan O Line
    'NOP' : 'North Point',\
    'QUB' : 'Quarry Bay',\
    'YAT' : 'Yau Tong',\
    'TIK' : 'Tiu Keng Leng',\
    'TKO' : 'Tseung Kwan O',\
    'LHP' : 'LOHAS Park',\
    'HAH' : 'Hang Hau',\
    'POA' : 'Po Lam',\
    # EAL East Rail Line
    'ADM' : 'Admiralty',\
    'EXC' : 'Exhibition Centre',\
    'HUH' : 'Hung Hom',\
    'MKK' : 'Mong Kok East',\
    'KOT' : 'Kowloon Tong',\
    'TAW' : 'Tai Wai',\
    'SHT' : 'Sha Tin',\
    'FOT' : 'Fo Tan',\
    'RAC' : 'Racecourse',\
    'UNI' : 'University',\
    'TAP' : 'Tai Po Market',\
    'TWO' : 'Tai Wo',\
    'FAN' : 'Fanling',\
    'SHS' : 'Sheung Shui',\
    'LOW' : 'Lo Wu',\
    'LMC' : 'Lok Ma Chau'}

list_line_key = []
list_line_val = []
for i, j in line.items():
    list_line_key.append(str(i))
    list_line_val.append(str(j))
#print(list_line_key)
#print(list_line_val)
list_sta_key = []
list_sta_val = []
for i, j in sta.items():
    list_sta_key.append(str(i))
    list_sta_val.append(str(j))
#print(list_sta_key)
#print(list_sta_val)