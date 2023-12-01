def kv_dict_to_map(inobj: [dict,pd.DataFrame()], klab = 'Test', vlab = 'Control', kcol = None, vcol = None)-> dict:
    '''
    Identifies passed object, inobj, as dictionary, dataframe or other
    Converts a dictionary of key-value pairs to a dictionary of key : label + value : label
    Example: {a0 : b0, a1 : b1, a1 : b0} --> {a0 : llab, b0 : rlab, a1: llab, b1 : rlab}
    
    Converts a dataframe of the identified key column, kcol, and value column, vcol, into a dictionary
    of key : label + value : label
    Example : 
        Index     col1       col2
        0          abc        dba
        1          foo        bar
        
        kv_dict_to_map(inobj = df, klab = 'Test', vlab = 'Control', kcol = 'col1', vcol = 'col2')
        returns {'abc' : 'Test', 'foo' : 'Test', 'dba' : 'Control', 'bar' : 'Control'}

    param:
        inobj -> dictionary or dataframe to be evaluated
        klab -> label to be placed on keys
        vlab -> label to be placed on values
        kcol -> optional, if inobj is dataframe, the name of the column to be given the label in klab
        vcol -> optional, if inobj is dataframe, the name of the column to be given the label in vlab

    returns:
        dictionary
    '''
    try:
        assert(len(inobj) > 0)
    except AssertionError:
        raise AssertionError("Dictionary must not be empty")
    except Exception as e:
        raise e
    
    if type(inobj)==dict:
        ### Validate no common values
        _klab = set([k for k in inobj.keys()])
        _vlab = set([v for v in inobj.values()])
        if len(_klab.intersection(_vlab)) > 0:
            _badset = _klab.intersection(_vlab)
            raise ValueError("Common value(s) in input dictionaries: %s" %str(_badset))
        else:
            kdict = {k:klab for k in inobj.keys()}
            vdict = {v:vlab for v in inobj.values()}
            kdict.update(vdict)
            return kdict
    elif type(inobj)==pd.DataFrame:
        incol = inobj.columns
        if kcol is None:
            kcol = incol[0]
            print("Warning: inferred kcol=%s. If a different column is needed please specify in kcol." %kcol)
        if vcol is None:
            vcol = incol[1]
            print("Warning: inferred vcol=%s. If a different column is needed please specify in vcol." %vcol)
        kdict = {k:klab for k in inobj['%s' %kcol]}
        vdict = {v:vlab for v in inobj['%s' %vcol]}
        kdict.update(vdict)
        return kdict
    else:
        raise TypeError("Object in position inobj is of type %s. Please supply a dictionary." %type(inobj))
        
### Unit tests - emptydict and badict will fail, simpledict, okdict and dframe will pass
emptydict = {}
simpledict = {600662 : 202408}
okdict = {600662 : 202408, 600662 : 202410, 600662: 203910, 600608 : 203910, 600608 : 203911, 600608 : 202408}
badict = {600662 : 202408, 202408 : 202451}
dframe = pd.DataFrame({'testcafe' : [600662, 600662, 600608], 'matchcafe' : [202408, 202410, 202409]})

test_set = [simpledict, okdict, badict, dframe]
name_set = ['simpledict', 'okdict', 'badict','dframe']
for i in range(len(test_set)):
    print("\n--------------------testing %s which is of type %s-----------------" %(name_set[i], type(test_set[i])))
    res = kv_dict_to_map(test_set[i])
    print(type(res))
    print("Testing %s" %test_set[i])
    for key, val in res.items():
        print(key, val)
