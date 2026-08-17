"""Static reference data: external resources & scientific journals.

These lists mirror the constants from the original React app. They aren't
user-editable content, so they live here as plain Python data rather than
database models (unlike Researchers / Publications / News, which are real
Django models backed by SQLite).
"""

from .models import Category

# Real logo images sourced from Wikimedia Commons (stable, hotlink-friendly
# URLs via Special:FilePath — used by many external sites for exactly this
# purpose). Only filled in where a confirmed, clearly-identifiable official
# logo file was found; everything else in RESOURCES/JOURNALS below falls
# back to the built-in colored category icon in the templates.
WIKIMEDIA_COMMONS = "https://commons.wikimedia.org/wiki/Special:FilePath/{}"
WIKIMEDIA_DE = "https://de.wikipedia.org/wiki/Special:FilePath/{}"

RESOURCES = [
    {"name": "FEMA – Federal Emergency Management Agency", "url": "https://www.fema.gov",
     "desc": "US federal agency for disaster response, recovery, and preparedness planning.",
     "cat": Category.DISASTER_MEDICINE, "img": "photo-1573164574511-73c773193279",
     "logo_url": WIKIMEDIA_COMMONS.format("FEMA_logo.svg")},
    {"name": "European Civil Protection & Humanitarian Aid (ECHO)", "url": "https://civil-protection-humanitarian-aid.ec.europa.eu",
     "desc": "EU mechanism for civil protection and international humanitarian assistance.",
     "cat": Category.DISASTER_MEDICINE, "img": "photo-1560520653-9e0e4c89eb11",
     "logo_url": WIKIMEDIA_COMMONS.format("CivilDefence.svg")},
    {"name": "ICDO – International Civil Defence Organisation", "url": "https://www.icdo.org",
     "desc": "Intergovernmental body promoting civil protection best practices worldwide.",
     "cat": Category.FIRE_SAFETY, "img": "photo-1621905251918-48416bd8575a"},
    {"name": "OPCW – Organisation for the Prohibition of Chemical Weapons", "url": "https://www.opcw.org",
     "desc": "International body implementing the Chemical Weapons Convention globally.",
     "cat": Category.CBRN, "img": "photo-1582719508461-905c673771fd",
     "logo_url": WIKIMEDIA_DE.format("OPCW-Logo.svg")},
    {"name": "IAEA – International Atomic Energy Agency", "url": "https://www.iaea.org",
     "desc": "UN body for peaceful nuclear applications, radiation safety, and emergency response.",
     "cat": Category.CBRN, "img": "photo-1628348070889-cb656235b4eb",
     "logo_url": WIKIMEDIA_COMMONS.format("International_Atomic_Energy_Agency_Logo.svg")},
    {"name": "UNDRR – UN Office for Disaster Risk Reduction", "url": "https://www.undrr.org",
     "desc": "UN body coordinating global disaster risk reduction and the Sendai Framework.",
     "cat": Category.DISASTER_MEDICINE, "img": "photo-1527515637462-cff94aca3584"},
    {"name": "CTIF – International Association of Fire and Rescue Services", "url": "https://www.ctif.org",
     "desc": "Global network of fire brigades promoting international cooperation and standards.",
     "cat": Category.FIRE_SAFETY, "img": "photo-1504711434969-e33886168f5c"},
    {"name": "WADEM – World Association for Disaster and Emergency Medicine", "url": "https://wadem.org",
     "desc": "International professional society advancing disaster and emergency medicine.",
     "cat": Category.DISASTER_MEDICINE, "img": "photo-1551601651-2a8555f1a136"},
    {"name": "NATO JCBRN Defence Centre of Excellence", "url": "https://www.jcbrn-coe.nato.int",
     "desc": "NATO's primary CBRN defence doctrine, training, and research body.",
     "cat": Category.CBRN, "img": "photo-1554734867-bf3c00a49371"},
    {"name": "UNEP – Environment & Emergency Response", "url": "https://www.unep.org",
     "desc": "Rapid environmental assessment and response in humanitarian emergencies.",
     "cat": Category.ENVIRONMENTAL_SAFETY, "img": "photo-1441974231531-c6227db76b6e",
     "logo_url": WIKIMEDIA_COMMONS.format("United_Nations_Environment_Programme_Logo.svg")},
    {"name": "CTBTO – Comprehensive Nuclear-Test-Ban Treaty Organization", "url": "https://www.ctbto.org",
     "desc": "International monitoring of nuclear tests and radiological incident detection.",
     "cat": Category.CBRN, "img": "photo-1564564321837-a57b7070ac4f"},
    {"name": "ITOPF – International Tanker Owners Pollution Federation", "url": "https://www.itopf.org",
     "desc": "Technical support for marine oil spill response and environmental protection.",
     "cat": Category.ENVIRONMENTAL_SAFETY, "img": "photo-1473341304170-971dccb5ac1e"},
]

