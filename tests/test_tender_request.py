import json
import pytest
from datetime import datetime


@pytest.fixture(scope="session")
def tender_data():
with open("requests/tender_request.json", encoding="utf-8") as f:
return json.load(f)




def test_required_fields(tender_data):
assert "type" in tender_data
assert "tenderPeriod" in tender_data
assert "title" in tender_data
assert "description" in tender_data
assert "lots" in tender_data




def test_dates_valid(tender_data):
start = datetime.fromisoformat(tender_data["tenderPeriod"]["startDate"])
end = datetime.fromisoformat(tender_data["tenderPeriod"]["endDate"])
assert start < end, "startDate must be earlier than endDate"




def test_additional_cpvs_match_ids(tender_data):
lot = tender_data["lots"][0]
ids = lot["AdditionalCpvIds"]
cpvs = [c["id"] for c in lot["AdditionalCpvs"]]
assert set(ids) == set(cpvs), "AdditionalCpvIds must match AdditionalCpvs IDs"




def test_items_valid(tender_data):
lot = tender_data["lots"][0]
for item in lot["items"]:
assert item["quantity"] > 0
assert "unit" in item and "id" in item["unit"]




def test_title_and_description_not_empty(tender_data):
assert tender_data["title"].strip() != ""
assert tender_data["description"].strip() != ""