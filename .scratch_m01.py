# -*- coding: utf-8 -*-
import json, pathlib
p = pathlib.Path("C:/Users/Karthikeya Reddy/OneDrive - RITE/Desktop/Office Work/Subject/03_Databases_and_Storage_Engines/Module_01_Storage_Theory_ACID_Relational_Model/quiz.json")
raw = p.read_bytes()
crlf = b"\r\n" in raw
data = json.loads(raw.decode("utf-8"))

new_texts = {
    1: [
        "A raw CSV file must be fully decompressed into memory before any row can be read, whereas an indexed database streams compressed pages directly from disk, so the speed gain comes from compression, not the search algorithm.",
        "Both a CSV scan and an indexed lookup examine every row; the database only appears faster because it caches the whole table in RAM after the first query, turning later O(N) scans into O(log N) memory reads.",
        "The operating system reads a CSV one byte at a time, while a database reads whole 4KB pages at once; the O(log N) figure reflects fewer disk pages touched per row, not a tree-based search structure.",
    ],
    2: [
        "Atomicity guarantees that once a transaction reports success, its effects survive any later crash or power loss, because the writes have already been flushed to non-volatile storage.",
        "Atomicity guarantees that concurrent transactions cannot see each other's uncommitted intermediate writes, preventing one transaction's partial changes from being read by another before it finishes.",
        "Atomicity guarantees that a disk error is logged and the failed write is automatically retried up to three times before the transaction is aborted, so a single bad sector cannot corrupt data.",
    ],
    3: [
        "The database keeps two synchronized copies of every data file on separate physical disks; if power is lost mid-write, the mirrored copy is used to reconstruct the committed row on restart.",
        "The database defers writing changes to disk until the operating system flushes its buffer cache on a clean shutdown; an abrupt power loss is instead absorbed by a capacitor-backed cache in the disk controller.",
        "The COMMIT call blocks until the row has been copied to a replica server over the network; durability comes from the replica's in-memory copy, not from anything written to local disk.",
    ],
    4: [
        "- Tuple: The table itself (the full set of rows). - Relation: A single row within that table. - Attribute: The data type assigned to each relation, such as INTEGER or VARCHAR.",
        "- Relation: A named column representing one domain of data. - Attribute: A single row or record in the table. - Tuple: The overall schema definition, including primary and foreign keys.",
        "- Relation: The set of all tables in a database (the schema). - Tuple: A single table within that schema. - Attribute: A single row inside a given table.",
    ],
    5: ["3", "0", "4"],
    6: ["2", "0", "3"],
    7: ["ALICE", "Bob", None],
    8: [{"id": "k1", "val": "dirty"}, None, "Raises KeyError"],
    9: [
        "Two concurrent processes read the same account balance before either writes back, so the second process's write silently overwrites the first process's increment instead of both being applied.",
        "Power was lost mid-write of an 8KB database page split across two 4KB disk sectors, leaving a partially written page that the storage engine cannot parse on restart.",
        "commit() sends the write-ahead log record to the OS write buffer but never calls fsync(), so the acknowledged transaction can still be sitting in a volatile page cache when the crash occurs.",
    ],
}

for q in data:
    qid = q["id"]
    texts = new_texts[qid]
    assert len(q["options"]) == 4
    for idx, opt_key in enumerate(["opt_1", "opt_2", "opt_3"]):
        opt = q["options"][idx+1]
        assert opt["id"] == opt_key, (qid, opt["id"], opt_key)
        assert opt["is_correct"] is False
        opt["text"] = texts[idx]

out = json.dumps(data, indent=2, ensure_ascii=True)
if crlf:
    out = out.replace("\n", "\r\n")
p.write_bytes(out.encode("utf-8"))
print("done")
