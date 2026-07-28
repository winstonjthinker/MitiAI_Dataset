import csv
import json
import hashlib
import os

processed_dir = r"C:\Users\HP\Downloads\Miti Ai BioBank_v1.0\mitiAI_ZW_Biobank v1.1_Dataset\mitiai_zw_biobank_v1.0_ai4i_data\processed"
governance_dir = r"C:\Users\HP\Downloads\Miti Ai BioBank_v1.0\mitiAI_ZW_Biobank v1.1_Dataset\mitiai_zw_biobank_v1.0_ai4i_data\governance"
labels_dir = r"C:\Users\HP\Downloads\Miti Ai BioBank_v1.0\mitiAI_ZW_Biobank v1.1_Dataset\mitiai_zw_biobank_v1.0_ai4i_data\labels"

def sha256_text(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

# ---------------------------------------------------------
# 1. HERITAGE KNOWLEDGE (50 records) & CONSENT LOG (50 entries)
# Anchored on the 3 Focal Pillars:
#  1. African / Wild Ginger (Tsangamidzi / Isiphepheto)
#  2. Pepper-bark Tree (Muranga / Isibhaha)
#  3. Water Hyacinth (Yacinthi Yemumvura / Inkazana Yemanzini)
# ---------------------------------------------------------

heritage_plants = [
    # Pillar 1: African Ginger / Wild Ginger (Zingiberaceae)
    ("Tsangamidzi", "sn", "Siphonochilus aethiopicus", "Midzi inoshandiswa pachikosoro nemhino dzakavharika", "Rhizome used for cough, flu, and asthma relief", "CA23", "Midzi inotsengwa kana kubikwa zvidiki", "decoction", "root", "oral", "both", "Manicaland", "Chimanimani", "W12", "HLD-EH-007", "CC-CHIMANIMANI-03", "END-CC03-2026-011", "public", "confidential", "AUD-RES-001", "VAL-002", "LIA-EH-01"),
    ("Isiphepheto", "nd", "Siphonochilus aethiopicus", "Izimpande zisetshenziselwa umkhuhlane wezifuba nefiva", "Rhizomes used for severe respiratory distress and fever", "CA23", "Izimpande ziyagxotshwa amanzini afudumeleyo", "infusion", "root", "oral", "both", "Matabeleland North", "Hwange", "W14", "HLD-MW-081", "CC-HWANGE-06", "END-CC06-2026-003", "community-restricted", "confidential", "AUD-RES-002", "VAL-001", "LIA-MW-03"),
    ("Tsangamidzi Yemukati", "sn", "Zingiber officinale", "Midzi inoshandiswa pakurwadziwa kwedumbu nefiva", "Ginger rhizome used for stomach cramps and nausea", "DD90", "Midzi inokuyiwa kuita hupfu hunonwiwa", "powder", "root", "oral", "both", "Mashonaland Central", "Mazowe", "W03", "HLD-EH-011", "CC-CHIMANIMANI-03", "END-CC03-2026-011", "public", "confidential", "AUD-RES-003", "VAL-002", "LIA-EH-01"),

    # Pillar 2: Pepper-bark Tree (Warburgia salutaris)
    ("Muranga", "sn", "Warburgia salutaris", "Makwati anobikwa pachikosoro nemamota emuchipfuva", "Bark decoction used for severe cough and chest pain", "CA23", "Makwati anobikwa kwemaminetsi makumi maviri", "decoction", "bark", "oral", "both", "Manicaland", "Chimanimani", "W12", "HLD-EH-019", "CC-CHIMANIMANI-03", "END-CC03-2026-011", "public", "confidential", "AUD-RES-004", "VAL-002", "LIA-EH-01"),
    ("Isibhaha", "nd", "Warburgia salutaris", "Amaxolo amuleyo asetshenziselwa umkhuhlane nembuzane", "Peppery bark used for fever, malaria, and chest tightness", "1F40", "Amaxolo agxotshwa aphekwe emanzini", "decoction", "bark", "oral", "both", "Masvingo", "Chiredzi", "W08", "HLD-LV-004", "CC-CHIREDZI-07", "END-CC07-2026-004", "community-restricted", "confidential", "AUD-RES-005", "VAL-005", "LIA-LV-02"),
    ("Mubvamaropa", "sn", "Pterocarpus angolensis", "Inoshandiswa pakumira kweropa", "Used to stop bleeding", "", "Muto unoiswa panxeba", "poultice", "bark", "topical", "both", "Manicaland", "Nyanga", "W03", "HLD-EH-022", "CC-NYANGA-05", "END-CC05-2026-002", "public", "confidential", "", "VAL-002", "LIA-EH-01"), # WITHDRAWN

    # Pillar 3: Water Hyacinth (Eichhornia crassipes)
    ("Yacinthi Yemumvura", "sn", "Eichhornia crassipes", "Inoshandiswa pakuchenesa mvura nekugadzira mufudze", "Aquatic plant used for water filtration and organic mulch", "", "Mashizha nemidzi zvinoomeswa", "other", "na", "na", "both", "Mashonaland Central", "Mazowe", "W08", "HLD-MW-002", "CC-GOKWE-02", "END-CC02-2026-009", "public", "public", "", "VAL-004", "LIA-MW-01"),
    ("Inkazana Yemanzini", "nd", "Eichhornia crassipes", "Isihlahla samanzini esisetshenziswa ukuhlanza imifula", "Aquatic plant monitored for river phytoremediation", "", "Izimfundo zamakhasi emanzini", "other", "na", "na", "both", "Matabeleland North", "Binga", "W02", "HLD-LV-009", "CC-BINGA-01", "END-CC01-2026-002", "public", "public", "", "VAL-005", "LIA-LV-02"),

    # Supporting flora
    ("Mukamba", "sn", "Afzelia quanzensis", "Makwati anoshandiswa pazino rinorwadza", "Bark used for toothache", "1F40", "Makwati anoshandiswa pazino rinorwadza", "decoction", "bark", "oral", "dry", "Manicaland", "Chimanimani", "W07", "HLD-EH-026", "CC-CHIMANIMANI-03", "END-CC03-2026-011", "community-restricted", "confidential", "AUD-RES-007", "VAL-001", "LIA-EH-01"),
    ("Umnyii", "nd", "Berchemia discolor", "Izithelo zisetshenziselwa ukudla okuncane", "Fruit used for poor appetite", "DA0Z", "Izithelo zisetshenziselwa ukudla okuncane", "infusion", "fruit", "oral", "both", "Matabeleland North", "Hwange", "W17", "HLD-MW-088", "CC-HWANGE-06", "END-CC06-2026-003", "community-restricted", "confidential", "AUD-RES-008", "VAL-001", "LIA-MW-03"),
    ("Umsehla", "nd", "Peltophorum africanum", "Amaxolo asetshenziselwa isisu", "Bark used for stomach complaints", "CA23", "Amaxolo asetshenziselwa isisu", "decoction", "bark", "oral", "both", "Masvingo", "Chiredzi", "W21", "HLD-LV-039", "CC-CHIREDZI-07", "END-CC07-2026-004", "public", "confidential", "AUD-RES-009", "VAL-003", "LIA-LV-03"),
    ("Munhondo", "sn", "Julbernardia globiflora", "Makwati anoshandiswa pahosha yedumbu", "Bark used for stomach complaints", "DD90", "Makwati anobikwa mumvura", "decoction", "bark", "oral", "dry", "Manicaland", "Chimanimani", "W14", "HLD-EH-024", "CC-CHIMANIMANI-03", "END-CC03-2026-011", "public", "confidential", "AUD-RES-010", "VAL-001", "LIA-EH-01"),
    ("Mupangara", "sn", "Dichrostachys cinerea", "Midzi inotsengwa pakurwadziwa kwezino", "Root chewed for toothache", "1F40", "Midzi inotsengwa mumuromo", "chewed_raw", "root", "oral", "both", "Manicaland", "Nyanga", "W09", "HLD-EH-042", "CC-NYANGA-05", "END-CC05-2026-002", "community-restricted", "confidential", "AUD-RES-011", "VAL-002", "LIA-EH-02"),
    ("Umtshwili", "nd", "Tarchonanthus camphoratus", "Amaqabunga asetshenziselwa inhlungu zezinkondo", "Leaves used for chest pains and colds", "CA23", "Amaqabunga apheka athuswe", "smoke_inhalation", "leaf", "inhalation", "both", "Midlands", "Gokwe", "W11", "HLD-MW-055", "CC-GOKWE-02", "END-CC02-2026-009", "community-restricted", "confidential", "AUD-RES-012", "VAL-004", "LIA-MW-02"),
    ("Umkhwenkwe", "nd", "Pittosporum viridiflorum", "Amaxolo asetshenziselwa umkhuhlane", "Bark used for fever and malaria", "1F40", "Amaxolo aphekwa phansi", "decoction", "bark", "oral", "dry", "Masvingo", "Chiredzi", "W15", "HLD-LV-069", "CC-CHIREDZI-07", "END-CC07-2026-004", "public", "confidential", "AUD-RES-013", "VAL-003", "LIA-LV-01"),
    ("Muunga", "sn", "Vachellia karroo", "Makwati anoshandiswa pachikosoro", "Bark used for cough", "CA23", "Makwati anonyikwa mumvura inopisa", "infusion", "bark", "oral", "wet", "Masvingo", "Chiredzi", "W02", "HLD-LV-021", "CC-CHIREDZI-07", "END-CC07-2026-004", "public", "confidential", "AUD-RES-014", "VAL-005", "LIA-LV-02"),
    ("Mupfuti", "sn", "Brachystegia boehmii", "Makwati anoshandiswa panxeba", "Bark used for open wounds", "1B70", "Hupfu hwemakwati hunoiswa panxeba", "powder", "bark", "topical", "both", "Manicaland", "Nyanga", "W01", "HLD-EH-088", "CC-NYANGA-05", "END-CC05-2026-002", "community-restricted", "confidential", "AUD-RES-015", "VAL-001", "LIA-EH-02"),
    ("Mubvumira", "sn", "Kirkia acuminata", "Midzi inoshandiswa pazvirwere zvomudumbu", "Roots used for abdominal disorders", "DD90", "Midzi inobikwa kwenguva pfupi", "decoction", "root", "oral", "dry", "Midlands", "Gokwe", "W08", "HLD-MW-019", "CC-GOKWE-02", "END-CC02-2026-009", "public", "confidential", "AUD-RES-016", "VAL-004", "LIA-MW-01"),
    ("Umgampondo", "nd", "Bauhinia thonningii", "Amaqabunga asetshenziselwa umkhuhlane wephesheya", "Leaves used for severe respiratory infections", "CA23", "Amaqabunga aphekwa emanzini", "decoction", "leaf", "oral", "both", "Matabeleland North", "Hwange", "W04", "HLD-MW-094", "CC-HWANGE-06", "END-CC06-2026-003", "public", "confidential", "AUD-RES-017", "VAL-001", "LIA-MW-03"),
    ("Musasa", "sn", "Brachystegia spiciformis", "Makwati anoshandiswa pamaziiso anorwadza", "Bark used for eye inflammation", "9A00", "Muto womukati memakwati", "infusion", "bark", "topical", "dry", "Manicaland", "Chimanimani", "W05", "HLD-EH-052", "CC-CHIMANIMANI-03", "END-CC03-2026-011", "public", "confidential", "AUD-RES-018", "VAL-002", "LIA-EH-01"),
    ("Gavakava", "sn", "Aloe excelsa", "Muto wemashizha unoshandiswa pazvidonda zvemudumbu", "Leaf sap used for gastric ulcers", "DA42", "Muto unonwiwa zvishoma", "infusion", "leaf", "oral", "both", "Manicaland", "Chimanimani", "W10", "HLD-EH-061", "CC-CHIMANIMANI-03", "END-CC03-2026-011", "public", "confidential", "AUD-RES-019", "VAL-002", "LIA-EH-01"),
    ("Inhlaba", "nd", "Aloe arborescens", "Ijusi yamakhasi isetshenziswa esiswini", "Leaf gel used for stomach pain and burns", "DA42", "Ijusi inwiswa emanzini", "infusion", "leaf", "oral", "both", "Matabeleland South", "Matobo", "W04", "HLD-MS-012", "CC-MATOBO-04", "END-CC04-2026-001", "public", "confidential", "AUD-RES-020", "VAL-003", "LIA-MS-01"),
    ("Muuyu", "sn", "Adansonia digitata", "Hupfu hwemuchero hunoshandiswa pahosha dzedumbu nefiva", "Fruit pulp used for fever and diarrhea", "DD91", "Hupfu hunosanganiswa nemvura", "infusion", "fruit", "oral", "dry", "Masvingo", "Chiredzi", "W12", "HLD-LV-051", "CC-CHIREDZI-07", "END-CC07-2026-004", "public", "confidential", "AUD-RES-021", "VAL-005", "LIA-LV-02"),
    ("Umkhomo", "nd", "Adansonia digitata", "Umgubho wesithelo usetshenziswa lapho umntwana ethola umkhuhlane", "Fruit pulp given to children for fever", "MG50", "Umgubho uyagxotshwa emanzini", "infusion", "fruit", "oral", "dry", "Matabeleland North", "Binga", "W02", "HLD-BN-008", "CC-BINGA-01", "END-CC01-2026-002", "public", "confidential", "AUD-RES-022", "VAL-001", "LIA-BN-01"),
    ("Mufufa", "sn", "Securidaca longipedunculata", "Midzi inoshandiswa pamusoro nechipfuva", "Root bark used for severe headache and chest pain", "CA23", "Hupfu hwemidzi hunoiswa mumvura", "decoction", "root", "oral", "both", "Midlands", "Gokwe", "W15", "HLD-MW-033", "CC-GOKWE-02", "END-CC02-2026-009", "community-restricted", "confidential", "AUD-RES-023", "VAL-004", "LIA-MW-02"),
    ("Umuvuma", "nd", "Securidaca longipedunculata", "Amaxolo ezimpande asetshiswa emzimbeni obuhlungu", "Root bark used for body aches and joint inflammation", "FA20", "Izimpande ziyasikwa ziphekwe", "decoction", "root", "oral", "both", "Matabeleland North", "Hwange", "W08", "HLD-MW-077", "CC-HWANGE-06", "END-CC06-2026-003", "community-restricted", "confidential", "AUD-RES-024", "VAL-001", "LIA-MW-03"),
    ("Zumbani", "sn", "Lippia javanica", "Mashizha anobikwa tii yechikosoro nefiva", "Leaves brewed as tea for cough, flu, and fever", "CA23", "Mashizha anobikwa semurimo", "infusion", "leaf", "oral", "both", "Manicaland", "Nyanga", "W04", "HLD-EH-033", "CC-NYANGA-05", "END-CC05-2026-002", "public", "confidential", "AUD-RES-025", "VAL-002", "LIA-EH-02"),
    ("Inzinziniba", "nd", "Lippia javanica", "Amakhasi ayaphekwa asetshenziselwe umkhuhlane", "Leaves boiled as tea for respiratory infection", "CA23", "Amakhasi ayaphuzwa esiphuselweni", "infusion", "leaf", "oral", "both", "Matabeleland South", "Matobo", "W06", "HLD-MS-024", "CC-MATOBO-04", "END-CC04-2026-001", "public", "confidential", "AUD-RES-026", "VAL-003", "LIA-MS-01"),
    ("Mufandichimuka", "sn", "Myrothamnus flabellifolius", "Mashizha anobikwa pazvirwere zvhitsvo nechikosoro", "Leaves used for kidney complaints and chest colds", "GB60", "Mashizha akaoma anobikwa mumvura", "infusion", "leaf", "oral", "dry", "Manicaland", "Chimanimani", "W16", "HLD-EH-071", "CC-CHIMANIMANI-03", "END-CC03-2026-011", "public", "confidential", "AUD-RES-027", "VAL-001", "LIA-EH-01"),
    ("Mumveve", "sn", "Kigelia africana", "Muchero nemakwati zvinoitwa hupfu hwezvidonda zvenguvo", "Fruit powder applied topically for skin ulcers", "1B70", "Hupfu hunosanganiswa nemafuta", "topical_oil", "fruit", "topical", "both", "Masvingo", "Chiredzi", "W10", "HLD-LV-063", "CC-CHIREDZI-07", "END-CC07-2026-004", "public", "confidential", "AUD-RES-028", "VAL-005", "LIA-LV-02"),
    ("Mukute", "sn", "Syzygium cordatum", "Makwati anoshandiswa pamukono wedumbu", "Bark decoction used for severe diarrhea", "DD90", "Makwati anobikwa mumvura zhinji", "decoction", "bark", "oral", "wet", "Manicaland", "Nyanga", "W07", "HLD-EH-092", "CC-NYANGA-05", "END-CC05-2026-002", "public", "confidential", "AUD-RES-029", "VAL-002", "LIA-EH-02"),
    ("Umnyushwa", "nd", "Syzygium cordatum", "Amaxolo asetshenziswa lapho umhlane ubuhlungu", "Bark decoction used for abdominal cramps", "DD90", "Amaxolo ayaphekwa amanzini", "decoction", "bark", "oral", "wet", "Matabeleland North", "Binga", "W05", "HLD-BN-014", "CC-BINGA-01", "END-CC01-2026-002", "public", "confidential", "AUD-RES-030", "VAL-001", "LIA-BN-01"),
    ("Muchechete", "sn", "Mimusops zeyheri", "Midzi inoshandiswa pachirwere cheropa", "Roots used for internal ailments", "1F40", "Midzi inobikwa kwenguva ndefu", "decoction", "root", "oral", "both", "Midlands", "Gokwe", "W06", "HLD-MW-041", "CC-GOKWE-02", "END-CC02-2026-009", "public", "confidential", "AUD-RES-031", "VAL-004", "LIA-MW-01"),
    ("Umthunduluka", "nd", "Ximenia americana", "Izimpande zisetshenziswa emazinyweni", "Roots used for toothache and mouth sores", "1F40", "Izimpande ziyagxotshwa asetshenziswe emulonyeni", "decoction", "root", "oral", "both", "Matabeleland South", "Matobo", "W09", "HLD-MS-038", "CC-MATOBO-04", "END-CC04-2026-001", "community-restricted", "confidential", "AUD-RES-032", "VAL-003", "LIA-MS-01"),
    ("Mutshikili", "sn", "Trichilia emetica", "Makwati anoshandiswa pahosha yefiva nedumbu", "Bark used for fever and indigestion", "MG50", "Makwati anobikwa mumvura", "decoction", "bark", "oral", "both", "Masvingo", "Chiredzi", "W18", "HLD-LV-082", "CC-CHIREDZI-07", "END-CC07-2026-004", "public", "confidential", "AUD-RES-033", "VAL-005", "LIA-LV-03"),
    ("Mufundamengwe", "sn", "Croton gratissimus", "Makwati anoshandiswa pachikosoro nechipfuva", "Bark used for fever and chest complaints", "CA23", "Makwati anopiswa utsi huchinwiwa", "smoke_inhalation", "bark", "inhalation", "dry", "Manicaland", "Chimanimani", "W02", "HLD-EH-049", "CC-CHIMANIMANI-03", "END-CC03-2026-011", "community-restricted", "confidential", "AUD-RES-034", "VAL-001", "LIA-EH-01"),
    ("Umgonogono", "nd", "Lannea discolor", "Amaxolo asetshenziswa esiswini nesisindo", "Bark infusion used for convulsions and diarrhea", "DD90", "Amaxolo agxotshwa emanzini", "infusion", "bark", "oral", "both", "Matabeleland North", "Hwange", "W12", "HLD-MW-105", "CC-HWANGE-06", "END-CC06-2026-003", "public", "confidential", "AUD-RES-035", "VAL-001", "LIA-MW-03"),
    ("Muchecheni", "sn", "Ziziphus mucronata", "Mashizha anotsengwa anoiswa pamota", "Leaf poultice applied to boils and infections", "1B70", "Mashizha anokuyiwa anoiswa pamota", "poultice", "leaf", "topical", "both", "Midlands", "Gokwe", "W19", "HLD-MW-062", "CC-GOKWE-02", "END-CC02-2026-009", "public", "confidential", "AUD-RES-036", "VAL-004", "LIA-MW-02"),
    ("Umtshekesane", "nd", "Euclea divinorum", "Izimpande zisetshenziselwa inhlungu zekhanda", "Roots used for severe headache and toothache", "1F40", "Izimpande ziyaphekwa emanzini", "decoction", "root", "oral", "dry", "Matabeleland South", "Matobo", "W11", "HLD-MS-051", "CC-MATOBO-04", "END-CC04-2026-001", "community-restricted", "confidential", "AUD-RES-037", "VAL-003", "LIA-MS-01"),
    ("Munhundu", "sn", "Flacourtia indica", "Midzi inoshandiswa pachirwere chejaundice", "Roots used for jaundice and liver ailments", "DB93", "Midzi inobikwa zvikuru", "decoction", "root", "oral", "wet", "Manicaland", "Nyanga", "W12", "HLD-EH-104", "CC-NYANGA-05", "END-CC05-2026-002", "public", "confidential", "AUD-RES-038", "VAL-002", "LIA-EH-02"),
    ("Munzviru", "sn", "Vangueria infausta", "Midzi inoshandiswa pamakonye emudumbu", "Root decoction used for intestinal worms", "1F40", "Midzi inobikwa nenyama", "decoction", "root", "oral", "both", "Masvingo", "Chiredzi", "W04", "HLD-LV-091", "CC-CHIREDZI-07", "END-CC07-2026-004", "public", "confidential", "AUD-RES-039", "VAL-005", "LIA-LV-01"),
    ("Muvazvi", "sn", "Hoslundia opposita", "Mashizha anoshandiswa pakurwadziwa kwechipfuva", "Leaves used for chest pains and herpes infection", "CA23", "Mashizha anobikwa anomwiwa", "decoction", "leaf", "oral", "both", "Midlands", "Gokwe", "W22", "HLD-MW-079", "CC-GOKWE-02", "END-CC02-2026-009", "public", "confidential", "AUD-RES-040", "VAL-004", "LIA-MW-02"),
    ("Mupambangoma", "sn", "Vernonia amygdalina", "Mashizha inovava inoshandiswa pazvirwere zvedumbu", "Bitter leaves used for malaria fever and stomach ailments", "1F40", "Mashizha anokuyiwa emanzini", "infusion", "leaf", "oral", "both", "Manicaland", "Chimanimani", "W18", "HLD-EH-115", "CC-CHIMANIMANI-03", "END-CC03-2026-011", "public", "confidential", "AUD-RES-041", "VAL-001", "LIA-EH-01"),
    ("Umgonondo", "nd", "Terminalia phanerophlebia", "Amaxolo asetshenziselwa umkhuhlane nesisu", "Bark used for dysentery and fever", "DD90", "Amaxolo aphekwa phansi", "decoction", "bark", "oral", "both", "Matabeleland North", "Binga", "W09", "HLD-BN-027", "CC-BINGA-01", "END-CC01-2026-002", "public", "confidential", "AUD-RES-042", "VAL-001", "LIA-BN-01"),
    ("Mutowa", "sn", "Diplorhynchus condylocarpon", "Makwati anoshandiswa pazvirwere zvomudumbu", "Bark used for gastrointestinal disorders", "DD90", "Makwati anobikwa mumvura", "decoction", "bark", "oral", "dry", "Masvingo", "Chiredzi", "W19", "HLD-LV-102", "CC-CHIREDZI-07", "END-CC07-2026-004", "public", "confidential", "AUD-RES-043", "VAL-003", "LIA-LV-02"),
    ("Mugaranhjanja", "sn", "Gymnosporia senegalensis", "Midzi inoshandiswa pamapundu nemazino", "Roots used for chest pains and skin boils", "CA23", "Midzi inobikwa nemvura", "decoction", "root", "oral", "both", "Midlands", "Gokwe", "W14", "HLD-MW-088", "CC-GOKWE-02", "END-CC02-2026-009", "public", "confidential", "AUD-RES-044", "VAL-004", "LIA-MW-01"),
    ("Umthathi", "nd", "Ptaeroxylon obliquum", "Amaxolo ayaphekwa asetshenziswe ekhanda", "Bark decoction used for severe migraine", "1F40", "Amaxolo agxotshwa abikwe", "decoction", "bark", "oral", "dry", "Matabeleland South", "Matobo", "W15", "HLD-MS-067", "CC-MATOBO-04", "END-CC04-2026-001", "community-restricted", "confidential", "AUD-RES-045", "VAL-003", "LIA-MS-01"),
    ("Mupiningura", "sn", "Euclea natalensis", "Midzi inoshandiswa pahosha dzomudumbu", "Roots used for toothache and abdominal pain", "DD90", "Midzi inotsengwa mumuromo", "chewed_raw", "root", "oral", "both", "Manicaland", "Nyanga", "W15", "HLD-EH-122", "CC-NYANGA-05", "END-CC05-2026-002", "public", "confidential", "AUD-RES-046", "VAL-002", "LIA-EH-02"),
    ("Umsimbithi", "nd", "Milletia grandis", "Amaxolo asetshenziselwa inhlungu emzimbeni", "Bark used for muscular pain and rheumatism", "FA20", "Amaxolo agxotshwa emanzini", "infusion", "bark", "oral", "both", "Matabeleland North", "Hwange", "W15", "HLD-MW-118", "CC-HWANGE-06", "END-CC06-2026-003", "public", "confidential", "AUD-RES-047", "VAL-001", "LIA-MW-03"),
    ("Mundari", "sn", "Gardenia volkensii", "Midzi neshizha zvinoshandiswa pahosha dzefiva", "Roots and leaves used for fever and headache", "MG50", "Midzi inobikwa pamwe nemashizha", "decoction", "root", "oral", "wet", "Masvingo", "Chiredzi", "W22", "HLD-LV-114", "CC-CHIREDZI-07", "END-CC07-2026-004", "public", "confidential", "AUD-RES-048", "VAL-005", "LIA-LV-03"),
    ("Umsungunu", "nd", "Searsia pyroides", "Amakhasi asetshenziswa panxeba", "Leaves applied to skin wounds and burns", "1B70", "Amakhasi agxotshwa afakwe enxebeni", "poultice", "leaf", "topical", "both", "Matabeleland South", "Matobo", "W18", "HLD-MS-082", "CC-MATOBO-04", "END-CC04-2026-001", "public", "confidential", "AUD-RES-049", "VAL-003", "LIA-MS-01"),
    ("Mukombigo", "sn", "Crossopteryx febrifuga", "Makwati anoshandiswa pafiva nedumbu", "Bark used for malarial fever and dysentery", "MG50", "Makwati anobikwa zvakasimba", "decoction", "bark", "oral", "dry", "Manicaland", "Chimanimani", "W20", "HLD-EH-135", "CC-CHIMANIMANI-03", "END-CC03-2026-011", "public", "confidential", "AUD-RES-050", "VAL-001", "LIA-EH-01")
]

heritage_records = []
consent_records = []

for idx, p in enumerate(heritage_plants, 1):
    tk_id = f"ZW-TK-2026-{idx:03d}"
    consent_ref = f"FPIC-ZW-2026-C{idx:03d}"
    bsa_ref = f"BSA-ZW-2026-{idx:03d}"
    source_id = "ZW-SRC-004"
    
    c_day = 10 + (idx % 15)
    month = 9 if idx <= 15 else (10 if idx <= 32 else (11 if idx <= 42 else 12))
    c_date = f"2026-{month:02d}-{c_day:02d}"
    i_date = f"2026-{month:02d}-{(c_day+1):02d}"
    created_at = f"2026-{month:02d}-{(c_day+2):02d}T09:30:00+02:00"
    
    is_withdrawn = (tk_id == "ZW-TK-2026-006")
    w_status = "withdrawn" if is_withdrawn else "active"
    w_date = "2026-12-08" if is_withdrawn else ""
    rec_status = "redacted" if is_withdrawn else "active"
    
    local_name, lang, sci_name, dis_loc, dis_en, icd11, prep_meth, prep_class, plant_part, admin_rt, season, prov, dist, ward, holder_id, council_id, end_ref, sens_lvl, data_sens, aud_ref, val_id, lia_id = p
    
    k_type = "ecological" if plant_part == "na" else "plant-disease"
    trans_stat = "human_verified" if dis_en else ""
    
    heritage_row = [
        tk_id, source_id, holder_id, council_id, end_ref, consent_ref, c_date, lang, i_date, f"INT-{(idx%5)+1:03d}",
        k_type, local_name, lang, sci_name, dis_loc, dis_en, trans_stat, icd11, prep_meth, prep_class, plant_part,
        admin_rt, season, prov, dist, ward, "0", sens_lvl, data_sens, bsa_ref, w_status, w_date, aud_ref, "passed", val_id, created_at, rec_status
    ]
    heritage_records.append(heritage_row)
    
    c_fmt = f"signed_paper_{'shona' if lang=='sn' else 'ndebele'}"
    consent_row = [
        consent_ref, tk_id, holder_id, council_id, end_ref, lang, c_fmt, c_date, "yes", "no", bsa_ref, w_status, w_date, lia_id
    ]
    consent_records.append(consent_row)

heritage_headers = ["tk_id","source_id","holder_pseudonym_id","community_council_id","council_endorsement_ref","consent_reference","consent_date","collection_language","interview_date","interviewer_id","knowledge_type","local_plant_name","language_tag","scientific_name","disease_target_local","disease_target_en","translation_status","disease_target_icd11","preparation_method","preparation_class","plant_part_used","administration_route","seasonality_of_use","province","district","ward","named_attribution_opt_in","sensitivity_level","data_sensitivity","benefit_sharing_agreement_ref","withdrawal_status","withdrawal_date","audio_recording_ref","bilingual_validation_status","validator_id","created_at","record_status"]

with open(os.path.join(processed_dir, "heritage_knowledge_v1.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(heritage_headers)
    writer.writerows(heritage_records)

consent_headers = ["consent_reference","tk_id","holder_pseudonym_id","community_council_id","council_endorsement_ref","consent_language","consent_format","consent_date","audio_consent_granted","named_attribution_opt_in","benefit_sharing_agreement_ref","withdrawal_status","withdrawal_date","witnessed_by"]

with open(os.path.join(governance_dir, "consent_log.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(consent_headers)
    writer.writerows(consent_records)

# ---------------------------------------------------------
# 2. ENVIRONMENTAL SAMPLES (120 records)
# ---------------------------------------------------------

env_records = []

for i in range(1, 121):
    smp_id = f"ZW-SMP-2026-{i:03d}"
    
    if i <= 45:
        ecozone = "Eastern Highlands"
        prov = "Manicaland"
        dist = "Chimanimani" if i % 2 == 0 else "Nyanga"
        ward = "W12" if dist == "Chimanimani" else "W04"
        src_id = "ZW-SRC-001"
        lat = -19.80 + (i * 0.005)
        lon = 32.86 + (i * 0.003)
        loc_desc = ""
        col_date = f"2026-09-{(i%25)+1:02d}"
    elif i <= 80:
        ecozone = "Mazowe"
        prov = "Masvingo"
        dist = "Chiredzi"
        ward = "W08"
        src_id = "ZW-SRC-002"
        lat = -21.05 - (i * 0.004)
        lon = 31.67 + (i * 0.004)
        loc_desc = ""
        col_date = f"2026-10-{(i%25)+1:02d}"
    elif i <= 105:
        ecozone = "Zvishavane"
        prov = "Midlands"
        dist = "Gokwe"
        ward = "W04"
        src_id = "ZW-SRC-003"
        lat = -18.22 + (i * 0.003)
        lon = 28.93 - (i * 0.002)
        loc_desc = ""
        col_date = f"2026-11-{(i%25)+1:02d}"
    else:
        ecozone = "Other"
        prov = "Matabeleland South" if i % 2 == 0 else "Matabeleland North"
        dist = "Matobo" if i % 2 == 0 else "Binga"
        ward = "W06" if dist == "Matobo" else "W02"
        src_id = "ZW-SRC-007"
        lat = -20.55 if dist == "Matobo" else -17.62
        lon = 28.52 if dist == "Matobo" else 27.34
        loc_desc = f"Holder-directed bushland site in {dist} communal ward {ward}"
        col_date = f"2026-10-{(i%25)+1:02d}"

    is_soil = (i % 3 == 0)
    s_type = "soil" if is_soil else ("bark" if i%3==1 else "plant_tissue")
    depth = "10" if is_soil else ""
    
    tk_idx = ((i - 1) % 50) + 1
    tk_id = f"ZW-TK-2026-{tk_idx:03d}"
    consent_ref = f"FPIC-ZW-2026-C{tk_idx:03d}"
    
    is_withdrawn_link = (tk_id == "ZW-TK-2026-006")
    rec_status = "redacted" if is_withdrawn_link else "active"
    
    h_plant = heritage_plants[tk_idx-1]
    loc_name = "" if is_soil else h_plant[0]
    loc_lang = "" if is_soil else h_plant[1]
    sci_name = "" if is_soil else h_plant[2]
    tax_conf = "" if is_soil else "herbarium_confirmed"
    vouch_ref = "" if is_soil else f"HERB-ZW-2026-{i:04d}"
    
    season = "dry" if i % 2 == 1 else "wet"
    created_at = f"{col_date}T14:00:00+02:00"
    
    env_row = [
        smp_id, f"CE-2026-{i:03d}", src_id, ecozone, prov, dist, ward, loc_desc, "communal",
        round(lat, 2), round(lon, 2), "5000", "1", 1200 + (i*5), s_type, depth,
        loc_name, loc_lang, sci_name, tax_conf, vouch_ref, col_date, season,
        "6.2", "24.5", "15.0", "50", "COL-003", "silica_gel" if not is_soil else "flash_frozen",
        "25", "MOBILE-LEC-01", f"COC-2026-{i:04d}", tk_id, consent_ref, "NBA-ZW-2026-014", "",
        "complete", "complete", "public", created_at, rec_status
    ]
    env_records.append(env_row)

env_headers = ["sample_id","collection_event_id","source_id","ecozone","province","district","ward","locality_description","land_tenure","gps_latitude","gps_longitude","gps_precision_m","location_masked","altitude_m","sample_type","collection_depth_cm","local_name","local_name_language","scientific_name","taxon_confidence","voucher_specimen_ref","collection_date","season","soil_ph","temperature_celsius","rainfall_prior_30d_mm","canopy_cover_pct","collector_id","preservation_method","minutes_to_preservation","processing_lab","chain_of_custody_ref","heritage_use_ref","consent_reference","nba_permit_ref","access_permit_ref","sequencing_status","lc_ms_status","data_sensitivity","created_at","record_status"]

with open(os.path.join(processed_dir, "environmental_samples_v1.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(env_headers)
    writer.writerows(env_records)

# ---------------------------------------------------------
# 3. GENOMIC SEQUENCES (55 records)
# ---------------------------------------------------------

genomic_records = []
target_regions = ['16s_rrna', 'its', 'rbcl', 'matk', 'shotgun_metagenome']

for i in range(1, 56):
    seq_id = f"ZW-SEQ-2026-{i:03d}"
    smp_idx = ((i - 1) % 120) + 1
    smp_id = f"ZW-SMP-2026-{smp_idx:03d}"
    
    parent_env = env_records[smp_idx - 1]
    h_link = parent_env[32] # heritage_use_ref
    
    platform = "ont_minion" if i % 2 == 1 else "illumina_miseq"
    target = target_regions[i % len(target_regions)]
    q_score = 14.5 if platform == "ont_minion" else 32.4
    bgc = 4 + (i % 15)
    nov = "divergent" if i % 3 == 0 else ("putative_novel" if i % 3 == 1 else "known")
    
    checksum = sha256_text(f"genomic_file_{seq_id}")
    fasta_path = f"raw/zw_src_001_eastern_highlands/{seq_id}.fasta"
    
    seq_row = [
        seq_id, smp_id, platform, "SQK-RBK114-24", f"FAX{12300+i}", "dna_r10.4.1_e8.2_400bps_sup",
        "2026-10-15", "MOBILE-LEC-01", target, "150000", "220000000", "1450", "1600",
        q_score, "flye", "45000", "300", "Streptomyces sp." if target=="16s_rrna" else "Fungal endophyte",
        "kraken2/GTDB-r214", nov, "NR_112345.1", "96.5", "polyketide synthase (predicted)",
        "0.75", "0.92", bgc, h_link, fasta_path, checksum, "1850000000", "public", "pass", "2026-10-16T08:00:00+02:00"
    ]
    genomic_records.append(seq_row)

genomic_headers = ["sequence_id","sample_id","platform","library_prep_kit","flowcell_id","basecalling_model","run_date","sequencing_lab","target_region","read_count","total_bases","mean_read_length_bp","read_n50_bp","mean_q_score","assembly_method","assembly_n50_bp","contig_count","taxonomic_assignment","assignment_method","organism_novelty","best_blast_accession","best_blast_pct_identity","predicted_function","disease_target_relevance","annotation_confidence","bgc_count","heritage_link","file_path_fasta","file_checksum_sha256","file_size_bytes","data_sensitivity","qc_status","created_at"]

with open(os.path.join(processed_dir, "genomic_sequences_v1.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(genomic_headers)
    writer.writerows(genomic_records)

# ---------------------------------------------------------
# 4. METABOLOMIC PROFILES (90 records)
# Featuring compounds from:
#  - Ginger: Gingerol, Shogaol, Zerumbone, Siphonochilone
#  - Pepper-bark Tree: Warburganal, Polygodial, Ugandensidial
#  - Water Hyacinth & aquatic phytoremediation: Luteolin, Apigenin, Phytosterols
# ---------------------------------------------------------

compounds = [
    # Ginger Bioactives
    ("[6]-Gingerol (putative)", "C17H26O4", 294.1831, 2, "GNPS", 0.91, "CHEBI:28812", "anti-inflammatory", "known", 0.91),
    ("[6]-Shogaol (putative)", "C17H24O3", 276.1725, 2, "GNPS", 0.89, "CHEBI:35072", "anti-inflammatory", "known", 0.89),
    ("Zerumbone (putative)", "C15H22O", 218.1671, 2, "GNPS", 0.87, "CHEBI:67140", "anti-inflammatory", "known", 0.87),
    ("Siphonochilone (putative)", "C15H20O2", 232.1463, 2, "GNPS", 0.85, "CNP0876543", "antimicrobial", "putative_novel", 0.85),

    # Pepper-bark Tree Bioactives
    ("Warburganal (putative)", "C15H20O2", 235.1693, 2, "GNPS", 0.87, "CNP0123456", "antimicrobial", "known", 0.87),
    ("Polygodial (putative)", "C15H22O2", 234.1619, 2, "GNPS", 0.88, "CNP0234567", "antimicrobial", "known", 0.88),
    ("Ugandensidial (putative)", "C15H20O3", 248.1412, 2, "GNPS", 0.83, "CNP0456789", "antimicrobial", "known", 0.83),

    # Water Hyacinth Phytochemicals
    ("Luteolin", "C15H10O6", 286.0477, 1, "MassBank", 0.97, "CHEBI:15364", "anti-inflammatory", "known", 0.97),
    ("Apigenin", "C15H10O5", 270.0528, 1, "MassBank", 0.96, "CHEBI:18361", "anti-inflammatory", "known", 0.96),

    # Broader Phytochemicals
    ("Quercetin", "C15H10O7", 301.0354, 1, "MassBank", 0.96, "CHEBI:16243", "anti-inflammatory", "known", 0.96),
    ("Kaempferol", "C15H10O6", 285.0405, 1, "MassBank", 0.95, "CHEBI:28364", "anti-inflammatory", "known", 0.95),
    ("Securidacaside A (putative)", "C23H26O11", 478.1475, 2, "GNPS", 0.84, "CNP0987654", "anti-inflammatory", "putative_novel", 0.84),
    ("Maslinic acid", "C30H48O4", 472.3553, 1, "NIST", 0.94, "CHEBI:6690", "anti-inflammatory", "known", 0.94),
    ("Aloin A (putative)", "C21H22O9", 418.1264, 2, "GNPS", 0.89, "CHEBI:2743", "anti-inflammatory", "known", 0.89),
    ("Betulinic acid", "C30H48O3", 456.3603, 1, "NIST", 0.97, "CHEBI:28445", "antimicrobial", "known", 0.97),
    ("Lupeol", "C30H50O", 426.3861, 1, "NIST", 0.96, "CHEBI:6580", "anti-inflammatory", "known", 0.96),
    ("Oleanolic acid", "C30H48O3", 456.3603, 1, "MassBank", 0.95, "CHEBI:28682", "antimicrobial", "known", 0.95),
    ("Rutin", "C27H30O16", 610.1534, 1, "MassBank", 0.98, "CHEBI:28527", "anti-inflammatory", "known", 0.98),
    ("Gallic acid", "C7H6O5", 170.0215, 1, "MassBank", 0.99, "CHEBI:30778", "anti-inflammatory", "known", 0.99),
    ("Chlorogenic acid", "C16H18O9", 354.0951, 1, "MassBank", 0.97, "CHEBI:17521", "anti-inflammatory", "known", 0.97),
    ("Ellagic acid", "C14H6O8", 302.0063, 1, "MassBank", 0.96, "CHEBI:4816", "anti-inflammatory", "known", 0.96),
    ("Mangiferin", "C19H18O11", 422.0849, 1, "MassBank", 0.97, "CHEBI:6687", "anti-inflammatory", "known", 0.97),
    ("Shanzhiside methyl ester (putative)", "C17H26O11", 406.1475, 2, "GNPS", 0.82, "CNP0345678", "anti-inflammatory", "known", 0.82),
    ("Verbascoside (putative)", "C29H36O15", 624.2054, 2, "GNPS", 0.86, "CHEBI:6789", "anti-inflammatory", "known", 0.86),
    ("Unknown sesquiterpenoid dimer", "C27H36O6", 449.2278, 4, "GNPS", 0.31, "", "unknown", "putative_novel", 0.31),
    ("Unknown polyketide", "C34H51NO11", 658.3421, 4, "GNPS", 0.22, "", "unknown", "putative_novel", 0.22),
    ("Triterpenoid saponin (putative)", "C48H78O19", 958.5137, 3, "GNPS", 0.58, "", "antimicrobial", "putative_novel", 0.58),
    ("Anthraquinone glycoside (putative)", "C21H20O10", 432.1056, 3, "GNPS", 0.61, "", "anti-parasitic", "putative_novel", 0.61),
    ("Sesquiterpene lactone (putative)", "C15H18O4", 262.1205, 3, "GNPS", 0.64, "", "anti-parasitic", "putative_novel", 0.64),
    ("Unannotated feature", "C20H30O5", 350.2093, 4, "GNPS", 0.18, "", "unknown", "putative_novel", 0.18)
]

met_records = []
for i in range(1, 91):
    met_id = f"ZW-MET-2026-{i:03d}"
    smp_idx = ((i - 1) % 120) + 1
    smp_id = f"ZW-SMP-2026-{smp_idx:03d}"
    
    cp = compounds[(i - 1) % len(compounds)]
    c_name, c_formula, mz_m, msi_lvl, spec_lib, match_sc, db_hit, c_cls, c_nov, conf = cp
    
    checksum = sha256_text(f"metabolite_file_{met_id}")
    mzml_path = f"raw/zw_src_006_sirdc_lcms/EXT-{(smp_idx):04d}_pos.mzML"
    qc_stat = "warning" if msi_lvl in [3, 4] else "pass"
    
    met_row = [
        met_id, smp_id, f"EXT-{(smp_idx):04d}", "MeOH:H2O 80:20", "2026-10-18", "Agilent 6545 Q-TOF",
        "C18 2.1x100mm 1.8um", "positive", "20.0", round(4.5 + (i*0.1), 2), round(mz_m, 4), "1.8",
        "4820115", "0.142", c_name, c_formula, "", "", msi_lvl, spec_lib, match_sc, db_hit,
        c_cls, c_nov, conf, mzml_path, checksum, "confidential", qc_stat, "2026-10-19T12:00:00+02:00"
    ]
    met_records.append(met_row)

met_headers = ["metabolite_id","sample_id","extract_id","extraction_solvent","extraction_date","instrument","chromatography_column","ionization_mode","collision_energy_ev","retention_time_min","mz_measured","mz_error_ppm","peak_area","relative_abundance","putative_compound_name","molecular_formula","smiles_canonical","inchikey","msi_annotation_level","spectral_library","library_match_score","external_db_hit","compound_class","compound_novelty","annotation_confidence","file_path_mzml","file_checksum_sha256","data_sensitivity","qc_status","created_at"]

with open(os.path.join(processed_dir, "metabolomic_profiles_v1.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(met_headers)
    writer.writerows(met_records)

# ---------------------------------------------------------
# 5. LABELS (annotations_v1.jsonl)
# ---------------------------------------------------------

annotation_items = []
for g in genomic_records:
    seq_id = g[0]
    annotation_items.append({"record_id": seq_id, "table": "genomic_sequences", "label": "organism_novelty", "value": g[19], "assigned_by": "automated_blast+human_review", "guide_version": "v1.0.0", "assigned_at": g[32], "review_status": "reviewed", "reviewer_id": "REV-BIO-01", "disagreement": False})
    annotation_items.append({"record_id": seq_id, "table": "genomic_sequences", "label": "predicted_function", "value": g[22], "assigned_by": "model_inference", "guide_version": "v1.0.0", "assigned_at": g[32], "review_status": "single_pass", "reviewer_id": None, "disagreement": False})
    annotation_items.append({"record_id": seq_id, "table": "genomic_sequences", "label": "disease_target_relevance", "value": str(g[23]), "assigned_by": "model_inference", "guide_version": "v1.0.0", "assigned_at": g[32], "review_status": "single_pass", "reviewer_id": None, "disagreement": False})
    annotation_items.append({"record_id": seq_id, "table": "genomic_sequences", "label": "annotation_confidence", "value": str(g[24]), "assigned_by": "automated", "guide_version": "v1.0.0", "assigned_at": g[32], "review_status": "single_pass", "reviewer_id": None, "disagreement": False})

for m in met_records:
    met_id = m[0]
    annotation_items.append({"record_id": met_id, "table": "metabolomic_profiles", "label": "compound_class", "value": m[22], "assigned_by": "spectral_match", "guide_version": "v1.0.0", "assigned_at": m[29], "review_status": "single_pass", "reviewer_id": None, "disagreement": False})
    annotation_items.append({"record_id": met_id, "table": "metabolomic_profiles", "label": "compound_novelty", "value": m[23], "assigned_by": "spectral_match", "guide_version": "v1.0.0", "assigned_at": m[29], "review_status": "single_pass", "reviewer_id": None, "disagreement": False})

with open(os.path.join(labels_dir, "annotations_v1.jsonl"), "w", encoding="utf-8") as f:
    for item in annotation_items:
        f.write(json.dumps(item) + "\n")

print("Generated expanded datasets with the 3 Focal Pillars!")
