# initiate script
import pandas as pd
from kgmodel import Barnehage

def initiate_db(db_name):
    kg1 = Barnehage(1,"Falkåsen Barnehage",25,12)
    kg2 = Barnehage(2,"Grasmyr naturbarnehage",60,0)
    kg3 = Barnehage(3,"Nustad Barnehage",30,5)
    kg4 = Barnehage(4,"Rønholdt Barnehage",18,2)
    kg5 = Barnehage(5,"Sunby Barnehage",18,6)
    kg6 = Barnehage(6,"Uksodden Barnehage",15,0)
    kg7 = Barnehage(7,"Stokkevannet Barnehage",45,8)
    kg8 = Barnehage(8, "Grashoppa Barnehage", 35,4)
    kg9 = Barnehage(9, "Solstua Barnehage", 24, 8)
    kg10 = Barnehage(10, "Tiriltoppen Barnehage", 50, 9)

    barnehage_liste = [kg1, kg2, kg3, kg4, kg5, kg6, kg7, kg8, kg9, kg10]
    
    
    kolonner_forelder =  ['foresatt_id',
                          'foresatt_navn',
                          'foresatt_adresse',
                          'foresatt_tlfnr',
                          'foresatt_pnr']
    kolonner_barnehage = ['barnehage_id',
                          'barnehage_navn',
                          'barnehage_antall_plasser',
                          'barnehage_ledige_plasser']
    kolonner_barn = ['barn_id',
                     'barn_pnr']
    kolonner_soknad = ['sok_id',
                       'foresatt_1',
                       'foresatt_2',
                       'barn_1',
                       'fr_barnevern',
                       'fr_sykd_familie',
                       'fr_sykd_barn',
                       'fr_annet',
                       'barnehager_prioritert',
                       'sosken__i_barnehagen',
                       'tidspunkt_oppstart',
                       'brutto_inntekt']
    
    forelder = pd.DataFrame(columns = kolonner_forelder)
    barnehage = pd.DataFrame(barnehage_liste, columns = kolonner_barnehage)
    barn = pd.DataFrame(columns = kolonner_barn)
    soknad  = pd.DataFrame(columns = kolonner_soknad)
    
    
    with pd.ExcelWriter(db_name) as writer:  
        forelder.to_excel(writer, sheet_name='foresatt')
        barnehage.to_excel(writer, sheet_name='barnehage')
        barn.to_excel(writer, sheet_name='barn')
        soknad.to_excel(writer, sheet_name='soknad')
    
    """
    b1 = Barn(1, "09012356472")
    f1 = Foresatt(1, "Ole Nordmann", "Bekkeveien 100", "98434344", "09079089332")
    f2 = Foresatt(2, "Solveig Imsdal", "Bekkeveien 100", "98434312", "09079233221")
    """




