import json
from pathlib import Path

import pytest
from gltest import get_contract_factory
from gltest.assertions import tx_execution_succeeded
from gltest.types import TransactionStatus
from gltest.utils import extract_contract_address


def _ok(receipt):
    assert tx_execution_succeeded(receipt)
    return receipt


@pytest.mark.integration
def test_studionet_plan_deviation_classification(default_account, secondary_account):
    factory = get_contract_factory(contract_file_path=Path(__file__).resolve().parents[2] / "contracts" / "deviation_ledger.py")
    args = [secondary_account.address, "Public park wayfinding comprehension study", "EXPECTED means allowed by the frozen plan. JUSTIFIED requires a documented unforeseen constraint and proportionate response. Otherwise UNEXPLAINED."]
    deployed = _ok(factory.deploy_contract_tx(args=args, account=default_account, wait_transaction_status=TransactionStatus.FINALIZED))
    address = extract_contract_address(deployed)
    principal = factory.build_contract(address, account=default_account)
    researcher = factory.build_contract(address, account=secondary_account)
    _ok(principal.add_plan_section(args=["sample", "Recruit forty adult volunteers at the east entrance and alternate assignment between two sign variants."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    _ok(principal.freeze_plan(args=[]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    _ok(researcher.record_deviation(args=["sample", "Moved the final six recruitments to the west entrance.", "The east entrance was unexpectedly closed, so identical criteria were used at the west entrance.", "Recorded before those six volunteers were recruited."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    intelligent = _ok(researcher.classify_deviation(args=[1]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    entry = principal.get_deviation(args=[1]).call()
    assert entry["classification"] in ("EXPECTED", "JUSTIFIED", "UNEXPLAINED")
    assert entry["impact"] in ("LOW", "MEDIUM", "HIGH")
    print("STUDIONET_RECORD=" + json.dumps({"address": address, "deploy_tx": deployed["hash"], "intelligent_tx": intelligent["hash"], "observed": entry["classification"] + "/" + entry["impact"]}, sort_keys=True))
