from Products.ZCatalog.Catalog import Catalog


def catalogObject(self, object, uid, threshold=None, idxs=None, update_metadata=1):
    if not hasattr(object.aq_base, 'tm_serial'):
        return 0
    return self._patched_catalogObject(object
        , uid
        , threshold
        , idxs
        , update_metadata
    )


Catalog._patched_catalogObject = Catalog.catalogObject
Catalog.catalogObject = catalogObject

#import pdb;pdb.set_trace()

def updateMetadata(self, object, uid):
    data = self.data
    index = self.uids.get(uid, None)
    newDataRecord = self.recordify(object)
    if index is None:
        index = object.tm_serial
        data[index] = newDataRecord
        return index
    else:
        if data.get(index, 0) != newDataRecord:
            data[index] = newDataRecord
    return index
    
Catalog.updateMetadata = updateMetadata