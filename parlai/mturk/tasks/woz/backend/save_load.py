import os

from scipy import sparse
import tables


def hdf_to_sparse_csx_matrix(path, name, sparse_format):
    attrs = _get_attrs_from_hdf_file(path, name, 'csx', ['data', 'indices', 'indptr', 'shape'])
    constructor = getattr(sparse, f'{sparse_format}_matrix')

    return constructor(tuple(attrs[:3]), shape=tuple(attrs[3]))


def hdf_to_sparse_coo_matrix(path, name):
    attrs = _get_attrs_from_hdf_file(path, name, 'coo', ['data', 'rows', 'cols', 'shape'])

    return sparse.coo_matrix((attrs[0], tuple(attrs[1:3])), shape=attrs[3])


def _get_attrs_from_hdf_file(path, name, sparse_format, attributes):
    with tables.open_file(os.path.join(path, name), 'r') as f:
        attrs = []
        for attr in attributes:
            attrs.append(getattr(f.root, f'{sparse_format}_{attr}').read())
    return attrs