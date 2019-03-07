import numpy as np
from constants import BATCH_SIZE

class Record():

    def __init__(self, positions, values, policies, history = []):
        self.pos = positions
        self.val = values
        self.pol = policies
        self.hst = history

    def __add__(self, other):
        return Record(positions = np.vstack((self.pos, other.pos)),
                      values    = np.vstack((self.val, other.val)),
                      policies  = np.vstack((self.pol, other.pol)),
                      history   = self.hst + other.hst)

    def __len__(self):
        return int(self.pos.shape[0])

    def data(self):
        return [self.pos, self.val, self.pol]

    def batch(self, batch_size = BATCH_SIZE):
        i = np.random.choice(len(self), batch_size)
        return [self.pos[i], self.val[i], self.pol[i]]

    def cull(self, nrows):
        self.pos = self.pos[nrows:]
        self.val = self.val[nrows:]
        self.pol = self.pol[nrows:]
        self.hst = self.hst[nrows:]
        return self

    def save(self, dir):
        np.savez(dir + "/record.npz",
                 pos  = self.pos,
                 val  = self.val,
                 pol  = self.pol,
                 hst  = self.hst)

def load_record(dir):
    npz = np.load(dir + "/record.npz")
    return Record(npz['pos'], npz['val'], npz['pol'], list(npz['hst']))

def combine_records(record1, record2):
    return (record1 + record2 if record1 else record2) if record2 else None
