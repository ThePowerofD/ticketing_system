import time

from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()     # argon2id with recommended settings

# --- register: hash the password, store only the hash ---
stored_ana = password_hash.hash("Summer2026!")
stored_luis = password_hash.hash("Summer2026!")
print("Ana's stored hash: ", stored_ana)
print("Luis's stored hash:", stored_luis)
print("Same hash?", stored_ana == stored_luis)

# --- login: check what the user typed against the stored hash ---
print("Ana types the right password:", password_hash.verify("Summer2026!", stored_ana))
print("Ana types it in lowercase:   ", password_hash.verify("summer2026!", stored_ana))

# --- cost: how long one hash takes ---
start = time.perf_counter()
password_hash.hash("anything")
print(f"One hash took {time.perf_counter() - start:.3f} s")