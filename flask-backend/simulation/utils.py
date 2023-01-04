import math
import enum
import sys
FLOAT_MAX = sys.float_info.max

class SimulationState(enum.Enum):
  Running = enum.auto()
  Finished = enum.auto()
  Paused = enum.auto()
  Cancelled = enum.auto()

def secToTimeStr(race_time :float) -> str:
    if race_time == FLOAT_MAX:
        return "No Time"
    elif race_time < FLOAT_MAX and race_time > FLOAT_MAX / 2:
        return "---"
    temp_time = round(race_time, 3)
    hours = 0
    minutes = 0
    seconds = 0
    milliseconds = 0
    time_str = ""

    if temp_time > 3600:
        hours = int(temp_time // 3600)
        temp_time = temp_time - (hours * 3600)
    
    if temp_time > 60:
        minutes = int(temp_time // 60)
        temp_time = temp_time - (minutes * 60)

    if temp_time > 0:
        seconds = int(math.floor(temp_time))
        temp_time = temp_time - seconds

    if temp_time > 0:
        milliseconds = int(temp_time * 1000)

    if hours > 0:
        time_str = "{hours}:{minutes:02}:{seconds:02}.{milliseconds:03}".format(hours=hours, minutes=minutes, seconds=seconds, milliseconds=milliseconds)
    elif minutes > 0:
        time_str = "{minutes}:{seconds:02}.{milliseconds:03}".format(minutes=minutes, seconds=seconds, milliseconds=milliseconds)
    elif seconds >= 0:
        time_str = "{seconds}.{milliseconds:03}".format(seconds=seconds, milliseconds=milliseconds)


    return time_str

def nationCodeToFlag(nationCode: str) -> str:
    flags = {"AND": "ad.png", #Andorra
         "UAE": "ae.png", #UAE
         "AFG": "af.png", #Afghanistan (republic)
         "ALB": "al.png", #Albania
         "ARM": "am.png", #Armenia
         "ANG": "ao.png", #Angola
         "ANT": "aq.png", #Antarctica
         "ARG": "ar.png", #Argentina
         "ASA": "as.png", #American Samoa
         "AUT": "at.png", #Austria
         "AUS": "au.png", #Australia
         "ARU": "aw.png", #Aruba
         "ALA": "ax.png", #Aland
         "AZE": "az.png", #Azerbaijan
         "BIH": "ba.png", #Bosnia and Herzegovina
         "BAR": "bb.png", #Barbados
         "BAN": "bd.png", #Bangladesh
         "BEL": "be.png", #Belgium
         "BUR": "bf.png", #Burkina Faso
         "BUL": "bg.png", #Bulgaria
         "BAH": "bh.png", #Bahrain
         "BDI": "bi.png", #Burundi
         "BEN": "bj.png", #Benin
         "BER": "bm.png", #Bermuda
         "BRU": "bn.png", #Brunei
         "BOL": "bo.png", #Bolivia
         "BRA": "br.png", #Brazil
         "BHM": "bs.png", #Bahrain
         "BHU": "bt.png", #Bhutan
         "BOT": "bw.png", #Botswana
         "BLR": "by.png", #Belarus
         "BLZ": "bz.png", #Belize
         "CAN": "ca.png", #Canada
         "COC": "cc.png", #Cocos Islands
         "CON": "cd.png", #DR Congo
         "CAR": "cf.png", #CAR
         "CGO": "cg.png", #Republic of the COngo
         "SUI": "ch.png", #Switzerland
         "CIV": "ci.png", #Cote d'Ivoire
         "COO": "ck.png", #Cook Islands
         "CHI": "cl.png", #Chile
         "CAM": "cm.png", #Cameroon
         "CHN": "cn.png",
         "COL": "co.png",
         "COS": "cr.png",
         "CUB": "cu.png",
         "CAV": "cv.png",
         "CUR": "cw.png",
         "CHR": "cx.png",
         "CYP": "cy.png",
         "CZE": "cz.png",
         "CSSR": "cz.png", #Czechoslovakia 
         "GER": "de.png",
         "DJI": "dj.png",
         "DEN": "dk.png",
         "DMI": "dm.png",
         "DOM": "do.png",
         "ALG": "dz.png",
         "ECU": "ec.png",
         "EST": "ee.png",
         "EGY": "eg.png",
         "ERI": "er.png",
         "ESP": "es.png",
         "ETH": "et.png",
         "FIN": "fi.png",
         "FIJ": "fj.png",
         "MIC": "fm.png",
         "FAR": "fo.png",
         "FRA": "fr.png",
         "GAB": "ga.png",
         "GBR": "gb.png",
         "ENG": "gb-eng.png",
         "SCO": "gb-sct.png",
         "WAL": "gb-wls.png",
         "NIR": "gb-nir.png",
         "GRE": "gd.png",
         "GEO": "ge.png",
         "GUR": "gg.png",
         "GHA": "gh.png",
         "GIB": "gi.png",
         "GRL": "gl.png", #Greenland
         "GAM": "gm.png", #Gambia
         "GUI": "gn.png", #Guinea
         "GDL": "gp.png", #Guadeloupe
         "EQG": "gq.png", #Equatorial Guinea
         "GRE": "gr.png", #Greece
         "GUA": "gt.png", #Guatemala
         "GUM": "gu.png", #Guam
         "GUB": "gw.png", #Guinea Bissau
         "GUY": "gy.png", #Guyana
         "HKG": "hk.png", #Hong Kong
         "HON": "hn.png", #Honduras
         "CRO": "hr.png", #Croatia
         "HAI": "ht.png", #Haiti
         "HUN": "hu.png", #Hungary
         "INA": "id.png", #Indonesia
         "IRE": "ie.png", #Irealnd
         "IRL": "ie.png", #Ireland 2 (because I'm inconsistent with abbreviations)
         "ISR": "il.png", #Israel
         "IOM": "im.png", #Isle of Man (baker pls!)
         "IND": "in.png", #India
         "IRQ": "iq.png", #Iraq
         "IRN": "ir.png", #Iran
         "ICE": "is.png", #Iceland
         "ITA": "it.png", #Italy
         "JER": "je.png", #Jersey
         "JAM": "jm.png", #Jamaica
         "JOR": "jo.png", #Jordan
         "JPN": "jp.png", #Japan
         "KEN": "ke.png", #Kenya
         "KYR": "kg.png", #Kyrgyzstan
         "CBD": "kh.png", #Cambodia
         "KIR": "ki.png", #Kiribati
         "COM": "km.png", #Comoros
         "KNV": "kn.png", #St. Kitts and Nevis
         "DPK": "kp.png", #Best Korea
         "KOR": "kr.png", #Korea
         "KUW": "kw.png", #Kuwait
         "KAZ": "kz.png", #Kazakhstan (greatest country in the world!)
         "LAO": "la.png", #Laos
         "LEB": "lb.png", #Lebanon
         "LUC": "lc.png", #St. Lucia
         "LIE": "li.png", #Liechtenstein
         "SRI": "lk.png", #Sri Lanka
         "LIB": "li.png", #Liberia
         "LES": "ls.png", #Lesotho
         "LIT": "lt.png", #Lithuania
         "LUX": "lu.png", #Luxembourg
         "LAT": "lv.png", #Latvia
         "LBY": "ly.png", #Libya
         "MOR": "ma.png", #Morocco
         "MON": "mc.png", #Monaco
         "MOL": "md.png", #Moldova
         "MNE": "me.png", #Montenegro
         "MAD": "mg.png", #Madagascar
         "MSH": "mh.png", #Marshal Islands (this is where the marshals come from)
         "MAC": "mk.png", #North Macedonia (not to be confused with South Macedonia aka Greece)
         "MLI": "ml.png", #Mali
         "MNG": "mn.png", #Mongolia
         "MCO": "mo.png", #Macau
         "MNQ": "mq.png", #Martinique
         "MAU": "mr.png", #Mauritania
         "MTA": "mt.png", #Malta
         "MRI": "mu.png", #Mauritius 
         "MDV": "mv.png", #Maldives
         "MWI": "mw.png", #Malawi
         "MEX": "mx.png", #Mexico
         "MAL": "my.png", #Malaysia
         "MOZ": "mz.png", #Mozambique
         "NAM": "na.png", #Namibia
         "NCD": "nc.png", #New Caledonia (old Caledonia isn't French!)
         "NIG": "ne.png", #Niger
         "NFI": "nf.png", #Norfolk Island - Second best flag with tree
         "NGA": "ng.png", #Nigeria
         "NIC": "ni.png", #Nicaragua
         "NED": "nl.png", #Netherlands MAX MAX MAX SUPER MAX MAX MAX
         "NOR": "no.png", #Norway 
         "NEP": "np.png", #Nepal
         "NAU": "nr.png", #Nauru
         "NIU": "nu.png", #Niue
         "NZL": "nz.png", #New Zealand
         "OMA": "om.png", #Oman
         "PAN": "pa.png", #Panama
         "PER": "pe.png", #Peru
         "TAH": "pf.png", #Tahiti
         "PNG": "pg.png", #Papua New Guinea
         "PHI": "ph.png", #Philippines
         "PAK": "pk.png", #Pakistan
         "POL": "pl.png", #Poland
         "PRI": "pr.png", #Puerto Rico
         "PAL": "ps.png", #Palestine
         "POR": "pt.png", #Portugal
         "PLU": "pw.png", #Palau
         "PAR": "py.png", #Paraguay
         "QAT": "qa.png", #Qatar
         "ROM": "ro.png", #Romania
         "SER": "rs.png", #Serbia
         "RUS": "ru.png", #Russia
         "RWA": "rw.png", #Rwanda
         "SAU": "sa.png", #Saudi Arabia
         "KSA": "sa.png", #Saudi Arabia
         "SOL": "sb.png", #Solomon Islands
         "SEY": "sc.png", #Seychelles
         "SUD": "sd.png", #Sudan
         "SWE": "se.png", #Sweden
         "SIN": "sg.png", #Singapore
         "SLO": "si.png", #Slovenia
         "SVK": "sk.png", #Slovakia
         "SLE": "sl.png", #Sierra Leone
         "SMR": "sm.png", #San Marino
         "SEN": "sn.png", #Senegal
         "SOM": "so.png", #Somalia
         "SUR": "sr.png", #Suriname
         "SSD": "ss.png", #South Sudan
         "STP": "st.png", #Sao Tome and Principe
         "SAL": "sv.png", #El Salvador
         "SYR": "sy.png", #Syria
         "SWA": "sz.png", #ESwatini
         "CHA": "td.png", #Chad
         "TOG": "tg.png", #Togo
         "THA": "th.png", #Thailand
         "TAJ": "tj.png", #Tajikistan
         "TOK": "tk.png", #Tokelau
         "TIL": "tl.png", #Timor-Leste
         "TME": "tm.png", #Turkmenistan
         "TUN": "tn.png", #Tunisia
         "TON": "to.png", #Tonga
         "TUR": "tr.png", #Turkey
         "TRI": "tt.png", #Trinidad and Tobago
         "TUV": "tv.png", #Tuvalu
         "TAI": "tw.png", #Taiwan
         "TAN": "tz.png", #Tanzania
         "UKR": "ua.png", #Ukraine
         "UGA": "ug.png", #Uganda
         "USA": "us.png", #USA
         "URU": "uy.png", #Uruguay
         "UZB": "uz.png", #Uzbekistan
         "VAT": "va.png", #Vatican
         "SVI": "vc.png", #St Vicent
         "VEN": "ve.png", #Venezuela
         "VIE": "vn.png", #Vietnam
         "VAN": "vu.png", #Vanuatu
         "SAM": "ws.png", #Samoa
         "KOS": "xk.png", #Kosovo
         "YEM": "ye.png", #Yemen
         "RSA": "za.png", #South Africa
         "ZAM": "zm.png", #Zambia
         "ZIM": "zw.png", #Zimbabwe
         "RHO": "rh.png", #Rhodesia
         "YUG": "rs.png", #Yugoslavia
         "USSR": "su.png", #USSR
         }
    return flags.get(nationCode)