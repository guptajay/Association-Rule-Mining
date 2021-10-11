from cba import ClassificationBasedAssociation
from models import TransactionDB
from qcba.data_structures import QuantitativeDataFrame
import pandas as pd
from qcba import QCBA
from sklearn.utils import shuffle


from qcba.data_structures import (
    IntervalReader,
    Interval,
    QuantitativeDataFrame,
    QuantitativeCAR,
)

interval_reader = IntervalReader()

interval_reader.closed_bracket = "", "NULL"
interval_reader.open_bracket = "NULL", ""
interval_reader.infinity_symbol = "inf", "inf"
interval_reader.members_separator = "_to_"

interval_reader.compile_reader()

QuantitativeCAR.interval_reader = interval_reader

data_train_discretized = pd.read_csv("qcba_datasets/binned-tic-tac-toe-endgame.csv")
data_train_undiscretized = pd.read_csv("qcba_datasets/tic-tac-toe-endgame.csv")
data_test = pd.read_csv("qcba_datasets/binned-tic-tac-toe-endgame.csv")

# data_train_discretized = shuffle(data_train_discretized)
# data_train_undiscretized = shuffle(data_train_undiscretized)
# data_test = shuffle(data_test)


txns_train = TransactionDB.from_DataFrame(data_train_discretized)
txns_test = TransactionDB.from_DataFrame(data_test)

quant_dataframe_train_disc = QuantitativeDataFrame(data_train_discretized)
quant_dataframe_train_undisc = QuantitativeDataFrame(data_train_undiscretized)

cba = ClassificationBasedAssociation()
cba.fit(txns_train)
cba.rule_model_accuracy(txns_train)

print("-"*50)

qcba_cba = QCBA(quant_dataframe_train_undisc, cba_rule_model=cba)
qcba_stages = {
    "refitting": True,
    "literal_pruning": True,
    "trimming": True,
    "extension": True,
    "overlap_pruning": True,
    "based_drop": True}

qcba_cba.fit(qcba_stages)

print("CBA accuracy:", cba.rule_model_accuracy(txns_train))
print("QCBA accuracy:", qcba_cba.score(quant_dataframe_train_undisc))