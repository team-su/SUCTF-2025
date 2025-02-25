# type: ignore
import os
from dotenv import load_dotenv
from poseidon.evm import Chain, Account, Contract, Utils  # https://github.com/B1ue1nWh1te/Poseidon

load_dotenv()
rpc_url = os.getenv("RPC_URL")
private_key = os.getenv("PRIVATE_KEY")
Utils.set_solidity_version("0.8.28")
abi, bytecode = Utils.compile_solidity_contract("./contracts/MagicBox.sol", "MagicBox")

chain = Chain(rpc_url)
account = Account(chain, private_key)
contract = Contract(account, "<ContractAddress>", abi)

contract.read_only_call_function("isSolved")
message_hash = contract.read_only_call_function("getMessageHash", account.address)
signature1 = account.sign_message_hash(message_hash).signature_data
contract.call_function("signIn", [int(signature1.v.hex(), 16), signature1.r, signature1.s])

signature2 = Utils.convert_equivalent_signature(signature1.signature)
contract.call_function("openBox", [int(signature2.v.hex(), 16), signature2.r, signature2.s])
contract.read_only_call_function("isSolved")
