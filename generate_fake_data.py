import random
from datetime import date, timedelta, time
from faker import Faker
from django.utils import timezone
from djmoney.money import Money

from apps.customer.models import Customer
from apps.country.models import Agency, Country, Town
from apps.passengers.models import Ticket

fake = Faker("fr_FR")

# --- CONFIG ---
COUNTRY_IDS = [3, 4, 5]
AGENCY_IDS = [9, 10, 11]
NB_CUSTOMERS = 500
NB_TICKETS = 10000
START_DATE = date(2025, 9, 1)
END_DATE = date(2025, 10, 31)
PAYMENT_METHODS = ["CASH", "CARD", "Mobile Money"]
STATUS = ["PAYE", "NON_PAYE"]

# --- Helper functions ---
def random_date(start, end):
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))

def random_hour():
    return time(hour=random.randint(5, 21), minute=random.choice([0, 15, 30, 45]))

def generate_customer_code(agency_code, seq_num):
    """Génère un code client unique par agence"""
    year = timezone.now().year
    return f"{agency_code}-{year}-{seq_num:06d}"

# --- Génération des CLIENTS ---
print("🚀 Création de 500 clients...")

agencies = {a.id: a.code for a in Agency.objects.filter(id__in=AGENCY_IDS)}
town_ids = list(Town.objects.values_list("id", flat=True))
customers = []

seq_counters = {aid: 1 for aid in AGENCY_IDS}

for _ in range(NB_CUSTOMERS):
    agency_id = random.choice(AGENCY_IDS)
    country_id = random.choice(COUNTRY_IDS)
    agency_code = agencies[agency_id]
    seq_num = seq_counters[agency_id]
    seq_counters[agency_id] += 1

    sex = random.choice(["M", "F"])
    first = fake.first_name_male() if sex == "M" else fake.first_name_female()
    last = fake.last_name()
    phone = f"+2289{random.randint(1000000,9999999)}"
    email = f"{first.lower()}.{last.lower()}@{fake.free_email_domain()}"
    code = generate_customer_code(agency_code, seq_num)

    customer = Customer(
        agency_id=agency_id,
        code=code,
        firstName=first,
        lastName=last,
        sex=sex,
        phone_number=phone,
        email=email,
        IDCardNumber=f"ID{random.randint(10000,99999)}",
        address=fake.street_address(),
        country_id=country_id,
    )
    customers.append(customer)

Customer.objects.bulk_create(customers)
print("✅ 500 clients créés avec succès.")

customer_ids = list(Customer.objects.values_list("id", flat=True))

# --- Génération des TICKETS ---
print("🎟️ Création de 10 000 tickets...")

tickets = []
batch_size = 500
for i in range(NB_TICKETS):
    agency_id = random.choice(AGENCY_IDS)
    customer_id = random.choice(customer_ids)
    departure_town_id, arrival_town_id = random.sample(town_ids, 2)
    departure_date = random_date(START_DATE, END_DATE)
    departure_hour = random_hour()
    price = Money(random.randint(2000, 15000), "XOF")
    payment_method = random.choice(PAYMENT_METHODS)
    status = random.choices(STATUS, weights=[0.6, 0.4])[0]

    mobile_money = None
    if payment_method == "Mobile Money":
        mobile_money = f"+2289{random.randint(1000000,9999999)}"

    ticket = Ticket(
        agency_id=agency_id,
        customer_id=customer_id,
        departure_town_id=departure_town_id,
        arrival_town_id=arrival_town_id,
        departure_date=departure_date,
        departure_hour=departure_hour,
        ticket_price=price,
        payment_method=payment_method,
        mobile_money_phone_number=mobile_money,
        status=status,
    )
    tickets.append(ticket)

    # Insertion par lots
    if (i + 1) % batch_size == 0:
        Ticket.objects.bulk_create(tickets)
        print(f"   → {i+1} tickets insérés...")
        tickets = []

# insère les tickets restants
if tickets:
    Ticket.objects.bulk_create(tickets)
print("✅ 10 000 tickets générés avec succes")