# Real publisher logos (also from Wikimedia Commons). A single journal
# "cover" isn't a stable thing (it changes every issue), so we use each
# publisher's official logo instead — the same approach most journal
# directory sites use. Add more publishers here as you find good logos;
# JOURNALS entries whose "pub" isn't listed here just keep the category icon.
PUBLISHER_LOGOS = {
    "Elsevier": WIKIMEDIA_COMMONS.format("Elsevier_wordmark.svg"),
}

JOURNALS = [
    {"title": "Fire Safety Journal", "pub": "Elsevier", "url": "https://www.sciencedirect.com/journal/fire-safety-journal",
     "cat": Category.FIRE_SAFETY, "if_": "3.4",
     "desc": "Leading peer-reviewed journal on fire safety science and engineering across all environments."},
    {"title": "Journal of Hazardous Materials", "pub": "Elsevier", "url": "https://www.sciencedirect.com/journal/journal-of-hazardous-materials",
     "cat": Category.CBRN, "if_": "13.6",
     "desc": "Research on hazardous material identification, risk assessment, and emergency response."},
    {"title": "Disaster Medicine and Public Health Preparedness", "pub": "Cambridge University Press",
     "url": "https://www.cambridge.org/core/journals/disaster-medicine-and-public-health-preparedness",
     "cat": Category.DISASTER_MEDICINE, "if_": "2.1",
     "desc": "Scientific investigations into disaster preparedness, response, and healthcare resilience."},
    {"title": "Environmental Science & Technology", "pub": "American Chemical Society", "url": "https://pubs.acs.org/journal/esthag",
     "cat": Category.ENVIRONMENTAL_SAFETY, "if_": "10.8",
     "desc": "High-impact research on environmental chemistry, toxicology, and remediation."},
    {"title": "International Journal of Disaster Risk Reduction", "pub": "Elsevier",
     "url": "https://www.sciencedirect.com/journal/international-journal-of-disaster-risk-reduction",
     "cat": Category.DISASTER_MEDICINE, "if_": "4.2",
     "desc": "Cross-disciplinary research on disaster risk across all natural and technological hazards."},
    {"title": "Journal of Conventional Weapons Destruction", "pub": "JMU Scholarly Commons",
     "url": "https://commons.lib.jmu.edu/cisr-journal", "cat": Category.EOD, "if_": "—",
     "desc": "Field reports and research on unexploded ordnance, mine action, and EOD techniques."},
    {"title": "Prehospital Emergency Care", "pub": "Taylor & Francis", "url": "https://www.tandfonline.com/journals/ipec20",
     "cat": Category.DISASTER_MEDICINE, "if_": "2.8",
     "desc": "Emergency medical services, trauma care, and disaster medicine research and protocols."},
    {"title": "Environmental Hazards", "pub": "Taylor & Francis", "url": "https://www.tandfonline.com/journals/tenh20",
     "cat": Category.ENVIRONMENTAL_SAFETY, "if_": "3.1",
     "desc": "Multidisciplinary research on environmental and socio-economic risk assessment."},
    {"title": "Fire Technology", "pub": "Springer", "url": "https://link.springer.com/journal/10694",
     "cat": Category.FIRE_SAFETY, "if_": "3.0",
     "desc": "Fire science, suppression systems, and structural fire engineering research."},
    {"title": "Chemosphere", "pub": "Elsevier", "url": "https://www.sciencedirect.com/journal/chemosphere",
     "cat": Category.ENVIRONMENTAL_SAFETY, "if_": "8.8",
     "desc": "Environmental chemistry and toxicology including emergency pollution incidents."},
    {"title": "Journal of Emergency Management", "pub": "Weston Medical Publishing", "url": "https://www.pnpco.com/pn06000.html",
     "cat": Category.DISASTER_MEDICINE, "if_": "1.2",
     "desc": "Practical research for emergency management practitioners and policymakers."},
    {"title": "Radiation Protection Dosimetry", "pub": "Oxford University Press", "url": "https://academic.oup.com/rpd",
     "cat": Category.CBRN, "if_": "1.6",
     "desc": "Radiation protection, dosimetry, and radiological emergency response research."},
]

for _journal in JOURNALS:
    _journal["logo_url"] = PUBLISHER_LOGOS.get(_journal["pub"], "")
