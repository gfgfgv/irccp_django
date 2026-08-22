"""One-time seed data for Resources & Journals.

IMPORTANT: this file is NOT used directly by the site anymore. Resources and
Journals are now real database models (core.models.Resource / Journal),
editable from /admin/. This file only exists as the source data for the
one-time `python manage.py seed_resources_journals` import command — after
that command has run once, editing this file has no effect on the live site.
To change content going forward, use /admin/.
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
     "cat": Category.DISASTER_MEDICINE, "img": "photo-1527515637462-cff94aca3584",
     "logo_url": WIKIMEDIA_COMMONS.format("United_Nations_Office_for_Disaster_Risk_Reduction_Logo.svg")},
    {"name": "CTIF – International Association of Fire and Rescue Services", "url": "https://www.ctif.org",
     "desc": "Global network of fire brigades promoting international cooperation and standards.",
     "cat": Category.FIRE_SAFETY, "img": "photo-1504711434969-e33886168f5c",
     "logo_url": WIKIMEDIA_COMMONS.format("CTIF_logo.jpg")},
    {"name": "WADEM – World Association for Disaster and Emergency Medicine", "url": "https://wadem.org",
     "desc": "International professional society advancing disaster and emergency medicine.",
     "cat": Category.DISASTER_MEDICINE, "img": "photo-1551601651-2a8555f1a136"},
    {"name": "NATO JCBRN Defence Centre of Excellence", "url": "https://www.jcbrn-coe.nato.int",
     "desc": "NATO's primary CBRN defence doctrine, training, and research body.",
     "cat": Category.CBRN, "img": "photo-1554734867-bf3c00a49371",
     "logo_url": WIKIMEDIA_COMMONS.format("NATO_OTAN_landscape_logo.svg")},
    {"name": "UNEP – Environment & Emergency Response", "url": "https://www.unep.org",
     "desc": "Rapid environmental assessment and response in humanitarian emergencies.",
     "cat": Category.ENVIRONMENTAL_SAFETY, "img": "photo-1441974231531-c6227db76b6e",
     "logo_url": WIKIMEDIA_COMMONS.format("United_Nations_Environment_Programme_Logo.svg")},
    {"name": "CTBTO – Comprehensive Nuclear-Test-Ban Treaty Organization", "url": "https://www.ctbto.org",
     "desc": "International monitoring of nuclear tests and radiological incident detection.",
     "cat": Category.CBRN, "img": "photo-1564564321837-a57b7070ac4f",
     "logo_url": WIKIMEDIA_COMMONS.format("Preparatory_Commission_for_the_Comprehensive_Nuclear-Test-Ban_Treaty_Organization_Logo.svg")},
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
    "Springer": WIKIMEDIA_COMMONS.format("Springer_Nature_Logo.svg"),
    "Taylor & Francis": WIKIMEDIA_COMMONS.format("Taylor_%26_Francis_Group_logo.svg"),
    "American Chemical Society": WIKIMEDIA_COMMONS.format("American_Chemical_Society_logo.svg"),
    "Cambridge University Press": WIKIMEDIA_COMMONS.format("Cambridge_University_Press_logo.svg"),
    "Oxford University Press": WIKIMEDIA_COMMONS.format("OUP_logo.svg"),
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

# ---------------------------------------------------------------------------
# Seed data for Products (Company) and Events (Event) — same pattern as
# RESOURCES/JOURNALS above. Used once by `python manage.py
# seed_products_events`; after that, edit via /admin/.
#
# Companies: only large, well-known manufacturers with a confirmed logo file
# on Wikimedia Commons (verified via Special:FilePath before adding).
# Events: only real, currently-upcoming conferences/exhibitions (dates
# verified via the organiser's own site at the time this list was written).
# ---------------------------------------------------------------------------

PRODUCTS = [
    # Fire Safety
    {"name": "MSA Safety", "url": "https://us.msasafety.com",
     "desc": "Manufactures self-contained breathing apparatus, firefighter helmets, "
             "protective apparel, and fixed gas and flame detection systems for fire services worldwide.",
     "cat": Category.FIRE_SAFETY, "logo_url": WIKIMEDIA_COMMONS.format("MSA_Safety_Logo.svg")},
    {"name": "Dräger", "url": "https://www.draeger.com",
     "desc": "German manufacturer of breathing apparatus, gas detection instruments, and "
             "fire and rescue equipment used by fire departments and industry worldwide.",
     "cat": Category.FIRE_SAFETY, "logo_url": WIKIMEDIA_COMMONS.format("Dräger_Logo.svg")},
    {"name": "Rosenbauer", "url": "https://www.rosenbauer.com",
     "desc": "Austrian manufacturer of firefighting vehicles, pumps, and rescue equipment "
             "for municipal, industrial, and airport fire brigades.",
     "cat": Category.FIRE_SAFETY, "logo_url": WIKIMEDIA_COMMONS.format("Rosenbauer_Logo.svg")},
    # CBRN
    {"name": "Bruker", "url": "https://www.bruker.com",
     "desc": "Makes portable and laboratory chemical, biological, and radiological detection "
             "instruments used by CBRN response and forensic teams.",
     "cat": Category.CBRN, "logo_url": WIKIMEDIA_COMMONS.format("Bruker_logo.svg")},
    {"name": "Smiths Detection", "url": "https://www.smithsdetection.com",
     "desc": "Develops threat-detection and screening technology for chemical, biological, "
             "radiological, and explosive threats at borders, airports, and military sites.",
     "cat": Category.CBRN, "logo_url": WIKIMEDIA_COMMONS.format("Smiths_Group_logo.svg")},
    {"name": "Thermo Fisher Scientific", "url": "https://www.thermofisher.com",
     "desc": "Supplies handheld and lab-based radiation, chemical, and biological identification "
             "instruments used by CBRN and hazmat responders.",
     "cat": Category.CBRN, "logo_url": WIKIMEDIA_COMMONS.format("Thermo_Fisher_Scientific_logo.svg")},
    # EOD
    {"name": "Northrop Grumman", "url": "https://www.northropgrumman.com",
     "desc": "Produces the Andros line of remotely operated EOD/IED robots used by military "
             "and civilian bomb disposal units worldwide.",
     "cat": Category.EOD, "logo_url": WIKIMEDIA_COMMONS.format("Northrop_Grumman_logo_blue-on-clear_2020.svg")},
    {"name": "QinetiQ", "url": "https://www.qinetiq.com",
     "desc": "British defence technology company developing robotic and remote-controlled "
             "systems for explosive ordnance disposal and counter-IED operations.",
     "cat": Category.EOD, "logo_url": WIKIMEDIA_COMMONS.format("QinetiQ-Logo.svg")},
    # Disaster Medicine
    {"name": "Stryker", "url": "https://www.stryker.com",
     "desc": "Manufactures patient-handling equipment, emergency medical devices, and "
             "mass-casualty response gear used by EMS and hospitals worldwide.",
     "cat": Category.DISASTER_MEDICINE, "logo_url": WIKIMEDIA_COMMONS.format("Stryker_Corporation_logo.svg")},
    {"name": "Laerdal Medical", "url": "https://laerdal.com",
     "desc": "Norwegian manufacturer of resuscitation training manikins, CPR training aids, "
             "and emergency medical training equipment used to prepare disaster-response teams.",
     "cat": Category.DISASTER_MEDICINE},
    # Environmental Safety
    {"name": "3M", "url": "https://www.3m.com",
     "desc": "Supplies personal protective equipment, respirators, and environmental spill "
             "containment and cleanup products.",
     "cat": Category.ENVIRONMENTAL_SAFETY, "logo_url": WIKIMEDIA_COMMONS.format("3M_wordmark.svg")},
    {"name": "Honeywell", "url": "https://www.honeywell.com",
     "desc": "Provides gas detection, industrial safety, and environmental monitoring "
             "equipment for hazardous-site and spill-response operations.",
     "cat": Category.ENVIRONMENTAL_SAFETY, "logo_url": WIKIMEDIA_COMMONS.format("Honeywell_logo.svg")},
    {"name": "Veolia", "url": "https://www.veolia.com",
     "desc": "Global environmental services company specializing in hazardous waste "
             "management, industrial decontamination, and spill remediation.",
     "cat": Category.ENVIRONMENTAL_SAFETY, "logo_url": WIKIMEDIA_COMMONS.format("Veolia_logo.svg")},
]

EVENTS = [
    # Fire Safety
    {"title": "The Emergency Services Show 2026", "date": "2026-09-16", "end_date": "2026-09-17",
     "location": "NEC, Birmingham, UK", "cat": Category.FIRE_SAFETY,
     "desc": "Europe's leading annual trade show for the fire and rescue, police, ambulance, "
             "and search & rescue community, with 500+ exhibitors and live equipment demonstrations.",
     "registration_url": "https://www.emergencyuk.com/"},
    {"title": "The Fire Safety Event Europe 2027", "date": "2027-04-27", "end_date": "2027-04-29",
     "location": "NEC, Birmingham, UK", "cat": Category.FIRE_SAFETY,
     "desc": "A major European exhibition for fire safety professionals, installers, and consultants, "
             "showcasing detection, suppression, and passive fire protection technology.",
     "registration_url": "https://www.firesafetyevent.com/"},
    {"title": "SFPE European Conference & Expo on Fire Safety Engineering 2027", "date": "2027-04-14", "end_date": "2027-04-15",
     "location": "Geneva, Switzerland", "cat": Category.FIRE_SAFETY,
     "desc": "The Society of Fire Protection Engineers' European conference bringing together fire "
             "safety engineers for technical sessions on performance-based design and research.",
     "registration_url": "https://www.sfpe.org/events-education/conferences/conferences/euroconf"},
    # CBRN
    {"title": "CBRNe Convergence 2026", "date": "2026-11-03", "end_date": "2026-11-05",
     "location": "Knoxville, Tennessee, USA", "cat": Category.CBRN,
     "desc": "An annual international conference and exhibition for CBRN and hazmat responders, "
             "with workshops, capability demonstrations, and technology exhibits.",
     "registration_url": "https://cbrneworld.com/"},
    {"title": "NCT Middle East 2026", "date": "2026-11-10", "end_date": "2026-11-11",
     "location": "Abu Dhabi, UAE", "cat": Category.CBRN,
     "desc": "The region's largest CBRNe, counter-IED, and EOD conference and exhibition, bringing "
             "together civil and military first responders with industry and government leaders.",
     "registration_url": "https://nct-events.com/nct-middle-east"},
    # EOD
    {"title": "Explosive Ordnance Seminar Europe 2026", "date": "2026-09-22", "end_date": "2026-09-24",
     "location": "Rome, Italy", "cat": Category.EOD,
     "desc": "A European seminar and exhibition on explosive ordnance disposal, unexploded ordnance "
             "clearance, and the latest detection, robotic, and drone technology for EOD teams.",
     "registration_url": "https://intelligence-sec.com/events/explosive-ordnance-seminar-europe-2026/"},
    {"title": "Milipol Qatar 2026", "date": "2026-10-20", "end_date": "2026-10-22",
     "location": "Doha, Qatar", "cat": Category.EOD,
     "desc": "A global homeland security and civil defence exhibition covering fire & rescue, bomb "
             "disposal, and public safety equipment for the Middle East market.",
     "registration_url": "https://www.milipolqatar.com/en"},
    # Disaster Medicine
    {"title": "EUSEM 2026", "date": "2026-09-23", "end_date": "2026-09-27",
     "location": "Paris, France", "cat": Category.DISASTER_MEDICINE,
     "desc": "The European Society for Emergency Medicine's annual congress, covering trauma care, "
             "mass-casualty response, and disaster and emergency medicine research.",
     "registration_url": "https://eusem.org/"},
    {"title": "WADEM World Congress on Disaster and Emergency Medicine 2027", "date": "2027-04-26", "end_date": "2027-04-30",
     "location": "Paris, France", "cat": Category.DISASTER_MEDICINE,
     "desc": "The World Association for Disaster and Emergency Medicine's flagship congress, connecting "
             "researchers and responders working on disaster preparedness, response, and recovery.",
     "registration_url": "https://wadem.org/congress/paris-2027/"},
    # Environmental Safety
    {"title": "IOSSC 2026 — International Oil Spill Science Conference", "date": "2026-10-13", "end_date": "2026-10-16",
     "location": "Montreal, Canada", "cat": Category.ENVIRONMENTAL_SAFETY,
     "desc": "A scientific conference on oil spill prevention, contingency planning, and environmental "
             "rehabilitation across marine, coastal, and freshwater environments.",
     "registration_url": "https://iossc2026.org/"},
    {"title": "International Oil Spill Conference (IOSC) 2027", "date": "2027-05-17", "end_date": "2027-05-20",
     "location": "Savannah, Georgia, USA", "cat": Category.ENVIRONMENTAL_SAFETY,
     "desc": "A long-running international forum for oil spill response professionals, regulators, and "
             "researchers to exchange lessons learned from real-world spill responses.",
     "registration_url": "https://www.iosc.org/"},
]
