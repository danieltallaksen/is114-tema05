import pandas as pd
from dbexcel import forelder, barnehage, barn, soknad
from kgmodel import Foresatt, Barn, Soknad, Barnehage

# CRUD-metoder

def insert_foresatt(f):
    """Legger til en ny foresatt i DataFrame."""
    global forelder
    # Sjekk om DataFrame er tom og initialiser hvis nødvendig
    if 'foresatt_id' not in forelder.columns:
        forelder['foresatt_id'] = pd.Series(dtype='int')  # Initialiser foresatt_id kolonne hvis ikke finnes
    
    # Sørg for at foresatt_id er numerisk (tving konvertering til int)
    forelder['foresatt_id'] = pd.to_numeric(forelder['foresatt_id'], errors='coerce')
    
    # Sett foresatt_id til neste ledige ID
    new_id = 1  # Start med ID 1 hvis DataFrame er tom
    if not forelder.empty:
        new_id = forelder['foresatt_id'].max(skipna=True) + 1  # Hent neste ledige ID
    
    # Legg til ny foresatt i DataFrame
    forelder = pd.concat([pd.DataFrame([[new_id,
                                         f.foresatt_navn,
                                         f.foresatt_adresse,
                                         f.foresatt_tlfnr,
                                         f.foresatt_pnr]],
                                        columns=forelder.columns), forelder], ignore_index=True)
    
    return forelder

def insert_barn(b):
    """Legger til et nytt barn i DataFrame."""
    global barn
    # Sjekk om DataFrame er tom og initialiser hvis nødvendig
    if 'barn_id' not in barn.columns:
        barn['barn_id'] = pd.Series(dtype='int')  # Initialiser barn_id kolonne hvis ikke finnes
    
    # Sørg for at barn_id er numerisk
    barn['barn_id'] = pd.to_numeric(barn['barn_id'], errors='coerce')

    new_id = 1  # Start med ID 1 hvis DataFrame er tom
    if not barn.empty:
        new_id = barn['barn_id'].max(skipna=True) + 1  # Hent neste ledige ID
    
    # Legg til nytt barn i DataFrame
    barn = pd.concat([pd.DataFrame([[new_id, b.barn_pnr]],
                                   columns=barn.columns), barn], ignore_index=True)
    
    return barn

def insert_soknad(s):
    """Legger inn en ny søknad i soknad DataFrame."""
    global soknad
    new_id = 1  # Start med ID 1 hvis DataFrame er tom
    if not soknad.empty:
        new_id = soknad['sok_id'].max(skipna=True) + 1  # Hent neste ledige ID

    soknad = pd.concat([pd.DataFrame([[new_id,
                                       s.foresatt_1.foresatt_id,
                                       s.foresatt_2.foresatt_id,
                                       s.barn_1.barn_id,
                                       s.fr_barnevern,
                                       s.fr_sykd_familie,
                                       s.fr_sykd_barn,
                                       s.fr_annet,
                                       s.barnehager_prioritert,
                                       s.sosken__i_barnehagen,
                                       s.tidspunkt_oppstart,
                                       s.brutto_inntekt]],
                                      columns=soknad.columns), soknad], ignore_index=True)
    
    # Skriv til Excel etter at søknaden er lagt til
    commit_all()

    return soknad

def commit_all():
    """Skriver alle dataframes til Excel."""
    with pd.ExcelWriter('kgdata.xlsx', mode='a', if_sheet_exists='replace') as writer:
        forelder.to_excel(writer, sheet_name='foresatt', index=False)
        barnehage.to_excel(writer, sheet_name='barnehage', index=False)
        barn.to_excel(writer, sheet_name='barn', index=False)
        soknad.to_excel(writer, sheet_name='soknad', index=False)
    print("Alle data er skrevet til kgdata.xlsx")

def form_to_object_soknad(sd):
    """Konverterer formdata til Soknad-objekt."""
    foresatt_1 = Foresatt(0,
                          sd.get('navn_forelder_1'),
                          sd.get('adresse_forelder_1'),
                          sd.get('tlf_nr_forelder_1'),
                          sd.get('personnummer_forelder_1'))
    foresatt_2 = Foresatt(0,
                          sd.get('navn_forelder_2'),
                          sd.get('adresse_forelder_2'),
                          sd.get('tlf_nr_forelder_2'),
                          sd.get('personnummer_forelder_2'))
    
    foresatt_1.foresatt_id = insert_foresatt(foresatt_1)['foresatt_id'].max()
    foresatt_2.foresatt_id = insert_foresatt(foresatt_2)['foresatt_id'].max()

    # Lagring i hurtigminne av informasjon om barn
    barn_1 = Barn(0, sd.get('personnummer_barnet_1'))
    barn_1.barn_id = insert_barn(barn_1)['barn_id'].max()

    soknad = Soknad(0,
                    foresatt_1,
                    foresatt_2,
                    barn_1,
                    sd.get('fortrinnsrett_barnevern'),
                    sd.get('fortrinnsrett_sykdom_i_familien'),
                    sd.get('fortrinnsrett_sykdome_paa_barnet'),
                    sd.get('fortrinssrett_annet'),
                    sd.get('liste_over_barnehager_prioritert_5'),
                    sd.get('har_sosken_som_gaar_i_barnehagen'),
                    sd.get('tidspunkt_for_oppstart'),
                    sd.get('brutto_inntekt_husholdning'))
    return soknad

def select_alle_barnehager():
    """Henter alle barnehager fra barnehage DataFrame og konverterer til Barnehage-objekter."""
    return barnehage.apply(lambda r: Barnehage(r['barnehage_id'],
                                               r['barnehage_navn'],
                                               r['barnehage_antall_plasser'],
                                               r['barnehage_ledige_plasser']),
                           axis=1).to_list()
